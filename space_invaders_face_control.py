import cv2
import threading
import pygame
import time
import random
import sys

# Global variable to store the player's x-coordinate (controlled by face tracking)
player_x = 400  # Start at the center (game window width is 800)
lock = threading.Lock()
game_over = False  # Global flag to signal game termination

def face_tracking(camera_index=0):
    """
    Capture video from the selected camera and detect the face to update the player's x-position.
    The frame is flipped horizontally so that movement is intuitive (tilt right = move right).
    """
    global player_x, game_over
    cap = cv2.VideoCapture(camera_index)
    # Load Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Assume webcam resolution of 640x480
    webcam_width = 640
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while not game_over:
        ret, frame = cap.read()
        if not ret:
            continue

        # Flip the frame horizontally for a mirror-like effect
        frame = cv2.flip(frame, 1)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        if len(faces) > 0:
            # Take the first detected face and compute its center x-coordinate
            (x, y, w, h) = faces[0]
            face_center_x = x + w / 2
            # Map the face center from webcam resolution (640) to game window width (800)
            game_x = int((face_center_x / webcam_width) * 800)
            with lock:
                player_x = game_x
        
        # (Optional debug window code is commented out for macOS stability)
        # cv2.imshow("Face Tracking", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    # cv2.destroyAllWindows()

def adjust_difficulty(score, elapsed_time):
    """
    Increase enemy speed gradually based on score and elapsed time.
    """
    base_speed = 1
    difficulty = base_speed + (score / 50) + (elapsed_time / 60)
    return difficulty

def respawn_enemy(enemy, screen_width, enemy_width):
    """
    Respawn an enemy at a random position near the top of the screen.
    """
    enemy["x"] = random.randint(0, screen_width - enemy_width)
    enemy["y"] = random.randint(20, 150)
    enemy["speed"] = random.choice([1, 1.5, 2])

def main_game():
    """
    Main game loop built with Pygame.
    """
    global player_x, game_over
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("HeadSpace Invaders - 3 Enemies Edition")
    clock = pygame.time.Clock()
    running = True

    # Player spaceship properties
    spaceship_width = 50
    spaceship_height = 30
    spaceship_y = screen_height - spaceship_height - 10

    # Bullet properties
    bullet_width = 5
    bullet_height = 10
    bullet_speed = 10
    bullets = []  # List to store active bullets

    # Enemy properties
    enemy_width = 40
    enemy_height = 30
    enemies = []
    for _ in range(3):
        enemy = {
            "x": random.randint(0, screen_width - enemy_width),
            "y": random.randint(20, 150),
            "speed": 1  # Will be updated via difficulty adjustment
        }
        enemies.append(enemy)

    score = 0
    start_time = time.time()
    font = pygame.font.SysFont("Arial", 24)

    while running:
        elapsed_time = time.time() - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            # Press SPACE to shoot a bullet
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    with lock:
                        x_pos = player_x
                    bullet_x = x_pos - (bullet_width // 2)
                    bullet_y = spaceship_y
                    bullets.append([bullet_x, bullet_y])

        with lock:
            x_pos = player_x

        # Ensure the spaceship stays within screen boundaries
        if x_pos < spaceship_width // 2:
            x_pos = spaceship_width // 2
        if x_pos > screen_width - spaceship_width // 2:
            x_pos = screen_width - spaceship_width // 2

        current_difficulty = adjust_difficulty(score, elapsed_time)

        # Update each enemy's position
        for enemy in enemies:
            enemy["speed"] = current_difficulty
            enemy["x"] += enemy["speed"]

            # Reverse direction and move down when hitting boundaries
            if enemy["x"] > screen_width - enemy_width or enemy["x"] < 0:
                enemy["speed"] = -enemy["speed"]
                enemy["y"] += enemy_height

            # If any enemy reaches the player's level, end the game gracefully
            if enemy["y"] + enemy_height >= spaceship_y:
                running = False
                game_over = True
                break

        # Update bullet positions
        for i in range(len(bullets) - 1, -1, -1):
            bullets[i][1] -= bullet_speed
            if bullets[i][1] < 0:
                bullets.pop(i)

        # Collision detection between bullets and enemies
        for i in range(len(bullets) - 1, -1, -1):
            bullet_rect = pygame.Rect(bullets[i][0], bullets[i][1], bullet_width, bullet_height)
            bullet_hit = False
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
                if bullet_rect.colliderect(enemy_rect):
                    bullets.pop(i)
                    bullet_hit = True
                    score += 5
                    respawn_enemy(enemy, screen_width, enemy_width)
                    break
            if bullet_hit:
                continue

        score += 0.01

        # Drawing
        screen.fill((0, 0, 0))
        spaceship_rect = pygame.Rect(x_pos - spaceship_width // 2, spaceship_y, spaceship_width, spaceship_height)
        pygame.draw.rect(screen, (0, 255, 0), spaceship_rect)
        for enemy in enemies:
            pygame.draw.rect(screen, (255, 0, 0), (enemy["x"], enemy["y"], enemy_width, enemy_height))
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 0), (bullet[0], bullet[1], bullet_width, bullet_height))
        score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    # Game Over: Display a message before quitting
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width // 2 - 60, screen_height // 2))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()

if __name__ == "__main__":
    # Allow selecting a camera index via a command-line argument (default is 0)
    camera_index = 0
    if len(sys.argv) > 1:
        try:
            camera_index = int(sys.argv[1])
        except ValueError:
            pass

    face_thread = threading.Thread(target=face_tracking, args=(camera_index,), daemon=True)
    face_thread.start()
    main_game()

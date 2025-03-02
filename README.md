# HeadSpace Invaders - 3 Enemies Edition

HeadSpace Invaders is an interactive game that combines real-time face tracking using OpenCV with a classic Space Invaders–style game built with Pygame. In this project, your face controls the spaceship's horizontal movement, and you can shoot bullets (using the Space key) to destroy enemies. The game features three enemies that move horizontally, bounce off the screen edges, and descend toward your spaceship—raising the stakes as they gradually increase in speed.

## Features

- **Face Tracking Control:**  
  Uses OpenCV's Haar Cascade classifier to detect your face via the webcam. The detected horizontal position is mapped to control the spaceship.
  
- **Intuitive Controls:**  
  The camera feed is flipped horizontally so that tilting your head to the right moves the spaceship to the right.
  
- **Classic Gameplay:**  
  Shoot bullets with the Space key to destroy enemies. Three enemies move back and forth and descend toward you.
  
- **Dynamic Difficulty:**  
  Enemies speed up over time based on your score and elapsed time, simulating an AI-inspired difficulty adjustment.
  
- **Graceful Game Over:**  
  The game ends gracefully with a "Game Over" screen if any enemy reaches the spaceship's level.

## Prerequisites

- **Python 3.x**
- **Pygame**
- **OpenCV (opencv-python)**

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/HeadSpace-Invaders.git
   cd HeadSpace-Invaders
   ```

2. **Set Up a Virtual Environment (Recommended):**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install Required Packages:**

   ```bash
   pip install opencv-python pygame
   ```

## Usage

1. **Run the Game:**

   By default, the game uses the built-in MacBook webcam (camera index 0). To start the game, run:

   ```bash
   python space_invaders_face_control.py
   ```

   To use a different camera (for example, a Continuity Camera), pass the camera index as a command-line argument:

   ```bash
   python space_invaders_face_control.py 1
   ```

2. **Game Controls:**

   - **Move Spaceship:**  
     Your face’s horizontal position controls the spaceship. (The frame is flipped horizontally so tilting right moves the ship right.)
     
   - **Shoot Bullets:**  
     Press the **Space** key to fire bullets.

3. **Gameplay:**

   - Destroy enemies by shooting them.
   - Avoid letting any enemy descend to your spaceship’s level—the game ends if this happens.
   - Your score increases gradually over time and with each enemy destroyed.

## Troubleshooting

- **Camera Issues:**  
  Ensure that your webcam is not being used by another application.  
- **macOS Stability:**  
  The OpenCV debug window is disabled by default for stability. If you need to debug, uncomment the `cv2.imshow` code in the `face_tracking` function—but note that it may cause crashes on macOS.
- **Game Crashes:**  
  If the game crashes as enemies descend, it now ends gracefully by displaying a "Game Over" message before quitting.

## Future Improvements

- **Enhanced AI Difficulty:**  
  Integrate a more sophisticated AI model for dynamic difficulty adjustment.
- **Additional Enemies & Patterns:**  
  Introduce multiple enemy types with varied movement patterns.
- **Gesture-based Shooting:**  
  Explore using facial gestures (such as blinking or mouth movements) to fire bullets instead of using the keyboard.
- **Improved Graphics & Sound:**  
  Replace basic shapes with images and add sound effects for a more polished experience.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgements

- [Pygame](https://www.pygame.org/) – for the game framework.
- [OpenCV](https://opencv.org/) – for the computer vision library.
- The open-source community and contributors who inspire projects like this.

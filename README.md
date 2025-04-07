Fruit Ninja: Multiple Cursor Modes
A Fruit Ninja–inspired game using real‑time computer vision to control multiple cursor modes ("hand" and "face"). The game leverages MediaPipe for hand and face mesh tracking, and PyGame for graphics, animations, and sound. Slice fruits, avoid bombs, and enjoy dynamic visual effects—all in full-screen mode.

Features
Real‑Time Tracking:
Use MediaPipe to track your hand (index finger tip) or face mesh (nose or forehead landmarks) for cursor control.

Multiple Cursor Modes:
Toggle between "hand" and "face" tracking by pressing M.

Dynamic Gameplay:
Fruits spawn with varying velocities; slice them by moving the cursor over them to score points.

Visual Effects:
Enjoy slicing animations, splash effects, and persistent water splash stains on the background.

Sound Effects:
Audio feedback with slicing sounds and bomb explosions.

Full‑Screen Experience:
The game automatically launches in full‑screen mode and displays a dynamic HUD.

Requirements
Python 3.x

OpenCV-Python

MediaPipe

PyGame

NumPy

pyttsx3

Installation
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/yourusername/fruit-ninja-cursor.git
cd fruit-ninja-cursor
(Optional) Create and Activate a Virtual Environment:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On macOS/Linux
Install Dependencies:
Ensure your requirements.txt includes:

text
Copy
Edit
opencv-python
mediapipe
pygame
numpy
pyttsx3
Then run:

bash
Copy
Edit
pip install -r requirements.txt
Place Asset Files:
Make sure that sound files (slice.mp3 and explosion.mp3) are in the project directory or update their paths in the code accordingly.

Usage
Run the game using:

bash
Copy
Edit
python filename.py
Controls
M: Toggle between hand and face tracking modes.

ESC: Exit the game.

Customization
Cursor Sensitivity:
Adjust the face_sensitivity and hand_sensitivity variables in the code.

Fruit Spawn Rate:
Modify the spawn interval in the spawn_fruit function to increase or decrease fruit spawn frequency.

Visual Effects:
Tweak the slicing animations, splash effects, and water splash stain parameters in their respective classes.

Troubleshooting
Webcam Issues:
Ensure your webcam is connected and that OpenCV can access it.

Sound File Errors:
Verify that slice.mp3 and explosion.mp3 are in the correct location or update the paths in the code.

Performance:
If the game runs slowly, consider reducing resolution or frame rate, or adjusting the sensitivity factors.

License
This project is licensed under the MIT License.


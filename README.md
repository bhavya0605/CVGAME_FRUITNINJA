<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fruit Ninja: Multiple Cursor Modes</title>
</head>
<body>
    <h1>Fruit Ninja: Multiple Cursor Modes</h1>

    <p>
        A Fruit Ninja–inspired game using real‑time computer vision to control multiple cursor modes ("hand" and "face").
        The game leverages <strong>MediaPipe</strong> for hand and face mesh tracking, and <strong>PyGame</strong> for graphics, animations, and sound.
        Slice fruits, avoid bombs, and enjoy dynamic visual effects—all in full-screen mode.
    </p>

    <h2>Features</h2>
    <ul>
        <li><strong>Real‑Time Tracking:</strong> Use MediaPipe to track your hand (index finger tip) or face mesh (nose or forehead landmarks) for cursor control.</li>
        <li><strong>Multiple Cursor Modes:</strong> Toggle between "hand" and "face" tracking by pressing <strong>M</strong>.</li>
        <li><strong>Dynamic Gameplay:</strong> Fruits spawn with varying velocities; slice them by moving the cursor over them to score points.</li>
        <li><strong>Visual Effects:</strong> Enjoy slicing animations, splash effects, and persistent water splash stains on the background.</li>
        <li><strong>Sound Effects:</strong> Audio feedback with slicing sounds and bomb explosions.</li>
        <li><strong>Full‑Screen Experience:</strong> The game automatically launches in full‑screen mode and displays a dynamic HUD.</li>
    </ul>

    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li><a href="https://pypi.org/project/opencv-python/">OpenCV-Python</a></li>
        <li><a href="https://pypi.org/project/mediapipe/">MediaPipe</a></li>
        <li><a href="https://pypi.org/project/pygame/">PyGame</a></li>
        <li><a href="https://pypi.org/project/numpy/">NumPy</a></li>
        <li><a href="https://pypi.org/project/pyttsx3/">pyttsx3</a></li>
    </ul>

    <h2>Installation</h2>
    <ol>
        <li><strong>Clone the Repository:</strong>
            <pre><code>git clone https://github.com/yourusername/fruit-ninja-cursor.git
cd fruit-ninja-cursor</code></pre>
        </li>
        <li><strong>(Optional) Create and Activate a Virtual Environment:</strong>
            <pre><code>python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On macOS/Linux</code></pre>
        </li>
        <li><strong>Install Dependencies:</strong><br>
            Ensure your <code>requirements.txt</code> includes:
            <pre><code>opencv-python
mediapipe
pygame
numpy
pyttsx3</code></pre>
            Then run:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li><strong>Place Asset Files:</strong>
            Ensure that <code>slice.mp3</code> and <code>explosion.mp3</code> are in the project directory or update their paths in the code accordingly.
        </li>
    </ol>

    <h2>Usage</h2>
    <p>Run the game using:</p>
    <pre><code>python filename.py</code></pre>

    <h2>Controls</h2>
    <ul>
        <li><strong>M:</strong> Toggle between hand and face tracking modes.</li>
        <li><strong>ESC:</strong> Exit the game.</li>
    </ul>

    <h2>Customization</h2>
    <ul>
        <li><strong>Cursor Sensitivity:</strong> Adjust the <code>face_sensitivity</code> and <code>hand_sensitivity</code> variables in the code.</li>
        <li><strong>Fruit Spawn Rate:</strong> Modify the spawn interval in the <code>spawn_fruit</code> function.</li>
        <li><strong>Visual Effects:</strong> Tweak the slicing animations, splash effects, and water splash stain parameters in their respective classes.</li>
    </ul>

    <h2>Troubleshooting</h2>
    <ul>
        <li><strong>Webcam Issues:</strong> Ensure your webcam is connected and that OpenCV can access it.</li>
        <li><strong>Sound File Errors:</strong> Verify that <code>slice.mp3</code> and <code>explosion.mp3</code> are in the correct location or update the paths.</li>
        <li><strong>Performance:</strong> If the game runs slowly, consider reducing resolution or frame rate, or adjusting the sensitivity factors.</li>
    </ul>

    <h2>License</h2>
    <p>This project is licensed under the <a href="#">MIT License</a>.</p>
</body>
</html>

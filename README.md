<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fruit Ninja: Cursor Modes</title>
  <style>
    body {
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 40px;
      background: #fdfdfd;
      color: #333;
      line-height: 1.6;
    }
    h1 {
      color: #e74c3c;
      font-size: 2.8em;
      margin-bottom: 10px;
    }
    h2 {
      color: #2c3e50;
      border-bottom: 2px solid #ddd;
      padding-bottom: 5px;
    }
    ul {
      margin-left: 20px;
    }
    pre {
      background-color: #f4f4f4;
      padding: 12px;
      border-radius: 5px;
      overflow-x: auto;
    }
    code {
      background: #eee;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.95em;
    }
    a {
      color: #2980b9;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    .container {
      max-width: 960px;
      margin: auto;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🍉 Fruit Ninja: Multiple Cursor Modes</h1>

    <p>
      A Fruit Ninja–inspired game using real‑time computer vision to control multiple cursor modes ("hand" and "face").
      The game leverages <strong>MediaPipe</strong> for hand and face mesh tracking, and <strong>PyGame</strong> for graphics, animations, and sound.
      Slice fruits, avoid bombs, and enjoy dynamic visual effects—all in full-screen mode.
    </p>

    <h2>🚀 Features</h2>
    <ul>
      <li><strong>Real‑Time Tracking:</strong> Use MediaPipe to track your hand (index finger tip) or face mesh for cursor control.</li>
      <li><strong>Multiple Cursor Modes:</strong> Toggle between "hand" and "face" tracking by pressing <strong>M</strong>.</li>
      <li><strong>Dynamic Gameplay:</strong> Fruits spawn with varying velocities; slice them by moving the cursor over them to score points.</li>
      <li><strong>Visual Effects:</strong> Enjoy slicing animations, splash effects, and persistent water splash stains on the background.</li>
      <li><strong>Sound Effects:</strong> Audio feedback with slicing sounds and bomb explosions.</li>
      <li><strong>Full‑Screen Experience:</strong> The game automatically launches in full‑screen mode and displays a dynamic HUD.</li>
    </ul>

    <h2>🧰 Requirements</h2>
    <ul>
      <li>Python 3.x</li>
      <li><a href="https://pypi.org/project/opencv-python/">OpenCV-Python</a></li>
      <li><a href="https://pypi.org/project/mediapipe/">MediaPipe</a></li>
      <li><a href="https://pypi.org/project/pygame/">PyGame</a></li>
      <li><a href="https://pypi.org/project/numpy/">NumPy</a></li>
      <li><a href="https://pypi.org/project/pyttsx3/">pyttsx3</a></li>
    </ul>

    <h2>📦 Installation</h2>
    <ol>
      <li><strong>Clone the Repository:</strong>
        <pre><code>git clone https://github.com/yourusername/fruit-ninja-cursor.git
cd fruit-ninja-cursor</code></pre>
      </li>
      <li><strong>(Optional) Create and Activate a Virtual Environment:</strong>
        <pre><code>python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux</code></pre>
      </li>
      <li><strong>Install Dependencies:</strong><br />
        Make sure your <code>requirements.txt</code> includes:
        <pre><code>opencv-python
mediapipe
pygame
numpy
pyttsx3</code></pre>
        Then run:
        <pre><code>pip install -r requirements.txt</code></pre>
      </li>
      <li><strong>Place Asset Files:</strong> Ensure <code>slice.mp3</code> and <code>explosion.mp3</code> are in the project directory, or update their paths in the code.
      </li>
    </ol>

    <h2>🎮 Usage</h2>
    <p>Run the game with:</p>
    <pre><code>python filename.py</code></pre>

    <h2>🎛️ Controls</h2>
    <ul>
      <li><strong>M:</strong> Toggle between hand and face tracking modes</li>
      <li><strong>ESC:</strong> Exit the game</li>
    </ul>

    <h2>⚙️ Customization</h2>
    <ul>
      <li><strong>Cursor Sensitivity:</strong> Adjust the <code>face_sensitivity</code> and <code>hand_sensitivity</code> variables in the code.</li>
      <li><strong>Fruit Spawn Rate:</strong> Modify the spawn interval in the <code>spawn_fruit</code> function.</li>
      <li><strong>Visual Effects:</strong> Customize slicing animations and splash effects in their respective classes.</li>
    </ul>

    <h2>🛠️ Troubleshooting</h2>
    <ul>
      <li><strong>Webcam Issues:</strong> Ensure your webcam is connected and accessible by OpenCV.</li>
      <li><strong>Sound Errors:</strong> Check that <code>slice.mp3</code> and <code>explosion.mp3</code> are correctly located.</li>
      <li><strong>Performance:</strong> Reduce resolution or frame rate if the game runs slowly.</li>
    </ul>

    <h2>📄 License</h2>
    <p>This project is licensed under the <a href="#">MIT License</a>.</p>
  </div>
</body>
</html>

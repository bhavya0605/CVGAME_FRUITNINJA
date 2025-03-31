import cv2
import mediapipe as mp
import pygame
import pygame.gfxdraw
import numpy as np
import time
import random
import math

# ----------------------------
# MediaPipe Hand Tracking Setup
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,      # continuous video stream
    max_num_hands=1,              # detect one hand at most
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# ----------------------------
# MediaPipe Face Mesh Setup (for Eye Tracking) with increased sensitivity
# ----------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,  # enables iris landmarks
    min_detection_confidence=0.3,  # lowered for increased detection sensitivity
    min_tracking_confidence=0.3)   # lowered for increased tracking sensitivity

# ----------------------------
# PyGame Setup (Full Screen)
# ----------------------------
pygame.init()
pygame.mixer.init()  # initialize the mixer for sound effects

# Get the full screen resolution.
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Fruit Ninja: Multiple Cursor Modes")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load sounds (ensure these files exist or update with correct paths)
try:
    slice_sound = pygame.mixer.Sound("slice.mp3")
    bomb_sound = pygame.mixer.Sound("explosion.mp3")
except Exception as e:
    print("Error loading sound files:", e)
    slice_sound = None
    bomb_sound = None

# ----------------------------
# Game Timer Setup
# ----------------------------
GAME_DURATION = 60  # seconds
start_time = time.time()

# ----------------------------
# Slicing Animation Class
# ----------------------------
class SlicingAnimation:
    def __init__(self, pos, color, duration=0.3, max_radius=50):
        self.pos = pos
        self.color = color
        self.duration = duration
        self.timer = duration
        self.max_radius = max_radius

    def update(self, dt):
        self.timer -= dt

    def draw(self, surface):
        progress = 1 - (self.timer / self.duration)
        radius = int(progress * self.max_radius)
        alpha = max(255 - int(progress * 255), 0)
        temp_surf = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(temp_surf, self.max_radius, self.max_radius, radius, self.color + (alpha,))
        pygame.gfxdraw.filled_circle(temp_surf, self.max_radius, self.max_radius, radius, self.color + (alpha,))
        temp_rect = temp_surf.get_rect(center=self.pos)
        surface.blit(temp_surf, temp_rect)

    def is_finished(self):
        return self.timer <= 0

# ----------------------------
# Splash Effect Class
# ----------------------------
class SplashEffect:
    def __init__(self, pos, color, num_particles=20, duration=0.5):
        self.pos = pos
        self.color = color
        self.duration = duration
        self.timer = duration
        self.particles = []
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            self.particles.append({
                'pos': [pos[0], pos[1]],
                'vel': [vx, vy],
                'radius': random.randint(2, 5)
            })

    def update(self, dt):
        self.timer -= dt
        for p in self.particles:
            p['pos'][0] += p['vel'][0] * dt
            p['pos'][1] += p['vel'][1] * dt
            p['radius'] = max(p['radius'] - 0.1, 0)

    def draw(self, surface):
        alpha = int(255 * (self.timer / self.duration))
        for p in self.particles:
            if p['radius'] > 0:
                s = pygame.Surface((p['radius'] * 2, p['radius'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, self.color + (alpha,), (int(p['radius']), int(p['radius'])), int(p['radius']))
                surface.blit(s, (int(p['pos'][0] - p['radius']), int(p['pos'][1] - p['radius'])))

    def is_finished(self):
        return self.timer <= 0

# ----------------------------
# Utility: Chaikin Smoothing for Polygons
# ----------------------------
def smooth_polygon(points, iterations=2):
    for _ in range(iterations):
        new_points = []
        n = len(points)
        for i in range(n):
            p0 = points[i]
            p1 = points[(i + 1) % n]
            q = (0.75 * p0[0] + 0.25 * p1[0], 0.75 * p0[1] + 0.25 * p1[1])
            r = (0.25 * p0[0] + 0.75 * p1[0], 0.25 * p0[1] + 0.75 * p1[1])
            new_points.append(q)
            new_points.append(r)
        points = new_points
    return points

# ----------------------------
# Utility: Create an Irregular, Amoeba-like Water Splash Surface
# ----------------------------
def create_water_splash_surface(size, color, irregularity=0.2, layers=5):
    padded_size = int(size * 1.5)
    surf = pygame.Surface((padded_size, padded_size), pygame.SRCALPHA)
    center = padded_size / 2
    num_points = random.randint(8, 12)
    base_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points + random.uniform(-irregularity, irregularity)
        r = center * random.uniform(0.7, 1.0)
        x = center + r * math.cos(angle)
        y = center + r * math.sin(angle)
        base_points.append((x, y))
    smooth_points = smooth_polygon(base_points, iterations=2)
    for layer in range(layers):
        scale = 1 - (layer / layers) * 0.5
        points = [(center + (x - center) * scale, center + (y - center) * scale) for (x, y) in smooth_points]
        alpha = int(150 * (1 - layer / layers))
        pygame.draw.polygon(surf, color[:3] + (alpha,), points)
    for _ in range(15):
        angle = random.uniform(0, 2 * math.pi)
        r = center + random.uniform(0, center * 0.4)
        x = center + r * math.cos(angle)
        y = center + r * math.sin(angle)
        splatter_radius = random.randint(2, 5)
        splatter_alpha = random.randint(50, 100)
        pygame.draw.circle(surf, color[:3] + (splatter_alpha,), (int(x), int(y)), splatter_radius)
    return surf

# ----------------------------
# Stain Class (Irregular Amoeba-like Water Splash Effect)
# ----------------------------
class Stain:
    def __init__(self, pos, color, duration=10, size=80):
        self.pos = pos
        self.color = color
        self.duration = duration
        self.timer = duration
        self.size = size
        self.image = create_water_splash_surface(self.size, color, irregularity=0.2, layers=5)

    def update(self, dt):
        self.timer -= dt

    def draw(self, surface):
        fade_factor = self.timer / self.duration
        temp = self.image.copy()
        temp.set_alpha(int(255 * fade_factor))
        rect = temp.get_rect(center=self.pos)
        surface.blit(temp, rect)

    def is_finished(self):
        return self.timer <= 0

# Lists to hold active animations, splash effects, and stains.
slicing_animations = []
splash_effects = []
stains = []  # persistent background water splash stains

# ----------------------------
# Fruit Class Definition
# ----------------------------
class Fruit:
    def __init__(self, pos, velocity, fruit_type):
        self.pos = list(pos)         # [x, y]
        self.velocity = list(velocity)  # [vx, vy]
        self.type = fruit_type
        if self.type == "fruit":
            base_radius = 20
            self.color = (255, 0, 0)  # red for apple
            self.stem_color = (139, 69, 19)  # brown stem
            self.leaf_color = (0, 128, 0)    # green leaf
        elif self.type == "banana":
            base_radius = 20
            self.color = (255, 215, 0)
        elif self.type == "watermelon":
            base_radius = 30
            self.outer_color = (0, 128, 0)
            self.inner_color = (255, 0, 0)
            self.seed_color = (0, 0, 0)
            self.seeds = [(-10, -10), (10, -10), (-10, 10), (10, 10),
                          (0, -15), (0, 15), (-15, 0), (15, 0)]
        else:
            base_radius = 20
            self.color = (30, 30, 30)
            self.fuse_color = (255, 140, 0)

        scale_factor = random.uniform(1.5, 1.8)
        self.radius = int(base_radius * scale_factor)
        if self.type == "watermelon":
            self.seeds = [(int(dx * scale_factor), int(dy * scale_factor)) for dx, dy in self.seeds]

    def update(self, dt):
        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt
        self.velocity[1] += 300 * dt  # gravity

    def draw(self, surface):
        if self.type == "banana":
            x, y = int(self.pos[0]), int(self.pos[1])
            pygame.draw.arc(surface, (255, 215, 0), [x - 40, y - 20, 80, 40], 3.5, 5.9, 8)
            pygame.draw.arc(surface, (255, 223, 100), [x - 35, y - 18, 70, 35], 3.5, 5.9, 6)
            pygame.draw.circle(surface, (120, 100, 0), (x - 40, y), 5)
            pygame.draw.circle(surface, (120, 100, 0), (x + 40, y), 5)
        elif self.type == "fruit":
            pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
            stem_start = (int(self.pos[0]), int(self.pos[1] - self.radius))
            stem_end = (int(self.pos[0]), int(self.pos[1] - self.radius - 10))
            pygame.draw.line(surface, self.stem_color, stem_start, stem_end, 4)
            leaf_points = [
                (int(self.pos[0]), int(self.pos[1] - self.radius - 10)),
                (int(self.pos[0] + 10), int(self.pos[1] - self.radius - 5)),
                (int(self.pos[0] + 5), int(self.pos[1] - self.radius))
            ]
            pygame.draw.polygon(surface, self.leaf_color, leaf_points)
        elif self.type == "watermelon":
            pygame.draw.circle(surface, self.outer_color, (int(self.pos[0]), int(self.pos[1])), self.radius)
            inner_radius = self.radius - 5
            pygame.draw.circle(surface, self.inner_color, (int(self.pos[0]), int(self.pos[1])), inner_radius)
            for dx, dy in self.seeds:
                seed_x = int(self.pos[0] + dx)
                seed_y = int(self.pos[1] + dy)
                pygame.draw.circle(surface, self.seed_color, (seed_x, seed_y), 3)
        else:
            pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
            fuse_start = (int(self.pos[0]), int(self.pos[1] - self.radius))
            fuse_mid = (int(self.pos[0] - 10), int(self.pos[1] - self.radius - 15))
            fuse_end = (int(self.pos[0] - 5), int(self.pos[1] - self.radius - 25))
            pygame.draw.lines(surface, self.fuse_color, False, [fuse_start, fuse_mid, fuse_end], 3)
            pygame.draw.circle(surface, (255, 255, 0), fuse_end, 4)

def spawn_fruit(elapsed_time):
    x = random.randint(50, screen_width - 50)
    y = screen_height + 30  # start below screen
    vx = random.uniform(-100, 100)
    vy = random.uniform(-700, -400)
    bomb_probability = 0.1 + 0.1 * (elapsed_time / GAME_DURATION)
    apple_prob = 0.6
    banana_prob = 0.15
    watermelon_prob = 0.15 - (bomb_probability - 0.1)
    r = random.random()
    if r < apple_prob:
        fruit_type = "fruit"  # apple
    elif r < apple_prob + banana_prob:
        fruit_type = "banana"
    elif r < apple_prob + banana_prob + watermelon_prob:
        fruit_type = "watermelon"
    else:
        fruit_type = "bomb"
    return Fruit((x, y), (vx, vy), fruit_type)

fruits = []
last_spawn_time = time.time()
score = 0
game_over = False

# ----------------------------
# OpenCV Video Capture Setup
# ----------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Unable to access the webcam.")

def get_index_finger_tip(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        h, w, _ = frame.shape
        lm = hand_landmarks.landmark[8]  # index finger tip
        x_px, y_px = int(lm.x * w), int(lm.y * h)
        return (x_px, y_px)
    return None

def get_eye_cursor(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        # Use right iris landmarks (indices 468-472) for an approximate center.
        iris_points = [landmarks[i] for i in range(468, 473)]
        h, w, _ = frame.shape
        avg_x = sum([pt.x for pt in iris_points]) / len(iris_points)
        avg_y = sum([pt.y for pt in iris_points]) / len(iris_points)
        x_px, y_px = int(avg_x * w), int(avg_y * h)
        return (x_px, y_px)
    return None

# Variable for smoothed cursor (common for both modes)
smoothed_cursor = None

# ----------------------------
# Mode Setup: "hand" or "eye"
# ----------------------------
mode = "hand"  # default mode is hand tracking

# Sensitivity factors for movement.
eye_sensitivity = 3.5  
hand_sensitivity = 1.45 

# ----------------------------
# Main Game Loop
# ----------------------------
running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds per frame

    # Process events including a mode toggle (press M)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_m:
                # Toggle between "hand" and "eye" mode
                mode = "eye" if mode == "hand" else "hand"
                smoothed_cursor = None  # reset smoothing when switching modes

    if game_over:
        running = False

    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(GAME_DURATION - elapsed_time))
    if remaining_time <= 0:
        running = False

    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)  # mirror view

    # --- Cursor Position Depending on Mode ---
    cursor_pos = None
    if mode == "hand":
        pos = get_index_finger_tip(frame)
        if pos is not None:
            cam_h, cam_w, _ = frame.shape
            center_x, center_y = cam_w / 2, cam_h / 2
            offset_x = pos[0] - center_x
            offset_y = pos[1] - center_y
            new_x = int(screen_width / 2 + offset_x * hand_sensitivity)
            new_y = int(screen_height / 2 + offset_y * hand_sensitivity)
            cursor_pos = (new_x, new_y)
    elif mode == "eye":
        pos = get_eye_cursor(frame)
        if pos is not None:
            cam_h, cam_w, _ = frame.shape
            center_x, center_y = cam_w / 2, cam_h / 2
            offset_x = pos[0] - center_x
            offset_y = pos[1] - center_y
            new_x = int(screen_width / 2 + offset_x * eye_sensitivity)
            new_y = int(screen_height / 2 + offset_y * eye_sensitivity)
            cursor_pos = (new_x, new_y)

    # --- Smooth the Cursor ---
    if cursor_pos is not None:
        if smoothed_cursor is None:
            smoothed_cursor = cursor_pos
        else:
            smoothed_cursor = (int(smoothed_cursor[0] * 0.5 + cursor_pos[0] * 0.5),
                               int(smoothed_cursor[1] * 0.5 + cursor_pos[1] * 0.5))
    # If no new detection, smoothed_cursor remains unchanged.

    # --- Gradually Increase Spawn Rate ---
    current_spawn_interval = max(2.0 - (elapsed_time / GAME_DURATION) * 1.5, 0.5)
    current_time = time.time()
    if current_time - last_spawn_time > current_spawn_interval:
        fruits.append(spawn_fruit(elapsed_time))
        last_spawn_time = current_time

    # --- Update fruits ---
    for fruit in fruits:
        fruit.update(dt)
    fruits = [fruit for fruit in fruits if fruit.pos[1] < screen_height + 50]

    # --- Check collisions (slicing) ---
    for fruit in fruits[:]:
        if smoothed_cursor is not None:
            dist = np.hypot(fruit.pos[0] - smoothed_cursor[0], fruit.pos[1] - smoothed_cursor[1])
            if dist < fruit.radius:
                if fruit.type == "bomb":
                    anim_color = (255, 0, 0)
                elif fruit.type == "banana":
                    anim_color = (255, 255, 0)
                elif fruit.type == "watermelon":
                    anim_color = (0, 255, 0)
                else:
                    anim_color = (255, 0, 0)
                slicing_animations.append(SlicingAnimation((int(fruit.pos[0]), int(fruit.pos[1])), anim_color))
                if fruit.type != "bomb":
                    if fruit.type == "banana":
                        splash_color = (255, 255, 0)
                    elif fruit.type == "watermelon":
                        splash_color = (0, 255, 0)
                    else:
                        splash_color = (255, 0, 0)
                    splash_effects.append(SplashEffect((int(fruit.pos[0]), int(fruit.pos[1])), splash_color))
                    stains.append(Stain((int(fruit.pos[0]), int(fruit.pos[1])), splash_color, duration=10, size=random.randint(50,80)))
                if fruit.type == "bomb":
                    if bomb_sound:
                        bomb_sound.play()
                    print("Bomb sliced! Game over.")
                    game_over = True
                    fruits.remove(fruit)
                    break
                else:
                    if slice_sound:
                        slice_sound.play()
                    fruits.remove(fruit)
                    if fruit.type == "banana":
                        score += 2
                        print("Banana sliced! Score:", score)
                    elif fruit.type == "watermelon":
                        score += 3
                        print("Watermelon sliced! Score:", score)
                    else:
                        score += 1
                        print("Apple sliced! Score:", score)

    # --- Update slicing animations ---
    for anim in slicing_animations:
        anim.update(dt)
    slicing_animations = [anim for anim in slicing_animations if not anim.is_finished()]

    # --- Update splash effects ---
    for splash in splash_effects:
        splash.update(dt)
    splash_effects = [splash for splash in splash_effects if not splash.is_finished()]

    # --- Update stains (persistent background water splash stains) ---
    for stain in stains:
        stain.update(dt)
    stains = [stain for stain in stains if not stain.is_finished()]

    # --- Render the game scene ---
    screen.fill((54, 39, 18))
    num_lines = 10
    for i in range(1, num_lines):
        x = int(i * screen_width / num_lines)
        pygame.draw.line(screen, (154, 123, 79), (x, 0), (x, screen_height), 1)
    for stain in stains:
        stain.draw(screen)
    for fruit in fruits:
        fruit.draw(screen)
    for anim in slicing_animations:
        anim.draw(screen)
    for splash in splash_effects:
        splash.draw(screen)
    if smoothed_cursor is not None:
        # Draw a different cursor color depending on mode.
        cursor_color = (0, 255, 255) if mode == "eye" else (255, 255, 255)
        pygame.draw.circle(screen, cursor_color, smoothed_cursor, 5)
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    timer_surface = font.render(f"Time: {remaining_time}", True, (255, 255, 255))
    screen.blit(timer_surface, (screen_width - 150, 10))
    mode_surface = font.render(f"Mode: {mode.upper()} (Press M to toggle)", True, (200, 200, 200))
    screen.blit(mode_surface, (10, 50))
    pygame.display.flip()

# ----------------------------
# Game Over Screen
# ----------------------------
screen.fill((0, 0, 0))
game_over_text = font.render("Game Over!", True, (255, 0, 0))
final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2))
pygame.display.flip()
pygame.time.delay(3000)
# ----------------------------
# Cleanup
# ----------------------------
cap.release()
pygame.quit()
hands.close()
face_mesh.close()
import pygame
import random
import sys
import math
import json
import os
import asyncio  # Add this with other imports

# Then at the very bottom of your file, REPLACE the main() call with:
if __name__ == "__main__":
    asyncio.run(main())
# Initialize
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("💥 CANDY BLAST DELUXE - 10 NEW FEATURES! 💥")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 255)
ORANGE = (255, 150, 50)
PINK = (255, 100, 150)
CYAN = (50, 255, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
DARK_GRAY = (64, 64, 64)
BROWN = (139, 69, 19)

# Neon colors
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (0, 255, 255)
NEON_PURPLE = (191, 0, 255)
NEON_ORANGE = (255, 165, 0)
NEON_YELLOW = (255, 255, 0)
NEON_RED = (255, 30, 30)

# Characters
CHARACTERS = {
    0: {"name": "🍬 BASIC", "color": GOLD, "speed": 8, "ability": "Normal", "special": "None"},
    1: {"name": "⚡ SPEEDSTER", "color": NEON_GREEN, "speed": 13, "ability": "Fast", "special": "30% faster"},
    2: {"name": "🛡️ TANK", "color": NEON_BLUE, "speed": 6, "ability": "Tough", "special": "Start with 7 lives"},
    3: {"name": "💰 MAGNET", "color": NEON_PURPLE, "speed": 8, "ability": "Magnet", "special": "Pulls items"},
    4: {"name": "✨ DOUBLE", "color": NEON_PINK, "speed": 8, "ability": "Double", "special": "Double points always"},
    5: {"name": "🔥 PHOENIX", "color": NEON_RED, "speed": 9, "ability": "Rebirth", "special": "One free revive"},
    6: {"name": "🌈 RAINBOW", "color": NEON_YELLOW, "speed": 10, "ability": "Rainbow", "special": "Rainbow trail"},
    7: {"name": "👑 KING", "color": GOLD, "speed": 9, "ability": "Royal", "special": "Extra coins + double combo"}
}

# Levels
LEVELS = {
    1: {"name": "🍭 CANDY MEADOW", "required": 0, "bg_color": (50, 150, 255)},
    2: {"name": "🍬 GUMDROP FOREST", "required": 500, "bg_color": (50, 200, 100)},
    3: {"name": "🍫 CHOCOLATE MOUNTAIN", "required": 1500, "bg_color": (139, 69, 19)},
    4: {"name": "🍦 ICE CREAM VALLEY", "required": 3000, "bg_color": (100, 200, 255)},
    5: {"name": "🎂 CAKE KINGDOM", "required": 5000, "bg_color": (255, 182, 193)},
    6: {"name": "⭐ STAR DESSERT", "required": 7500, "bg_color": (255, 215, 0)},
    7: {"name": "🌈 RAINBOW LAND", "required": 10000, "bg_color": (147, 112, 219)},
    8: {"name": "💎 DIAMOND WORLD", "required": 15000, "bg_color": (192, 192, 192)},
    9: {"name": "👑 ROYAL SWEETS", "required": 20000, "bg_color": (255, 215, 0)},
    10: {"name": "🎉 PARTY PARADISE", "required": 30000, "bg_color": (255, 105, 180)}
}

# Power-ups
POWERUPS = {
    "shield": {"name": "🛡️", "color": BLUE, "duration": 10},
    "double": {"name": "✨", "color": GOLD, "duration": 10},
    "slow": {"name": "🐢", "color": CYAN, "duration": 8},
    "coin": {"name": "💰", "color": GOLD, "duration": 0},
    "magnet": {"name": "🧲", "color": NEON_PURPLE, "duration": 8},
    "heart": {"name": "❤️", "color": RED, "duration": 0},
    "star": {"name": "⭐", "color": GOLD, "duration": 0},
    "rainbow": {"name": "🌈", "color": NEON_PINK, "duration": 12},
    "freeze": {"name": "❄️", "color": CYAN, "duration": 5},
    "super": {"name": "💥", "color": NEON_RED, "duration": 8}
}

# Game variables
score = 0
lives = 5
level = 1
coins = 0
streak = 0
max_streak = 0
selected_character = 0
game_active = True
invincible_timer = 0
rainbow_trail = []
super_active = False

# Player
player_width = 90
player_height = 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 70
player_speed = CHARACTERS[selected_character]["speed"]

# Game objects
candies = []
bombs = []
mines = []
powerups = []
hearts = []
stars = []
golden_candies = []
rainbow_candies = []

# Timers
double_points_timer = 0
slow_motion_timer = 0
shield_active = False
magnet_active = False
magnet_timer = 0
rainbow_power_timer = 0
freeze_timer = 0
phoenix_used = False
super_timer = 0

# Sound system
pygame.mixer.set_num_channels(8)

def create_simple_sound(frequency, duration, volume=0.3):
    try:
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        samples = bytearray()
        for i in range(n_samples):
            value = int(volume * 32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
            samples.append(value & 0xFF)
            samples.append((value >> 8) & 0xFF)
            samples.append(value & 0xFF)
            samples.append((value >> 8) & 0xFF)
        return pygame.mixer.Sound(buffer=bytes(samples))
    except:
        return None

# Create sounds
catch_sound = create_simple_sound(880, 0.15, 0.3)
bomb_sound = create_simple_sound(220, 0.3, 0.4)
mine_sound = create_simple_sound(110, 0.4, 0.5)
powerup_sound = create_simple_sound(1318, 0.2, 0.3)
coin_sound = create_simple_sound(1568, 0.1, 0.3)
levelup_sound = create_simple_sound(1046, 0.2, 0.4)
menu_sound = create_simple_sound(880, 0.15, 0.4)
heart_sound = create_simple_sound(988, 0.2, 0.3)
star_sound = create_simple_sound(1174, 0.2, 0.3)
super_sound = create_simple_sound(1318, 0.3, 0.5)
level_complete_sound = create_simple_sound(1568, 0.5, 0.4)

def play_sound(sound):
    if sound:
        try:
            sound.stop()
            sound.play()
        except:
            pass

# Background music
def create_background_music():
    try:
        sample_rate = 22050
        duration = 4.0
        melody = [523, 587, 659, 698, 784, 659, 587, 523, 523, 587, 659, 784, 880]
        note_duration = duration / len(melody)
        samples = bytearray()
        for freq in melody:
            note_samples = int(sample_rate * note_duration)
            for t in range(note_samples):
                envelope = 1.0
                if t < 500:
                    envelope = t / 500
                if t > note_samples - 500:
                    envelope = (note_samples - t) / 500
                value = int(8192 * envelope * math.sin(2 * math.pi * freq * t / sample_rate))
                samples.append(value & 0xFF)
                samples.append((value >> 8) & 0xFF)
                samples.append(value & 0xFF)
                samples.append((value >> 8) & 0xFF)
        sound = pygame.mixer.Sound(buffer=bytes(samples))
        sound.set_volume(0.2)
        return sound
    except:
        return None

background_music = create_background_music()
music_playing = False
music_channel = None

def start_background_music():
    global music_playing, music_channel
    if background_music and not music_playing:
        try:
            music_channel = pygame.mixer.find_channel()
            if music_channel:
                music_channel.play(background_music, loops=-1)
                music_playing = True
        except:
            pass

def stop_background_music():
    global music_playing, music_channel
    if music_playing and music_channel:
        try:
            music_channel.stop()
            music_playing = False
        except:
            pass

# Particle systems
particles = []
floating_candies = []
sparkles = []
confetti = []

def add_confetti(x, y, count=30):
    for _ in range(count):
        confetti.append({
            "x": x, "y": y,
            "vx": random.uniform(-8, 8),
            "vy": random.uniform(-12, -3),
            "life": 60,
            "color": random.choice([NEON_PINK, NEON_GREEN, NEON_BLUE, NEON_YELLOW, NEON_ORANGE, NEON_PURPLE]),
            "size": random.randint(3, 7)
        })

def update_confetti():
    for c in confetti[:]:
        c["x"] += c["vx"]
        c["y"] += c["vy"]
        c["vy"] += 0.2
        c["life"] -= 1
        if c["life"] <= 0:
            confetti.remove(c)

def draw_confetti():
    for c in confetti:
        alpha = c["life"] / 60
        color = tuple(int(c_color * alpha) for c_color in c["color"])
        pygame.draw.rect(screen, color, (int(c["x"]), int(c["y"]), int(c["size"]), int(c["size"])))

def create_floating_candies():
    global floating_candies
    floating_candies = []
    for i in range(25):
        floating_candies.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),
            "speed": random.uniform(0.5, 2.5),
            "size": random.randint(20, 45),
            "color": random.choice([(255, 182, 193), (216, 191, 216), (152, 255, 152), (255, 218, 185)]),
            "rotation": random.randint(0, 360),
            "rot_speed": random.uniform(-3, 3),
            "pulse": random.uniform(0, math.pi * 2)
        })

def update_floating_candies():
    for candy in floating_candies:
        candy["y"] += candy["speed"]
        candy["rotation"] += candy["rot_speed"]
        candy["pulse"] += 0.05
        if candy["y"] > HEIGHT + 100:
            candy["y"] = -100
            candy["x"] = random.randint(0, WIDTH)
        if candy["y"] < -100:
            candy["y"] = HEIGHT + 100

def draw_floating_candies():
    for candy in floating_candies:
        pulse_size = candy["size"] + math.sin(candy["pulse"]) * 5
        candy_surface = pygame.Surface((int(pulse_size * 2), int(pulse_size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(candy_surface, candy["color"], (int(pulse_size), int(pulse_size)), int(pulse_size))
        pygame.draw.line(candy_surface, WHITE, (int(pulse_size - 12), int(pulse_size - 8)), 
                        (int(pulse_size + 12), int(pulse_size - 8)), 4)
        pygame.draw.line(candy_surface, WHITE, (int(pulse_size - 12), int(pulse_size + 8)), 
                        (int(pulse_size + 12), int(pulse_size + 8)), 4)
        pygame.draw.circle(candy_surface, BLACK, (int(pulse_size - 8), int(pulse_size - 5)), 3)
        pygame.draw.circle(candy_surface, BLACK, (int(pulse_size + 8), int(pulse_size - 5)), 3)
        pygame.draw.arc(candy_surface, BLACK, (int(pulse_size - 10), int(pulse_size), 20, 10), 0, 3.14, 2)
        rotated = pygame.transform.rotate(candy_surface, candy["rotation"])
        screen.blit(rotated, (candy["x"] - pulse_size, candy["y"] - pulse_size))

def add_sparkle(x, y):
    sparkles.append({
        "x": x, "y": y,
        "life": 60,
        "size": random.randint(2, 5),
        "color": random.choice([GOLD, NEON_PINK, NEON_BLUE, NEON_GREEN, NEON_YELLOW])
    })

def update_sparkles():
    for s in sparkles[:]:
        s["life"] -= 1
        s["size"] *= 0.95
        if s["life"] <= 0 or s["size"] < 0.5:
            sparkles.remove(s)

def draw_sparkles():
    for s in sparkles:
        alpha = s["life"] / 60
        color = tuple(int(c * alpha) for c in s["color"])
        pygame.draw.circle(screen, color, (int(s["x"]), int(s["y"])), int(s["size"]))

def add_particles(x, y, color, count=20):
    for _ in range(count):
        particles.append({
            "x": x, "y": y,
            "vx": random.uniform(-5, 5),
            "vy": random.uniform(-8, -2),
            "life": 30,
            "color": color,
            "size": random.randint(3, 7)
        })

def update_particles():
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.3
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

def draw_particles():
    for p in particles:
        alpha = p["life"] / 30
        color = tuple(int(c * alpha) for c in p["color"])
        pygame.draw.circle(screen, color, (int(p["x"]), int(p["y"])), int(p["size"]))

def draw_player():
    global player_x, rainbow_trail
    char = CHARACTERS[selected_character]
    
    if selected_character == 6:
        rainbow_trail.append((player_x + 45, player_y + 20, pygame.time.get_ticks()))
        for trail in rainbow_trail[:]:
            if pygame.time.get_ticks() - trail[2] > 500:
                rainbow_trail.remove(trail)
            else:
                alpha = 255 - (pygame.time.get_ticks() - trail[2]) * 0.5
                color = (int(255 * alpha/255), int(100 * alpha/255), int(255 * alpha/255))
                pygame.draw.circle(screen, color, (int(trail[0]), int(trail[1])), 10)
    
    for i in range(3):
        glow_rect = pygame.Rect(player_x - i*2, player_y - i*2, 90 + i*4, 40 + i*4)
        pygame.draw.rect(screen, char["color"], glow_rect, border_radius=10, width=2)
    
    pygame.draw.rect(screen, char["color"], (player_x, player_y, player_width, player_height), border_radius=8)
    pygame.draw.rect(screen, NEON_PINK, (player_x + 5, player_y - 12, 80, 15), border_radius=5)
    
    pygame.draw.circle(screen, WHITE, (player_x + 25, player_y + 15), 8)
    pygame.draw.circle(screen, WHITE, (player_x + 65, player_y + 15), 8)
    pygame.draw.circle(screen, BLACK, (player_x + 25, player_y + 15), 4)
    pygame.draw.circle(screen, BLACK, (player_x + 65, player_y + 15), 4)
    pygame.draw.arc(screen, BLACK, (player_x + 35, player_y + 20, 20, 15), 0, 3.14, 3)
    
    if invincible_timer > 0:
        if pygame.time.get_ticks() % 200 < 100:
            pygame.draw.circle(screen, GOLD, (player_x + 45, player_y + 20), 60, 5)
    
    if shield_active or rainbow_power_timer > 0:
        pygame.draw.circle(screen, CYAN, (player_x + 45, player_y + 20), 55, 3)
        for i in range(8):
            angle = pygame.time.get_ticks() * 0.005 + i * math.pi/4
            x = player_x + 45 + math.cos(angle) * 50
            y = player_y + 20 + math.sin(angle) * 30
            pygame.draw.circle(screen, NEON_BLUE, (int(x), int(y)), 3)
    
    if magnet_active or rainbow_power_timer > 0:
        for i in range(6):
            angle = pygame.time.get_ticks() * 0.01 + i * math.pi/3
            x = player_x + 45 + math.cos(angle) * 40
            y = player_y + 20 + math.sin(angle) * 30
            pygame.draw.circle(screen, NEON_PURPLE, (int(x), int(y)), 5)

def spawn_objects():
    global candies, bombs, mines, powerups, hearts, stars, golden_candies, rainbow_candies
    
    if random.randint(1, 18) < 4:
        points = 10 * (2 if double_points_timer > 0 or selected_character == 4 else 1)
        if rainbow_power_timer > 0 or super_active:
            points *= 5
        candies.append({
            "x": random.randint(30, WIDTH - 30),
            "y": -30,
            "points": points,
            "speed": 4 + level // 2
        })
    
    if random.randint(1, 150) < 3:
        golden_candies.append({
            "x": random.randint(30, WIDTH - 30),
            "y": -30,
            "points": 50 * (2 if double_points_timer > 0 or selected_character == 4 else 1),
            "speed": 3 + level // 3
        })
    
    if random.randint(1, 200) < 3:
        rainbow_candies.append({
            "x": random.randint(30, WIDTH - 30),
            "y": -30,
            "points": 30,
            "speed": 3 + level // 3
        })
    
    if random.randint(1, 55) < 3 + level // 3:
        bombs.append({
            "x": random.randint(30, WIDTH - 30),
            "y": -30,
            "speed": 5 + level // 3
        })
    
    if random.randint(1, 85) < 2 + level // 4:
        mines.append({
            "x": random.randint(30, WIDTH - 30),
            "y": -30,
            "speed": 4 + level // 3
        })
    
    if random.randint(1, 220) < 3:
        hearts.append({
            "x": random.randint(30, WIDTH - 30),
            "y": -30,
            "speed": 3
        })
    
    if random.randint(1, 180) < 4:
        stars.append({
            "x": random.randint(30, WIDTH - 30),
            "y": -30,
            "speed": 3,
            "points": 50
        })
    
    if random.randint(1, 160) < 3:
        power_type = random.choice(["shield", "double", "slow", "coin", "magnet", "rainbow", "freeze", "super"])
        powerups.append({
            "x": random.randint(30, WIDTH - 30),
            "y": -30,
            "type": power_type,
            "speed": 4
        })

def check_collision(obj_x, obj_y, obj_size=30):
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    obj_rect = pygame.Rect(obj_x - obj_size//2, obj_y - obj_size//2, obj_size, obj_size)
    return player_rect.colliderect(obj_rect)

def draw_ui():
    rainbow_colors = [NEON_RED, NEON_ORANGE, NEON_YELLOW, NEON_GREEN, NEON_BLUE, NEON_PURPLE]
    color_index = (pygame.time.get_ticks() // 100) % len(rainbow_colors)
    score_text = font_large.render(str(score), True, rainbow_colors[color_index])
    screen.blit(score_text, (20, 10))
    
    char_text = font_tiny.render(CHARACTERS[selected_character]["name"], True, CHARACTERS[selected_character]["color"])
    screen.blit(char_text, (20, 75))
    
    for i in range(min(lives, 10)):
        heart_x = WIDTH - 40 - i * 45
        heart_y = 30 + math.sin(pygame.time.get_ticks() * 0.005 + i) * 5
        pygame.draw.circle(screen, RED, (heart_x, heart_y), 15)
        pygame.draw.circle(screen, RED, (heart_x, heart_y - 8), 12)
        pygame.draw.polygon(screen, RED, [
            (heart_x - 8, heart_y - 5), (heart_x, heart_y + 10), (heart_x + 8, heart_y - 5)
        ])
    
    coin_text = font_small.render(f"💰 {coins}", True, GOLD)
    screen.blit(coin_text, (WIDTH - 150, 10))
    
    level_name = LEVELS[level]["name"]
    level_text = font_small.render(f"⭐ {level_name} ⭐", True, NEON_BLUE)
    pulse = math.sin(pygame.time.get_ticks() * 0.008) * 5
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10 + pulse))
    
    if streak > 0:
        if streak >= 20:
            streak_text = font_medium.render(f"🎉 MEGA STREAK: {streak} 🎉", True, NEON_RED)
        elif streak >= 10:
            streak_text = font_medium.render(f"⚡ SUPER STREAK: {streak} ⚡", True, NEON_ORANGE)
        else:
            streak_text = font_medium.render(f"🔥 STREAK: {streak} 🔥", True, NEON_PINK)
        combo_pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 10
        screen.blit(streak_text, (WIDTH // 2 - streak_text.get_width() // 2, 70 + combo_pulse))
    
    y_offset = 120
    if double_points_timer > 0:
        text = font_tiny.render(f"✨ 2x POINTS: {double_points_timer//60}s", True, GOLD)
        screen.blit(text, (20, y_offset))
        y_offset += 22
    if slow_motion_timer > 0:
        text = font_tiny.render(f"🐢 SLOW TIME: {slow_motion_timer//60}s", True, CYAN)
        screen.blit(text, (20, y_offset))
        y_offset += 22
    if magnet_active:
        text = font_tiny.render(f"🧲 MAGNET: {magnet_timer//60}s", True, NEON_PURPLE)
        screen.blit(text, (20, y_offset))
        y_offset += 22
    if rainbow_power_timer > 0:
        text = font_tiny.render(f"🌈 RAINBOW: {rainbow_power_timer//60}s", True, NEON_PINK)
        screen.blit(text, (20, y_offset))
        y_offset += 22
    if freeze_timer > 0:
        text = font_tiny.render(f"❄️ FREEZE: {freeze_timer//60}s", True, CYAN)
        screen.blit(text, (20, y_offset))
        y_offset += 22
    if super_active:
        text = font_tiny.render(f"💥 SUPER: {super_timer//60}s", True, NEON_RED)
        screen.blit(text, (20, y_offset))

def show_game_over():
    global game_active, score, max_streak, coins
    
    screen.fill(BLACK)
    
    rainbow_colors = [NEON_RED, NEON_ORANGE, NEON_YELLOW, NEON_GREEN, NEON_BLUE, NEON_PURPLE]
    for i, letter in enumerate("GAME OVER!"):
        y_offset = math.sin(pygame.time.get_ticks() * 0.005 + i) * 10
        color = rainbow_colors[i % len(rainbow_colors)]
        text = font_large.render(letter, True, color)
        screen.blit(text, (WIDTH//2 - 200 + i * 45, HEIGHT//2 - 150 + y_offset))
    
    stats = [
        (f"🎯 Final Score: {score}", GOLD),
        (f"💪 BEST STREAK: {max_streak}", NEON_PINK),
        (f"💰 Coins Collected: {coins}", YELLOW),
        (f"👑 Character: {CHARACTERS[selected_character]['name']}", CHARACTERS[selected_character]["color"]),
        (f"🌟 Highest Level: {level}", NEON_BLUE)
    ]
    
    y_pos = HEIGHT // 2 - 80
    for stat, color in stats:
        text = font_small.render(stat, True, color)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, y_pos))
        y_pos += 40
    
    play_text = font_medium.render("🎮 PRESS SPACE TO PLAY AGAIN 🎮", True, NEON_GREEN)
    menu_text = font_small.render("ESC for MENU", True, WHITE)
    
    pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 10
    screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, HEIGHT//2 + 100 + pulse))
    screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT - 100))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
    return False

def reset_game():
    global score, lives, level, coins, streak, max_streak, game_active
    global player_x, candies, bombs, mines, powerups, hearts, stars, golden_candies, rainbow_candies
    global double_points_timer, slow_motion_timer, shield_active, magnet_active, magnet_timer
    global rainbow_power_timer, freeze_timer, super_active, super_timer, phoenix_used, particles
    global invincible_timer, selected_character, player_speed
    
    score = 0
    lives = 5
    if selected_character == 2:
        lives = 7
    level = 1
    coins = 0
    streak = 0
    max_streak = 0
    game_active = True
    phoenix_used = False
    player_speed = CHARACTERS[selected_character]["speed"]
    player_x = WIDTH // 2 - player_width // 2
    candies.clear()
    bombs.clear()
    mines.clear()
    powerups.clear()
    hearts.clear()
    stars.clear()
    golden_candies.clear()
    rainbow_candies.clear()
    particles.clear()
    double_points_timer = 0
    slow_motion_timer = 0
    shield_active = False
    magnet_active = False
    magnet_timer = 0
    rainbow_power_timer = 0
    freeze_timer = 0
    super_active = False
    super_timer = 0
    invincible_timer = 0

def show_character_select():
    global selected_character
    selecting = True
    
    while selecting:
        screen.fill(BLACK)
        
        title = font_large.render("SELECT YOUR CHARACTER!", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        for i, (key, char) in enumerate(CHARACTERS.items()):
            y_pos = 150 + i * 55
            color = NEON_GREEN if i == selected_character else WHITE
            text = font_small.render(f"{char['name']} - {char['special']}", True, color)
            screen.blit(text, (WIDTH//2 - 250, y_pos))
            
            if i == selected_character:
                pygame.draw.circle(screen, NEON_GREEN, (WIDTH//2 - 280, y_pos + 15), 10)
        
        instruct = font_small.render("Press UP/DOWN to change | SPACE to select | ESC to back", True, WHITE)
        screen.blit(instruct, (WIDTH//2 - instruct.get_width()//2, HEIGHT - 100))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_character = (selected_character - 1) % len(CHARACTERS)
                    play_sound(menu_sound)
                elif event.key == pygame.K_DOWN:
                    selected_character = (selected_character + 1) % len(CHARACTERS)
                    play_sound(menu_sound)
                elif event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
    
    return True

# Fonts
font_title = pygame.font.Font(None, 120)
font_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)
font_tiny = pygame.font.Font(None, 24)
font_very_tiny = pygame.font.Font(None, 18)

def show_main_menu():
    global floating_candies
    
    start_background_music()
    create_floating_candies()
    
    clouds = []
    for i in range(5):
        clouds.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(50, 200),
            "speed": random.uniform(0.3, 0.8),
            "size": random.randint(50, 100)
        })
    
    stars_bg = []
    for i in range(100):
        stars_bg.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),
            "size": random.randint(1, 3),
            "twinkle_speed": random.uniform(0.5, 2)
        })
    
    while True:
        screen.fill(NEON_BLUE)
        
        # Gradient sky
        for y in range(HEIGHT):
            color_val = int(100 + y * 0.1)
            pygame.draw.line(screen, (50, color_val, 255), (0, y), (WIDTH, y))
        
        # Clouds
        for cloud in clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > WIDTH + 100:
                cloud["x"] = -100
            pygame.draw.ellipse(screen, WHITE, (cloud["x"], cloud["y"], cloud["size"], cloud["size"]//2))
            pygame.draw.ellipse(screen, WHITE, (cloud["x"] + 30, cloud["y"] - 20, cloud["size"]//1.5, cloud["size"]//2))
        
        # Stars
        for star in stars_bg:
            twinkle = 100 + math.sin(pygame.time.get_ticks() * 0.002 * star["twinkle_speed"]) * 100
            pygame.draw.circle(screen, (255, 255, int(twinkle)), (star["x"], star["y"]), star["size"])
        
        # Floating candies
        update_floating_candies()
        draw_floating_candies()
        
        # Title
        bounce = math.sin(pygame.time.get_ticks() * 0.003) * 10
        rainbow_colors = [NEON_RED, NEON_ORANGE, NEON_YELLOW, NEON_GREEN, NEON_BLUE, NEON_PURPLE]
        
        for i, letter in enumerate("CANDY"):
            color = rainbow_colors[i % len(rainbow_colors)]
            letter_text = font_title.render(letter, True, color)
            screen.blit(letter_text, (WIDTH//2 - 180 + i * 55, 50 + bounce))
        
        blast_text = font_title.render("BLAST", True, GOLD)
        screen.blit(blast_text, (WIDTH//2 - blast_text.get_width()//2, 130 + bounce))
        
        subtitle = font_medium.render("🎈 DELUXE EDITION - 8 CHARACTERS! 🎈", True, NEON_PINK)
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 200))
        
        # Rainbow arch
        for i in range(7):
            color = pygame.Color(0)
            color.hsva = (i * 50, 100, 100, 100)
            arc_rect = pygame.Rect(WIDTH//2 - 300 + i*20, 270, 600 - i*40, 80)
            pygame.draw.arc(screen, color, arc_rect, 0, math.pi, 5)
        
        # High score
        try:
            with open("highscore.json", "r") as f:
                highscore = json.load(f)["highscore"]
        except:
            highscore = 0
        
        high_pulse = abs(math.sin(pygame.time.get_ticks() * 0.003)) * 5
        high_text = font_medium.render(f"🏆 {highscore} 🏆", True, GOLD)
        screen.blit(high_text, (WIDTH//2 - high_text.get_width()//2, 310 + high_pulse))
        high_label = font_small.render("HIGH SCORE", True, NEON_PINK)
        screen.blit(high_label, (WIDTH//2 - high_label.get_width()//2, 280))
        
        # Play button
        button_pulse = abs(math.sin(pygame.time.get_ticks() * 0.003)) * 10
        play_rect = pygame.Rect(WIDTH//2 - 180, 360, 360, 70)
        pygame.draw.rect(screen, BLACK, play_rect.move(5, 5), border_radius=20)
        for i in range(70):
            color = pygame.Color(0)
            color.hsva = ((pygame.time.get_ticks() * 0.05 + i * 2) % 360, 100, 100, 100)
            pygame.draw.rect(screen, color, (play_rect.x, play_rect.y + i, play_rect.width, 1))
        pygame.draw.rect(screen, NEON_GREEN, play_rect, border_radius=20, width=3)
        play_text = font_medium.render("🎮 PLAY NOW! 🎮", True, WHITE)
        screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, 380 + button_pulse//2))
        
        # Characters button
        char_rect = pygame.Rect(WIDTH//2 - 190, 450, 400, 60)
        pygame.draw.rect(screen, BLACK, char_rect.move(5, 5), border_radius=15)
        pygame.draw.rect(screen, NEON_PURPLE, char_rect, border_radius=15, width=3)
        char_text = font_medium.render("👑 CHOOSE CHARACTER", True, WHITE)
        screen.blit(char_text, (WIDTH//2 - char_text.get_width()//2, 468))
        
        # Current character
        current_char = font_small.render(f"Current: {CHARACTERS[selected_character]['name']}", 
                                         True, CHARACTERS[selected_character]["color"])
        screen.blit(current_char, (WIDTH//2 - current_char.get_width()//2, 520))
        
        # Feature boxes - FIXED: Larger boxes with proper text fitting
        features = [
            {"icon": "🎮", "title": "8 CHARACTERS", "line1": "Each unique", "line2": "ability!", "color": NEON_GREEN},
            {"icon": "💥", "title": "10 POWER-UPS", "line1": "Rainbow, Freeze,", "line2": "Super!", "color": NEON_RED},
            {"icon": "⭐", "title": "10 LEVELS", "line1": "Each with", "line2": "unique theme!", "color": NEON_BLUE},
            {"icon": "🏆", "title": "HIGH SCORE", "line1": "Beat your", "line2": "record!", "color": GOLD}
        ]
        
        box_width = 210
        box_height = 85
        start_x = (WIDTH - (box_width * 4 + 20)) // 2
        
        for i, feature in enumerate(features):
            box_x = start_x + i * (box_width + 7)
            box_y = HEIGHT - 115
            
            # Box background
            pygame.draw.rect(screen, (20, 20, 40), (box_x, box_y, box_width, box_height), border_radius=12)
            pygame.draw.rect(screen, feature["color"], (box_x, box_y, box_width, box_height), border_radius=12, width=2)
            
            # Icon
            icon_text = font_medium.render(feature["icon"], True, feature["color"])
            screen.blit(icon_text, (box_x + 12, box_y + 12))
            
            # Title
            title_text = font_very_tiny.render(feature["title"], True, WHITE)
            screen.blit(title_text, (box_x + 55, box_y + 12))
            
            # Description lines
            line1_text = font_very_tiny.render(feature["line1"], True, SILVER)
            screen.blit(line1_text, (box_x + 55, box_y + 35))
            line2_text = font_very_tiny.render(feature["line2"], True, SILVER)
            screen.blit(line2_text, (box_x + 55, box_y + 55))
        
        # Controls
        controls_text = font_small.render("← → or A D to move | SPACE to start | M to mute", True, WHITE)
        screen.blit(controls_text, (WIDTH//2 - controls_text.get_width()//2, HEIGHT - 28))
        
        # Music indicator
        if music_playing:
            music_indicator = font_very_tiny.render("🎵 MUSIC ON (M to mute)", True, NEON_GREEN)
        else:
            music_indicator = font_very_tiny.render("🔇 MUSIC OFF (M to unmute)", True, SILVER)
        screen.blit(music_indicator, (15, HEIGHT - 28))
        
        # Quit
        quit_text = font_very_tiny.render("ESC to quit", True, SILVER)
        screen.blit(quit_text, (WIDTH - 85, HEIGHT - 28))
        
        # Particles
        update_sparkles()
        draw_sparkles()
        update_confetti()
        draw_confetti()
        update_particles()
        draw_particles()
        
        if random.randint(1, 30) == 1:
            add_sparkle(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_background_music()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_sound(menu_sound)
                    add_confetti(WIDTH//2, HEIGHT//2)
                    stop_background_music()
                    pygame.display.flip()
                    pygame.time.wait(300)
                    return True
                if event.key == pygame.K_ESCAPE:
                    stop_background_music()
                    return False
                if event.key == pygame.K_m:
                    if music_playing:
                        stop_background_music()
                    else:
                        start_background_music()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_x, mouse_y):
                    play_sound(menu_sound)
                    add_confetti(WIDTH//2, HEIGHT//2)
                    stop_background_music()
                    pygame.display.flip()
                    pygame.time.wait(300)
                    return True
                if char_rect.collidepoint(mouse_x, mouse_y):
                    play_sound(menu_sound)
                    show_character_select()
        
        clock.tick(60)

def run_game():
    global score, lives, level, coins, streak, max_streak, game_active, player_x
    global double_points_timer, slow_motion_timer, shield_active, magnet_active, magnet_timer
    global rainbow_power_timer, freeze_timer, super_active, super_timer, phoenix_used
    global invincible_timer, candies, bombs, mines, powerups, hearts, stars
    global golden_candies, rainbow_candies, particles, selected_character
    
    reset_game()
    
    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        if invincible_timer > 0:
            invincible_timer -= 1
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
            add_particles(player_x + 45, player_y + 20, CYAN, 2)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
            add_particles(player_x + 45, player_y + 20, CYAN, 2)
        
        if player_x < 0:
            player_x = 0
        if player_x > WIDTH - player_width:
            player_x = WIDTH - player_width
        
        if double_points_timer > 0:
            double_points_timer -= 1
        if slow_motion_timer > 0:
            slow_motion_timer -= 1
        if magnet_active:
            magnet_timer -= 1
            if magnet_timer <= 0:
                magnet_active = False
        if rainbow_power_timer > 0:
            rainbow_power_timer -= 1
        if freeze_timer > 0:
            freeze_timer -= 1
        if super_active:
            super_timer -= 1
            if super_timer <= 0:
                super_active = False
        
        spawn_objects()
        
        if magnet_active or rainbow_power_timer > 0 or super_active:
            all_items = candies + golden_candies + rainbow_candies + hearts + stars + powerups
            for item in all_items:
                dx = player_x + 45 - item["x"]
                dy = player_y + 20 - item["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < 200:
                    item["x"] += dx * 0.08
                    item["y"] += dy * 0.05
        
        speed_mult = 0 if freeze_timer > 0 else (0.5 if slow_motion_timer > 0 else 1.0)
        
        # Update candies
        for candy in candies[:]:
            candy["y"] += candy["speed"] * speed_mult
            if candy["y"] > HEIGHT:
                candies.remove(candy)
                streak = 0
            elif check_collision(candy["x"], candy["y"]):
                candies.remove(candy)
                points = candy["points"]
                if selected_character == 4:
                    points *= 2
                if selected_character == 7:
                    streak += 2
                else:
                    streak += 1
                score += points
                coins += points // 10
                max_streak = max(max_streak, streak)
                add_particles(candy["x"], candy["y"], YELLOW, 15)
                add_sparkle(candy["x"], candy["y"])
                play_sound(catch_sound)
                
                if level < 10 and score >= LEVELS[level + 1]["required"]:
                    level += 1
                    add_confetti(WIDTH//2, HEIGHT//2, 50)
                    play_sound(level_complete_sound)
        
        # Update golden candies
        for golden in golden_candies[:]:
            golden["y"] += golden["speed"] * speed_mult
            if golden["y"] > HEIGHT:
                golden_candies.remove(golden)
            elif check_collision(golden["x"], golden["y"]):
                golden_candies.remove(golden)
                points = golden["points"]
                if selected_character == 4:
                    points *= 2
                score += points
                coins += points // 10
                streak += 2
                max_streak = max(max_streak, streak)
                add_confetti(golden["x"], golden["y"], 20)
                play_sound(coin_sound)
        
        # Update rainbow candies
        for rainbow in rainbow_candies[:]:
            rainbow["y"] += rainbow["speed"] * speed_mult
            if rainbow["y"] > HEIGHT:
                rainbow_candies.remove(rainbow)
            elif check_collision(rainbow["x"], rainbow["y"]):
                rainbow_candies.remove(rainbow)
                score += rainbow["points"]
                coins += rainbow["points"] // 10
                streak += 3
                max_streak = max(max_streak, streak)
                add_confetti(rainbow["x"], rainbow["y"], 30)
                play_sound(star_sound)
        
        # Update hearts
        for heart in hearts[:]:
            heart["y"] += heart["speed"] * speed_mult
            if heart["y"] > HEIGHT:
                hearts.remove(heart)
            elif check_collision(heart["x"], heart["y"], 20):
                hearts.remove(heart)
                lives += 1
                add_particles(heart["x"], heart["y"], RED, 20)
                play_sound(heart_sound)
        
        # Update stars
        for star in stars[:]:
            star["y"] += star["speed"] * speed_mult
            if star["y"] > HEIGHT:
                stars.remove(star)
            elif check_collision(star["x"], star["y"], 20):
                stars.remove(star)
                score += star["points"]
                coins += star["points"] // 10
                add_confetti(star["x"], star["y"], 25)
                play_sound(star_sound)
        
        # Update bombs
        for bomb in bombs[:]:
            bomb["y"] += bomb["speed"] * speed_mult
            if bomb["y"] > HEIGHT:
                bombs.remove(bomb)
            elif check_collision(bomb["x"], bomb["y"]):
                bombs.remove(bomb)
                if shield_active or rainbow_power_timer > 0 or super_active:
                    shield_active = False
                    add_particles(bomb["x"], bomb["y"], BLUE, 20)
                else:
                    lives -= 1
                    streak = 0
                    add_particles(bomb["x"], bomb["y"], RED, 30)
                    play_sound(bomb_sound)
                    
                    if selected_character == 5 and not phoenix_used and lives <= 0:
                        lives = 3
                        phoenix_used = True
                        invincible_timer = 120
                        add_confetti(WIDTH//2, HEIGHT//2, 100)
                        play_sound(super_sound)
                    elif lives <= 0:
                        game_active = False
        
        # Update mines
        for mine in mines[:]:
            mine["y"] += mine["speed"] * speed_mult
            if mine["y"] > HEIGHT:
                mines.remove(mine)
            elif check_collision(mine["x"], mine["y"], 25):
                mines.remove(mine)
                if shield_active or rainbow_power_timer > 0 or super_active:
                    shield_active = False
                    add_particles(mine["x"], mine["y"], BLUE, 30)
                else:
                    lives -= 2
                    streak = 0
                    add_particles(mine["x"], mine["y"], NEON_RED, 50)
                    play_sound(mine_sound)
                    
                    if selected_character == 5 and not phoenix_used and lives <= 0:
                        lives = 3
                        phoenix_used = True
                        invincible_timer = 120
                        add_confetti(WIDTH//2, HEIGHT//2, 100)
                        play_sound(super_sound)
                    elif lives <= 0:
                        game_active = False
        
        # Update power-ups
        for power in powerups[:]:
            power["y"] += power["speed"] * speed_mult
            if power["y"] > HEIGHT:
                powerups.remove(power)
            elif check_collision(power["x"], power["y"], 25):
                powerups.remove(power)
                
                if power["type"] == "shield":
                    shield_active = True
                elif power["type"] == "double":
                    double_points_timer = 600
                elif power["type"] == "slow":
                    slow_motion_timer = 300
                elif power["type"] == "coin":
                    coins += 100
                elif power["type"] == "magnet":
                    magnet_active = True
                    magnet_timer = 480
                elif power["type"] == "rainbow":
                    rainbow_power_timer = 720
                elif power["type"] == "freeze":
                    freeze_timer = 300
                elif power["type"] == "super":
                    super_active = True
                    super_timer = 480
                    double_points_timer = 480
                    magnet_active = True
                    magnet_timer = 480
                    shield_active = True
                
                add_particles(power["x"], power["y"], GOLD, 30)
                play_sound(powerup_sound)
        
        update_particles()
        update_sparkles()
        update_confetti()
        
        # Draw everything
        screen.fill(LEVELS[level]["bg_color"])
        
        for y in range(HEIGHT):
            color_val = int(100 + y * 0.1)
            base_color = LEVELS[level]["bg_color"]
            pygame.draw.line(screen, (base_color[0], color_val, base_color[2]), (0, y), (WIDTH, y))
        
        # Draw candies
        for candy in candies:
            color = random.choice([(255, 182, 193), (216, 191, 216), (152, 255, 152), (255, 218, 185)])
            pygame.draw.circle(screen, color, (int(candy["x"]), int(candy["y"])), 20)
            pygame.draw.line(screen, WHITE, (candy["x"] - 10, candy["y"] - 5), 
                           (candy["x"] + 10, candy["y"] - 5), 3)
            pygame.draw.circle(screen, BLACK, (int(candy["x"] - 6), int(candy["y"] - 3)), 3)
            pygame.draw.circle(screen, BLACK, (int(candy["x"] + 6), int(candy["y"] - 3)), 3)
            pygame.draw.arc(screen, BLACK, (int(candy["x"] - 8), int(candy["y"]), 16, 10), 0, 3.14, 2)
        
        # Draw golden candies
        for golden in golden_candies:
            pygame.draw.circle(screen, GOLD, (int(golden["x"]), int(golden["y"])), 20)
            pygame.draw.circle(screen, NEON_YELLOW, (int(golden["x"]), int(golden["y"])), 15)
            star_text = font_very_tiny.render("⭐", True, GOLD)
            screen.blit(star_text, (golden["x"] - 8, golden["y"] - 10))
        
        # Draw rainbow candies
        for rainbow in rainbow_candies:
            pygame.draw.circle(screen, NEON_PURPLE, (int(rainbow["x"]), int(rainbow["y"])), 20)
            pygame.draw.circle(screen, NEON_PINK, (int(rainbow["x"]), int(rainbow["y"])), 15)
            pygame.draw.circle(screen, NEON_BLUE, (int(rainbow["x"]), int(rainbow["y"])), 10)
        
        # Draw hearts
        for heart in hearts:
            pygame.draw.circle(screen, RED, (int(heart["x"]), int(heart["y"])), 12)
            pygame.draw.circle(screen, RED, (int(heart["x"]), int(heart["y"] - 6)), 9)
        
        # Draw stars
        for star in stars:
            points = []
            for i in range(5):
                angle = math.radians(i * 72 - 90)
                x1 = star["x"] + math.cos(angle) * 15
                y1 = star["y"] + math.sin(angle) * 15
                points.append((x1, y1))
                angle2 = math.radians(i * 72 + 36 - 90)
                x2 = star["x"] + math.cos(angle2) * 7
                y2 = star["y"] + math.sin(angle2) * 7
                points.append((x2, y2))
            pygame.draw.polygon(screen, GOLD, points)
        
        # Draw bombs
        for bomb in bombs:
            pygame.draw.circle(screen, BLACK, (int(bomb["x"]), int(bomb["y"])), 18)
            pygame.draw.line(screen, RED, (bomb["x"] - 10, bomb["y"] - 10), 
                           (bomb["x"] + 10, bomb["y"] + 10), 3)
            pygame.draw.line(screen, RED, (bomb["x"] + 10, bomb["y"] - 10), 
                           (bomb["x"] - 10, bomb["y"] + 10), 3)
        
        # Draw mines
        for mine in mines:
            pygame.draw.circle(screen, DARK_GRAY, (int(mine["x"]), int(mine["y"])), 20)
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                x1 = mine["x"] + math.cos(rad) * 18
                y1 = mine["y"] + math.sin(rad) * 18
                x2 = mine["x"] + math.cos(rad) * 26
                y2 = mine["y"] + math.sin(rad) * 26
                pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 3)
            pygame.draw.circle(screen, RED, (int(mine["x"]), int(mine["y"])), 8)
        
        # Draw power-ups
        for power in powerups:
            info = POWERUPS[power["type"]]
            pygame.draw.circle(screen, info["color"], (int(power["x"]), int(power["y"])), 15)
            pygame.draw.circle(screen, WHITE, (int(power["x"]), int(power["y"])), 10, 2)
            icon_text = font_very_tiny.render(info["name"], True, WHITE)
            screen.blit(icon_text, (power["x"] - 8, power["y"] - 10))
        
        draw_player()
        draw_particles()
        draw_sparkles()
        draw_confetti()
        draw_ui()
        
        pygame.display.flip()
        clock.tick(60)
    
    # Save high score
    try:
        with open("highscore.json", "r") as f:
            highscore_data = json.load(f)
        if score > highscore_data["highscore"]:
            with open("highscore.json", "w") as f:
                json.dump({"highscore": score}, f)
    except:
        with open("highscore.json", "w") as f:
            json.dump({"highscore": score}, f)
    
    return show_game_over()

def main():
    while True:
        if not show_main_menu():
            break
        
        if not run_game():
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

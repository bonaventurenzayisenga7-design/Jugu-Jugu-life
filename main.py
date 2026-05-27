"""
JUGU JUGU - LIFE: 3D Boy Adventure
A retro 3D-style running game where a boy runs forward in a 3D world!
"""

import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("JUGU JUGU - LIFE: 3D Boy Adventure")
clock = pygame.time.Clock()

# Colors
SKY_BLUE = (135, 206, 235)
GROUND_BROWN = (101, 67, 33)
DARK_GREEN = (34, 139, 34)
PLAYER_SKIN = (255, 206, 158)
PLAYER_SHIRT = (50, 150, 255)
PLAYER_PANTS = (70, 70, 200)
PLAYER_HAIR = (101, 67, 33)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GOLD = (255, 215, 0)

# Game variables
score = 0
energy = 100
distance = 0
game_running = True
show_start_screen = True

# Obstacle class for 3D effect
class Obstacle:
    def __init__(self):
        self.x = random.randint(200, 700)
        self.y = SCREEN_HEIGHT - 100
        self.width = 40
        self.height = 40
        self.speed = 5
        self.color = RED
        self.z_position = random.randint(1, 10)
        
    def move(self):
        self.x -= self.speed
        # 3D effect: bigger when closer
        self.size_multiplier = 1 + (10 - self.z_position) / 10
        
    def draw(self, screen):
        scaled_width = int(self.width * self.size_multiplier)
        scaled_height = int(self.height * self.size_multiplier)
        rect_x = int(self.x - scaled_width/2)
        rect_y = int(self.y - scaled_height)
        
        # 3D shadow effect
        shadow_rect = pygame.Rect(rect_x + 5, rect_y + 5, scaled_width, scaled_height)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect)
        pygame.draw.rect(screen, self.color, (rect_x, rect_y, scaled_width, scaled_height))
        
        # 3D highlight
        pygame.draw.line(screen, (255, 100, 100), (rect_x, rect_y), 
                        (rect_x + scaled_width//3, rect_y), 3)
        
    def get_rect(self):
        scaled_width = int(self.width * self.size_multiplier)
        scaled_height = int(self.height * self.size_multiplier)
        rect_x = int(self.x - scaled_width/2)
        rect_y = int(self.y - scaled_height)
        return pygame.Rect(rect_x, rect_y, scaled_width, scaled_height)

class PowerUp:
    def __init__(self):
        self.x = random.randint(300, 750)
        self.y = SCREEN_HEIGHT - 110
        self.width = 30
        self.height = 30
        self.speed = 4
        self.z_position = random.randint(1, 8)
        
    def move(self):
        self.x -= self.speed
        self.size_multiplier = 1 + (8 - self.z_position) / 8
        
    def draw(self, screen):
        scaled_width = int(self.width * self.size_multiplier)
        scaled_height = int(self.height * self.size_multiplier)
        rect_x = int(self.x - scaled_width/2)
        rect_y = int(self.y - scaled_height)
        
        # Draw star-shaped power-up
        pygame.draw.polygon(screen, GOLD, [
            (rect_x + scaled_width//2, rect_y),
            (rect_x + scaled_width//2 + 10, rect_y + scaled_height//3),
            (rect_x + scaled_width, rect_y + scaled_height//3),
            (rect_x + scaled_width//2 + 15, rect_y + scaled_height//2),
            (rect_x + scaled_width//2 + 10, rect_y + scaled_height),
            (rect_x + scaled_width//2, rect_y + scaled_height - 15),
            (rect_x + scaled_width//2 - 10, rect_y + scaled_height),
            (rect_x + scaled_width//2 - 15, rect_y + scaled_height//2),
            (rect_x, rect_y + scaled_height//3),
            (rect_x + scaled_width//2 - 10, rect_y + scaled_height//3)
        ])
        
    def get_rect(self):
        scaled_width = int(self.width * self.size_multiplier)
        scaled_height = int(self.height * self.size_multiplier)
        rect_x = int(self.x - scaled_width/2)
        rect_y = int(self.y - scaled_height)
        return pygame.Rect(rect_x, rect_y, scaled_width, scaled_height)

def draw_3d_road():
    """Draw a 3D perspective road"""
    # Sky gradient
    for i in range(SCREEN_HEIGHT):
        color_ratio = i / SCREEN_HEIGHT
        sky_color = (int(135 * (1 - color_ratio)), 
                    int(206 * (1 - color_ratio)), 
                    int(235 * (1 - color_ratio)))
        pygame.draw.line(screen, sky_color, (0, i), (SCREEN_WIDTH, i))
    
    # Ground with perspective lines
    horizon = SCREEN_HEIGHT // 2
    ground_rect = pygame.Rect(0, horizon, SCREEN_WIDTH, SCREEN_HEIGHT - horizon)
    pygame.draw.rect(screen, GROUND_BROWN, ground_rect)
    
    # Draw road lines with 3D perspective
    for i in range(0, SCREEN_WIDTH, 50):
        start_width = i
        end_width = i + 50
        start_height = horizon + 100
        end_height = SCREEN_HEIGHT
        
        # Road line color
        pygame.draw.line(screen, (255, 215, 0), 
                        (start_width, start_height), 
                        (end_width, end_height), 3)
    
    # Sidewalk
    sidewalk_rect = pygame.Rect(0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120)
    pygame.draw.rect(screen, (150, 150, 150), sidewalk_rect)
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - 120), (SCREEN_WIDTH, SCREEN_HEIGHT - 120), 3)

def draw_3d_boy(x, y, size=1.0):
    """Draw a 3D-styled boy character"""
    # Body (3D effect with shadow)
    body_rect = pygame.Rect(x - 20, y - 60, 40 * size, 60 * size)
    pygame.draw.ellipse(screen, PLAYER_SHIRT, body_rect)
    
    # Shadow under body
    shadow_rect = pygame.Rect(x - 22, y - 58, 44 * size, 64 * size)
    pygame.draw.ellipse(screen, (30, 30, 30), shadow_rect)
    pygame.draw.ellipse(screen, PLAYER_SHIRT, body_rect)
    
    # Pants
    pants_rect = pygame.Rect(x - 18, y - 30, 36 * size, 30 * size)
    pygame.draw.rect(screen, PLAYER_PANTS, pants_rect)
    
    # Head (3D sphere-like)
    head_rect = pygame.Rect(x - 18, y - 85, 36 * size, 36 * size)
    pygame.draw.circle(screen, PLAYER_SKIN, (x, y - 70), 18 * size)
    
    # Hair
    hair_rect = pygame.Rect(x - 16, y - 88, 32 * size, 15 * size)
    pygame.draw.ellipse(screen, PLAYER_HAIR, hair_rect)
    
    # Eyes
    pygame.draw.circle(screen, WHITE, (x - 8, y - 76), 4 * size)
    pygame.draw.circle(screen, WHITE, (x + 8, y - 76), 4 * size)
    pygame.draw.circle(screen, BLACK, (x - 8, y - 76), 2 * size)
    pygame.draw.circle(screen, BLACK, (x + 8, y - 76), 2 * size)
    
    # Smile
    pygame.draw.arc(screen, BLACK, (x - 12, y - 74, 24 * size, 15 * size), 0, math.pi, 2)
    
    # Arms
    left_arm = pygame.Rect(x - 32, y - 55, 15 * size, 40 * size)
    right_arm = pygame.Rect(x + 17, y - 55, 15 * size, 40 * size)
    pygame.draw.rect(screen, PLAYER_SHIRT, left_arm)
    pygame.draw.rect(screen, PLAYER_SHIRT, right_arm)
    
    # Legs
    left_leg = pygame.Rect(x - 15, y - 25, 12 * size, 35 * size)
    right_leg = pygame.Rect(x + 3, y - 25, 12 * size, 35 * size)
    pygame.draw.rect(screen, PLAYER_PANTS, left_leg)
    pygame.draw.rect(screen, PLAYER_PANTS, right_leg)
    
    # Shoes
    shoe_color = (100, 60, 30)
    pygame.draw.ellipse(screen, shoe_color, (x - 18, y + 8, 15 * size, 8 * size))
    pygame.draw.ellipse(screen, shoe_color, (x + 3, y + 8, 15 * size, 8 * size))

def draw_text(text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def start_screen():
    screen.fill(SKY_BLUE)
    draw_3d_boy(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50, 1.2)
    draw_text("JUGU JUGU - LIFE", 60, SCREEN_WIDTH//2, 100, GOLD)
    draw_text("3D Boy Adventure", 40, SCREEN_WIDTH//2, 170, WHITE)
    draw_text("Press SPACE to start running!", 30, SCREEN_WIDTH//2, 300, WHITE)
    draw_text("Use LEFT/RIGHT arrows to move", 25, SCREEN_WIDTH//2, 360, WHITE)
    draw_text("Collect stars ⭐ for energy!", 25, SCREEN_WIDTH//2, 400, WHITE)
    draw_text("Avoid red obstacles ❌", 25, SCREEN_WIDTH//2, 440, WHITE)
    draw_text("Press ESC to quit", 25, SCREEN_WIDTH//2, 520, WHITE)
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
    return True

# Main game loop
def main_game():
    global game_running, score, energy
    
    # Player position
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - 100
    
    # Game objects
    obstacles = []
    powerups = []
    frame_count = 0
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True  # Back to start screen
        
        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 60:
            player_x -= 7
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 60:
            player_x += 7
        
        # Spawn obstacles
        if frame_count % 45 == 0 and len(obstacles) < 5:
            obstacles.append(Obstacle())
        
        # Spawn power-ups
        if frame_count % 120 == 0 and len(powerups) < 3:
            powerups.append(PowerUp())
        
        # Update obstacles
        for obstacle in obstacles[:]:
            obstacle.move()
            if obstacle.x < -50:
                obstacles.remove(obstacle)
                score += 10  # Dodge successfully!
            elif obstacle.get_rect().colliderect(pygame.Rect(player_x - 20, player_y - 60, 40, 60)):
                energy -= 20
                obstacles.remove(obstacle)
                if energy <= 0:
                    return False
        
        # Update power-ups
        for powerup in powerups[:]:
            powerup.move()
            if powerup.x < -50:
                powerups.remove(powerup)
            elif powerup.get_rect().colliderect(pygame.Rect(player_x - 20, player_y - 60, 40, 60)):
                energy = min(100, energy + 15)
                score += 25
                powerups.remove(powerup)
        
        # Increase distance
        distance += 1
        if distance % 300 == 0:
            score += 50
            energy = min(100, energy + 5)
        
        # Natural energy decrease
        if frame_count % 60 == 0:
            energy = max(0, energy - 1)
            if energy <= 0:
                return False
        
        # Drawing
        draw_3d_road()
        draw_3d_boy(player_x, player_y)
        
        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Draw power-ups
        for powerup in powerups:
            powerup.draw(screen)
        
        # Draw UI
        draw_text(f"Score: {score}", 30, 100, 40, GOLD)
        draw_text(f"Energy: {energy}", 30, 100, 80, WHITE)
        draw_text(f"Distance: {distance}m", 30, 100, 120, WHITE)
        
        # Draw energy bar
        bar_width = 200
        bar_height = 15
        bar_x = SCREEN_WIDTH - bar_width - 20
        bar_y = 20
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * (energy/100), bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        draw_text("ENERGY", 20, bar_x + bar_width//2, bar_y - 10, WHITE)
        
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1
    
    return True

# Game execution
while game_running:
    if show_start_screen:
        result = start_screen()
        if result:
            # Reset game variables
            score = 0
            energy = 100
            distance = 0
            show_start_screen = False
            # Run the game
            game_result = main_game()
            if not game_result:
                # Game over
                screen.fill(BLACK)
                draw_3d_boy(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50, 1.5)
                draw_text("GAME OVER!", 60, SCREEN_WIDTH//2, 150, RED)
                draw_text(f"Final Score: {score}", 40, SCREEN_WIDTH//2, 230, WHITE)
                draw_text(f"Distance: {distance}m", 40, SCREEN_WIDTH//2, 290, WHITE)
                draw_text("Press SPACE to play again", 30, SCREEN_WIDTH//2, 400, WHITE)
                draw_text("Press ESC to quit", 30, SCREEN_WIDTH//2, 460, WHITE)
                pygame.display.flip()
                
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_running = False
                            waiting = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                show_start_screen = True
                                waiting = False
                            if event.key == pygame.K_ESCAPE:
                                game_running = False
                                waiting = False
        else:
            game_running = False
    else:
        show_start_screen = True

pygame.quit()
sys.exit()

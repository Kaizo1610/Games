import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Stickman dimensions
STICKMAN_WIDTH = 50
STICKMAN_HEIGHT = 100

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stickman Game")

# Stickman properties
stickman_x = SCREEN_WIDTH // 2
stickman_y = SCREEN_HEIGHT - STICKMAN_HEIGHT
stickman_speed = 5

# Jump properties
is_jumping = False
jump_velocity = 15
gravity = 1
initial_y = stickman_y

# Obstacle properties
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacles = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Function to create a new obstacle
def create_obstacle():
    x = SCREEN_WIDTH
    y = SCREEN_HEIGHT - obstacle_height
    return pygame.Rect(x, y, obstacle_width, obstacle_height)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        stickman_x -= stickman_speed
    if keys[pygame.K_RIGHT]:
        stickman_x += stickman_speed
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        jump_velocity = -15

    # Update stickman position
    if is_jumping:
        stickman_y += jump_velocity
        jump_velocity += gravity
        if stickman_y >= initial_y:
            stickman_y = initial_y
            is_jumping = False

    # Ensure stickman stays within screen bounds
    stickman_x = max(0, min(stickman_x, SCREEN_WIDTH - STICKMAN_WIDTH))

    # Create new obstacles at random intervals
    if random.randint(1, 100) < 2:
        obstacles.append(create_obstacle())

    # Move obstacles
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed

    # Remove off-screen obstacles and update score
    obstacles = [obstacle for obstacle in obstacles if obstacle.x + obstacle_width > 0]
    score += len([obstacle for obstacle in obstacles if obstacle.x + obstacle_width == SCREEN_WIDTH - obstacle_speed])

    # Check for collisions
    stickman_rect = pygame.Rect(stickman_x, stickman_y, STICKMAN_WIDTH, STICKMAN_HEIGHT)
    for obstacle in obstacles:
        if stickman_rect.colliderect(obstacle):
            running = False  # End the game on collision

    # Clear screen
    screen.fill(WHITE)

    # Draw stickman
    head_radius = 20
    body_length = 60
    arm_length = 30
    leg_length = 40

    # Head
    pygame.draw.circle(screen, BLACK, (stickman_x + STICKMAN_WIDTH // 2, stickman_y - head_radius), head_radius)
    # Body
    pygame.draw.line(screen, BLACK, (stickman_x + STICKMAN_WIDTH // 2, stickman_y), (stickman_x + STICKMAN_WIDTH // 2, stickman_y + body_length), 2)
    # Arms
    pygame.draw.line(screen, BLACK, (stickman_x + STICKMAN_WIDTH // 2, stickman_y + 20), (stickman_x + STICKMAN_WIDTH // 2 - arm_length, stickman_y + 20), 2)
    pygame.draw.line(screen, BLACK, (stickman_x + STICKMAN_WIDTH // 2, stickman_y + 20), (stickman_x + STICKMAN_WIDTH // 2 + arm_length, stickman_y + 20), 2)
    # Legs
    pygame.draw.line(screen, BLACK, (stickman_x + STICKMAN_WIDTH // 2, stickman_y + body_length), (stickman_x + STICKMAN_WIDTH // 2 - leg_length, stickman_y + body_length + leg_length), 2)
    pygame.draw.line(screen, BLACK, (stickman_x + STICKMAN_WIDTH // 2, stickman_y + body_length), (stickman_x + STICKMAN_WIDTH // 2 + leg_length, stickman_y + body_length + leg_length), 2)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Render score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
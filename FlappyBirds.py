import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load images
bird_img = pygame.image.load("flappy_bird.png").convert_alpha()  # Single bird image
bird_img = pygame.transform.scale(bird_img, (30, 30))  # Resize bird image

# Game variables
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.8
jump_strength = -8
score = 0

# Pipe variables
pipe_width = 50
pipe_gap = 100
pipes = [[WIDTH, random.randint(150, 450)]]
pipe_speed = 5

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 30)

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe[0], 0, pipe_width, pipe[1]))  # Top pipe
        pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap))  # Bottom pipe

def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pygame.Rect(pipe[0], 0, pipe_width, pipe[1])) or \
           bird_rect.colliderect(pygame.Rect(pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap)):
            return True
    return False

def game_over_screen():
    screen.fill(WHITE)
    game_over_surface = font.render(f"Game Over! Score: {score}", True, BLACK)
    screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - game_over_surface.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

    # Display continue or quit options
    continue_surface = font.render("Press C to Continue or Q to Quit", True, BLACK)
    screen.blit(continue_surface, (WIDTH // 2 - continue_surface.get_width() // 2, HEIGHT // 2 + game_over_surface.get_height()))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    waiting = False
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
    return False

def reset_game():
    global bird_y, bird_velocity, score, pipes, pipe_speed
    bird_y = HEIGHT // 2
    bird_velocity = 0
    score = 0
    pipes = [[WIDTH, random.randint(150, 450)]]
    pipe_speed = 5

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    # Bird mechanics
    bird_velocity += gravity
    bird_y += bird_velocity

    # Pipe mechanics
    if pipes[-1][0] < WIDTH - 200:
        pipes.append([WIDTH, random.randint(150, 450)])
    for pipe in pipes:
        pipe[0] -= pipe_speed

    # Remove off-screen pipes
    if pipes[0][0] < -pipe_width:
        pipes.pop(0)
        score += 1
        if score % 5 == 0:
            pipe_speed += 1  # Increase difficulty

    # Check for collisions
    bird_rect = pygame.Rect(50, bird_y, 30, 30)
    if bird_y > HEIGHT or bird_y < 0 or check_collision(bird_rect, pipes):
        if not game_over_screen():
            running = False
        else:
            reset_game()

    # Drawing
    screen.fill(WHITE)  # Draw background color
    screen.blit(bird_img, (50, bird_y))
    draw_pipes(pipes)

    # Score
    score_surface = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_surface, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
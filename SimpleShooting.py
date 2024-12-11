import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Shooter Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - player_size]
player_speed = 10

# Bullet settings
bullet_size = 5
bullet_speed = 15
bullets = []

# Enemy settings
enemy_size = 50
enemy_speed = 5
enemies = [[random.randint(0, WIDTH - enemy_size), 0]]

# Score settings
score = 0
font = pygame.font.SysFont("Arial", 30)

# Game over flag
game_over = False

# Function to display the game over message
def display_game_over():
    game_over_font = pygame.font.SysFont("Arial", 60)
    game_over_text = game_over_font.render("Game Over!", True, BLACK)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before closing

# Game loop
def game_loop():
    global score, game_over
    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_SPACE]:
            bullets.append([player_pos[0] + player_size // 2, player_pos[1]])

        # Move bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if random.randint(1, 20) == 1:
            enemies.append([random.randint(0, WIDTH - enemy_size), 0])

        # Move enemies
        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)

        # Check for collisions
        for bullet in bullets:
            for enemy in enemies:
                if (enemy[0] < bullet[0] < enemy[0] + enemy_size) and (enemy[1] < bullet[1] < enemy[1] + enemy_size):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1  # Increase score
                    break

        # Check for player collision with enemies
        for enemy in enemies:
            if (enemy[0] < player_pos[0] < enemy[0] + enemy_size) and (enemy[1] < player_pos[1] < enemy[1] + enemy_size):
                game_over = True
                break

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))

        for bullet in bullets:
            pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_size, bullet_size))

        for enemy in enemies:
            pygame.draw.rect(screen, BLACK, (enemy[0], enemy[1], enemy_size, enemy_size))

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    # Display game over message
    display_game_over()
    pygame.quit()

if __name__ == "__main__":
    game_loop()

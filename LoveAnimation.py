import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Love Animation")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 182, 193)

# Heart shape function
def draw_heart(surface, x, y, size):
    points = [
        (x, y + size // 4),
        (x + size // 2, y),
        (x + size, y + size // 4),
        (x + size, y + size // 2),
        (x + size // 2, y + size),
        (x, y + size // 2),
    ]
    pygame.draw.polygon(surface, RED, points)

# Main animation loop
def love_animation():
    running = True
    clock = pygame.time.Clock()
    hearts = []
    for _ in range(10):  # Generate 10 hearts with random sizes and positions
        size = random.randint(30, 100)
        x = random.randint(0, width - size)
        y = random.randint(0, height - size)
        hearts.append([x, y, size, random.uniform(0.02, 0.05)])  # [x, y, size, speed]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        for heart in hearts:
            x, y, size, speed = heart
            draw_heart(screen, x, y, size)

            # Update the position and size of the heart
            heart[1] -= speed * 10  # Move up
            heart[2] += speed * 5  # Increase size

            # Reset heart if it goes off screen
            if y < -size or size > 150:
                heart[0] = random.randint(0, width - size)
                heart[1] = height + size
                heart[2] = random.randint(30, 100)  # Reset size

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    love_animation()

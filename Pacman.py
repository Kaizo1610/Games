import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60
PACMAN_RADIUS = 20
PACMAN_SPEED = 5
GHOST_SPEED = 3
DOT_RADIUS = 5
NUM_DOTS = 30

# Colors
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman Game")

# Clock object to control FPS
clock = pygame.time.Clock()

# Pacman class
class Pacman:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = PACMAN_RADIUS
        self.speed = PACMAN_SPEED
        self.direction = pygame.K_RIGHT

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = pygame.K_LEFT
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = pygame.K_RIGHT
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = pygame.K_UP
        if keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = pygame.K_DOWN

        # Boundaries
        if self.x < self.radius:
            self.x = self.radius
        if self.x > SCREEN_WIDTH - self.radius:
            self.x = SCREEN_WIDTH - self.radius
        if self.y < self.radius:
            self.y = self.radius
        if self.y > SCREEN_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - self.radius

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)
        # Drawing Pacman's mouth
        mouth_start = (self.x, self.y)
        if self.direction == pygame.K_RIGHT:
            mouth_end = (self.x + self.radius, self.y)
        elif self.direction == pygame.K_LEFT:
            mouth_end = (self.x - self.radius, self.y)
        elif self.direction == pygame.K_UP:
            mouth_end = (self.x, self.y - self.radius)
        elif self.direction == pygame.K_DOWN:
            mouth_end = (self.x, self.y + self.radius)
        pygame.draw.polygon(screen, BLACK, [mouth_start, mouth_end, (self.x, self.y)])

# Ghost class
class Ghost:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed = GHOST_SPEED

    def move(self):
        self.x += random.choice([-self.speed, self.speed])
        self.y += random.choice([-self.speed, self.speed])

        # Boundaries
        if self.x < PACMAN_RADIUS:
            self.x = PACMAN_RADIUS
        if self.x > SCREEN_WIDTH - PACMAN_RADIUS:
            self.x = SCREEN_WIDTH - PACMAN_RADIUS
        if self.y < PACMAN_RADIUS:
            self.y = PACMAN_RADIUS
        if self.y > SCREEN_HEIGHT - PACMAN_RADIUS:
            self.y = SCREEN_HEIGHT - PACMAN_RADIUS

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), PACMAN_RADIUS)

# Dots
def create_dots():
    dots = []
    for _ in range(NUM_DOTS):
        dot_x = random.randint(DOT_RADIUS, SCREEN_WIDTH - DOT_RADIUS)
        dot_y = random.randint(DOT_RADIUS, SCREEN_HEIGHT - DOT_RADIUS)
        dots.append((dot_x, dot_y))
    return dots

def draw_dots(dots):
    for dot in dots:
        pygame.draw.circle(screen, WHITE, dot, DOT_RADIUS)

# Main game loop
def main():
    pacman = Pacman()
    ghost = Ghost()
    dots = create_dots()
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pacman.move()
        ghost.move()

        # Check collision with ghost
        if abs(pacman.x - ghost.x) < PACMAN_RADIUS and abs(pacman.y - ghost.y) < PACMAN_RADIUS:
            print("Game Over!")
            running = False

        # Check collision with dots
        dots = [dot for dot in dots if not (abs(pacman.x - dot[0]) < PACMAN_RADIUS and abs(pacman.y - dot[1]) < PACMAN_RADIUS)]
        score = NUM_DOTS - len(dots)

        screen.fill(BLACK)
        pacman.draw()
        ghost.draw()
        draw_dots(dots)

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()

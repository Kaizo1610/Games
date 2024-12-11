import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        mario_image = pygame.image.load("Mario.png").convert_alpha()  # Load the Mario image
        self.image = pygame.transform.scale(mario_image, (50, 50))  # Scale the image to 50x50 pixels
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 70
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False

    def update(self):
        # Apply gravity
        self.change_y += GRAVITY
        self.rect.y += self.change_y
        
        # Check for collisions with the ground
        if self.rect.y >= SCREEN_HEIGHT - 50:
            self.rect.y = SCREEN_HEIGHT - 50
            self.change_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        self.rect.x += self.change_x

        # Screen boundaries
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

    def jump(self):
        if self.on_ground:
            self.change_y = -JUMP_STRENGTH

# Monster class
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        monster_image = pygame.image.load("Monster.png").convert_alpha()  # Load the Monster image
        self.image = pygame.transform.scale(monster_image, (50, 50))  # Scale the image to 50x50 pixels
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create player, monster, and obstacles
player = Player()
monster = Monster(400, SCREEN_HEIGHT - 70)
obstacle1 = Obstacle(300, SCREEN_HEIGHT - 100, 50, 50)
obstacle2 = Obstacle(600, SCREEN_HEIGHT - 150, 50, 100)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(monster)
all_sprites.add(obstacle1)
all_sprites.add(obstacle2)

# Main game loop
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.change_x = -5
                if event.key == pygame.K_d:
                    player.change_x = 5
                if event.key == pygame.K_SPACE:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.change_x = 0
                if event.key == pygame.K_d and player.change_x > 0:
                    player.change_x = 0

        # Update sprites
        all_sprites.update()

        # Draw everything
        screen.fill(WHITE)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
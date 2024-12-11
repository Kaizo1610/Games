import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock-Paper-Scissors Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load fonts
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)

# Function to get computer's choice
def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

# Function to determine the winner
def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "It's a tie!"
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'paper' and computer_choice == 'rock') or \
         (player_choice == 'scissors' and computer_choice == 'paper'):
        return "You win!"
    else:
        return "You lose!"

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Main function to run the game
def main():
    player_choice = ""
    computer_choice = ""
    result = ""

    # Create buttons for rock, paper, scissors
    buttons = [
        Button("Rock", 50, 300, 100, 50, GREEN),
        Button("Paper", 250, 300, 100, 50, GREEN),
        Button("Scissors", 450, 300, 100, 50, GREEN)
    ]

    # Game loop
    while True:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        player_choice = button.text.lower()
                        computer_choice = get_computer_choice()
                        result = determine_winner(player_choice, computer_choice)

        # Draw buttons
        for button in buttons:
            button.draw(screen)

        # Display choices and result
        if player_choice and computer_choice:
            player_text = big_font.render(f"You chose: {player_choice}", True, BLACK)
            computer_text = big_font.render(f"Computer chose: {computer_choice}", True, BLACK)
            result_text = big_font.render(result, True, BLACK)

            screen.blit(player_text, (50, 50))
            screen.blit(computer_text, (50, 150))
            screen.blit(result_text, (50, 250))

        pygame.display.flip()

if __name__ == "__main__":
    main()

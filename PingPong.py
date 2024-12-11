import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Paddle settings
paddle_width = 10
paddle_height = 100
paddle_speed = 5

# Ball settings
ball_radius = 10
ball_speed_x = 3 * random.choice([1, -1])
ball_speed_y = 3 * random.choice([1, -1])

# Paddle positions
player_x = 50
player_y = screen_height // 2 - paddle_height // 2

opponent_x = screen_width - 50 - paddle_width
opponent_y = screen_height // 2 - paddle_height // 2

# Ball position
ball_x = screen_width // 2
ball_y = screen_height // 2

# Scores
player_score = 0
opponent_score = 0

# Font
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Game duration (2 minutes)
game_duration = 120  # seconds

# Power-up settings
power_ups = []
power_up_spawn_time = 5  # seconds
last_power_up_spawn = time.time()

# Function to display the countdown timer
def display_timer(time_left):
    timer_text = small_font.render(f"Time: {time_left} s", True, white)
    screen.blit(timer_text, (screen_width // 2 - 50, 20))

# Function to display winner and play again option
def display_winner():
    screen.fill(black)
    if player_score > opponent_score:
        winner_text = font.render("Player Wins!", True, white)
    elif opponent_score > player_score:
        winner_text = font.render("Opponent Wins!", True, white)
    else:
        winner_text = font.render("It's a Draw!", True, white)
    
    screen.blit(winner_text, (screen_width // 4, screen_height // 3))
    
    option_text = small_font.render("Press R to Play Again or Q to Quit", True, white)
    screen.blit(option_text, (screen_width // 4 - 50, screen_height // 2))
    pygame.display.flip()

# Function to reset the game state
def reset_game():
    global player_score, opponent_score, ball_x, ball_y, ball_speed_x, ball_speed_y, player_y, opponent_y, power_ups
    player_score = 0
    opponent_score = 0
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_speed_x = 3 * random.choice([1, -1])
    ball_speed_y = 3 * random.choice([1, -1])
    player_y = screen_height // 2 - paddle_height // 2
    opponent_y = screen_height // 2 - paddle_height // 2
    power_ups = []

# Function to spawn power-ups
def spawn_power_up():
    power_up_type = random.choice(['increase_speed', 'decrease_speed', 'increase_paddle'])
    power_up_x = random.randint(100, screen_width - 100)
    power_up_y = random.randint(100, screen_height - 100)
    power_ups.append({'type': power_up_type, 'x': power_up_x, 'y': power_up_y})

# Function to apply power-up effects
def apply_power_up(power_up):
    global ball_speed_x, ball_speed_y, paddle_height
    if power_up['type'] == 'increase_speed':
        ball_speed_x *= 1.5
        ball_speed_y *= 1.5
    elif power_up['type'] == 'decrease_speed':
        ball_speed_x *= 0.75
        ball_speed_y *= 0.75
    elif power_up['type'] == 'increase_paddle':
        paddle_height += 20

# Main game loop
while True:
    # Reset the game at the start of each round
    reset_game()
    
    # Track start time
    start_time = time.time()

    running = True
    while running:
        screen.fill(black)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_y > 0:
            player_y -= paddle_speed
        if keys[pygame.K_s] and player_y < screen_height - paddle_height:
            player_y += paddle_speed

        # Opponent movement (simple AI)
        if opponent_y + paddle_height // 2 < ball_y:
            opponent_y += paddle_speed
        if opponent_y + paddle_height // 2 > ball_y:
            opponent_y -= paddle_speed

        # Ball movement
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Collision with top/bottom walls
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= screen_height:
            ball_speed_y *= -1

        # Collision with paddles
        if (player_x < ball_x - ball_radius < player_x + paddle_width and
                player_y < ball_y < player_y + paddle_height):
            ball_speed_x *= -1
        if (opponent_x < ball_x + ball_radius < opponent_x + paddle_width and
                opponent_y < ball_y < opponent_y + paddle_height):
            ball_speed_x *= -1

        # Ball out of bounds
        if ball_x < 0:
            opponent_score += 1
            ball_x, ball_y = screen_width // 2, screen_height // 2
            ball_speed_x *= random.choice([1, -1])
            ball_speed_y *= random.choice([1, -1])
        if ball_x > screen_width:
            player_score += 1
            ball_x, ball_y = screen_width // 2, screen_height // 2
            ball_speed_x *= random.choice([1, -1])
            ball_speed_y *= random.choice([1, -1])

        # Spawn power-ups
        current_time = time.time()
        if current_time - last_power_up_spawn > power_up_spawn_time:
            spawn_power_up()
            last_power_up_spawn = current_time

        # Check for power-up collisions
        for power_up in power_ups:
            if abs(ball_x - power_up['x']) < ball_radius and abs(ball_y - power_up['y']) < ball_radius:
                apply_power_up(power_up)
                power_ups.remove(power_up)

        # Draw paddles and ball
        pygame.draw.rect(screen, blue, (player_x, player_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, red, (opponent_x, opponent_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)

        # Draw power-ups
        for power_up in power_ups:
            if power_up['type'] == 'increase_speed':
                color = green
            elif power_up['type'] == 'decrease_speed':
                color = red
            elif power_up['type'] == 'increase_paddle':
                color = blue
            pygame.draw.circle(screen, color, (power_up['x'], power_up['y']), 15)

        # Draw scores
        player_text = font.render(str(player_score), True, white)
        screen.blit(player_text, (screen_width // 4, 20))

        opponent_text = font.render(str(opponent_score), True, white)
        screen.blit(opponent_text, (screen_width // 4 * 3, 20))

        # Calculate remaining time and display timer
        elapsed_time = time.time() - start_time
        time_left = max(0, int(game_duration - elapsed_time))
        display_timer(time_left)

        # Update the screen
        pygame.display.flip()

        # Frame rate
        pygame.time.Clock().tick(60)

        # End game after 2 minutes
        if elapsed_time >= game_duration:
            running = False

    # Display winner and prompt to play again or quit
    display_winner()

    # Wait for the player to choose to play again or quit
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                pygame.quit()
                exit()

            # Play again if 'R' is pressed, quit if 'Q' is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting_for_input = False
                elif event.key == pygame.K_q:
                    waiting_for_input = False
                    pygame.quit()
                    exit()
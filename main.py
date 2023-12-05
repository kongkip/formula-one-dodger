import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 100
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
INITIAL_SPEED = 5

# Setting up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Formula One Dodger")

# Player Car
player_car = pygame.Rect(SCREEN_WIDTH // 2 - CAR_WIDTH // 2, SCREEN_HEIGHT - CAR_HEIGHT - 10, CAR_WIDTH, CAR_HEIGHT)

# Obstacle Car
def create_obstacle():
    return pygame.Rect(random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH), -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

# Human Decision Making
def human_move():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_car.left > 0:
        player_car.x -= 5
    elif keys[pygame.K_RIGHT] and player_car.right < SCREEN_WIDTH:
        player_car.x += 5


# Game Variables
speed = INITIAL_SPEED
score = 0
obstacles = [create_obstacle()]

# Create a font object
font = pygame.font.SysFont(None, 36)  # You can choose a different font and size

# Function to display score and speed
def display_score_speed(score, speed):
    score_text = font.render(f'Score: {score}', True, BLACK)
    speed_text = font.render(f'Speed: {speed}', True, BLACK)
    screen.blit(score_text, (10, 10))  # Top-left corner
    screen.blit(speed_text, (10, 50))  # Below the score

# Main game loop
def game_loop(is_human=True):

    global speed, score, obstacles
    
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        human_move()

        # Update obstacles
        for obstacle in obstacles:
            obstacle.y += speed
            if obstacle.top > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
                obstacles.append(create_obstacle())
                score += 10
                speed += 1

        # Check for collisions
        for obstacle in obstacles:
            if player_car.colliderect(obstacle):
                print(f"Game Over! Your score: {score}")
                running = False

        # Drawing
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, player_car)
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, obstacle)

        # Display score and speed
        display_score_speed(score, speed)  # Added this line

        # Update the display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
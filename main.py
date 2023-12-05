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
GREY = (169, 169, 169)  # Color for the road
LANE_COLOR = (255, 255, 255)  # Color for lane markings
INITIAL_SPEED = 5
LANE_WIDTH = SCREEN_WIDTH // 3

# Setting up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Formula One Dodger")

# Create background with lanes
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(GREY)

# Draw lane markings
lane_marking_width = 5  # Width of the lane markings
pygame.draw.line(background, LANE_COLOR, (LANE_WIDTH, 0), (LANE_WIDTH, SCREEN_HEIGHT), lane_marking_width)
pygame.draw.line(background, LANE_COLOR, (2 * LANE_WIDTH, 0), (2 * LANE_WIDTH, SCREEN_HEIGHT), lane_marking_width)

# Calculate lane centers
left_lane_center = LANE_WIDTH // 2
right_lane_center = LANE_WIDTH + LANE_WIDTH // 2

# Player Car
player_car = pygame.Rect(left_lane_center - CAR_WIDTH // 2, SCREEN_HEIGHT - CAR_HEIGHT - 10, CAR_WIDTH, CAR_HEIGHT)
current_lane = "left"

# Obstacle Car
def create_obstacle():
    lane_choice = random.choice(["left", "right"])
    if lane_choice == "left":
        x_pos = left_lane_center - OBSTACLE_WIDTH // 2
    else:
        x_pos = right_lane_center - OBSTACLE_WIDTH // 2

    return pygame.Rect(x_pos, -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

# Human Decision Making
def human_move():
    global current_lane
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and current_lane != "left":
        player_car.x = left_lane_center - CAR_WIDTH // 2
        current_lane = "left"
    elif keys[pygame.K_RIGHT] and current_lane != "right":
        player_car.x = right_lane_center - CAR_WIDTH // 2
        current_lane = "right"

# Game Variables
speed = INITIAL_SPEED
score = 0
obstacles = [create_obstacle()]

# Create a font object
font = pygame.font.SysFont(None, 36)

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
        screen.blit(background, (0, 0))  # Draw the background each frame
        pygame.draw.rect(screen, RED, player_car)
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, obstacle)

        # Display score and speed
        display_score_speed(score, speed)

        # Update the display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()

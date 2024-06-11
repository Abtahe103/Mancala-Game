import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mancala')

# Board dimensions
BOARD_WIDTH = 600
BOARD_HEIGHT = 200
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2

# Pit dimensions
PIT_RADIUS = 30
PIT_GAP = 20

# Mancala dimensions
MANCALA_WIDTH = 60
MANCALA_HEIGHT = 180

def draw_board():
    screen.fill(WHITE)
    
    # Draw the Mancala board background
    pygame.draw.rect(screen, BROWN, (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT))
    
    # Draw the left mancala
    pygame.draw.rect(screen, DARK_BROWN, (BOARD_X + PIT_RADIUS - MANCALA_WIDTH, BOARD_Y + (BOARD_HEIGHT - MANCALA_HEIGHT) // 2, MANCALA_WIDTH, MANCALA_HEIGHT))
    
    # Draw the right mancala
    pygame.draw.rect(screen, DARK_BROWN, (BOARD_X + BOARD_WIDTH - PIT_RADIUS, BOARD_Y + (BOARD_HEIGHT - MANCALA_HEIGHT) // 2, MANCALA_WIDTH, MANCALA_HEIGHT))
    
    # Draw the pits on the left side
    for i in range(6):
        pit_x = BOARD_X + (PIT_RADIUS * 2 + PIT_GAP) * i + MANCALA_WIDTH + PIT_RADIUS
        pit_y = BOARD_Y + PIT_RADIUS + PIT_GAP
        pygame.draw.circle(screen, DARK_BROWN, (pit_x, pit_y), PIT_RADIUS)
    
    # Draw the pits on the right side
    for i in range(6):
        pit_x = BOARD_X + (PIT_RADIUS * 2 + PIT_GAP) * i + MANCALA_WIDTH + PIT_RADIUS
        pit_y = BOARD_Y + BOARD_HEIGHT - PIT_RADIUS - PIT_GAP
        pygame.draw.circle(screen, DARK_BROWN, (pit_x, pit_y), PIT_RADIUS)

def main():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        draw_board()
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()

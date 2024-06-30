import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
HIGHLIGHT_COLOR = (255, 0, 0)
BLACK = (0, 0, 0)

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

# Font for displaying stones and messages
font = pygame.font.SysFont(None, 36)
message_font = pygame.font.SysFont(None, 48)

def draw_board(mancala, highlight_pit=None, message=""):
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
        color = HIGHLIGHT_COLOR if highlight_pit == (12 - i) else DARK_BROWN
        pygame.draw.circle(screen, color, (pit_x, pit_y), PIT_RADIUS)
        stones_text = font.render(str(mancala[12 - i]), True, WHITE)
        screen.blit(stones_text, (pit_x - 10, pit_y - 10))
    
    # Draw the pits on the right side
    for i in range(6):
        pit_x = BOARD_X + (PIT_RADIUS * 2 + PIT_GAP) * i + MANCALA_WIDTH + PIT_RADIUS
        pit_y = BOARD_Y + BOARD_HEIGHT - PIT_RADIUS - PIT_GAP
        color = HIGHLIGHT_COLOR if highlight_pit == i else DARK_BROWN
        pygame.draw.circle(screen, color, (pit_x, pit_y), PIT_RADIUS)
        stones_text = font.render(str(mancala[i]), True, WHITE)
        screen.blit(stones_text, (pit_x - 10, pit_y - 10))
    
    # Draw stones in mancalas
    left_mancala_text = font.render(str(mancala[13]), True, WHITE)
    screen.blit(left_mancala_text, (BOARD_X + PIT_RADIUS - MANCALA_WIDTH + 10, BOARD_Y + (BOARD_HEIGHT - MANCALA_HEIGHT) // 2 + 70))
    
    right_mancala_text = font.render(str(mancala[6]), True, WHITE)
    screen.blit(right_mancala_text, (BOARD_X + BOARD_WIDTH - PIT_RADIUS + 10, BOARD_Y + (BOARD_HEIGHT - MANCALA_HEIGHT) // 2 + 70))

    # Draw message
    if message:
        message_text = message_font.render(message, True, BLACK)
        screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT - 100))

def animate_move(mancala, index):
    draw_board(mancala, highlight_pit=index)
    pygame.display.flip()
    time.sleep(0.5)  

class Mancala_Board:
    def __init__(self, mancala):
        if mancala is not None:
            self.mancala = mancala[:]
        else:
            self.mancala = [4] * 6 + [0] + [4] * 6 + [0]

    def player_move(self, i):
        j = i
        repeat_turn = False
        add = self.mancala[j]
        self.mancala[j] = 0
        if i > 6:
            stones = add
            while stones > 0:
                i += 1             
                i = i % 14
                if i == 6:
                    continue
                else:
                    self.mancala[i % 14] += 1
                stones -= 1
            if i > 6 and self.mancala[i] == 1 and i != 13 and self.mancala[-i + 12] != 0:
                self.mancala[13] += 1 + self.mancala[-i + 12]
                self.mancala[i] = 0
                self.mancala[-i + 12] = 0
            if i == 13:
                repeat_turn = True
                
        else:
            stones = add
            while stones > 0:
                i += 1
                i = i % 14
                if i == 13:
                    continue
                else:
                    self.mancala[i % 14] += 1
                stones -= 1
            if i < 6 and self.mancala[i] == 1 and i != 6 and self.mancala[-i + 12] != 0:
                self.mancala[6] += 1 + self.mancala[-i + 12]
                self.mancala[i] = 0
                self.mancala[-i + 12] = 0
            if i == 6:
                repeat_turn = True
        return repeat_turn

    def isEnd(self):
        if sum(self.mancala[0:6]) == 0:
            self.mancala[13] += sum(self.mancala[7:13])
            for i in range(14):
                if i != 13 and i != 6:
                    self.mancala[i] = 0
            return True
        elif sum(self.mancala[7:13]) == 0:
            self.mancala[6] += sum(self.mancala[0:6])
            for i in range(14):
                if i != 13 and i != 6:
                    self.mancala[i] = 0
            return True
        return False

    def print_mancala(self):
        for i in range(12, 6, -1):
            print('  ', self.mancala[i], '   ', end='')
        print('  ')
        print(self.mancala[13], '                                           ', self.mancala[6])
        for i in range(0, 6, 1):
            print('  ', self.mancala[i], '   ', end='')
        print('  ')

    def husVal(self):
        if self.isEnd():
            if self.mancala[13] > self.mancala[6]:
                return 100
            elif self.mancala[13] == self.mancala[6]:
                return 0
            else:
                return -100
        else:
            return self.mancala[13] - self.mancala[6]

def alphabeta(mancala, depth, alpha, beta, MinorMax):
    if depth == 0 or mancala.isEnd():
        return mancala.husVal(), -1
    if MinorMax:
        v = -1000000
        player_move = -1
        for i in range(7, 13, 1):
            if mancala.mancala[i] == 0: continue
            a = Mancala_Board(mancala.mancala[:])
            minormax = a.player_move(i)
            newv, _ = alphabeta(a, depth - 1, alpha, beta, minormax)
            if v < newv:
                player_move = i
                v = newv
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, player_move
    else:
        v = 1000000
        player_move = -1
        for i in range(0, 6, 1):
            if mancala.mancala[i] == 0: continue
            a = Mancala_Board(mancala.mancala[:])
            minormax = a.player_move(i)
            newv, _ = alphabeta(a, depth - 1, alpha, beta, not minormax)
            if v > newv:
                player_move = i
                v = newv
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v, player_move

def player_aibot():
    mancala_board = Mancala_Board(None)
    clock = pygame.time.Clock()
    running = True
    player_turn = True
    selected_pit = -1
    
    draw_board(mancala_board.mancala)
    pygame.display.flip()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                x, y = event.pos
                for i in range(6):
                    pit_x = BOARD_X + (PIT_RADIUS * 2 + PIT_GAP) * i + MANCALA_WIDTH + PIT_RADIUS
                    pit_y = BOARD_Y + BOARD_HEIGHT - PIT_RADIUS - PIT_GAP
                    if (x - pit_x) ** 2 + (y - pit_y) ** 2 <= PIT_RADIUS ** 2:
                        if mancala_board.mancala[i] > 0:
                            selected_pit = i
                            break
        
        if selected_pit != -1 and player_turn:
            repeat_turn = mancala_board.player_move(selected_pit)
            animate_move(mancala_board.mancala, selected_pit)
            draw_board(mancala_board.mancala)  # Draw the updated board state
            pygame.display.flip()  # Update the display
            time.sleep(0.5)  # Adjust animation speed as needed
            
            # Check if the player gets another turn
            player_turn = repeat_turn
            
            # Reset selected pit
            selected_pit = -1
        
        if not player_turn and not mancala_board.isEnd():
            _, ai_move = alphabeta(mancala_board, 5, -100000, 100000, True)  # Calculate AI's move
            repeat_turn = mancala_board.player_move(ai_move)
            animate_move(mancala_board.mancala, ai_move)  # Animate the AI's move
            draw_board(mancala_board.mancala)  # Draw the updated board state
            pygame.display.flip()  # Update the display
            time.sleep(0.5)  # Adjust animation speed as needed
            
            # Check if the AI gets another turn
            player_turn = not repeat_turn
        
        if mancala_board.isEnd():
            winner_message = "AI-BOT WINS" if mancala_board.mancala[13] > mancala_board.mancala[6] else "YOU WIN"
            draw_board(mancala_board.mancala, message=winner_message)
            pygame.display.flip()
            time.sleep(3)
            running = False
        
        clock.tick(60)


print("\n:::: MANCALA BOARD GAME ::::")
print("!!! Welcome to Mancala Gameplay !!!")
while True:
    print("\nPlay the game")
    player_aibot()
    break
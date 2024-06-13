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
    def __init__(self, mancala=None):
        if mancala is not None:
            self.mancala = mancala[:]
        else:
            self.mancala = [4 for _ in range(14)]
            self.mancala[6] = 0
            self.mancala[13] = 0

    def player_move(self, i):
        j = i
        repeat_turn = False
        add = self.mancala[j]
        self.mancala[j] = 0
        stones = add
        while stones > 0:
            i += 1
            if i > 13:
                i = 0
            if (j <= 5 and i == 13) or (j >= 7 and i == 6):
                continue
            self.mancala[i] += 1
            animate_move(self.mancala, i)
            stones -= 1
        
        # Capture stones if last stone lands in an empty pit on the player's side
        if (j <= 5 and 0 <= i <= 5 and self.mancala[i] == 1) or (j >= 7 and 7 <= i <= 12 and self.mancala[i] == 1):
            opposite_pit = 12 - i
            if self.mancala[opposite_pit] > 0:
                if j <= 5:  # Player 1
                    self.mancala[6] += 1 + self.mancala[opposite_pit]
                else:  # Player 2
                    self.mancala[13] += 1 + self.mancala[opposite_pit]
                self.mancala[i] = 0
                self.mancala[opposite_pit] = 0

        # Check if last stone lands in the player's Store
        if (j <= 5 and i == 6) or (j >= 7 and i == 13):
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
        for i in range(7, 13):
            if mancala.mancala[i] == 0:
                continue
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
        for i in range(0, 6):
            if mancala.mancala[i] == 0:
                continue
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

def get_pit_index(x, y):
    # Check pits on the left side (12 to 7)
    for i in range(6):
        pit_x = BOARD_X + (PIT_RADIUS * 2 + PIT_GAP) * i + MANCALA_WIDTH + PIT_RADIUS
        pit_y = BOARD_Y + PIT_RADIUS + PIT_GAP
        if (x - pit_x) ** 2 + (y - pit_y) ** 2 <= PIT_RADIUS ** 2:
            return 12 - i

    # Check pits on the right side (0 to 5)
    for i in range(6):
        pit_x = BOARD_X + (PIT_RADIUS * 2 + PIT_GAP) * i + MANCALA_WIDTH + PIT_RADIUS
        pit_y = BOARD_Y + BOARD_HEIGHT - PIT_RADIUS - PIT_GAP
        if (x - pit_x) ** 2 + (y - pit_y) ** 2 <= PIT_RADIUS ** 2:
            return i

    return None

def player_player():
    j = Mancala_Board(None)
    player_turn = random.choice([1, 2])  # Randomly choose starting player
    draw_board(j.mancala, message=f"Player {player_turn}'s turn")
    pygame.display.flip()

    while True:
        if j.isEnd():
            break
        valid_move = False
        while not valid_move:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    pit_index = get_pit_index(x, y)
                    if pit_index is not None:
                        if (player_turn == 1 and 7 <= pit_index <= 12) or (player_turn == 2 and 0 <= pit_index <= 5):
                            if j.mancala[pit_index] != 0:
                                valid_move = True
                                t = j.player_move(pit_index)
                                draw_board(j.mancala, message=f"Player {player_turn}'s turn")
                                pygame.display.flip()
                                if not t:  # If not repeat turn
                                    player_turn = 2 if player_turn == 1 else 1  # Switch player turn

    # Determine the winner
    if j.mancala[6] > j.mancala[13]:
        winner = "Player 1"
    elif j.mancala[6] < j.mancala[13]:
        winner = "Player 2"
    else:
        winner = "It's a tie"

    draw_board(j.mancala, message=f"Game over! {winner} wins!")
    pygame.display.flip()

print("\n:::: MANCALA BOARD GAME ::::")
print("!!! Welcome to Mancala Gameplay !!!")
while True:
    print("\nPlay the game")
    player_player()
    input("Press Enter to play again or close the window to exit...")

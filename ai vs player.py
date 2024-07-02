import pygame
import sys
import time
import random
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
HIGHLIGHT_COLOR = (255, 0, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (169, 169, 169)
DARK_BLUE=(55, 52, 235)
YELLOW = (235, 143, 52)
RETRO_BLUE = (66, 134, 244)
RETRO_YELLOW = (255, 207, 64)
RETRO_PINK = (244, 66, 182)

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
splash_font = pygame.font.Font("PressStart2P-Regular.ttf", 50)  # Use the retro pixelated font
turn_font = pygame.font.SysFont(None, 48)

# Fuzzy logic system setup
stones_diff = ctrl.Antecedent(np.arange(-48, 49, 1), 'stones_diff')
extra_turns = ctrl.Antecedent(np.arange(0, 2, 1), 'extra_turns')
capturing_opportunities = ctrl.Antecedent(np.arange(0, 2, 1), 'capturing_opportunities')
winning_prob = ctrl.Consequent(np.arange(0, 101, 1), 'winning_prob')

stones_diff['negative'] = fuzz.trimf(stones_diff.universe, [-48, -48, 0])
stones_diff['zero'] = fuzz.trimf(stones_diff.universe, [-10, 0, 10])
stones_diff['positive'] = fuzz.trimf(stones_diff.universe, [0, 48, 48])

extra_turns['no'] = fuzz.trimf(extra_turns.universe, [0, 0, 1])
extra_turns['yes'] = fuzz.trimf(extra_turns.universe, [0, 1, 1])

capturing_opportunities['no'] = fuzz.trimf(capturing_opportunities.universe, [0, 0, 1])
capturing_opportunities['yes'] = fuzz.trimf(capturing_opportunities.universe, [0, 1, 1])

winning_prob['low'] = fuzz.trimf(winning_prob.universe, [0, 0, 50])
winning_prob['medium'] = fuzz.trimf(winning_prob.universe, [25, 50, 75])
winning_prob['high'] = fuzz.trimf(winning_prob.universe, [50, 100, 100])

rule1 = ctrl.Rule(stones_diff['negative'] & extra_turns['no'] & capturing_opportunities['no'], winning_prob['low'])
rule2 = ctrl.Rule(stones_diff['negative'] & extra_turns['yes'] & capturing_opportunities['no'], winning_prob['medium'])
rule3 = ctrl.Rule(stones_diff['negative'] & capturing_opportunities['yes'], winning_prob['medium'])
rule4 = ctrl.Rule(stones_diff['zero'], winning_prob['medium'])
rule5 = ctrl.Rule(stones_diff['positive'] & extra_turns['no'] & capturing_opportunities['no'], winning_prob['medium'])
rule6 = ctrl.Rule(stones_diff['positive'] & extra_turns['yes'] & capturing_opportunities['no'], winning_prob['high'])
rule7 = ctrl.Rule(stones_diff['positive'] & capturing_opportunities['yes'], winning_prob['high'])

winning_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
winning_sim = ctrl.ControlSystemSimulation(winning_ctrl)

def calculate_winning_probability(mancala):
    stones_difference = mancala[6] - mancala[13]
    extra_turn = 1 if mancala[6] == 1 else 0
    capturing_opportunity = 1 if any(mancala[i] == 1 and mancala[-i + 12] != 0 for i in range(6)) else 0
    
    winning_sim.input['stones_diff'] = stones_difference
    winning_sim.input['extra_turns'] = extra_turn
    winning_sim.input['capturing_opportunities'] = capturing_opportunity
    winning_sim.compute()
    
    return winning_sim.output['winning_prob']

def draw_board(mancala, highlight_pit=None, message="", probability=0, turn_message=""):
    screen.fill(WHITE)
    
    # Draw the Mancala board background
    pygame.draw.rect(screen, DARK_BLUE, (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT))
    
    # Draw the left mancala
    pygame.draw.rect(screen, YELLOW, (BOARD_X + PIT_RADIUS - MANCALA_WIDTH, BOARD_Y + (BOARD_HEIGHT - MANCALA_HEIGHT) // 2, MANCALA_WIDTH, MANCALA_HEIGHT))
    
    # Draw the right mancala
    pygame.draw.rect(screen, YELLOW, (BOARD_X + BOARD_WIDTH - PIT_RADIUS, BOARD_Y + (BOARD_HEIGHT - MANCALA_HEIGHT) // 2, MANCALA_WIDTH, MANCALA_HEIGHT))
    
    # Draw the pits on the left side
    for i in range(6):
        pit_x = BOARD_X + (PIT_RADIUS * 2 + PIT_GAP) * i + MANCALA_WIDTH + PIT_RADIUS
        pit_y = BOARD_Y + PIT_RADIUS + PIT_GAP
        color = HIGHLIGHT_COLOR if highlight_pit == (12 - i) else YELLOW
        pygame.draw.circle(screen, color, (pit_x, pit_y), PIT_RADIUS)
        stones_text = font.render(str(mancala[12 - i]), True, WHITE)
        screen.blit(stones_text, (pit_x - 10, pit_y - 10))
    
    # Draw the pits on the right side
    for i in range(6):
        pit_x = BOARD_X + (PIT_RADIUS * 2 + PIT_GAP) * i + MANCALA_WIDTH + PIT_RADIUS
        pit_y = BOARD_Y + BOARD_HEIGHT - PIT_RADIUS - PIT_GAP
        color = HIGHLIGHT_COLOR if highlight_pit == i else YELLOW
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
    
    # Draw winning probability
    probability_text = font.render(f'Your Winning Probability: {probability:.2f}%', True, BLACK)
    screen.blit(probability_text, (10, 10))

    # Draw turn message
    if turn_message:
        turn_text = turn_font.render(turn_message, True, BLACK)
        screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, SCREEN_HEIGHT - 50))



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
    suggested_move = None
    
    draw_board(mancala_board.mancala, probability=calculate_winning_probability(mancala_board.mancala), turn_message="Your Turn")
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
        
        if player_turn and suggested_move is None:
            suggested_move = genetic_algorithm(mancala_board)
        
        if player_turn:
            suggestion_font = pygame.font.SysFont('Arial', 28)  # Use Arial font for better clarity
            suggestion_text = suggestion_font.render(f"Suggested move: Pit {suggested_move + 1}", True, BLACK)
            
            # Clear the area where the suggestion will be displayed
            pygame.draw.rect(screen, WHITE, (10, 50, 300, 40))
            
            # Display the suggestion text
            screen.blit(suggestion_text, (10, 55))
            pygame.display.flip()
        
        if selected_pit != -1 and player_turn:
            repeat_turn = mancala_board.player_move(selected_pit)
            animate_move(mancala_board.mancala, selected_pit)
            draw_board(mancala_board.mancala, probability=calculate_winning_probability(mancala_board.mancala), turn_message="Your Turn" if repeat_turn else "AI's Turn")
            pygame.display.flip()
            time.sleep(0.5)
            
            player_turn = repeat_turn
            selected_pit = -1
            suggested_move = None  # Reset suggested move for next turn
        
        if not player_turn and not mancala_board.isEnd():
            _, ai_move = alphabeta(mancala_board, 5, -100000, 100000, True)
            repeat_turn = mancala_board.player_move(ai_move)
            animate_move(mancala_board.mancala, ai_move)
            draw_board(mancala_board.mancala, probability=calculate_winning_probability(mancala_board.mancala), turn_message="AI's Turn" if repeat_turn else "Your Turn")
            pygame.display.flip()
            time.sleep(0.5)
            
            player_turn = not repeat_turn
            suggested_move = None  # Reset suggested move for next turn
        
        if mancala_board.isEnd():
            if mancala_board.mancala[13] > mancala_board.mancala[6]:
                winner_message = "AI-BOT WINS"
            elif mancala_board.mancala[13] < mancala_board.mancala[6]: 
                winner_message = "YOU WIN" 
            else: 
                winner_message = "TIE"
            draw_board(mancala_board.mancala, message=winner_message)
            pygame.display.flip()
            time.sleep(3)
            running = False
        
        clock.tick(60)

        
def initialize_population(size, num_pits):
    return [random.sample(range(6), num_pits) for _ in range(size)]

def fitness(individual, mancala_board):
    board_copy = Mancala_Board(mancala_board.mancala[:])
    total_stones = 0
    for move in individual:
        if board_copy.mancala[move] > 0:
            board_copy.player_move(move)
            total_stones += board_copy.mancala[6]  # Player's mancala
    return total_stones

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, 5)
    return individual

def genetic_algorithm(mancala_board, population_size=50, generations=20, mutation_rate=0.1):
    population = initialize_population(population_size, 3)  # Consider sequences of 3 moves
    
    for _ in range(generations):
        population = sorted(population, key=lambda x: fitness(x, mancala_board), reverse=True)
        new_population = population[:population_size // 2]
        
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:population_size // 2], 2)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    best_sequence = max(population, key=lambda x: fitness(x, mancala_board))
    return best_sequence[0]  # Return the first move of the best sequence
        
def splash_screen():
    screen.fill(WHITE)
    title_text = splash_font.render("MANCALA", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    prompt_text = message_font.render("Press any key to start", True, BLACK)
    screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()
    
    # Wait for a key press to start the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

print("\n:::: MANCALA BOARD GAME ::::")
print("!!! Welcome to Mancala Gameplay !!!")
while True:
    print("\nPlay the game")
    splash_screen()
    player_aibot()
    break

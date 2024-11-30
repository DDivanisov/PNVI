import pygame
import sys
import time


pygame.init()

WIDTH, HEIGHT = 500, 650  
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH // COLS
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")

font = pygame.font.SysFont(None, 40)

def draw_board(board, selected_color):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, board[row][col], (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

    for i, color in enumerate(COLORS):
        pygame.draw.rect(screen, color, (i * SQUARE_SIZE, HEIGHT - SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if color == selected_color:
            pygame.draw.rect(screen, (255, 255, 255), (i * SQUARE_SIZE, HEIGHT - SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

def draw_start_buttons():
    button_texts = ["Easy", "Medium", "Hard"]
    buttons = []
    for i, text in enumerate(button_texts):
        button_text = font.render(text, True, BG_COLOR, TEXT_COLOR)
        button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + i * 60))
        pygame.draw.rect(screen, TEXT_COLOR, button_rect.inflate(20, 10))
        screen.blit(button_text, button_rect)
        buttons.append((button_rect, text))
    return buttons

def draw_timer(start_time, time_limit):
    elapsed_time = time.time() - start_time
    remaining_time = max(0, time_limit - elapsed_time)
    timer_text = font.render(f"Time: {remaining_time:.2f}s", True, TEXT_COLOR)
    
    timer_rect = timer_text.get_rect(center=(WIDTH // 2, 30))  
    pygame.draw.rect(screen, (0, 0, 0), timer_rect.inflate(20, 10))
    screen.blit(timer_text, timer_rect)
    
    return remaining_time

def is_valid(board, row, col, color, difficulty):
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    if difficulty in ["Medium", "Hard"]:
        neighbors += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for d_row, d_col in neighbors:
        n_row, n_col = row + d_row, col + d_col
        if 0 <= n_row < ROWS and 0 <= n_col < COLS:
            if board[n_row][n_col] == color:
                return False
    return True

def is_game_won(board, difficulty):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == WHITE or not is_valid(board, row, col, board[row][col], difficulty):
                return False
    return True

def draw_play_again_button():
    button_text = font.render("Play Again", True, BG_COLOR, TEXT_COLOR)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, TEXT_COLOR, button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)
    return button_rect

board = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]
selected_color = COLORS[0]
game_started = False
start_time = None
time_limit = None
current_difficulty = None
running = True
game_won = False
game_lost = False
while running:
    screen.fill(BG_COLOR)

    if game_started:
        draw_board(board, selected_color)

        if is_game_won(board, current_difficulty) and not game_won:
            game_won = True
            end_time = time.time()

        if not game_won and draw_timer(start_time, time_limit) <= 0:
            game_lost = True

        if game_won:
            win_text = font.render(f"You won! Time: {end_time - start_time:.2f}s", True, TEXT_COLOR)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT - SQUARE_SIZE - 100))
            play_again_button = draw_play_again_button()
        elif game_lost:
            lose_text = font.render("Time's up! You lost!", True, TEXT_COLOR)
            screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, HEIGHT - SQUARE_SIZE - 100))
            play_again_button = draw_play_again_button()
    else:
        start_buttons = draw_start_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if game_started and (game_won or game_lost):
                if play_again_button.collidepoint(x, y):
                    board = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]
                    selected_color = COLORS[0]
                    game_started = False
                    game_won = False
                    game_lost = False
            elif game_started and not (game_won or game_lost):
                if y < HEIGHT - SQUARE_SIZE: 
                    col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                    board[row][col] = selected_color
                else: 
                    color_index = x // SQUARE_SIZE
                    if color_index < len(COLORS):
                        selected_color = COLORS[color_index]
            elif not game_started:
                for button_rect, difficulty in start_buttons:
                    if button_rect.collidepoint(x, y):
                        game_started = True
                        current_difficulty = difficulty
                        start_time = time.time()
                        time_limit = {"Easy": 90, "Medium": 60, "Hard": 30}[difficulty]
    pygame.display.flip()

pygame.quit()
sys.exit()

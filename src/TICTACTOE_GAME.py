import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
LINE_WIDTH = 15
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
WHITE = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

# Game variables
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
player = "X"
game_over = False

# Font
font = pygame.font.Font(None, 48)

# Create display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe with High Graphics")
screen.fill(BG_COLOR)


def draw_lines():
    """Draws the grid lines for the board."""
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)


def draw_figures():
    """Draws Xs and Os based on the board state."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                start_x = col * SQUARE_SIZE + SPACE
                start_y = row * SQUARE_SIZE + SPACE
                end_x = (col + 1) * SQUARE_SIZE - SPACE
                end_y = (row + 1) * SQUARE_SIZE - SPACE
                pygame.draw.line(screen, CROSS_COLOR, (start_x, start_y), (end_x, end_y), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (start_x, end_y), (end_x, start_y), CROSS_WIDTH)


def check_winner():
    """Checks if there is a winner and returns the winning player."""
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0], [(row, 0), (row, 1), (row, 2)]
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col], [(0, col), (1, col), (2, col)]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    return None, []


def check_tie():
    """Checks if the board is full, resulting in a tie."""
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True


def draw_winning_line(cells):
    """Draws a winning line across the winning cells."""
    if cells:
        start_cell = cells[0]
        end_cell = cells[-1]
        start_x = start_cell[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        start_y = start_cell[0] * SQUARE_SIZE + SQUARE_SIZE // 2
        end_x = end_cell[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        end_y = end_cell[0] * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), 10)


def restart_game():
    """Resets the game board for a new round."""
    global board, player, game_over
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    player = "X"
    game_over = False
    screen.fill(BG_COLOR)
    draw_lines()
    draw_restart_button()


def draw_restart_button():
    """Draws the restart button."""
    pygame.draw.rect(screen, WHITE, (200, HEIGHT - 80, 200, 50), border_radius=10)
    text = font.render("Restart", True, TEXT_COLOR)
    screen.blit(text, (250, HEIGHT - 70))


# Draw the initial board and restart button
draw_lines()
draw_restart_button()

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_restart_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE

            if row < BOARD_ROWS and board[row][col] is None:
                board[row][col] = player
                winner, win_cells = check_winner()

                if winner:
                    print(f"Player {winner} wins!")
                    draw_winning_line(win_cells)
                    game_over = True
                elif check_tie():
                    print("It's a tie!")
                    game_over = True
                player = "O" if player == "X" else "X"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if 200 <= mx <= 400 and HEIGHT - 80 <= my <= HEIGHT - 30:
                restart_game()

    pygame.display.update()

pygame.quit()
sys.exit()

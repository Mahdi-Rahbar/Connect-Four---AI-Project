# Mahdi Rahbar

# Importing necessary libraries
import numpy as np
import pygame
import sys
import math
import copy

# Colors - RGB values for various colors used in the game
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Dimensions - Constants for the board size and window dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# Initialize pygame
pygame.init()

# Fonts - Fonts for displaying text
font = pygame.font.SysFont("monospace", 50)
score_font = pygame.font.SysFont("monospace", 35)

# Constants - Game-related constants
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

# Load images
board_img = pygame.image.load("board.png")
red_piece_img = pygame.image.load("red_piece.png")
yellow_piece_img = pygame.image.load("yellow_piece.png")
empty_slot_img = pygame.image.load("empty_slot.png")
header_img = pygame.image.load("header.png")
game_over_img = pygame.image.load("game_over.png")

# Resize images
board_img = pygame.transform.scale(board_img, (width, height - SQUARESIZE))
red_piece_img = pygame.transform.scale(red_piece_img, (SQUARESIZE, SQUARESIZE))
yellow_piece_img = pygame.transform.scale(yellow_piece_img, (SQUARESIZE, SQUARESIZE))
empty_slot_img = pygame.transform.scale(empty_slot_img, (SQUARESIZE, SQUARESIZE))
header_img = pygame.transform.scale(header_img, (width, SQUARESIZE))



def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diagonals for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diagonals for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    ai_score = 0
    player_score = 0

    # Horizontal Scoring
    for row in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[row, :])]
        for col in range(COLUMN_COUNT - 3):
            window = row_array[col:col + 4]
            ai_score += evaluate_window(window, AI_PIECE)
            player_score += evaluate_window(window, PLAYER_PIECE)

    # Vertical Scoring
    for col in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(ROW_COUNT - 3):
            window = col_array[row:row + 4]
            ai_score += evaluate_window(window, AI_PIECE)
            player_score += evaluate_window(window, PLAYER_PIECE)

    # Positive Diagonal Scoring
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            window = [board[row + i][col + i] for i in range(4)]
            ai_score += evaluate_window(window, AI_PIECE)
            player_score += evaluate_window(window, PLAYER_PIECE)

    # Negative Diagonal Scoring
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            window = [board[row + 3 - i][col + i] for i in range(4)]
            ai_score += evaluate_window(window, AI_PIECE)
            player_score += evaluate_window(window, PLAYER_PIECE)

    return ai_score if piece == AI_PIECE else player_score


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def is_terminal_node(board):
    return (
            winning_move(board, PLAYER_PIECE)
            or winning_move(board, AI_PIECE)
            or len(get_valid_locations(board)) == 0
    )


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = np.random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


board = create_board()
game_over = False
turn = np.random.randint(PLAYER, AI)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four Game")


def draw_board_with_images(board, player_score, ai_score):
    # Draw board background
    screen.blit(board_img, (0, SQUARESIZE))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == EMPTY:
                screen.blit(empty_slot_img, (c * SQUARESIZE, height - (r + 1) * SQUARESIZE))
            elif board[r][c] == PLAYER_PIECE:
                screen.blit(red_piece_img, (c * SQUARESIZE, height - (r + 1) * SQUARESIZE))
            elif board[r][c] == AI_PIECE:
                screen.blit(yellow_piece_img, (c * SQUARESIZE, height - (r + 1) * SQUARESIZE))

    # Draw score bar
    screen.blit(header_img, (0, 0))
    player_label = score_font.render(f"Player: {player_score}", 1, RED)
    ai_label = score_font.render(f"AI: {ai_score}", 1, YELLOW)
    screen.blit(player_label, (40, 10))
    screen.blit(ai_label, (width - 200, 10))

    pygame.display.update()


def animate_piece_drop(col, row, piece):
    piece_img = red_piece_img if piece == PLAYER_PIECE else yellow_piece_img
    for i in range(row + 1):
        draw_board_with_images(board, player_score, ai_score)
        screen.blit(piece_img, (col * SQUARESIZE, height - (i + 1) * SQUARESIZE))
        pygame.display.update()
        pygame.time.delay(50)


# Initialize scores
player_score = 0
ai_score = 0

# Draw the initial board with scores
draw_board_with_images(board, player_score, ai_score)


def winning_move_in_one_step(board, piece):
    valid_locations = get_valid_locations(board)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        if winning_move(temp_board, piece):
            return col
    return None





def minimax(board, depth, alpha, beta, maximizing_player):

    terminal_state = is_terminal_node(board)
    posible_moves = get_valid_locations(board)

    if terminal_state or depth == 0:

        if terminal_state:
            if winning_move(board, AI_PIECE):
                return None, 50
            elif winning_move(board, PLAYER_PIECE):
                return None, -50
            else:
                return None, 0
        else:
            return None, score_position(board, AI_PIECE)

    if maximizing_player:
        best_col = np.random.choice(posible_moves)
        value = -math.inf

        for col in posible_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            _, new_score = minimax(temp_board, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return best_col, value

    else:  # Minimizing player
        best_col = np.random.choice(posible_moves)
        value = math.inf

        for col in posible_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            _, new_score = minimax(temp_board, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_col, value





class GameState:
    def __init__(self, board, last_move=None):
        self.board = board
        self.last_move = last_move


    def legal_moves(self):

        return [col for col in range(COLUMN_COUNT) if is_valid_location(self.board, col)]


    def tryMove(self, col):

        if is_valid_location(self.board, col):
            return get_next_open_row(self.board, col)
        return None


    def terminal(self):

        return is_terminal_node(self.board)


    def winner(self):

        if winning_move(self.board, PLAYER_PIECE):
            return PLAYER_PIECE
        elif winning_move(self.board, AI_PIECE):
            return AI_PIECE
        return None


    def next_state(self, col, piece):
        row = self.tryMove(col)
        if row is not None:
            new_board = self.board.copy()
            drop_piece(new_board, row, col, piece)
            return GameState(new_board, last_move=(row, col))
        return None



class Node:
    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state
        self.children = []
        self.children_move = []
        self.parent = parent


    def add_child(self, child_state, move):
        child = Node(child_state, self)
        self.children.append(child)
        self.children_move.append(move)


    def update(self, reward):
        self.reward += reward
        self.visits += 1


    def fully_explored(self):
        return len(self.children) == len(self.state.legal_moves())



def MCTS(max_iter, root, factor):
    for _ in range(max_iter):
        front, turn = tree_policy(root, 1, factor)
        reward = default_policy(front.state, turn)
        backup(front, reward, turn)

    best = best_child(root, 0)
    print([c.reward / c.visits for c in root.children])
    return best


def tree_policy(node, turn, factor):
    while not node.state.terminal():
        if not node.fully_explored():
            return expand(node, turn), -turn
        else:
            node = best_child(node, factor)
            turn *= -1
    return node, turn


def expand(node, turn):
    tried_children_moves = node.children_move
    possible_moves = node.state.legal_moves()

    for move in possible_moves:
        if move not in tried_children_moves:
            new_state = node.state.next_state(move, turn)
            node.add_child(new_state, move)
            break

    return node.children[-1]


def best_child(node, factor):
    best_score = -float('inf')
    best_children = []

    for child in node.children:
        exploit = child.reward / child.visits
        explore = math.sqrt(math.log(node.visits) / child.visits)
        score = exploit + factor * explore

        if score == best_score:
            best_children.append(child)
        elif score > best_score:
            best_children = [child]
            best_score = score

    return np.random.choice(best_children)


def default_policy(state, turn):
    while not state.terminal():
        valid_moves = state.legal_moves()
        move = np.random.choice(valid_moves)
        state = state.next_state(move, turn)
        turn *= -1

    winner = state.winner()
    if winner == AI_PIECE:
        return 1
    elif winner == PLAYER_PIECE:
        return -1
    else:
        return 0


def backup(node, reward, turn):
    while node is not None:
        node.visits += 1
        node.reward += reward if turn == 1 else -reward
        node = node.parent
        turn *= -1





def display_end_screen(winner_message, player_score, ai_score):
    end_screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Game Over")

    end_screen.blit(game_over_img, (0, 0))

    title_font = pygame.font.SysFont("monospace", 50)
    score_font = pygame.font.SysFont("monospace", 35)

    winner_label = title_font.render(winner_message, 1, RED)
    player_score_label = score_font.render(f"Player Score: {player_score}", 1, WHITE)
    ai_score_label = score_font.render(f"AI Score: {ai_score}", 1, WHITE)

    end_screen.blit(winner_label, (100, 50))
    end_screen.blit(player_score_label, (100, 150))
    end_screen.blit(ai_score_label, (100, 200))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()



def show_menu():

    menu_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Menu")


    background_img = pygame.image.load("menu_background.png")
    background_img = pygame.transform.scale(background_img, (800, 600))

    title_img = pygame.image.load("title_image.png")
    title_img = pygame.transform.scale(title_img, (400, 100))

    button_minimax_img = pygame.image.load("button_minimax.png")
    button_minimax_img = pygame.transform.scale(button_minimax_img, (290, 130))

    button_mcts_img = pygame.image.load("button_mcts.png")
    button_mcts_img = pygame.transform.scale(button_mcts_img, (290, 130))


    button_width, button_height = 290, 130
    button_minimax_rect = pygame.Rect(
        (800 - button_width) // 2,
        250,
        button_width,
        button_height
    )
    button_mcts_rect = pygame.Rect(
        (800 - button_width) // 2,
        button_minimax_rect.bottom + 30,
        button_width,
        button_height
    )


    menu_screen.blit(background_img, (0, 0))
    menu_screen.blit(title_img, ((800 - 400) // 2, 50))
    menu_screen.blit(button_minimax_img, (button_minimax_rect.x, button_minimax_rect.y))
    menu_screen.blit(button_mcts_img, (button_mcts_rect.x, button_mcts_rect.y))

    pygame.display.update()

   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_minimax_rect.collidepoint(mouse_pos):
                    return "minimax"
                elif button_mcts_rect.collidepoint(mouse_pos):
                    return "mcts"



selected_ai = show_menu()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four Game")
draw_board_with_images(board, player_score, ai_score)
pygame.display.update()



# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            if turn == PLAYER:
                mouse_x = event.pos[0]
                draw_board_with_images(board, player_score, ai_score)
                screen.blit(red_piece_img, (mouse_x - SQUARESIZE // 2, 10))
                pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Player Turn
            if turn == PLAYER:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    animate_piece_drop(col, row, PLAYER_PIECE)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    player_score += score_position(board, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        player_score += 1000
                        display_end_screen("Player Wins!", player_score, ai_score)
                        game_over = True


                    turn = AI
                    draw_board_with_images(board, player_score, ai_score)
    # AI Turn
    if turn == AI and not game_over:

        if selected_ai == "minimax":
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            ai_score += minimax_score

        elif selected_ai == "mcts":
            root_node = Node(GameState(board.copy()))
            best_node = MCTS(max_iter=1000, root=root_node, factor=0.8)
            col = best_node.parent.children_move[root_node.children.index(best_node)]

            ai_reward = float(f"{best_node.reward / best_node.visits:.3f}")
            ai_score += ai_reward


        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            animate_piece_drop(col, row, AI_PIECE)
            drop_piece(board, row, col, AI_PIECE)


            if winning_move(board, AI_PIECE):
                ai_score += 1000
                display_end_screen("AI Wins!", player_score, ai_score)
                game_over = True

            turn = PLAYER
            draw_board_with_images(board, player_score, ai_score)



    if game_over:              
        pygame.time.wait(3000)

        if winning_move(board, PLAYER_PIECE):
            display_end_screen(player_score, ai_score, "Player Wins!")
        elif winning_move(board, AI_PIECE):
            display_end_screen(player_score, ai_score, "AI Wins!")
        else:
            display_end_screen(player_score, ai_score, "It's a Draw!")

        pygame.time.wait(3000)

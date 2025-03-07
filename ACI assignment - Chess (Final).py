import numpy as np
import copy

# Define constants
WHITE_PAWN = 'WP'
WHITE_HORSE = 'WH'
BLACK_PAWN = 'BP'
BLACK_HORSE = 'BH'
EMPTY = '..'

def initialize_board():
    return [
        [WHITE_PAWN, WHITE_HORSE, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, BLACK_PAWN, BLACK_HORSE]
    ]

def print_board(board):
    print("   0    1    2")
    for i, row in enumerate(board):
        print(i, " ".join(row))
    print("\n")

def evaluate_board(board):
    score = 0
    piece_values = {'WP': -1, 'WH': -5, 'BP': 1, 'BH': 5}
    
    for row in board:
        for cell in row:
            if cell in piece_values:
                score += piece_values[cell]
    
    return score

def print_scoreboard(board):
    score = evaluate_board(board)
    print(f"Scoreboard: {score} (Positive = AI Winning, Negative = Human Winning)\n")

def get_valid_moves(board, piece, x, y):
    moves = []
    if piece == WHITE_PAWN:
        if x < 2 and board[x+1][y] == EMPTY:
            moves.append((x+1, y))
        if x < 2 and y > 0 and board[x+1][y-1] in [BLACK_PAWN, BLACK_HORSE]:
            moves.append((x+1, y-1))
        if x < 2 and y < 2 and board[x+1][y+1] in [BLACK_PAWN, BLACK_HORSE]:
            moves.append((x+1, y+1))
    elif piece == BLACK_PAWN:
        if x > 0 and board[x-1][y] == EMPTY:
            moves.append((x-1, y))
        if x > 0 and y > 0 and board[x-1][y-1] in [WHITE_PAWN, WHITE_HORSE]:
            moves.append((x-1, y-1))
        if x > 0 and y < 2 and board[x-1][y+1] in [WHITE_PAWN, WHITE_HORSE]:
            moves.append((x-1, y+1))
    elif piece in [WHITE_HORSE, BLACK_HORSE]:
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in knight_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3 and board[nx][ny] not in [piece]:
                moves.append((nx, ny))
    return moves

def apply_move(board, x1, y1, x2, y2):
    board[x2][y2] = board[x1][y1]
    board[x1][y1] = EMPTY

def has_valid_moves(board, player_pieces):
    for x in range(3):
        for y in range(3):
            if board[x][y] in player_pieces:
                if get_valid_moves(board, board[x][y], x, y):
                    return True
    return False

def minimax(board, depth, is_maximizing):
    if depth == 0:
        return evaluate_board(board)
    
    best_move = None
    valid_moves = []
    
    if is_maximizing:
        max_eval = float('-inf')
        for x in range(3):
            for y in range(3):
                if board[x][y] in [BLACK_PAWN, BLACK_HORSE]:
                    moves = get_valid_moves(board, board[x][y], x, y)
                    for move in moves:
                        new_board = copy.deepcopy(board)
                        apply_move(new_board, x, y, move[0], move[1])
                        eval_score = minimax(new_board, depth-1, False)
                        if eval_score > max_eval:
                            max_eval = eval_score
                            best_move = (x, y, move[0], move[1])
                        valid_moves.append((x, y, move[0], move[1]))
        if best_move is None and valid_moves:
            best_move = valid_moves[0]
        return best_move if depth == 4 else max_eval
    else:
        min_eval = float('inf')
        for x in range(3):
            for y in range(3):
                if board[x][y] in [WHITE_PAWN, WHITE_HORSE]:
                    moves = get_valid_moves(board, board[x][y], x, y)
                    for move in moves:
                        new_board = copy.deepcopy(board)
                        apply_move(new_board, x, y, move[0], move[1])
                        eval_score = minimax(new_board, depth-1, True)
                        min_eval = min(min_eval, eval_score)
        return min_eval

def play_game():
    board = initialize_board()
    print_board(board)
    print_scoreboard(board)

    while True:
        score = evaluate_board(board)
        if score >= 6:
            print("AI wins! Score reached 6.")
            return
        if score <= -6:
            print("Human wins! Score reached -6.")
            return
        
        if not has_valid_moves(board, [WHITE_PAWN, WHITE_HORSE]) and any(p in row for row in board for p in [WHITE_PAWN, WHITE_HORSE]):
            print("Game drawn! No valid moves left for player.")
            return
        
        while True:
            try:
                x1, y1, x2, y2 = map(int, input("Enter your move (x1 y1 x2 y2): ").split())
                if (0 <= x1 < 3 and 0 <= y1 < 3 and 0 <= x2 < 3 and 0 <= y2 < 3 and
                    (x2, y2) in get_valid_moves(board, board[x1][y1], x1, y1)):
                    break
                else:
                    print("Move not allowed. Try again.")
            except ValueError:
                print("Invalid input. Please enter four numbers separated by spaces.")
        
        apply_move(board, x1, y1, x2, y2)
        print_board(board)
        print_scoreboard(board)

        score = evaluate_board(board)
        if score >= 6:
            print("AI wins! Score reached 6.")
            return
        if score <= -6:
            print("Human wins! Score reached -6.")
            return

        print("AI is thinking...")
        ai_move = minimax(board, 4, True)
        if ai_move:
            apply_move(board, *ai_move)
            print("AI's move:")
            print_board(board)
            print_scoreboard(board)
        else:
            if any(p in row for row in board for p in [BLACK_PAWN, BLACK_HORSE]):
                print("Game drawn! No valid moves left for AI.")
            return

play_game()

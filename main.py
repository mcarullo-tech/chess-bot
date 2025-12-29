import chess
import random

from piece_square_tables import (
    PIECE_SQUARE_TABLES,
    KING_MIDDLE_TABLE,
    KING_END_TABLE
)


UNICODE_PIECES = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚"
}

def print_board_unicode(board):
    board_str = str(board)
    for ascii_piece, uni_piece in UNICODE_PIECES.items():
        board_str = board_str.replace(ascii_piece, uni_piece)
    print(board_str)


# PERFT function to count nodes at a given depth
def perft(board, depth):
    if depth == 0:
        return 1

    nodes = 0
    for move in board.legal_moves:
        board.push(move)
        nodes += perft(board, depth - 1)
        board.pop()
    return nodes

# Run PERFT test
def run_perft(depth):
    print(f"\nRunning PERFT to depth {depth}...\n")
    result = perft(board, depth)
    print(f"Nodes: {result}\n")

# Human player move input and validation
def human_move():
    while True:
        san_move = input("Enter your move (SAN): ")

        # Allow player to resign
        if san_move.lower() == "resign":
            print("You resigned. Game over.")
            exit()

        # Checks legality and makes the move
        try:
            move = board.parse_san(san_move)
            board.push(move)
            break
        except ValueError:
            print("Illegal move")


# BetterFish: Chess bot using minimax with alpha-beta pruning
def engine_move(depth):
    best_move = None

    # Decide if we're maximizing or minimizing based on side to move
    if board.turn == chess.WHITE:
        maximizing_player = True
        best_eval = -float('inf')
    else:
        maximizing_player = False
        best_eval = float('inf')

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, -float('inf'), float('inf'), not maximizing_player)
        board.pop()

        if maximizing_player and eval > best_eval:
            best_eval = eval
            best_move = move
        elif not maximizing_player and eval < best_eval:
            best_eval = eval
            best_move = move

    san = board.san(best_move)
    board.push(best_move)
    return san


# Determine if we are in an endgame
def is_endgame(board):
    pieces = list(board.piece_map().values())

    # Condition A: no queens on the board
    if not any(p.piece_type == chess.QUEEN for p in pieces):
        return True

    # Condition B: no rooks and at most two minor pieces total
    minor_count = sum(p.piece_type in (chess.BISHOP, chess.KNIGHT) for p in pieces)
    rook_count = sum(p.piece_type == chess.ROOK for p in pieces)

    if rook_count == 0 and minor_count <= 2:
        return True

    return False


# Material evaluation function with piece-square tables
def material_evaluation(board):
    endgame = is_endgame(board)
    score = 0

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    # Loop through every occupied square on the board
    for square, piece in board.piece_map().items():
        # Store the material value of the piece in "base value"
        base_value = piece_values[piece.piece_type]

        # Select correct PST
        if piece.piece_type == chess.KING:
            pst = KING_END_TABLE if endgame else KING_MIDDLE_TABLE
        else:
            pst = PIECE_SQUARE_TABLES[piece.piece_type]

        # Apply PST value to base material value
        if piece.color == chess.WHITE:
            pst_value = pst[square]
            score += base_value + pst_value
        # Mirror for black
        else:
            mirrored = chess.square_mirror(square)
            pst_value = pst[mirrored]
            score -= base_value + pst_value

    # Score will be positive if white is better, and negative if black is better
    return score

# Improve searching via minimax function with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    # Base case: depth reached or game over
    if depth == 0 or board.is_game_over():
        return material_evaluation(board)

    if maximizing_player:
        value = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = max(value, minimax(board, depth - 1, alpha, beta, False))
            board.pop()

            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        return value

    else:
        value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = min(value, minimax(board, depth - 1, alpha, beta, True))
            board.pop()

            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cutoff
        return value


# Initialize the chess board
board = chess.Board()
print_board_unicode(board)

white_or_black = input("Choose your side (white/black): ").strip().lower()
if white_or_black == "white":
    while not board.is_game_over():
        # White to move: Human
        human_move()

        if board.is_game_over():
            break

        # Black to move: Engine with depth=3
        machine_move = engine_move(3)

        print_board_unicode(board)
        print("\nBlack plays:", machine_move, "\n")

    print("Game over:", board.result())
else:
    while not board.is_game_over():
        # White to move: Engine with depth=3
        machine_move = engine_move(3)

        print("\n" + str(board) + "\n")
        print("\nWhite plays:", machine_move, "\n")

        if board.is_game_over():
            break

        # Black to move: Human
        human_move()
    
    print("Game over:", board.result())

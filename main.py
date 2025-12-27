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

# RandomFish: Chess bot which simply plays random legal moves
def random_machine_move():
    legal_moves = list(board.legal_moves)
    bot_move = random.choice(legal_moves)

    # Convert to SAN for display
    bot_san = board.san(bot_move)
    board.push(bot_move)
    return bot_san

# SimpleFish: Chess bot which plays the move that maximizes material advantage
def simple_machine_move():
    best_move = None
    best_evaluation = -float('inf')

    for move in board.legal_moves:
        board.push(move)
        evaluation = material_evaluation(board)
        board.pop()

        # Flip evaluation if Black is moving
        if board.turn == chess.BLACK:
            evaluation = -evaluation

        if evaluation > best_evaluation:
            best_evaluation = evaluation
            best_move = move

    # Get SAN BEFORE pushing
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


# Simple material evaluation function
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

    for square, piece in board.piece_map().items():
        base_value = piece_values[piece.piece_type]

        # Select correct PST
        if piece.piece_type == chess.KING:
            pst = KING_END_TABLE if endgame else KING_MIDDLE_TABLE
        else:
            pst = PIECE_SQUARE_TABLES[piece.piece_type]

        # Mirror for black
        if piece.color == chess.WHITE:
            pst_value = pst[square]
            score += base_value + pst_value
        else:
            mirrored = chess.square_mirror(square)
            pst_value = pst[mirrored]
            score -= base_value + pst_value

    return score


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

        # Black to move: Simple AI
        machine_move = simple_machine_move()

        print_board_unicode(board)
        print("\nBlack plays:", machine_move, "\n")

    print("Game over:", board.result())
else:
    while not board.is_game_over():
        # White to move: Simple AI
        machine_move = simple_machine_move()

        print("\n" + str(board) + "\n")
        print("\nWhite plays:", machine_move, "\n")

        if board.is_game_over():
            break

        # Black to move: Human
        human_move()
    
    print("Game over:", board.result())

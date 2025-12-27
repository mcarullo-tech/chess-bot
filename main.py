import chess
import random

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


# Simple material evaluation function
def material_evaluation(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    white_material = sum(piece_values[piece.piece_type] for piece in board.piece_map().values() if piece.color == chess.WHITE)
    black_material = sum(piece_values[piece.piece_type] for piece in board.piece_map().values() if piece.color == chess.BLACK)

    return white_material - black_material



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

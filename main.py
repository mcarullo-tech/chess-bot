import chess
import random

def perft(board, depth):
    if depth == 0:
        return 1

    nodes = 0
    for move in board.legal_moves:
        board.push(move)
        nodes += perft(board, depth - 1)
        board.pop()
    return nodes

def run_perft(depth):
    print(f"\nRunning PERFT to depth {depth}...\n")
    result = perft(board, depth)
    print(f"Nodes: {result}\n")

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

# Initialize the chess board
board = chess.Board()
print(board)

# Run PERFT test at depth 1
run_perft(3)


white_or_black = input("Choose your side (white/black): ").strip().lower()
if white_or_black == "white":
    while not board.is_game_over():
        # White to move: Human
        human_move()

        if board.is_game_over():
            break

        # Black to move: Random AI
        machine_move = random_machine_move()

        print("\n" + str(board) + "\n")
        print("\nBlack plays:", machine_move, "\n")

    print("Game over:", board.result())
else:
    while not board.is_game_over():
        # White to move: Random AI
        machine_move = random_machine_move()

        print("\n" + str(board) + "\n")
        print("\nBlack plays:", machine_move, "\n")

        if board.is_game_over():
            break

        # Black to move: Human
        human_move()
    
    print("Game over:", board.result())

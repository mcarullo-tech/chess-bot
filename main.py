import chess
import random

board = chess.Board()
print(board)

while not board.is_game_over():

    # --- White to move: Human ---
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

    if board.is_game_over():
        break

    # --- Black to move: Random AI ---
    legal_moves = list(board.legal_moves)
    bot_move = random.choice(legal_moves)

    # Convert to SAN BEFORE pushing
    bot_san = board.san(bot_move)

    board.push(bot_move)

    print("\n" + str(board) + "\n")
    print("\nBlack plays:", bot_san, "\n")



print("Game over:", board.result())
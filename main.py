import chess
import random

board = chess.Board()
print(board)

while not board.is_game_over():

    # --- White to move: Human ---
    while True:
        chess_move = input("Enter your move (UCI): ")

        # Allow player to resign
        if chess_move.lower() == "resign":
            print("You resigned. Game over.")
            exit()

        # Error handling for invalid UCI format
        try:
            move = chess.Move.from_uci(chess_move)
        except ValueError:
            print("Invalid format, try again.")
            continue

        # Check if the move is legal
        if move in board.legal_moves:
            board.push(move)
            print(board)
            break
        else:
            print("Illegal move, try again.")

    # --- Black to move: Random AI ---
    legal_moves = list(board.legal_moves)
    bot_move = random.choice(legal_moves)
    board.push(bot_move)
    
    print("\n" + str(board) + "\n")
    print("\nBlack plays:", bot_move.uci(), "\n")


print("Game over:", board.result())
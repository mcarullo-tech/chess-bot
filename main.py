import chess

board = chess.Board()

while not board.is_game_over():

    while True:
        chess_move = input("Enter your move (UCI): ")

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

print("Game over:", board.result())
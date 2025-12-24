import chess

board = chess.Board()

Nf3 = chess.Move.from_uci("g1f3")
board.push(Nf3)

print(board)

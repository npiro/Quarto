
from board import Board, PieceStack, Turn, get_piece_text, EMPTY, ROWS, COLS
from evaluate import Evaluate, WIN

evaluator = Evaluate()

def AlphaBetaSearch(board, piecestack, piece, turn, depth, alpha, beta):
    global iter
    score = evaluator.get_score(board, turn)


    if score == WIN or depth == 0 or len(piecestack) == 0:
        return -score

    # Take the piece from the stack
    piecestack.TakePiece(piece)
    # Get a list of pieces in stack
    piecelist = piecestack.GetPieceList()

    for p in piecelist:
        for x in range(ROWS):
            for y in range(COLS):
                if board.pieces[x][y] is EMPTY:
                    board.place_piece(piece, x, y)
                    turn.change()

                    iter += 1

                    score = -AlphaBetaSearch(board, piecestack, p, turn, depth-1, -beta, -alpha)

                    if score >= beta:
                        turn.change()
                        board.unplace_piece(piece, x, y)
                        piecestack.PutPieceBack(piece)
                        return beta

                    if score  > alpha: alpha = score

                    if score == WIN:
                        board.unplace_piece(piece, x, y)
                        piecestack.PutPieceBack(piece)
                        return score

                    turn.change()
                    board.unplace_piece(piece, x, y)



    piecestack.PutPieceBack(piece)
    return alpha


def RootOfAlphaBetaSearch(board, piecestack, piece, turn, depth):
    global iter
    print('Depth:'+str(depth))
    iter = 0
    best = -100000
    piecelist = piecestack.GetPieceList()
    piecestack.show()
    for p in piecelist:
        for x in range(ROWS):
            for y in range(COLS):
                if board.pieces[x][y] is EMPTY:
                    board.place_piece(piece, x, y)
                    turn.change()
                    score = -AlphaBetaSearch(board, piecestack, p, turn, depth - 1, -10000, 10000)
                    if score > best:
                        best = score
                        bestx = x
                        besty = y
                        bestpiece = p
                        #piecestack.PutPieceBack(p)
                    turn.change()
                    board.unplace_piece(piece, x, y)

    return (bestx, besty, bestpiece, best)
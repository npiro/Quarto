from board import Board, PieceStack, Turn, Move, get_piece_text, EMPTY, ROWS, COLS
from evaluate import Evaluate, WIN
import time

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

                    score = -AlphaBetaSearch(board, piecestack, p, turn, depth - 1, -beta, -alpha)

                    if score >= beta:
                        turn.change()
                        board.unplace_piece(piece, x, y)
                        piecestack.PutPieceBack(piece)
                        return beta

                    if score > alpha: alpha = score

                    if score == WIN:
                        board.unplace_piece(piece, x, y)
                        piecestack.PutPieceBack(piece)
                        return score

                    turn.change()
                    board.unplace_piece(piece, x, y)

    piecestack.PutPieceBack(piece)
    return alpha


def RootOfAlphaBetaSearch(board, piecestack, piece, turn, max_depth, search_time):
    global iter

    iter = 0
    best = -100000
    piecelist = piecestack.GetPieceList()
    piecestack.show()
    move_list = [Move(x, y, piece, p, 0) for p in piecelist
                 for x in range(ROWS) for y in range(COLS) if board.pieces[x][y] is EMPTY]

    # Deepen search by 1 every iteration until time is up
    t = time.time()
    elapsed = 0
    for depth in range(2,max_depth):
        print('Depth:' + str(depth))
        for move in move_list:
            (x, y, piece, p, score) = move.get_move()
            board.place_piece(piece, x, y)
            turn.change()
            score = -AlphaBetaSearch(board, piecestack, p, turn, depth - 1, -10000, 10000)
            move.set_score(score)
            if score > best:
                best = score
                bestx = x
                besty = y
                bestpiece = p
                # piecestack.PutPieceBack(p)
            turn.change()
            board.unplace_piece(piece, x, y)

            # Stop if time is over
            elapsed = time.time() - t
            if elapsed > search_time:
                break

        move_list.sort(key=lambda m: m.get_score(), reverse=True)
        if best == WIN: break
        if elapsed > search_time: break






    return bestx, besty, bestpiece, best

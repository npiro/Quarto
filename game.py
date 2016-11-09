
from board import Board, PieceStack, Turn, get_piece_text, EMPTY
from evaluate import Evaluate, WIN
from random import randint
from search import RootOfAlphaBetaSearch

piecestack = PieceStack()

turn = Turn()

board = Board()

evaluate = Evaluate()

def UserTurn(piecestack, board, piece):

    board.show()
    piecestack.show()


    piecestack.TakePiece(piece)

    print('Piece: {0}'.format(get_piece_text(piece)))
    while True:
        x, y = [int(i)-1 for i in raw_input("Enter x y coordinates to place piece: ").split()]
        if board.pieces[x][y] is EMPTY:
            break
        else:
            print('Square is not empty. Try another one.')

    board.place_piece(piece, x, y)
    board.show()

def ComputerTurn(piecestack, board, piece, turn):
    piecestack.TakePiece(piece)

    (bestx, besty, bestpiece, bestscore) = RootOfAlphaBetaSearch(board, piecestack, piece, turn, int(5+0.2*(15-len(piecestack))),8.0)
    board.place_piece(piece, bestx, besty)
    print('Best score: '+str(bestscore))
    return bestpiece


# Select first user piece randomly
piecelist = piecestack.GetPieceList()
piecenum = randint(0,len(piecelist)-1)

piece = piecelist[piecenum]

while True:

    UserTurn(piecestack, board, piece)
    turn.change()
    score = evaluate.get_score(board, turn)
    print('Score: {0}'.format(score))
    if abs(score) == WIN:
        print ('Player wins')
        break

    piecestack.show()
    print ('Choose piece for computer to place:')
    piecenum = int(input())
    piecelist = list(piecestack)
    if piecenum in range(0, len(list(piecestack))):
        piece = piecelist[piecenum]
    print(get_piece_text(piece))
    piece = ComputerTurn(piecestack, board, piece, turn)
    turn.change()
    score = evaluate.get_score(board, turn)
    print('Score: {0}'.format(score))
    if abs(score) == WIN:
        print ('Computer wins')
        board.show()
        break




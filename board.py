from __future__ import print_function


ROWS = 4
COLS = 4
TYPES = 4
EMPTY = -1

COLOR = 0
WHITE = 0b0
BLACK = 0b1
ColorStr = ['W', 'B']

LENGTH = 1
SHORT = 0b00
LONG = 0b10
LengthStr = ['i', 'I']

HOLETYPE = 2
FULL = 0b000
HOLED = 0b100
HoletypeStr = ['F', 'H']

SHAPE = 3
SQUARE = 0b0000
CIRCLE = 0b1000
ShapeStr = ['=', 'O']

def get_piece_text(piece):
    color = piece & 0b1
    length = (piece >> 1) & 0b1
    holetype = (piece >> 2) & 0b1
    shape = (piece >> 3) & 0b1
    return '{0}{1}{2}{3}'.format(ColorStr[color], LengthStr[length], ShapeStr[shape], HoletypeStr[holetype])

class Board(object):
    """
    Board representation including 4x4 arrays representing pieces as a 4 bit word,
    colors, lengths, holetypes and shapes as a single bit and 5x4 arrays type_in_row/col
    as the number of each piece type in each row/column and diagonals (5th element of each array)
    """
    def __init__(self):
        self.pieces = [([EMPTY] * COLS) for row in xrange(ROWS)]
        self.colors = [([EMPTY] * COLS) for row in xrange(ROWS)]
        self.lengths = [([EMPTY] * COLS) for row in xrange(ROWS)]
        self.holetypes = [([EMPTY] * COLS) for row in xrange(ROWS)]
        self.shapes = [([EMPTY] * COLS) for row in xrange(ROWS)]

        self.type_in_row = [([0] * TYPES) for row in xrange(ROWS+1)]
        self.type_in_col = [([0] * TYPES) for row in xrange(COLS+1)]

    def place_piece(self, piece, x, y):
        # Piece type is encoded as a 4 bit word where each bit
        # represents color, length, holetype and shape
        color = piece & 0b1
        length = (piece >> 1) & 0b1
        holetype = (piece >> 2) & 0b1
        shape = (piece >> 3) & 0b1
        self.pieces[x][y] = piece
        self.colors[x][y] = color
        self.shapes[x][y] = shape
        self.lengths[x][y] = length
        self.holetypes[x][y] = holetype

        # Add/subtract 1 to type_in_row/col arrays at corresponsing row/col and piece specification
        self.type_in_row[x][COLOR] += (-1)**color
        self.type_in_row[x][LENGTH] += (-1)**length
        self.type_in_row[x][HOLETYPE] += (-1)**holetype
        self.type_in_row[x][SHAPE] += (-1)**shape
        self.type_in_col[y][COLOR] += (-1) ** color
        self.type_in_col[y][LENGTH] += (-1) ** length
        self.type_in_col[y][HOLETYPE] += (-1) ** holetype
        self.type_in_col[y][SHAPE] += (-1) ** shape
        # Same for any piece placed in each diagonal (use 5th array element for this)
        if x == y:
            self.type_in_row[4][COLOR] += (-1) ** color
            self.type_in_row[4][LENGTH] += (-1) ** length
            self.type_in_row[4][HOLETYPE] += (-1) ** holetype
            self.type_in_row[4][SHAPE] += (-1) ** shape

        if x == 3-y:
            self.type_in_col[4][COLOR] += (-1) ** color
            self.type_in_col[4][LENGTH] += (-1) ** length
            self.type_in_col[4][HOLETYPE] += (-1) ** holetype
            self.type_in_col[4][SHAPE] += (-1) ** shape


    def unplace_piece(self, piece, x, y):
    # Undo everything done in place_piece function

        color = piece & 0b1
        length = (piece >> 1) & 0b1
        holetype = (piece >> 2) & 0b1
        shape = (piece >> 3) & 0b1
        self.pieces[x][y] = EMPTY
        self.colors[x][y] = EMPTY
        self.shapes[x][y] = EMPTY
        self.lengths[x][y] = EMPTY
        self.holetypes[x][y] = EMPTY
        self.type_in_row[x][COLOR] -= (-1) ** color
        self.type_in_row[x][LENGTH] -= (-1) ** length
        self.type_in_row[x][HOLETYPE] -= (-1) ** holetype
        self.type_in_row[x][SHAPE] -= (-1) ** shape
        self.type_in_col[y][COLOR] -= (-1) ** color
        self.type_in_col[y][LENGTH] -= (-1) ** length
        self.type_in_col[y][HOLETYPE] -= (-1) ** holetype
        self.type_in_col[y][SHAPE] -= (-1) ** shape
        if x == y:
            self.type_in_row[4][COLOR] -= (-1) ** color
            self.type_in_row[4][LENGTH] -= (-1) ** length
            self.type_in_row[4][HOLETYPE] -= (-1) ** holetype
            self.type_in_row[4][SHAPE] -= (-1) ** shape

        if x == 3 - y:
            self.type_in_col[4][COLOR] -= (-1) ** color
            self.type_in_col[4][LENGTH] -= (-1) ** length
            self.type_in_col[4][HOLETYPE] -= (-1) ** holetype
            self.type_in_col[4][SHAPE] -= (-1) ** shape

    def show(self):
        for y in range(ROWS):
            print('+------+------+------+------+')
            print('|      |      |      |      |')
            for x in range(COLS):
                piece = self.pieces[x][y]

                if piece == EMPTY:
                    print('|      ', end = "")
                else:
                    print('| {0} '.format(get_piece_text(piece)), end = "")

            print('|')
            print('|      |      |      |      |')

        print('+------+------+------+------+')


class PieceStack(set):
    def __init__(self):
        # type: () -> None
        """
        :rtype: object
        """
        for piece in range(0,16):
            self.add(piece)

    def TakePiece(self, piece):
        self.remove(piece)
        return piece

    def PutPieceBack(self, piece):
        self.add(piece)

    def GetPieceList(self):
        return list(self)

    def show(self):
        piecelist = self.GetPieceList()
        print(', '.join([str(i) + ', ' + get_piece_text(p) for i, p in enumerate(piecelist)]))

class Turn(object):
    def __init__(self):
        self._turn = True

    def get_turn(self):
        return self._turn

    def set_turn(self, turn):
        self._turn = turn

    def other(self):
        return not self._turn

    def change(self):
        self._turn = not self._turn

    def sign(self):
        if self._turn:
            return 1
        else:
            return -1
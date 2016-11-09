from board import ROWS, COLS, TYPES

WIN = 1000


class Evaluate(object):
    def __init__(self):
        pass

    def get_score(self, board, turn):
        score = 0
        for x in range(ROWS + 1):
            for t in range(TYPES):

                if abs(board.type_in_row[x][t]) == 4:
                    score = WIN

        for y in range(COLS + 1):
            for t in range(TYPES):
                if abs(board.type_in_col[y][t]) == 4:
                    score = WIN

        return score


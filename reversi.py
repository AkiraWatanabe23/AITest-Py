'''リバーシテスト'''
import numpy as np

#マスの状態
NONE = 0
WHITE = 1
BLACK = -1
WALL = 2
BOARD_SIZE = 8

class Board():
    '''盤面の設定'''
    def __init__(self):
        #↓つくっているものは同じだけど、出力の形式が異なる
        #self.board = [[0] * 10 for _ in range(10)]
        self.board = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)

        #壁の設定
        self.board[0, :] = WALL
        self.board[:, 0] = WALL
        self.board[BOARD_SIZE + 1, :] = WALL
        self.board[:, BOARD_SIZE + 1] = WALL

        #石の初期配置
        self.board[4, 4] = WHITE
        self.board[5, 5] = WHITE
        self.board[4, 5] = BLACK
        self.board[5, 4] = BLACK

        self.turn = 0
        self.current_turn = WHITE

    def set_stone(self, x_pos, y_pos):
        '''石を配置する'''
        if x_pos < 1 or BOARD_SIZE < x_pos:
            return False
        if y_pos < 1 or BOARD_SIZE < y_pos:
            return False

        self.flip_stone(x_pos, y_pos)
        self.current_turn *= -1

        return True

    def flip_stone(self, x_pos, y_pos):
        '''盤面の反映'''
        self.board[x_pos, y_pos] = self.current_turn

instance = Board()

for y in range(10):
    for x in range(10):
        #「^」中央揃えのformat指定子
        print('{:^3}'.format(instance.board[x, y]), end="")
    print()

'''リバーシテスト'''
import numpy as np

#マスの状態
NONE = 0
WHITE = 1
BLACK = -1
WALL = 2
BOARD_SIZE = 8

class Board():
    '''盤面の初期設定'''
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

instance = Board()
print(instance.board)

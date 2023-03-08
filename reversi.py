'''リバーシテスト'''
import numpy as np

#マスの状態
EMPTY = 0
WHITE = 1
BLACK = -1
WALL = 2
BOARD_SIZE = 8

#探索方向の2進数表記
#以下のようにすることで、ひっくり返せる方向が考えやすくなる
#「00000000」の8bitの2進数として考えることで、1がたっている方向にはひっくり返せる、となる
LEFT = 1
UPPER_LEFT = 2
UPPER = 4
UPPER_RIGHT = 8
RIGHT = 16
LOWER_RIGHT = 32
LOWER = 64
LOWER_LEFT = 128

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

        self.movable_pos = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        self.movable_dir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)

        self.init_movables()

    def init_movables(self):
        ''' 判定用Listの初期化'''
        self.movable_pos[:, :] = False

        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):
                #各マスに石が置けるかの判定を行い、反映する
                move_dir = self.movable_check(x, y, self.current_turn)
                self.movable_dir[x, y] = move_dir

                #各マスの値が0でない(石が置ける)なら、Trueにする
                if move_dir != 0:
                    self.movable_pos[x, y] = True

    def movable_check(self, x_pos, y_pos, color) -> int:
        '''石を置ける位置の探索'''
        #指定したマスがどの方向に石をひっくり返せるかを格納する
        move_dir = 0

        #石が置かれていたらそこには置けない(この時点で以後の探索を行わず、終了する)
        if self.board[x_pos, y_pos] != EMPTY:
            return move_dir

        #各方向の表現を2進数で行う
        #探索したい方向に相手の石があれば、その方向の探索を始める
        #左
        if self.board[x_pos - 1, y_pos] == -color:
            x_check = x_pos - 2
            y_check = y_pos

            while self.board[x_check, y_check] == -color:
                x_check -= 1

            if self.board[x_check, y_check] == color:
                #ビット論理和
                #ex.) 0010 | 1000 -> 1010
                move_dir = move_dir | LEFT

        #左上
        if self.board[x_pos - 1, y_pos - 1] == -color:
            x_check = x_pos - 2
            y_check = y_pos - 2

            while self.board[x_check, y_check] == -color:
                x_check -= 1
                y_check -= 1

            if self.board[x_check, y_check] == color:
                move_dir = move_dir | UPPER_LEFT

        #上
        if self.board[x_pos, y_pos - 1] == -color:
            x_check = x_pos
            y_check = y_pos - 2

            while self.board[x_check, y_check] == -color:
                y_check -= 1

            if self.board[x_check, y_check] == color:
                move_dir = move_dir | UPPER

        #右上
        if self.board[x_pos + 1, y_pos - 1] == -color:
            x_check = x_pos + 2
            y_check = y_pos - 2

            while self.board[x_check, y_check] == -color:
                x_check += 1
                y_check -= 1

            if self.board[x_check, y_check] == color:
                move_dir = move_dir | UPPER_RIGHT

        #右
        if self.board[x_pos + 1, y_pos] == -color:
            x_check = x_pos + 2
            y_check = y_pos

            while self.board[x_check, y_check] == -color:
                x_check += 1

            if self.board[x_check, y_check] == color:
                move_dir = move_dir | RIGHT

        #右下
        if self.board[x_pos + 1, y_pos + 1] == -color:
            x_check = x_pos + 2
            y_check = y_pos + 2

            while self.board[x_check, y_check] == -color:
                x_check += 1
                y_check += 1

            if self.board[x_check, y_check] == color:
                move_dir = move_dir | LOWER_RIGHT

        #下
        if self.board[x_pos, y_pos + 1] == -color:
            x_check = x_pos
            y_check = y_pos + 2

            while self.board[x_check, y_check] == -color:
                y_check += 1

            if self.board[x_check, y_check] == color:
                move_dir = move_dir | LOWER

        #左下
        if self.board[x_pos - 1, y_pos + 1] == -color:
            x_check = x_pos - 2
            y_check = y_pos + 2

            while self.board[x_check, y_check] == -color:
                x_check -= 1
                y_check += 1

            if self.board[x_check, y_check] == color:
                move_dir = move_dir | LOWER_LEFT

        #移動可能な方向を格納した値を返す
        return move_dir

    def set_stone(self, x_pos, y_pos) -> bool:
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

#以下テスト表示
print('StartState')
for y in range(10):
    for x in range(10):
        #「^」中央揃えのformat指定子
        print('{:^3}'.format(instance.board[x, y]), end="")
    print()

print('1 is movable pos')
for y in range(10):
    for x in range(10):
        #「^」中央揃えのformat指定子
        print('{:^3}'.format(instance.movable_pos[x, y]), end="")
    print()

print('movable dir')
for y in range(10):
    for x in range(10):
        #「^」中央揃えのformat指定子
        print('{:^3}'.format(instance.movable_dir[x, y]), end="")
    print()

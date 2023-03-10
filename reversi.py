'''リバーシテスト'''
import numpy as np
import random

#マスの状態
EMPTY = 0
WHITE = -1
BLACK = 1
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

#入力の表現
INPUT_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
INPUT_NUMBER = ['1', '2', '3', '4', '5', '6', '7', '8']
#手数の上限
MAX_TURNS = 60

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
        self.current_color = BLACK

        self.movable_pos = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        self.movable_dir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)

        self.init_movables()

    def init_movables(self):
        ''' 判定用Listの初期化'''
        self.movable_pos[:, :] = False

        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):
                #各マスに石が置けるかの判定を行い、反映する
                move_dir = self.movable_check(x, y, self.current_color)
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
                move_dir = move_dir | LEFT
                #↑ビット論理和
                #ex.) 0010 | 1000 -> 1010

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
        if self.movable_pos[x_pos, y_pos] == 0:
            return False

        #盤面に反映
        self.flip_stone(x_pos, y_pos)
        #手番を進め、交代する
        self.turn += 1
        self.current_color = -self.current_color
        #探索Listをリセットし、再探索する
        self.init_movables()

        return True

    def flip_stone(self, x_pos, y_pos):
        '''石を置き、盤面に反映する'''
        #指定したマスをそのターンの色にする
        self.board[x_pos, y_pos] = self.current_color

        #指定したマスを格納
        set_dir = self.movable_dir[x_pos, y_pos]

        #石を裏返す処理
        #左(方向にひっくり返せるなら)
        if set_dir & LEFT:
            #↑ビット論理積
            #ex.) 1010 | 1000 -> 1000
            x_check = x_pos - 1

            while self.board[x_check, y_pos] == -self.current_color:
                #相手の石のマスを自分の色に変える
                self.board[x_check, y_pos] = self.current_color
                #探索先のマスを更新する
                x_check -= 1

        #左上
        if set_dir & UPPER_LEFT:
            x_check = x_pos - 1
            y_check = y_pos - 1

            while self.board[x_check, y_check] == -self.current_color:
                self.board[x_check, y_check] = self.current_color
                x_check -= 1
                y_check -= 1

        #上
        if set_dir & UPPER:
            y_check = y_pos - 1

            while self.board[x_pos, y_check] == -self.current_color:
                self.board[x_pos, y_check] = self.current_color
                y_check -= 1

        #右上
        if set_dir & UPPER_RIGHT:
            x_check = x_pos + 1
            y_check = y_pos - 1

            while self.board[x_check, y_check] == -self.current_color:
                self.board[x_check, y_check] = self.current_color
                x_check += 1
                y_check -= 1

        #右
        if set_dir & RIGHT:
            x_check = x_pos + 1

            while self.board[x_check, y_pos] == -self.current_color:
                self.board[x_check, y_pos] = self.current_color
                x_check += 1

        #右下
        if set_dir & LOWER_RIGHT:
            x_check = x_pos + 1
            y_check = y_pos + 1

            while self.board[x_check, y_check] == -self.current_color:
                self.board[x_check, y_check] = self.current_color
                x_check += 1
                y_check += 1

        #下
        if set_dir & LOWER:
            y_check = y_pos + 1

            while self.board[x_pos, y_check] == -self.current_color:
                self.board[x_pos, y_check] = self.current_color
                y_check += 1

        #左下
        if set_dir & LOWER_LEFT:
            x_check = x_pos - 1
            y_check = y_pos + 1

            while self.board[x_check, y_check] == -self.current_color:
                self.board[x_check, y_check] = self.current_color
                x_check -= 1
                y_check += 1

    def is_game_over(self) -> bool:
        '''ゲームの終了判定'''
        #手数が上限に達したらゲームを終了する
        if self.turn >= MAX_TURNS:
            return True

        #まだ打てる手があればゲームを続行する(自分の手番)
        if self.movable_pos[:, :].any():
            return False

        #まだ打てる手があればゲームを続行する(相手の手番)
        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):
                #置ける場所が1つでもあればゲーム続行
                if self.movable_check(x, y, self.current_color) != 0:
                    return False

        return True

    def skip(self) -> bool:
        '''パスの判定'''
        if any(self.movable_pos[:, :]):
            return False

        if self.is_game_over():
            return False

        self.current_color = -self.current_color
        self.init_movables()

        return True

    def display(self):
        '''盤面の表示'''
        #横軸
        print(' a b c d e f g h')

        for y in range(1, 9):
            #縦軸
            print(y, end="")
            for x in range(1, 9):
                grid = self.board[x, y]

                if grid == EMPTY:
                    print('🔳', end='')
                elif grid == WHITE:
                    print('白', end='')
                elif grid == BLACK:
                    print('黒', end='')

            print()

    def check_correct(self, select_pos) -> bool:
        '''入力された手が正しい手かどうか判定する'''
        if not select_pos:
            return False

        if select_pos[0] in INPUT_ALPHABET and select_pos[1] in INPUT_NUMBER:
            return True

        return False

    def random_input(self):
        '''CPU(ランダムに手を打つ)'''
        if instance.skip():
            return False

        grids = np.where(self.movable_pos == 1)

        random_chosen_index = random.randrange(len(grids[0]))
        x_grid = grids[0][random_chosen_index]
        y_grid = grids[1][random_chosen_index]

        return INPUT_ALPHABET[x_grid - 1] + INPUT_NUMBER[y_grid - 1]

#メイン処理
instance = Board()

while True:
    instance.display()

    if instance.current_color == BLACK:
        print('黒のターンです', end='')
    elif instance.current_color == WHITE:
        print('白のターンです', end='')

    get = input()
    print()

    if instance.check_correct(get):
        x = INPUT_ALPHABET.index(get[0]) + 1
        y = INPUT_NUMBER.index(get[1]) + 1
    else:
        print('正しい形式(ex. f5)で入力してください')
        continue

    if not instance.set_stone(x, y):
        print("そこには置けない")
        continue

    if instance.is_game_over():
        instance.display()
        print('ゲーム終了')
        break

    #指す手がなかったらパス
    if not instance.movable_pos[:, :].any():
        instance.current_color = -instance.current_color
        instance.init_movables()
        print('パスした')
        print()
        continue

#ゲーム終了時の判定、表示
print()

count_black = np.count_nonzero(instance.board[:, :] == BLACK)
count_white = np.count_nonzero(instance.board[:, :] == WHITE)

print('黒：', count_black)
print('白：', count_white)

diff = count_black - count_white
if diff > 0:
    print('黒の勝ち')
elif diff < 0:
    print('白の勝ち')
else:
    print('引き分け')

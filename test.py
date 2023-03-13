'''三目並べテスト'''
from enum import Enum, auto
import random
import math

class GameState(Enum):
    '''ゲームの勝敗を管理するためのクラス'''
    #enum.auto() ... enumの定義値を自動で振ってくれる
    DRAW = auto()
    ON = auto()
    OVER = auto()

class Mark(Enum):
    '''盤の印を管理するためのクラス'''
    X = auto()
    O = auto()
    EMPTY = auto()

class Board:
    '''盤の状態全体を管理するクラス'''
    def __init__(self):
        '''盤を初期化するメソッド'''
        self.cell = [[Mark.EMPTY for i in range(3)] for j in range(3)]
        self.is_first_player = True

    def state(self):
        '''現在のゲームの状態（決着がついたか進行中か）を判定するメソッド'''
        #ゲームの決着がついたら
        if self.won():
            return GameState.OVER
        #指せる手がなくなったら
        elif len(self.possible_moves()) == 0:
            return GameState.DRAW
        else:
            return GameState.ON

    def possible_moves(self):
        '''現在置くことができる場所を取得するメソッド'''
        moves = []
        for i in range(3):
            for j in range(3):
                if self.cell[i][j] == Mark.EMPTY:
                    moves.append((i, j))
        return moves

    def make_move(self, move_pos):
        '''指定された場所に印をつけるメソッド'''
        # make a move
        if self.cell[move_pos[0]][move_pos[1]] == Mark.EMPTY:
            if self.is_first_player:
                self.cell[move_pos[0]][move_pos[1]] = Mark.X
            else:
                self.cell[move_pos[0]][move_pos[1]] = Mark.O
            #ターン切り替え
            self.is_first_player = not self.is_first_player

    def won(self):
        '''印が３つそろったかを判定するメソッド'''
        def check_cells(x, y, dx, dy):
            '''指定された場所から指定された方向に3つの印がそろっているかを判定する関数'''
            if self.cell[x][y] == Mark.EMPTY:
                return False
            for i in range(3):
                if self.cell[x][y] != self.cell[x + i * dx][y + i * dy]:
                    return False
            return True

        for i in range(3):
            # 垂直方向にチェック
            if check_cells(i, 0, 0, 1):
                return True
            # 水平方向にチェック
            if check_cells(0, i, 1, 0):
                return True
        # 対角方向にチェック
        if check_cells(0, 0, 1, 1):
            return True
        if check_cells(0, 2, 1, -1):
            return True

    def rewind(self, move_pos):
        '''指定した場所の印を空欄にする（手を巻き戻す）メソッド'''
        # rewind the board
        self.cell[move_pos[0]][move_pos[1]] = Mark.EMPTY
        self.is_first_player = not self.is_first_player

    def __str__(self):
        '''盤面を表示する特殊メソッド'''
        # print(object自身)で呼ばれる
        board_str = ""
        for i in range(3):
            for j in range(3):
                if self.cell[i][j] == Mark.X:
                    board_str += "X"
                elif self.cell[i][j] == Mark.O:
                    board_str += "O"
                else:
                    board_str += "/"
            board_str += "\n"
        return board_str

def mini_max(cur_board):
    '''MiniMaxを再帰的に実行する関数'''
    if cur_board.state() == GameState.DRAW:
        return 0
    elif cur_board.state() == GameState.OVER:
        return -1

    best = -math.inf
    #指すことができる全ての手に対して評価関数を実行する
    for move_c in cur_board.possible_moves():
        cur_board.make_move(move_c)
        get_score = -mini_max(cur_board)
        cur_board.rewind(move_c)

        if get_score > best:
            best = get_score
    return best

board = Board()

while True:
    if board.state() == GameState.OVER or board.state() == GameState.DRAW:
        break

    print('先手' if board.is_first_player else '後手')
    best_score = -math.inf
    best_move = None
    # 先手の場合はmini-max法を用いて最善手を選択する
    if board.is_first_player:
        # 全ての可能な手について評価関数を計算し，最大の評価関数を持つ手を選択する
        move_dict = {}
        for move in board.possible_moves():
            board.make_move(move)
            score = -mini_max(board)
            move_dict[move] = score
            board.rewind(move)
            if score > best_score:
                best_score = score
                best_move = move
        next_move = best_move
        print(move_dict)
    else:
        # 後手の場合はランダムに手を選択する
        next_move = random.choice(board.possible_moves())
    board.make_move(next_move)
    print(board)

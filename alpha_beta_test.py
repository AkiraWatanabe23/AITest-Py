'''αβ法による三目並べのテスト'''
from enum import Enum, auto
import random
import math

class GameState(Enum):
    '''ゲームの勝敗を管理するためのクラス'''
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
        self.cell = [[Mark.EMPTY for _ in range(3)] for _ in range(3)]
        self.is_first_player = True

    def state(self):
        '''現在のゲームの状態（決着がついたか進行中か）を判定するメソッド'''
        if self.won():
            return GameState.OVER
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

    def make_move(self, move):
        '''指定された場所に印をつけるメソッド'''
        if self.cell[move[0]][move[1]] == Mark.EMPTY:
            if self.is_first_player:
                self.cell[move[0]][move[1]] = Mark.X
            else:
                self.cell[move[0]][move[1]] = Mark.O
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
            if check_cells(i, 0, 0, 1):
                return True
            if check_cells(0, i, 1, 0):
                return True
        if check_cells(0, 0, 1, 1):
            return True
        if check_cells(0, 2, 1, -1):
            return True

    def rewind(self, move):
        '''指定した場所の印を空欄にする（手を巻き戻す）メソッド'''
        self.cell[move[0]][move[1]] = Mark.EMPTY
        self.is_first_player = not self.is_first_player

    def __str__(self):
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

def alpha_beta(board, alpha, beta):
    '''αβ法を再帰的に実装するための関数'''
    if board.state() == GameState.DRAW:
        return 0
    elif board.state() == GameState.OVER:
        return -1

    # 現在のノードから選択可能な全ての手について評価関数を計算
    for move in board.possible_moves():
        board.make_move(move)
        # minimax法と同じように、符号を反転させることで最小値計算を省略
        # alphaは自分の最善手の評価値
        # betaは一つ下のノードの最善手の評価値
        # 木が一つ深くなると、alphaとbetaの値が入れ替わる
        score = -alpha_beta(board, alpha=-beta, beta=-alpha)
        if score > alpha:
            alpha = score
        board.rewind(move)

        # alphaよりもbetaが小さいなら、そのノードはalphaよりも大きい値を持つことはないので、
        # 現ノードと並列なノード（同じ親を持つノード）を探索する必要はない
        if alpha >= beta:
            return alpha

    return alpha

board = Board()

while True:
    if board.state() == GameState.OVER or board.state() == GameState.DRAW:
        break

    print("先手" if board.is_first_player else "後手")
    # best_score = -math.inf
    best_move = None
    alpha = -math.inf
    # 先手の場合はalpha-beta法を用いて最善手を選択する
    if board.is_first_player:
        # 全ての可能な手について評価関数を計算し，最大の評価関数を持つ手を選択する
        move_dict = {}
        for move in board.possible_moves():
            board.make_move(move)
            score = -alpha_beta(board, alpha=-math.inf, beta=-alpha)
            move_dict[move] = score
            board.rewind(move)
            if score > alpha:
                best_move = move
                alpha = score
        next_move = best_move
        print(move_dict)
    else:
        # 後手の場合はランダムに手を選択する
        next_move = random.choice(board.possible_moves())
    board.make_move(next_move)
    print(board)

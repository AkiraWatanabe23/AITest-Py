'''「easyAI」使ってみる'''
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

class GameController(TwoPlayerGame):
    '''ゲーム全体の管理'''
    def __init__(self, players):
        self.players = players
        self.n_player = 2
        self.current_player = 1
        self.board = [0] * 9

    def possible_moves(self):
        '''指すことができるマスの列挙'''
        return [a + 1 for a, b in enumerate(self.board) if b == 0]

    def make_move(self, move):
        '''盤面を更新する'''
        self.board[int(move) - 1] = self.n_player

    def loss_game(self):
        '''負け判定'''
        win_comb = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
                    [1, 4, 7], [2, 5, 8], [3, 6, 9],
                    [1, 5, 9], [3, 5, 7]]
        return any([all([(self.board[i-1] == self.opponent) for i in comb]) for comb in win_comb])

    def is_over(self):
        '''ゲームの終了判定'''
        return (self.possible_moves() == []) or self.loss_game()

    def show(self):
        '''盤面の表示'''
        print('\n' + '\n'.join([' '.join([['.', 'o', 'x'][self.board[3*j + i]]
                                          for i in range(3)]) for j in range(3)]))

    def scoring(self):
        '''負けた場合に負けのスコアを返す'''
        return -100 if self.loss_game() else 0

algorithm = Negamax(7)
#↓この部分でエラー出てる
game = GameController([Human_Player(), AI_Player(algorithm)])
game.play()

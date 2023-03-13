'''ひっくり返す数を基にしてマスを決める'''
import reversi

class Pos(reversi.Board):
    '''CPUのマス決定'''
    def decide_pos(self, x_pos, y_pos) -> int:
        '''石を置き、盤面に反映する(盤面の情報を更新するだけ...いくつひっくり返すか等は見ていない)'''
        #指定したマスをそのターンの色にする
        self.board[x_pos, y_pos] = self.current_color
        flip_count = 0

        #指定したマスを格納
        set_dir = self.movable_dir[x_pos, y_pos]

        #石を裏返す処理
        #左(方向にひっくり返せるなら)
        if set_dir & reversi.LEFT:
            #↑ビット論理積
            #ex.) 1010 | 1000 -> 1000
            x_check = x_pos - 1

            while self.board[x_check, y_pos] == -self.current_color:
                #相手の石のマスを自分の色に変える
                self.board[x_check, y_pos] = self.current_color
                #探索先のマスを更新する
                x_check -= 1
                #ひっくり返す数を加算
                flip_count += 1

        #左上
        if set_dir & reversi.UPPER_LEFT:
            x_check = x_pos - 1
            y_check = y_pos - 1

            while self.board[x_check, y_check] == -self.current_color:
                self.board[x_check, y_check] = self.current_color
                x_check -= 1
                y_check -= 1
                flip_count += 1

        #上
        if set_dir & reversi.UPPER:
            y_check = y_pos - 1

            while self.board[x_pos, y_check] == -self.current_color:
                self.board[x_pos, y_check] = self.current_color
                y_check -= 1
                flip_count += 1

        #右上
        if set_dir & reversi.UPPER_RIGHT:
            x_check = x_pos + 1
            y_check = y_pos - 1

            while self.board[x_check, y_check] == -self.current_color:
                self.board[x_check, y_check] = self.current_color
                x_check += 1
                y_check -= 1
                flip_count += 1

        #右
        if set_dir & reversi.RIGHT:
            x_check = x_pos + 1

            while self.board[x_check, y_pos] == -self.current_color:
                self.board[x_check, y_pos] = self.current_color
                x_check += 1
                flip_count += 1

        #右下
        if set_dir & reversi.LOWER_RIGHT:
            x_check = x_pos + 1
            y_check = y_pos + 1

            while self.board[x_check, y_check] == -self.current_color:
                self.board[x_check, y_check] = self.current_color
                x_check += 1
                y_check += 1
                flip_count += 1

        #下
        if set_dir & reversi.LOWER:
            y_check = y_pos + 1

            while self.board[x_pos, y_check] == -self.current_color:
                self.board[x_pos, y_check] = self.current_color
                y_check += 1
                flip_count += 1

        #左下
        if set_dir & reversi.LOWER_LEFT:
            x_check = x_pos - 1
            y_check = y_pos + 1

            while self.board[x_check, y_check] == -self.current_color:
                self.board[x_check, y_check] = self.current_color
                x_check -= 1
                y_check += 1
                flip_count += 1

        return flip_count

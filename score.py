import numpy as np
from math import inf
from board import Board
from tree import TreeNode


class ScoreScheme:
    def __init__(self, scheme, max_depth):
        self.scheme = scheme
        self.max_depth = max_depth

    def score(self, board: Board):
        return self.min_max(board, self.max_depth, True) if self.scheme == 'min_max' \
            else self.min_max(board, self.max_depth, True, -inf, inf)

    def min_max(self, board: Board, depth, player, alpha=None, beta=None):
        if depth == 0:
            h = self.calculate_heuristic(board)
            node = TreeNode(h, None, -1)
            return node
        if player:
            root = self.max_val(board, depth, alpha, beta)
        else:
            root = self.min_val(board, depth, alpha, beta)
        return root

    def max_val(self, board: Board, depth, alpha=None, beta=None):
        val = -inf
        children = []
        branch = -1
        for i in range(7):
            if board.col_pos[i]<0:
                continue
            b = board.clone()
            b.set_piece(i, True)
            children.append(self.min_max(b, depth - 1, False, alpha, beta))
            old = val
            val = max(val, children[-1].value())
            if val != old:
                branch = i
            if alpha is not None and beta is not None:
                if val >= beta:
                    return TreeNode(val, children, branch)
                alpha = max(val, alpha)
        return TreeNode(val, children, branch)

    def min_val(self, board: Board, depth, alpha=None, beta=None):
        val = inf
        children = []
        branch = -1
        for i in range(7):
            if board.col_pos[i]<0:
                continue
            b = board.clone()
            b.set_piece(i, False)
            children.append(self.min_max(b, depth - 1, True, alpha, beta))
            old = val
            val = min(val, children[-1].value())
            if val != old:
                branch = i
            if alpha is not None and beta is not None:
                if val <= alpha:
                    return TreeNode(val, children, branch)
                beta = min(val, beta)
        return TreeNode(val, children, branch)

    def board_conv(self, board: Board):
        # -1 human  1 computer   0 vacant
        b = np.zeros((6,7))
        for i in range(6):
            for j in range(7):
                if i >= 5 - board.col_pos[j]:
                    b[i,j] = 0
                elif board.board[5 - i,j]:
                    b[i,j] = 1
                else:
                    b[i,j] = -1
        b=list(b)
        return b

    def is_avail(self, board, i, j):
        if board[i][j] == 0:
            if (i == 0):
                return True
            if board[i - 1][j] != 0:
                return True
        return False

    def calculate_heuristic(self, board: Board):
        pass
        # (true(human),false(computer))
        # 4 consecutive   580  500
        # 3 that have available place from both sides (ya3ni mn el ne7yetein el le3ba el gaya tekamel 4 )  580,500
        # 3 that can grow from one side or mn el nos  (ya3ni el le3ba el gaya mn ne7ya wa7da tekamel 4)  120,90
        # 3 than we can add in the immediate next column bas msh el mara el gaya 3alatoul  aw 2 w wa7da w makan fadi fel nos 60, 40
        # 2 +surrounding N empty places where N>=2 25+N , 20+N
        score = 0
        b = self.board_conv(board)
        #print(b)
        for i in range(5 - int(np.amin(board.col_pos))):
            start = 0
            flag = 0
            wnds = 4
            while start + 3 < 7 :
                if i<6 and start+3<7 and b[i][start] == 1 and b[i][start + 1] == 1 and b[i][start + 2] == 1 and b[i][start + 3] == 1:
                    score = score + 500
                    flag = 1
                    break
                if i<6 and start+3<7 and b[i][start] == -1 and b[i][start + 1] == -1 and b[i][start + 2] == -1 and b[i][start + 3] == -1:
                    score = score - 580
                    flag = 1
                    break
                if i<6 and start+3<7 and b[i][start] == 1 and (
                        (b[i][start + 1] == 1 and b[i][start + 2] == 0 and self.is_avail(b, i, start + 2)) or (
                        b[i][start + 2] == 1 and b[i][start + 1] == 0 and self.is_avail(b, i, start + 1))) and b[i][
                    start + 3] == 1:
                    score = score + 90
                    start += 2
                if i<6 and start+3<7 and b[i][start] == -1 and (
                        (b[i][start + 1] == -1 and b[i][start + 2] == 0 and self.is_avail(b, i, start + 2)) or (
                        b[i][start + 2] == -1 and b[i][start + 1] == 0 and self.is_avail(b, i, start + 1))) and b[i][
                    start + 3] == -1:
                    score = score - 120
                    start += 2
                if i<6 and start+3<7 and b[i][start] == 1 and (
                        (b[i][start + 1] == 1 and b[i][start + 2] == 0 and not self.is_avail(b, i, start + 2)) or (
                        b[i][start + 2] == 1 and b[i][start + 1] == 0 and not self.is_avail(b, i, start + 1))) and b[i][
                    start + 3] == 1:
                    score = score + 40
                    start += 2
                #print(i,start)
                if i<6 and start+3<7 and  b[i][start] == -1 and (
                        (b[i][start + 1] == -1 and b[i][start + 2] == 0 and not self.is_avail(b, i, start + 2)) or (
                        b[i][start + 2] == -1 and b[i][start + 1] == 0 and not self.is_avail(b, i, start + 1))) and \
                        b[i][start + 3] == -1:
                    score = score - 60
                    start += 2
                else:
                    start = start + 1
            if flag == 1:
                continue

            start = 0
            wnds = 3
            while start + 2 < 7:
                if start+3 < 7 and i<6 and b[i][start] == 1 and b[i][start + 1] == 1 and b[i][start + 2] == 1 and not (
                        (start > 0 and b[i][start - 1] == 1) or (start + 2 != 6 and b[i][start + 3] == 1)):
                    if start > 0 and self.is_avail(b, i, start - 1):
                        if start + 3 < 7 and self.is_avail(b, i, start + 3):
                            score = score + 500
                            start = start + 4
                        else:
                            score = score + 90
                            start = start + 3
                    elif start + 3 < 7 and self.is_avail(b, i, start + 3):
                        score = score + 90
                        start = start + 4
                    elif (start > 0 and b[i][start - 1] == 0) or (start + 3 < 7 and b[i][start + 3] == 0):
                        score = score + 40
                        start = start + 3
                    else:
                        start=start+1
                elif start+3 < 7 and i<6  and b[i][start] == -1 and b[i][start + 1] == -1 and b[i][start + 2] == -1 and not (
                        (start != 0 and b[i][start - 1] == -1) or (start + 2 != 6 and b[i][start + 3] == -1)):
                    if start > 0 and self.is_avail(b, i, start - 1):
                        if start + 3 < 7 and self.is_avail(b, i, start + 3):
                            score = score - 580
                            start = start + 4
                        else:
                            score = score - 120
                            start = start + 3
                    elif start + 3 < 7 and self.is_avail(b, i, start + 3):
                        score = score - 120
                        start = start + 4
                    elif (start > 0 and b[i][start - 1] == 0) or (start + 3 < 7 and b[i][start + 3] == 0):
                        score = score - 60
                        start = start + 3
                    else:
                        start+=1
                else:
                    start = start + 1

            start = 0
            wnds = 2
            while start + 1 < 7:
                if start + 1 < 7 and i<6 and b[i][start] == 1 and b[i][start + 1] == 1 and not (
                        (start - 1 >= 0 and b[i][start - 1] == 1) or (start + 2 <= 6 and b[i][start + 2] == 1)):
                    count = 0
                    j = 1
                    while start - j >= 0 and b[i][start - j] == 0:
                        count += 1
                        j += 1
                    j = 1
                    while start + j + 1 < 7 and b[i][start + 1 + j] == 0:
                        count += 1
                        j += 1
                    if count > 1:
                        score = score + 20 + count
                    start = start + 2
                elif start + 1 < 7 and i<6 and b[i][start] == -1 and b[i][start + 1] == -1 and not ((start - 1 >= 0 and b[i][start - 1] == -1) or (start + 2 <= 6 and b[i][start + 2] == -1)):
                    count = 0
                    j = 1
                    while start - j >= 0 and b[i][start - j] == 0:
                        count += 1
                        j += 1
                    j = 1
                    while start + j + 1 < 7 and b[i][start + 1 +j] == 0:
                        count += 1
                        j += 1
                    if count > 1:
                        score = score - 25 - count
                    start = start + 2
                else:
                    start += 1

        for i in range(7):
            start =(int) (5 - board.col_pos[i]-1)
            if start >= 3:
                if b[start][i] == 1 and b[start - 1][i] == 1 and b[start - 2][i] == 1 and b[start - 3][i] == 1:
                    score += 500
                    continue
                if b[start][i] == -1 and b[start - 1][i] == -1 and b[start - 2][i] == -1 and b[start - 3][i] == -1:
                    score -= 580
                    continue
            if start >= 2:
                if b[start][i] == 1 and b[start - 1][i] == 1 and b[start - 2][i] == 1:
                    score += 90
                    continue
                if b[start][i] == -1 and b[start - 1][i] == -1 and b[start - 2][i] == -1:
                    score -= 120
                    continue
            if start >= 1:
                if b[start][i] == 1 and b[start - 1][i] == 1:
                    score += (20 + board.col_pos[i]+1)
                    continue
                if b[start][i] == -1 and b[start - 1][i] == -1:
                    score -= (25 + board.col_pos[i]+1)
                    continue

        for i in range(7):
            flag = 0
            if i >= 3:
                start = 0
                wnds = 4
                while i - start - 3 >= 0 and start + 3 < 6 and i-start>=0 :
                    if i - start - 3>=0 and start + 3<6 and  b[start][i - start] == 1 and b[start + 1][i - start - 1] == 1 and \
                            b[start + 2][i - start - 2] == 1 and b[start + 3][i - start - 3] == 1:
                        score = score + 500
                        flag = 1
                        break

                    elif i - start - 3>=0 and start + 3<6 and b[start][i - start] == -1 and b[start + 1][i - start - 1] == -1 and b[
                        start + 2][i - start - 2] == -1 and b[start + 3][i - start - 3] == -1:
                        score = score - 580
                        flag = 1
                        break
                    elif i - start - 3>=0 and start + 3<6 and b[start][i - start] == 1 and (
                            (b[start + 1][i - start - 1] == 1 and b[start + 2][i - start - 2] == 0 and self.is_avail(b,start + 2,i - start - 2)) or (
                                    b[start + 2][i - start - 2] == 1 and b[start + 1][
                                i - start - 1] == 0 and self.is_avail(b, start + 1, i - start - 1))) and b[
                        start + 3][i - start - 3] == 1:
                        score = score + 90
                        start += 2
                    elif i - start - 3>=0 and start + 3<6 and b[start][i - start] == -1 and (
                            (b[start + 1][i - start - 1] == -1 and b[start + 2][i - start - 2] == 0 and self.is_avail(b,
                                                                                                                      start + 2,
                                                                                                                      i - start - 2)) or (
                                    b[start + 2][i - start - 2] == -1 and b[start + 1][
                                i - start - 1] == 0 and self.is_avail(b, start + 1, i - start - 1))) and b[
                        start + 3][i - start - 3] == -1:
                        score = score - 120
                        start += 2
                    elif i - start - 3>=0 and start + 3<6 and b[start][i - start] == 1 and (
                            (b[start + 1][i - start - 1] == 1 and b[start + 2][
                                i - start - 2] == 0 and not self.is_avail(b, start + 2, i - start - 2)) or (
                                    b[start + 2][i - start - 2] == 1 and b[start + 1][
                                i - start - 1] == 0 and not self.is_avail(b, start + 1, i - start - 1))) and \
                            b[start + 3][i - start - 3] == 1:
                        score = score + 40
                        start += 2


                    elif i - start - 3>=0 and start + 3<6 and b[start][i - start] == -1 and (
                            (b[start + 1][i - start - 1] == -1 and b[
                                start + 2][i - start - 2] == 0 and not self.is_avail(b, start + 2, i - start - 2)) or (
                                    b[start + 2][i - start - 2] == -1 and b[start + 1][
                                i - start - 1] == 0 and not self.is_avail(b, start + 1, i - start - 1))) and \
                            b[start + 3][i - start - 3] == -1:
                        score = score - 60
                        start += 2
                    else:
                        start += 1
                if flag != 1:
                    start = 0
                    wnds = 3
                    while i - start - 2 >= 0 and start + 2 < 6:
                        if i - start - 2>=0 and start + 2<6 and b[start][i - start] == 1 and b[start + 1][i - start - 1] == 1 and b[start + 2][
                            i - start - 2] == 1:
                            if start - 1 >= 0 and i - start + 1 <= 6 and b[start - 1][
                                i - start + 1] == 0 and self.is_avail(b, start - 1, i - start + 1):
                                if i - start - 3 >= 0 and start + 3 <= 5 and b[start + 3][
                                    i - start - 3] == 0 and self.is_avail(b, start + 3, i - start - 3):
                                    score += 500
                                    start += 4
                                else:
                                    score += 90
                                    start += 3
                            elif i - start - 3 >= 0 and start + 3 <= 5 and b[start + 3][
                                i - start - 3] == 0 and self.is_avail(b, start + 3, i - start - 3):
                                score += 90
                                start += 4
                            elif (start - 1 >= 0 and i - start + 1 <= 6 and b[start - 1][i - start + 1] == 0) or (
                                    i - start - 3 >= 0 and start + 3 <= 5 and b[start + 3][i - start - 3] == 0):
                                score += 40
                                start += 3
                            else:
                                 start+=1
                        elif i - start - 2>=0 and start + 2<6 and b[start][i - start] == -1 and b[start + 1][i - start - 1] == -1 and b[start + 2][
                            i - start - 2] == -1:
                            if start - 1 >= 0 and i - start + 1 <= 6 and b[start - 1][
                                i - start + 1] == 0 and self.is_avail(b, start - 1, i - start + 1):
                                if i - start - 3 >= 0 and start + 3 <= 5 and b[start + 3][
                                    i - start - 3] == 0 and self.is_avail(b, start + 3, i - start - 3):
                                    score -= 580
                                    start += 4
                                else:
                                    score -= 120
                                    start += 3
                            elif i - start - 3 >= 0 and start + 3 <= 5 and b[start + 3][
                                i - start - 3] == 0 and self.is_avail(b, start + 3, i - start - 3):
                                score -= 120
                                start += 4
                            elif (start - 1 >= 0 and i - start + 1 <= 6 and b[start - 1][i - start + 1] == 0) or (
                                    i - start - 3 >= 0 and start + 3 <= 5 and b[start + 3][i - start - 3] == 0):
                                score -= 60
                                start += 3
                            else:
                                start+=1
                        else:
                            start+=1
                    start = 0
                    wnds = 2
                    while i - start - 1 >= 0 and start+1<6:
                        if i - start - 1<=0 and start+1<6 and b[start][i - start] == 1 and b[start+1][i - start - 1] == 1 and not (
                                (start > 0 and b[start - 1][i - start + 1] == 1) or (
                                start + 2 <= 5 and b[start + 2][i - start - 2] == 1)):
                            count = 0
                            j = 1
                            while i - start + j <= 6 and start - j >= 0 and b[start - j][i - start + j] == 0:
                                count += 1
                                j += 1
                            j = 1
                            while start + 1 + j < 6 and i - start - 1 - j >= 0 and b[start + 1 + j][
                                i - start - 1 - j] == 0:
                                count += 1
                                j += 1
                            if count > 1:
                                score = score + 20 + count
                            start = start + 2
                        elif i - start - 1<=0 and start+1<6 and  b[start][i - start] == -1 and b[start+1][i - start - 1] == -1 and not (
                                (start > 0 and b[start - 1][i - start + 1] == -1) or (
                                start + 2 <= 5 and b[start + 2][i - start - 2] == -1)):
                            count = 0
                            j = 1
                            while i - start + j <= 6 and start - j >= 0 and b[start - j][i - start + j] == 0:
                                count += 1
                                j += 1
                            j = 1
                            while start + 1 + j < 6 and i - start - 1 - j >= 0 and b[start + 1 + j][
                                i - start - 1 - j] == 0:
                                count += 1
                                j += 1
                            if count > 1:
                                score = score - 25 - count
                            start = start + 2
                        else:
                            start += 1

            if i <= 3:
                start = 0
                wnds = 4
                while i + start + 3 <= 6 and start + 3 < 6:
                    if i + start + 3<7 and start + 3<6 and b[start][i + start] == 1 and b[start + 1][i + start + 1] == 1 and b[start + 2][
                        i + start + 2] == 1 and b[start + 3][i + start + 3] == 1:
                        score = score + 500
                        flag = 1
                        break

                    elif i + start + 3<7 and start + 3<6 and b[start][i + start] == -1 and b[start + 1][i + start + 1] == -1 and b[
                        start + 2][i + start + 2] == -1 and b[start + 3][i + start + 3] == -1:
                        score = score - 580
                        flag = 1
                        break
                    elif i + start + 3<7 and start + 3<6 and b[start][i + start] == 1 and (
                            (b[start + 1][i + start + 1] == 1 and b[start + 2][i + start + 2] == 0 and self.is_avail(b,
                                                                                                                     start + 2,
                                                                                                                     i + start + 2)) or (
                                    b[start + 2][i + start + 2] == 1 and b[start + 1][
                                i + start + 1] == 0 and self.is_avail(b, start + 1, i + start + 1))) and b[
                        start + 3][i + start + 3] == 1:
                        score = score + 90
                        start += 2
                    elif i + start + 3<7 and start + 3<6 and b[start][i - start] == -1 and (
                            (b[start + 1][i + start + 1] == -1 and b[start + 2][i + start + 2] == 0 and self.is_avail(b,
                                                                                                                      start + 2,
                                                                                                                      i + start + 2)) or (
                                    b[start + 2][i + start + 2] == -1 and b[start + 1][
                                i + start + 1] == 0 and self.is_avail(b, start + 1, i + start + 1))) and b[
                        start + 3][i + start + 3] == -1:
                        score = score - 120
                        start += 2
                    elif i + start + 3<7 and start + 3<6 and b[start][i + start] == 1 and (
                            (b[start + 1][i + start + 1] == 1 and b[start + 2][
                                i + start + 2] == 0 and not self.is_avail(b, start + 2, i + start + 2)) or (
                                    b[start + 2][i + start + 2] == 1 and b[start + 1][
                                i + start + 1] == 0 and not self.is_avail(b, start + 1, i + start + 1))) and \
                            b[start + 3][i + start + 3] == 1:
                        score = score + 40
                        start += 2


                    elif i + start + 3<7 and start + 3<6 and b[start][i - start] == -1 and (
                            (b[start + 1][i + start + 1] == -1 and b[
                                start + 2][i + start + 2] == 0 and not self.is_avail(b, start + 2, i + start + 2)) or (
                                    b[start + 2][i + start + 2] == -1 and b[start + 1][
                                i + start + 1] == 0 and not self.is_avail(b, start + 1, i + start + 1))) and \
                            b[start + 3][i + start + 3] == -1:
                        score = score - 60
                        start += 2
                    else:
                        start += 1
                if flag != 1:
                    start = 0
                    wnds = 3
                    while i + start + 2 <= 6 and start + 2 < 6:
                        if i + start + 2<7 and start + 2<6 and b[start][i + start] == 1 and b[start + 1][i + start + 1] == 1 and b[start + 2][
                            i + start + 2] == 1:
                            if start - 1 >= 0 and i + start - 1 >= 0 and b[start - 1][
                                i + start - 1] == 0 and self.is_avail(b, start - 1, i + start - 1):
                                if i + start + 3 <7 and start + 3 <6 and b[start + 3][
                                    i + start + 3] == 0 and self.is_avail(b, start + 3, i + start + 3):
                                    score += 500
                                    start += 4
                                else:
                                    score += 90
                                    start += 3
                            elif i + start + 3 <7 and start + 3 <6 and b[start + 3][
                                i + start + 3] == 0 and self.is_avail(b, start + 3, i + start + 3):
                                score += 90
                                start += 4
                            elif (start - 1 >= 0 and i + start - 1 >= 0 and b[start - 1][i + start - 1] == 0) or (
                                    i + start + 3 <7 and start + 3 <6 and b[start + 3][i + start + 3] == 0):
                                score += 40
                                start += 3
                            # else:
                            #     start += 1
                        if i + start + 2<7 and start + 2<6 and  b[start][i + start] == -1 and b[start + 1][i + start + 1] == -1 and b[start + 2][
                            i + start + 2] == -1:
                            if start - 1 >= 0 and i + start - 1 >= 0 and b[start - 1][
                                i + start - 1] == 0 and self.is_avail(b, start - 1, i + start - 1):
                                if i + start + 3 <= 6 and start + 3 <= 5 and b[start + 3][
                                    i + start + 3] == 0 and self.is_avail(b, start + 3, i + start + 3):
                                    score -= 580
                                    start += 4
                                else:
                                    score -= 120
                                    start += 3
                            elif i + start + 3 <= 6 and start + 3 <= 5 and b[start + 3][
                                i + start + 3] == 0 and self.is_avail(b, start + 3, i + start + 3):
                                score -= 120
                                start += 4
                            elif (start - 1 >= 0 and i + start - 1 >= 0 and b[start - 1][i + start - 1] == 0) or (
                                    i + start + 3 <= 6 and start + 3 <= 5 and b[start + 3][i + start + 3] == 0):
                                score -= 60
                                start += 3
                            else:
                                start += 1
                        else:
                            start+=1
                    start = 0
                    wnds = 2
                    while i + start + 1 <= 6:
                        if i + start + 1<7 and start+1<6 and b[start][i + start] == 1 and b[start+1][i + start + 1] == 1 and not (
                                (start > 0 and i + start - 1 >= 0 and b[start - 1][i + start - 1] == 1) or (
                                start + 2 <= 5 and i + start + 2 <= 6 and b[start + 2][i + start + 2] == 1)):
                            count = 0
                            j = 1
                            while i + start - j >= 0 and start - j >= 0 and b[start - j][i + start - j] == 0:
                                count += 1
                                j += 1
                            j = 1
                            while start + 1 + j < 6 and i + start + 1 + j <= 6 and b[start + 1 + j][
                                i + start + 1 + j] == 0:
                                count += 1
                                j += 1
                            if count > 1:
                                score = score + 20 + count
                            start = start + 2
                        elif i + start + 1<7 and start+1<6 and b[start][i + start] == -1 and b[start+1][i + start + 1] == -1 and not (
                                (start > 0 and i + start - 1 >= 0 and b[start - 1][i + start - 1] == -1) or (
                                start + 2 <= 5 and i + start + 2 <= 6 and b[start + 2][i + start + 2] == -1)):
                            count = 0
                            j = 1
                            while i + start - j >= 0 and start - j >= 0 and b[start - j][i + start - j] == 0:
                                count += 1
                                j += 1
                            j = 1
                            while start + 1 + j < 6 and i + start + 1 + j <= 6 and b[start + 1 + j][
                                i + start + 1 + j] == 0:
                                count += 1
                                j += 1
                            if count > 1:
                                score = score - 25 - count
                            start = start + 2
                        else:
                            start += 1
        ones_matrix = [[3, 4, 5, 7, 5, 4, 3],
                       [4, 6, 8, 10, 8, 6, 4],
                       [5, 8, 11, 13, 11, 8, 5],
                       [5, 8, 11, 13, 11, 8, 5],
                       [4, 6, 8, 10, 8, 6, 4],
                       [3, 4, 5, 7, 5, 4, 3]]
        for i in range(6):
            for j in range(7):
                if b[i][j]==-1:
                    score+=1.5*ones_matrix[i][j] * b[i][j]
                else:
                    score += ones_matrix[i][j] * b[i][j]
        #print(score)
        return score

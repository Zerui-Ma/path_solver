#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: mazr

from __future__ import print_function

import sys

if sys.version[0] == '3':
    from tkinter import StringVar, Tk, ttk

else:
    import ttk
    from Tkinter import StringVar, Tk


def dfs(data, row, i, ways):
        data[row][i] = 3     # 3 表示该单元格已经通过

        if row + 1 < len(data) and data[row + 1][i] == 1:
            if not dfs(data, row + 1, i, ways):
                data[row + 1][i] = 1

        if row - 1 > -1 and data[row - 1][i] == 1:
            if not dfs(data, row - 1, i, ways):
                data[row - 1][i] = 1

        if i + 1 < len(data[0]) and data[row][i + 1] == 1:
            if not dfs(data, row, i + 1, ways):
                data[row][i + 1] = 1

        if i - 1 > -1 and data[row][i - 1] == 1:
            if not dfs(data, row, i - 1, ways):
                data[row][i - 1] = 1
        for single_row in data:
            for block in single_row:
                if(block == 1):
                    return False

        ways.append((row, i))
        return True


class PathSolver():
    def __init__(self, dimension):
        self.dimension = dimension
        self.x_y_list = None


    def print_path(self, ways):
        horizontals = []
        verticals = []
        blocks = []
        for _ in range(self.dimension):
            horizontals.append(['   ' for _ in range(self.dimension - 1)])
        for _ in range(self.dimension - 1):
            verticals.append([' ' for _ in range(self.dimension)])
        for _ in range(self.dimension):
            blocks.append(['x' for _ in range(self.dimension)])

        for i in range(len(ways) - 1):
            x_cur = ways[i][0]
            y_cur = ways[i][1]
            x_nxt = ways[i + 1][0]
            y_nxt = ways[i + 1][1]

            blocks[x_cur][y_cur] = 'o'
            # Up
            if x_nxt < x_cur and y_nxt == y_cur:
                verticals[x_nxt][y_nxt] = '|'
            # Left
            if x_nxt == x_cur and y_nxt < y_cur:
                horizontals[x_nxt][y_nxt] = ' = '
            # Down
            if x_nxt > x_cur and y_nxt == y_cur:
                verticals[x_cur][y_nxt] = '|'
            # Right
            if x_nxt == x_cur and y_nxt > y_cur:
                horizontals[x_nxt][y_cur] = ' = '

        blocks[ways[-1][0]][ways[-1][1]] = 's'
        path = ''
        for j in range(self.dimension):
            block_row = blocks[j]
            horizontal_row = horizontals[j]
            horizontal_row.append('\n')
            for k in range(self.dimension):
                path += block_row[k] + horizontal_row[k]

            if j != self.dimension - 1:
                vertical_row = verticals[j]
                path += '   '.join(vertical_row) + '\n'

        print(path)
        sys.stdout.flush()


    def show_path(self):
        '''
        0 表示起点
        1 表示需要通过的单元格
        2 表示不需要通过的单元格
        '''
        data = []
        row = [2 for _ in range(self.dimension)]
        for i in range(self.dimension):
            data.append(row[:])

        for x_y in self.x_y_list:
            if x_y.get() != '':
                val, x, y = x_y.get().split()
                x = int(x)
                y = int(y)
                if val == 'S':
                    data[x][y] = 0
                elif val == 'N':
                    data[x][y] = 1

        ways = []
        for row in data:
            for i in row:
                if i == 0:
                    dfs(data, data.index(row), row.index(i), ways)

        if ways:
            print('Found a path successfully:\n')
            self.print_path(ways)
        else:
            print('Unable to find a path.\n')
            sys.stdout.flush()


    def run_solver(self):
        root = Tk()
        root.title('Path Solver v1.0')
        frame = ttk.Frame(root)
        frame['padding'] = (5, 10)
        frame.grid(sticky='ns')

        self.x_y_list = []
        for i in range(self.dimension):
            for j in range(self.dimension):
                x_y = StringVar()
                coordinate = '{} {}'.format(str(i), str(j))
                check = ttk.Checkbutton(frame, variable=x_y,
                                        onvalue='N ' + coordinate,
                                        offvalue='S ' + coordinate)
                check.state(['alternate'])
                check.grid(row=i, column=j)
                self.x_y_list.append(x_y)

        button = ttk.Button(root, text='Solve', command=self.show_path)
        button.grid()

        root.mainloop()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python path_solver.py [dimension]')
        sys.exit(1)
    else:
        dimension = sys.argv[1]
        if not dimension.isdigit() or int(dimension) <= 0:
            print('[dimension] has to be a integer greater than zero.')
            sys.exit(1)
        else:
            print('\n')
            print('++++++++++++++++++++++++++++++++++++++')
            print('+          Path Solver v1.0          +')
            print('++++++++++++++++++++++++++++++++++++++')
            print('\n')
            path_solver = PathSolver(int(dimension))
            path_solver.run_solver()

import termcolor
import sys
import random
import itertools

from cell import Cell

class Board:
    def __init__(self, height, width, num_mines):
        self.height = height
        self.width = width
        self.num_mines = num_mines
        self.flags_left = num_mines
        self.mine_coords = self.init_mines() # (row, col) tuples
        self.board = self.init_board() # maps (row, col) tuples -> Cell objs
        #TODO: implement a timer for scoring purposes

    def print_board(self):
        # Print column numbering
        edge = '#'
        print '    ',
        for c in range(1, self.width + 1):
            col_num = '%2d' % c
            if c % 2:
                col_num = termcolor.colored(col_num, 'yellow')
            else:
                col_num = termcolor.colored(col_num, 'blue')
            sys.stdout.write(col_num)
        print

        # Print edge line below column numbering
        print '  ',
        for i in range(self.width + 2):
            print edge,
        print

        # Print cells with padding on ends and row numbering at beginning
        old_r = -1
        for (r, c) in sorted(self.board):
            if old_r != r:
                old_r = r
                row_num = '%2d' % (r + 1)
                if r % 2:
                    row_num = termcolor.colored(row_num, 'blue')
                else:
                    row_num = termcolor.colored(row_num, 'yellow')
                print row_num,
                print edge,
            print self.board[(r, c)],
            if (c + 1) % self.width == 0:
                print edge,
                print

        # Print bottom edge line
        print ' ',
        for i in range(self.width + 2):
            print edge,
        print

    def player_won(self):
        won = True
        not_mines = set(self.board) - set(self.mine_coords)
        for coord in self.mine_coords:
            won = won and self.board[coord].is_flagged
        for coord in not_mines:
            won = won and not self.board[coord].is_covered
        return won

    def get_adj_coords(self, coord):
        row, col = coord
        close_rows = range(row-1, row+2)
        close_cols = range(col-1, col+2)
        adj_coords = itertools.product(close_rows, close_cols)
        return [adj_coord for adj_coord in adj_coords if self.valid_coord(adj_coord)]

    def valid_coord(self, coord):
        row, col = coord
        return row >= 0 and col >= 0 and row < self.height and col < self.width

    def count_adj_mines(self, coord):
        if coord in self.mine_coords:
            return -1
        adj_cells = self.get_adj_coords(coord)
        adj_mines = [c for c in adj_cells if c in self.mine_coords] 
        return len(adj_mines)

    def init_board(self):
        rows = range(self.height)
        cols = range(self.width)
        coords = itertools.product(rows, cols)
        return {coord: Cell(coord in self.mine_coords, self.count_adj_mines(coord)) for coord in coords}

    def init_mines(self):
        mines = set() 
        while len(mines) < self.num_mines:
            row = random.randrange(self.height)
            col = random.randrange(self.width)
            mine = (row, col)
            mines.add(mine)
        return mines

    def uncover_cell(self, coord, seen):
        seen.append(coord)
        try:
            cell = self.board[coord]
        except KeyError:
            return
        cell.is_covered = False
        if cell.adj_mines == 0:
            for adj_coord in self.get_adj_coords(coord):
                if adj_coord not in seen:
                    self.uncover_cell(adj_coord, seen)
        return cell

    def toggle_cell_flag(self, coord):
        cell = self.board[coord]
        self.board[coord].is_flagged = not self.board[coord].is_flagged
        if self.board[coord].is_flagged:
            self.flags_left += 1
        else:
            self.flags_left += -1

    def game_over(self):
        for coord in self.mine_coords:
            self.board[coord].is_covered = False

if __name__ == '__main__':
    print 'Welcome to Minesweeper!'
    height = int(raw_input('Please enter the desired board height: '))
    width = int(raw_input('Please enter the desired board width: '))
    while True:
        mines = int(raw_input('Please enter the desired amount of mines: '))
        if mines <= width * height:
            break
        print "Your board isn't big enough for that many mines!"

    ms = Board(height, width, mines)

    lost = False
    won = False
    ms.print_board()
    while not lost and not won:
        print 'Please choose a cell to uncover or flag:'
        r = int(raw_input('Row: ')) - 1
        c = int(raw_input('Col: ')) - 1
        coord = (r, c)
        while True:
            action = int(raw_input('Uncover (1) or flag (2)?: '))
            if action == 1:
                cell = ms.uncover_cell(coord, [])
                won = ms.player_won()
                lost = cell.is_mine
                if lost:
                    cell.is_lethal = True
                    ms.game_over()
                break
            elif action == 2:
                ms.toggle_cell_flag(coord)
                break
            else:
                print "I didn't quite get that. Try again"
        ms.print_board()

    if won:
        print 'Congrats! You won!'
    elif lost:
        print 'You lost :('

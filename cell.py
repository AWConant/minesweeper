import termcolor

class Cell:
    def __init__(self, is_mine, adj_mines):
        self.is_covered = True
        self.is_lethal = False
        self.is_flagged = False
        self.is_mine = is_mine
        self.adj_mines = adj_mines
        self.mine_colors = {1 : 'blue',
                            2 : 'green',
                            3 : 'red',
                            4 : 'magenta',
                            5 : 'yellow',
                            6 : 'cyan',
                            7 : 'grey',
                            8 : 'white',
                            9 : 'white'}

    def __repr__(self):
        if self.is_flagged:
            s = 'F'
        elif self.is_covered:
            s = '.'
        elif self.is_mine:
            if self.is_lethal:
                s = termcolor.colored('*', 'white', 'on_red')
            else:
                s = '*'
        elif self.adj_mines == 0:
            s = ' '
        else:
            color = self.mine_colors[self.adj_mines]
            s = termcolor.colored(str(self.adj_mines), color) 
        return s

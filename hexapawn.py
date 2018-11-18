import utility_methods as util
import sys

# player notation:
#  -1 -> White
#   1 -> Black

initial_board = [
    ['W', 'W', 'W'],
    ['0', 'B', '0'],
    ['B', '0', 'B']
]


class node:
    def __init__(self, i_depth,  board, player, value=0):
        self.depth = i_depth
        self.board = board
        self.player = player
        self.value = value
        self.children = []
        self.create_children()

    def get_value(self):
        return self.value

    def get_player(self):
        if self.player == 1:
            return 'B'
        return 'W'

    def create_children(self):
        # check for depth here when iterative deepening
        possible_move = util.generate_move(self.board, self.get_player())
        if not possible_move:
            return
        # for a_board in possible_move:
        #     temp_node =

    def check_score(self):
        # if Black player
        if self.player == 1:
            for pawn in self.board[0]:
                if pawn == self.get_player():
                    self.value = self.player * sys.maxint
                    return
            score = (len(util.get_positions(self.board, 'B')) - (len(util.get_positions(self.board, 'W'))))
            # leaf node and game is tied
            if score == 0 and not self.children:
                self.value = self.player * sys.maxint
            else:
                self.value = score

        # White Player's turn
        else:
            for pawn in self.board[len(self.board) - 1]:
                if pawn == self.get_player():
                    self.value = self.player * sys.maxint
                    return
            score = (len(util.get_positions(self.board, 'W')) - (len(util.get_positions(self.board, 'B'))))
            score = score * self.player
            # leaf node and game is tied
            if score == 0 and not self.children:
                self.value = self.player * sys.maxint
            else:
                self.value = score


root = node(0, initial_board, -1)
root.check_score()
print(root.get_value())
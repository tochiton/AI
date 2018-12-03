import utility_methods as util
from sys import maxint

# player notation:
#  -1 -> White is negative value
#   1 -> Black is positive value

initial_board = [
    ['W', 'W', 'W'],
    ['0', 'B', '0'],
    ['B', '0', 'B']
]


class Node:
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

    def get_board(self):
        return self.board

    def display_board(self):
        for row in self.board:
            for elem in row:
                print elem,
            print("\n")
            print("---------------")

    def get_best_move(self):
        if not self.children:
            print self.get_value()
            print("no children - just myself")
            return self.board
        temp_score = -self.player * maxint
        if len(self.children) == 1:
            return self.get_value()
            print("only one children")
            return self.children[0].get_board()
        temp_board = []
        for child in self.children:
            local_score = child.get_best_score()
            if local_score > temp_score:
                temp_board.insert(0, child.get_board())
                print(child.get_value())

        if not temp_board:
            return [[]]
        return temp_board[0]

    def get_best_score(self):
        if not self.children:
            return self.value
        highest_score = -self.player * maxint
        for child in self.children:
            local_score = child.get_best_score()
            if local_score > highest_score:
                highest_score = local_score
        return highest_score


    def display_states(self, level):
        self.display_board()
        # if self.value != 0:
        #     print("Level: ", level, self.value)
        #     print(len(self.children))
        # print("******* Children ********")
        # print("Level {}".format(level))
        for a_node in self.children:
            a_node.display_board()
        for a_node in self.children:
            a_node.display_states(level + 1)

    def create_children(self):
        # check for depth here when iterative deepening
        possible_move = util.generate_move(self.board, self.get_player())
        if not possible_move:
            self.set_score()
            return
        else:
            for a_board in possible_move:
                temp_node = Node(0, a_board, -self.player, 0)
                self.children.append(temp_node)

    def set_score(self):
        # if Black player
        if self.player == 1:
            for pawn in self.board[0]:
                if pawn == self.get_player():
                    self.value = self.player * maxint
                    return
            num_black_pawn = len(util.get_positions(self.board, 'B'))
            num_white_pawn = len(util.get_positions(self.board, 'W'))
            if num_white_pawn == 0:
                self.value = self.player * maxint
                return
            score = num_black_pawn - num_white_pawn
            # leaf node and game is tied
            if score == 0 and not self.children:
                self.value = self.player * maxint
            else:
                self.value = score

        # White Player's turn
        else:
            for pawn in self.board[len(self.board) - 1]:
                if pawn == self.get_player():
                    self.value = self.player * maxint
                    return
            num_white_pawn = len(util.get_positions(self.board, 'W'))
            num_black_pawn = len(util.get_positions(self.board, 'B'))
            if num_black_pawn == 0:
                self.value = self.player * maxint
                return
            score = num_white_pawn - num_black_pawn
            score = score * self.player
            # leaf node and game is tied
            if score == 0 and not self.children:
                self.value = self.player * maxint
            else:
                self.value = score


# root = Node(0, initial_board, 1)
# my_board = root.get_best_move()
# util.print_twod_array(my_board)
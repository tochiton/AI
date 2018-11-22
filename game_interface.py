from hexapawn import Node
import utility_methods as util

game_board = [
    ['W', 'W', '0'],
    ['B', 'B', 'W'],
    ['0', '0', 'B']
]


def check_winner(board, player):
    if player == 'W':
        a_list = board[len(board) - 1]
        for elem in a_list:
            if elem == player:
                return True
        return False
    elif player == 'B':
        a_list = board[0]
        for elem in a_list:
            if elem == player:
                return True
        return False


while True:
    util.print_twod_array(game_board)
    move = raw_input("Make move from to: ")
    old_row, old_col = int(move[0]), int(move[1])
    new_row, new_col = int(move[3]), int(move[4])
    # print old_row, old_col
    # print new_row, new_col
    game_board[old_row][old_col] = 0
    game_board[new_row][new_col] = 'W'
    if check_winner(game_board, 'W'):
        print("I won")
        break
    temp_node = Node(0, game_board, 1, 0)
    game_board = temp_node.get_best_move()
    if check_winner(game_board, 'B'):
        print("Game over")
        util.print_twod_array(game_board)
        break

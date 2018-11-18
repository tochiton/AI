import copy


def print_twod_array(twoDarray):
    for row in twoDarray:
        for elem in row:
            print elem,
        print("\n")


def get_positions(board, player):
    list_of_coordinates = []
    for index_row in range(len(board)):
        for index_col in range(len(board)):
            if board[index_row][index_col] == player:
                list_of_coordinates.append((index_row, index_col))
    return list_of_coordinates


def generate_move(board, player):
    list_of_moves = []
    list_of_coordinates = get_positions(board, player)
    for coordinate in list_of_coordinates:
        temp_list = move(board, coordinate[0], coordinate[1])
        for a_board in temp_list:
            list_of_moves.append(a_board)

    return list_of_moves


def valid_position(length, row, col):
    if row >= 0 and row < length and col >= 0 and col < length:
        return True
    return False


def move(board, row, col):
    list_of_move = []
    length = len(board)
    if board[row][col] == 'B':
        move_up_row = row - 1
        if valid_position(length, move_up_row, col) and board[move_up_row][col] == '0':
            new_board = copy.deepcopy(board)
            new_board[row][col] = '0'
            new_board[move_up_row][col] = 'B'
            list_of_move.insert(0, new_board)
        diagonal_left_row = row - 1
        diagonal_left_col = col - 1
        if valid_position(length, diagonal_left_row, diagonal_left_col) \
                and board[diagonal_left_row][diagonal_left_col] == 'W':
            new_board = copy.deepcopy(board)
            new_board[row][col] = '0'
            new_board[diagonal_left_row][diagonal_left_col] = 'B'
            list_of_move.insert(0, new_board)

        diagonal_right_row = row - 1
        diagonal_right_col = col + 1
        if valid_position(length, diagonal_right_row, diagonal_right_col) \
                and board[diagonal_right_row][diagonal_right_col] == 'W':
            new_board = copy.deepcopy(board)
            new_board[row][col] = '0'
            new_board[diagonal_right_row][diagonal_right_col] = 'B'
            list_of_move.insert(0, new_board)
        return list_of_move
    else:
        move_down_row = row + 1
        if valid_position(length, move_down_row, col) and board[move_down_row][col] == '0':
            new_board = copy.deepcopy(board)
            new_board[row][col] = '0'
            new_board[move_down_row][col] = 'W'
            list_of_move.insert(0, new_board)
        diagonal_left_row = row + 1
        diagonal_left_col = col - 1
        if valid_position(length, diagonal_left_row, diagonal_left_col) \
                and board[diagonal_left_row][diagonal_left_col] == 'B':
            new_board = copy.deepcopy(board)
            new_board[row][col] = '0'
            new_board[diagonal_left_row][diagonal_left_col] = 'W'
            list_of_move.insert(0, new_board)

        diagonal_right_row = row + 1
        diagonal_right_col = col + 1
        if valid_position(length, diagonal_right_row, diagonal_right_col) \
                and board[diagonal_right_row][diagonal_right_col] == 'B':
            new_board = copy.deepcopy(board)
            new_board[row][col] = '0'
            new_board[diagonal_right_row][diagonal_right_col] = 'W'
            list_of_move.insert(0, new_board)
        return list_of_move
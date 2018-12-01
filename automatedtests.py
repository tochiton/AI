from __future__ import print_function
import copy
import time


##CS441/541
##tested on 2.7

##utility function to print 2d array
def print_twod_array(playboard):
  for x in playboard:
   print(*x, sep=" ")

##utility function to get all the current coordinates of the player's pawns
##returns a list of coordinates of player's pawns to be used in the
##generate_move function.
def get_positions(board, player):
  list_of_coordinates = []
  for index_row in range(len(board)):
      for index_col in range(len(board)):
          if board[index_row][index_col] == player:
              list_of_coordinates.append((index_row, index_col))
  return list_of_coordinates

##This utility function will return all the valid board states that can be
##made from a player's move.
##returns a list of moves that is used when generating the children
##this function will essentially call the move function on all the player'
##pawns in order to generate all the move possibilities.
def generate_move(board, player):
  list_of_coordinates = []
  list_of_moves = []
  list_of_coordinates = get_positions(board,player)
  for coordinate in list_of_coordinates:
      temp_list = move(board,coordinate[0],coordinate[1])
      for a_board in temp_list:
          list_of_moves.append(a_board)

  return list_of_moves

##This is a utility function that will check if a pawn is moving out of bounds
def valid_position(length, row, col):
  if row >= 0 and row < length and col >= 0 and col < length:
      return True
  return False

##This is a utility function that will actually move the player's pawn in all
##its possibilities and return the list of board states that are a result of
##that pawn moving.
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

##this is a utility function that is used to calculate the static evaluation
##values (heuristic) for node boards that aren't at their end state but at
##the end of the depth cutoff. The function is as follows: add 1 for every
##black pawn and another 1 if that black pawn has a clear path directly in front.
##subtract 1 for every white pawn and another 1 subtracted if that white pawn
##has a clear path directly in front.
def difference(board):
 count = 0
 for row in range(len(board)):
     for col in range(len(board)):
       if board[row][col] == 'B':
         count += 1
         if valid_position(len(board), row - 1, col) == True and board[row-1][col] == '0':
           count += 1
       elif board[row][col] == 'W':
         count -= 1
         if valid_position(len(board), row + 1, col) == True and board[row+1][col] == '0':
           count -= 1
 return count

##this is a utility function to check if a board is at an end state. if
##black wins then award +10, if white wins then award -10.
def end_state(pmove,player):
   if player == 'B':
       ##if black can't make any valid moves then its a loss.
       if not generate_move(pmove,player):
           return -10
       ##if there is a white pawn at the end of board, black losses.
       for i in range(0,len(pmove)):
           if pmove[(len(pmove)-1)][i] == 'W':
               return -10
   else:
       if not generate_move(pmove,player):
           return 10
       for i in range(0,len(pmove)):
           if pmove[0][i] == 'B':
               return 10
   return 0

##this is a utility function to convert a string input from user into a
##2d array.
def parsing(player_input):
   final = []
   my_list = []
   my_string = player_input
   my_list = my_string.split(';')
  
   for elem in my_list:
       temp = elem.split(',')
       final.append(temp)
      
   return final

##this is the node class that will hold all the necessary information to
##expand out a minimax tree.
class Node(object):
  def __init__(self, depth, player, board, value):
    self.depth = depth   ##this is the current depth of the node
    self.player = player ##this is the current player's turn 'B' or 'W'
    self.board = board   ##this is a 2d array representing the current board
    self.value = value   ##this is the minimax value of the node
    self.children = []   ##this is the array of nodes representing children
    self.createchildren()    ##function to generate children
  ##this function will create children by recieving all the possible moves that
  ##can be made by the player's pawns (using the generate_move function) and then
  ##loading the information into children. Notice the createchildren function
  ##is in the constructor of the node class and therefore children will be made
  ##in this recursive manner.
  def createchildren(self):
    ##stopping condition is if we are at the max depth or if a node is a final state.    
    if self.depth > 0 and abs(self.value) != 10:
      list_moves = generate_move(self.board, self.player)
      for moves in list_moves:
        if self.player == 'B':
          self.children.append(Node(self.depth-1, 'W', moves, self.calc_val(moves, self.depth-1, 'W') ))
        else:
          self.children.append(Node(self.depth-1, 'B', moves, self.calc_val(moves, self.depth-1, 'B') ))
  ##this function is called when generating children to assign minimax values for
  ##each node.
  def calc_val(self, move, depth, player):
    ##The first if-elf block will check to see if the nodes are terminal states
    ##and if so the minimax values are set for these nodes.
    if player == 'B':
      if not generate_move(move,player):
        return -10
      for i in range(0,len(move)):
        if move[(len(move)-1)][i] == 'W':
          return -10  
    else:
      if not generate_move(move,player):
        return 10
      for i in range(0,len(move)):
        if move[0][i] == 'B':
          return 10

    ##Otherwise, if the depth cutoff is reached then these nodes must be
    ##evaluated using the heuristic function (difference). Else we just assign
    ##the node with a temporary dummy minimax value of 1000 (this will be changed once the minimax alg is run)
    if depth == 0:
      differ = difference(move)
      return differ
    else:
      return 1000

##this is the minimax algorithim that will be called on the expanded tree in order to
##push up the most optimal value and determine what the next move player should make.
def minimax(node, depth, player):
   if (abs(node.value) == 10) or (depth == 0):
       return node.value

   optimal = 1000  ##this is a temporary value that will be changed

   for child in node.children:
       if player == 'B':
           value = minimax(child, depth-1, 'W')
       else:
           value = minimax(child, depth-1, 'B')
       if optimal == 1000:
           optimal = value
       elif player == 'B' and optimal < value:
           optimal = value
       elif player == 'W' and optimal > value:
           optimal = value
   node.value = optimal    ##this will essentially assign the parent node with optimal minimax val.
   return optimal

#this is minimax with alpha beta pruning to reduce the search space of the expanded tree
def minimaxalphabeta(node, depth, player, a, b):
   if (abs(node.value) == 10) or (depth == 0):
       return node.value

   optimal = 1000  ##this is a temporary value that will be changed
   alpha = a
   beta = b

   for child in node.children:
       if player == 'B':
           value = minimaxalphabeta(child, depth-1, 'W', alpha, beta)
       else:
           value = minimaxalphabeta(child, depth-1, 'B', alpha, beta)
       if optimal == 1000:
           optimal = value
           if player == 'B':
             if optimal >= beta:
               break
             if value > alpha:
               alpha = value
           else:
             if optimal <= alpha:
               break
             if value < beta:
               beta = value
       elif player == 'B' and optimal < value:
           optimal = value
           if optimal >= beta:
             break
           alpha = value
       elif player == 'W' and optimal > value:
           optimal = value
           if optimal <= alpha:
             break
           beta = value
   node.value = optimal    ##this will essentially assign the parent node with optimal minimax val.
   return optimal




##this utility function is for debugging purposes but it prints the node values
##of the tree
def print_path(node):
   print(node.board)
   print("**********")
   if not node.children:
       return

   for child in node.children:
       if node.value == child.value:
           print_path(child)
           break

##utility function for debugging. print node values in another manner.
def inorder(node):
   print(node.value)
   if not node.children:
       return
   for child in node.children:
       inorder(child)

def maxdepth(node):
 if node.children is None:
   return 0
 final = 0
 for child in node.children:
   value = maxdepth(child) + 1
   if final < value:
     final = value
 return final
      

##this is main and where the game will essentially be played.
if __name__ == '__main__':
  botplayer = 'B'    ##set the bot as black
  count = 1
  play3 = [
      ['W', 'W', 'W'],
      ['0', '0', '0'],
      ['B', 'B', 'B']
  ]

  play4 = [
      ['W', 'W', 'W', 'W'],
      ['0', '0', '0', '0'],
      ['0', '0', '0', '0'],
      ['B', 'B', 'B', 'B']
  ]

  play5 = [
      ['W', 'W', 'W', 'W', 'W'],
      ['0', '0', '0', '0', '0'],
      ['0', '0', '0', '0', '0'],
      ['0', '0', '0', '0', '0'],
      ['B', 'B', 'B', 'B', 'B']
  ]

  play6 = [
      ['W', 'W', 'W', 'W', 'W', 'W'],
      ['0', '0', '0', '0', '0', '0'],
      ['0', '0', '0', '0', '0', '0'],
      ['0', '0', '0', '0', '0', '0'],
      ['0', '0', '0', '0', '0', '0'],
      ['B', 'B', 'B', 'B', 'B', 'B']
  ]

  playboards3 = generate_move(play3,'W')
  playboards3.append(play3)
  playboards4 = generate_move(play4,'W')
  playboards5 = generate_move(play5,'W')
  playboards6 = generate_move(play6,'W')

  total1 = 0
  total3 = 0
  total6 = 0

  prunetotal1 = 0
  prunetotal3 = 0
  prunetotal6 = 0


  answer = int(raw_input("Enter test case (3,4,5 or 6):"))


  if answer == 3:
    for boards in playboards3:
      print ("TRIAL %s RESULTS:" % count)
      depth = 1
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total1 = total1 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal1 = prunetotal1 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      depth = 3
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total3 = total3 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal3 = prunetotal3 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      depth = 6
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total6 = total6 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal6 = prunetotal6 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      count += 1
      if count == 5:
        break

  if answer == 4:
    for boards in playboards4:
      print ("TRIAL %s RESULTS:" % count)
      depth = 1
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total1 = total1 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal1 = prunetotal1 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      depth = 3
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total3 = total3 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal3 = prunetotal3 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      depth = 6
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total6 = total6 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal6 = prunetotal6 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      count += 1
      if count == 5:
        break

  if answer == 5:
    for boards in playboards5:
      print ("TRIAL %s RESULTS:" % count)
      depth = 1
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total1 = total1 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal1 = prunetotal1 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      depth = 3
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total3 = total3 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal3 = prunetotal3 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      depth = 6
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total6 = total6 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal6 = prunetotal6 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      count += 1
      if count == 5:
        break

  if answer == 6:
    for boards in playboards6:
      print ("TRIAL %s RESULTS:" % count)
      depth = 1
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total1 = total1 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal1 = prunetotal1 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      depth = 3
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total3 = total3 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal3 = prunetotal3 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      depth = 6
      print ("Depth: %s" % depth)
      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimax(initial_state,depth,botplayer)
      end = time.time()
      total6 = total6 + (end - start)
      print("time: %f" % (end - start))

      start = time.time()
      initial_state = Node(depth,botplayer,boards,1000)
      decision = minimaxalphabeta(initial_state,depth,botplayer,-100,100)
      end = time.time()
      prunetotal6 = prunetotal6 + (end - start)
      print("time w/ pruning: %f" % (end - start))
      print("----------------------------------------------")
      count += 1
      if count == 5:
        break

  print ("Average results for %d x %d board:" % (answer,answer))
  print ("Average time with depth 1 cutoff: %f" % (total1/4))
  print ("Average time with depth 1 cutoff (w/ pruning): %f" % (prunetotal1/4))
  print ("Average time with depth 3 cutoff: %f" % (total3/4))
  print ("Average time with depth 3 cutoff (w/ pruning): %f" % (prunetotal3/4))
  print ("Average time with depth 6 cutoff: %f" % (total6/4))
  print ("Average time with depth 6 cutoff (w/ pruning): %f" % (prunetotal6/4))



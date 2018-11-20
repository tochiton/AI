# AI

tested on python 2.7
run AI using: python main.py

let’s formally define steps of the algorithm:

Construct the complete game tree
Evaluate scores for leaves using the evaluation function
Back-up scores from leaves to root, considering the player type:
For max player, select the child with the maximum score
For min player, select the child with the minimum score
At the root node, choose the node with max value and perform the corresponding move


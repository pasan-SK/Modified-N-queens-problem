import sys
from a_star_alogrithm_for_modified_n_puzzle_problem import *

## file names
initial_state_representation_file_name = sys.argv[1]
goal_state_representation_file_name = sys.argv[2]
output_file_name = "Output.txt"

# read from input files 
initial_state_representation = []
goal_state_representation = []

with open(initial_state_representation_file_name, "r") as startStateRepFile:
    lines = startStateRepFile.readlines()
    for line in lines:
        initial_state_representation.append(line.strip().split("\t"))

with open(goal_state_representation_file_name, "r") as goalStateRepFile:
    lines = goalStateRepFile.readlines()
    for line in lines:
        goal_state_representation.append(line.strip().split("\t"))

#########################################################
# NOTE: DEFINE THE HEURISTIC OPTION HERE
heuristicOption = 1 # 0 for tile diff, else => manhattan dis
#########################################################

(PATH, f_value, totalMoves) = run_A_start_algorithm(initial_state_representation, goal_state_representation, heuristicOption)
print(", ".join(PATH))
print("Total moves: ", totalMoves)

# write to output file
fo = open(output_file_name, "w")
fo.write(", ".join(PATH))
fo.close()

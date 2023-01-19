from copy import deepcopy
from math import sqrt
import random
from a_star_alogrithm_for_modified_n_puzzle_problem import *

def get_mean(sample_data: List):
    sample_size = len(sample_data)
    return sum(sample_data) / sample_size

def get_std_deviation(sample_data: List, sample_mean: float):
    sample_size = len(sample_data)
    sample_std_deviation = 0
    for k in sample_data:
        sample_std_deviation += (k - sample_mean) ** 2
    return sqrt(sample_std_deviation / (sample_size - 1))

differences_data = []
SAMPLE_SIZE = 110
for i in range(SAMPLE_SIZE): 
    n = random.randrange(5, 21, 1) 
    # n = 10
    possibleTileValues = [str(k) for k in range(1, n*n- 1)]
    possibleTileValues.append("-")
    possibleTileValues.append("-")
    random.shuffle(possibleTileValues)
    
    stateRepresentation = []

    start_state_representation = []

    for i1 in range(n):
        row = []
        for j1 in range(n):
            row.append(possibleTileValues[0])
            del possibleTileValues[0]
        start_state_representation.append(row)

    goal_state_representation = start_state_representation

    random_number_of_moves = -1
    if (16 <= n <= 20):
        random_number_of_moves = 12
    if (11 <= n <= 15):
        random_number_of_moves = 14
    if (5 <= n <= 10):
        random_number_of_moves = 16
    print("\n(n, random_number_of_moves): ", n, ",", random_number_of_moves)  
    print("Iteration: ", i) 
    for i2 in range(random_number_of_moves): 
        all_possible_moves = get_all_possible_moves(goal_state_representation)
        random_index = random.randint(0, len(all_possible_moves)-1)
        goal_state_representation = all_possible_moves[random_index]


    heuristicOption = 0 # 0 for tile difference heuristic, 1 for manhatten distance heuristic 
    (PATH, f_value, totalMoves) = run_A_start_algorithm(start_state_representation, goal_state_representation, heuristicOption)
    tile_difference_total_moves = totalMoves 
    print("total moves with Tile Difference heuristic: ", totalMoves)

    heuristicOption = 1 # 0 for tile difference heuristic, 1 for manhatten distance heuristic 
    (PATH, f_value, totalMoves) = run_A_start_algorithm(start_state_representation, goal_state_representation, heuristicOption)
    manhattan_total_moves = totalMoves
    print("total moves with Manhatten Distance heuristic: ", totalMoves, "\n")

    differences_data.append([n, tile_difference_total_moves, manhattan_total_moves, tile_difference_total_moves - manhattan_total_moves])

# Null Hypothesis (H0): actual/population mean (u) = 0
# Alternative Hypothesis (H1): u > 0
# NOTE that we got difference previously as: (tile_difference_total_moves - manhattan_total_moves) 
# Therefore if the H0 (null hypothesis) is wrong => It implies that the manhattan is better (since smaller number of total moves as an average than the tile difference heuristic)

only_differences = [l[3] for l in differences_data]
sample_mean = get_mean(only_differences)
sample_std_deviation = get_std_deviation(only_differences, sample_mean)
T_value = (sample_mean - 0) / (sample_std_deviation / sqrt(SAMPLE_SIZE))

# assuming 5% level of confidence
# from the student t-distribution table we can get the critical value (t @ 0.05, SAMPLE_SIZE-1) = (N @ 0.05) since SAMPLE_SIZE is large 
CRITICAL_VALUE = 1.64

print("sample mean: ", sample_mean)
print("sample standard deviation: ", sample_std_deviation)
print("Statistic value (T-value): ", T_value)
print("Critical value: ", CRITICAL_VALUE)

# REJECTION CRITERIA:
# If CRITICAL_VALUE < T_value => We can reject NUll Hypothesis (H0) at 5% level of confidence 
if (CRITICAL_VALUE < T_value):
    print("CRITICAL VALUE is less than T_value => Null hypothesis can be rejected with 5 percent level of significance")
else:
    print("Test failed (Null hypotheis cannot be rejected with 5% level of significance)")


# Printing out the differences data with the relevant n value 
n_values = sorted({k[0] for k in differences_data})
n_to_differences_dic = {}

for n in n_values:
    differences_for_n = [] 
    for d in differences_data:
        if n == d[0]: 
            differences_for_n.append(d)
    n_to_differences_dic[n] = differences_for_n

print ("{:<10} {:<5} {:<20} {:<20} {:<20}".format("test num.", "n", "Tile diff.", "Manhattan dis.", "difference"))
testNum = 0
for (key, val) in n_to_differences_dic.items():
    for u in val:
        testNum += 1
        print ("{:<10} {:<5} {:<20} {:<20} {:<20}".format(str(testNum), str(key), str(u[1]), str(u[2]), str(u[3])))

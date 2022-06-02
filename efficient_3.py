from math import floor
from constants import BLANK, DELTA, MISMATCH, CHAR2INDEX
from file_handling import read_file, write_file
import sys

def base(s1, s2):
    s1_len = len(s1)
    s2_len = len(s2)
    # Creating DP matrix
    dp = []
    for i in range(s1_len + 1):
        dp.append([0] * (s2_len + 1))

    # Initializing DP matrix
    for i in range(s1_len + 1):
        dp[i][0] = i * DELTA
    
    for j in range(s2_len + 1):
        dp[0][j] = j * DELTA

    # Calculating min cost of alignment
    for i in range(1, s1_len + 1):
        for j in range(1, s2_len + 1):
            dp[i][j] = min([dp[i][j - 1] + DELTA, 
                            dp[i - 1][j] + DELTA, 
                            dp[i - 1][j - 1] + MISMATCH[CHAR2INDEX[s1[i - 1]]][CHAR2INDEX[s2[j - 1]]]])

    s1_alignment = []
    s2_alignment = []
    i = s1_len
    j = s2_len

    while(i > 0 and j > 0):
        t1 = dp[i][j - 1] + DELTA
        t2 = dp[i - 1][j] + DELTA
        t3 = dp[i - 1][j - 1] + MISMATCH[CHAR2INDEX[s1[i - 1]]][CHAR2INDEX[s2[j - 1]]]
        
        if(dp[i][j] == t3):
            s1_alignment.append(s1[i - 1])
            s2_alignment.append(s2[j - 1])
            i = i - 1
            j = j - 1
        elif(dp[i][j] == t1):
            s1_alignment.append(BLANK)
            s2_alignment.append(s2[j - 1])
            j = j - 1
        else:
            s2_alignment.append(BLANK)
            s1_alignment.append(s1[i - 1])
            i = i - 1
    
    while(i > 0):
        s2_alignment.append(BLANK)
        s1_alignment.append(s1[i - 1])
        i = i - 1
    
    while(j > 0):
        s1_alignment.append(BLANK)
        s2_alignment.append(s2[j - 1])
        j = j - 1

    s1_alignment.reverse()
    s1_alignment = "".join(s1_alignment)
    s2_alignment.reverse()
    s2_alignment = "".join(s2_alignment)
    
    return (s1_alignment, s2_alignment, dp[s1_len][s2_len])

def space_efficient_alignment_left(X_l, Y):
    dp = []
    for i in range(2):
        dp.append([0] * (len(Y) + 1))

    for j in range(1, len(Y) + 1):
        dp[0][j] = j * DELTA

    for i in range (1, len(X_l) + 1):
        dp[1][0] = i * DELTA
        for j in range(1, len(Y) + 1):
            dp[1][j] = min([dp[1][j - 1] + DELTA, 
                            dp[0][j] + DELTA, 
                            dp[0][j - 1] + MISMATCH[CHAR2INDEX[X_l[i - 1]]][CHAR2INDEX[Y[j - 1]]]])
        
        for j in range(0, len(Y) + 1):
            dp[0][j] = dp[1][j]

    return dp[0]

def space_efficient_alignment_right(X_r, Y):
    dp = []
    for i in range(2):
        dp.append([0] * (len(Y) + 1))

    for j in range(len(Y) - 1, -1, -1):
        dp[1][j] = (len(Y) - j) * DELTA

    for i in range (len(X_r) - 1, -1, -1):
        dp[0][len(Y)] = (len(X_r) - i) * DELTA
        for j in range(len(Y) - 1, -1, -1):
            dp[0][j] = min([dp[0][j + 1] + DELTA, 
                            dp[1][j] + DELTA, 
                            dp[1][j + 1] + MISMATCH[CHAR2INDEX[X_r[i]]][CHAR2INDEX[Y[j]]]])
        
        for j in range(len(Y), -1, -1):
            dp[1][j] = dp[0][j]

    return dp[1]


def get_y_div(left_alignment, right_alignment):
    sum = []
    for i in range(0, len(left_alignment)):
        sum.append(left_alignment[i] + right_alignment[i])

    min_index = 0
    min_value = sum[0]
    for index, value in enumerate(sum):
        if(min_value > value):
            min_value = value
            min_index = index
    
    return min_index, min_value

def divide_and_conquer(X, Y, x_start, x_end, y_start, y_end):
    x_len = x_end - x_start + 1
    y_len = y_end - y_start + 1

    if(x_len <= 2 or y_len <= 2):
        return base(X[x_start: x_end + 1], Y[y_start: y_end + 1])

    x_div = x_end - floor((x_end - x_start) / 2)

    left_alignment = space_efficient_alignment_left(X[x_start: x_div], Y[y_start: y_end + 1])
    right_alignment = space_efficient_alignment_right(X[x_div: x_end + 1], Y[y_start: y_end + 1])

    y_div, cost = get_y_div(left_alignment, right_alignment)
    (x1, y1, c1) = divide_and_conquer(X, Y, x_start, x_div - 1, y_start, y_start + y_div - 1)
    (x2, y2, c2) = divide_and_conquer(X, Y, x_div, x_end, y_start + y_div, y_end)

    return (x1 + x2, y1 + y2, c1 + c2)

if __name__ == "__main__":
    arg_count = len(sys.argv)
    if(arg_count == 3):
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        s1, s2 = read_file(input_file_path)
        print(divide_and_conquer(s1, s2, 0, len(s1) - 1, 0, len(s2) - 1))
        
    else:
        print("INPUT IS NOT VALID")
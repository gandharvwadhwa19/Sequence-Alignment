from constants import BLANK, DELTA, MISMATCH, CHAR2INDEX
from file_handling import read_file, write_file
import sys

def main(input_file_path, output_file_path):
    s1, s2 = read_file(input_file_path)
    
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
    
    output = [str(dp[s1_len][s2_len]), s1_alignment, s2_alignment]
    print(output[0] + "\n" + output[1] + "\n" + output[2])

if __name__ == "__main__":
    arg_count = len(sys.argv)
    if(arg_count == 3):
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        main(input_file_path, output_file_path)
    else:
        print("INPUT IS NOT VALID")
from constants import IO_PATH

def append_string(s, i):
    i = int(i)
    s = s[: i + 1] + s + s[i + 1:]
    return s

def read_file(path):
    path = IO_PATH + path
    with open(path) as f:
        lines = f.readlines()

    i = 0
    line_count = len(lines)
    res_string = []    
    while i < line_count:
        s = lines[i].strip()
        i = i + 1
        while(i < line_count and lines[i].strip().isnumeric() == True):
            s = append_string(s, lines[i].strip())
            i = i + 1

        res_string.append(s)
    
    return res_string

def write_file(path, data):
    
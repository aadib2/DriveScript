# DriveScript interpreter - tests sample programs work
import sys
import argparse

def run(code):
    # Remove comments
    lines = code.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove comments (everything from '#' to end of line)
        if '#' in line:
            line = line[:line.index('#')]
        cleaned_lines.append(line)
    code = '\n'.join(cleaned_lines)
    
    # Tokenize
    tokens = []
    i = 0
    words = code.replace('\n', ' ').split() # store all of the words
    # print(words)
    j = 0
    pending_gear = 1
    pending_reverse = False
    while j < len(words):
        w = words[j].upper()
        if w == 'GEAR':
            j += 1 # go to next
            g = words[j].upper() # either a number or 'R'
            if g == 'R':
                pending_reverse = True
            else:
                pending_gear = int(g) # store n for repeating action
            j += 1
            continue
        # all other possible operations (except GEAR)
        if w in ('RIGHT', 'LEFT', 'GAS', 'BRAKE', 'HONK', 'LISTEN', 'PARK', 'DRIVE'):
            # Apply gear/reverse
            count = pending_gear
            instr = w
            if pending_reverse:
                # Reverse swaps GAS/BRAKE and LEFT/RIGHT
                if instr == 'GAS': instr = 'BRAKE'
                elif instr == 'BRAKE': instr = 'GAS'
                elif instr == 'RIGHT': instr = 'LEFT'
                elif instr == 'LEFT': instr = 'RIGHT'
            for _ in range(count):
                tokens.append(instr) # append repeated instructions to token list
            pending_gear = 1
            pending_reverse = False
        j += 1
    
    # Map to brainfuck-like
    bf_map = {'RIGHT':'>', 'LEFT':'<', 'GAS':'+', 'BRAKE':'-', 'HONK':'.', 'LISTEN':',', 'PARK':'[', 'DRIVE':']'}
    bf = ''.join(bf_map[t] for t in tokens) # convert each token to it's brainf equivalent
    
    # Build jump table
    jumps = {}
    stack = []
    for idx, c in enumerate(bf):
        if c == '[':
            stack.append(idx)
        elif c == ']':
            start = stack.pop()
            jumps[start] = idx
            jumps[idx] = start
    
    tape = [0] * 30000
    ptr = 0
    pc = 0
    output = []
    while pc < len(bf): # pc = program counter, akin to "instruction set"
        c = bf[pc]
        # perform operations
        if c == '>': ptr += 1
        elif c == '<': ptr -= 1
        elif c == '+': tape[ptr] = (tape[ptr] + 1) % 256
        elif c == '-': tape[ptr] = (tape[ptr] - 1) % 256
        elif c == '.': output.append(chr(tape[ptr])) # chr method converts ASCII to character
        elif c == '[' and tape[ptr] == 0: pc = jumps[pc]
        elif c == ']' and tape[ptr] != 0: pc = jumps[pc]
        pc += 1
    return ''.join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DriveScript Interpreter")
    parser.add_argument("file_name", help="Name of .ds file")

    args = parser.parse_args()

    if not args.file_name:
        raise Exception("Include the .ds program file!")
    
    # Read the .ds file and execute it
    with open(args.file_name, 'r') as f:
        code = f.read()
    
    result = run(code)
    print(result)

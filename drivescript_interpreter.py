# DriveScript interpreter - tests sample programs work
import sys
import os
import argparse

def preprocess_includes(code, base_dir, seen=None):
    """Resolve INCLUDE "path" directives recursively. Paths are relative to the
    file currently being processed, then to the stdlib directory next to this
    interpreter. Each file is included at most once per compilation unit."""

    if seen is None:
        seen = set()
    stdlib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stdlib')
    out_lines = []
    for raw in code.split('\n'):
        stripped = raw.strip()
        upper = stripped.upper()
        if upper.startswith('INCLUDE'):
            # Expect: INCLUDE "filename.ds"
            rest = stripped[len('INCLUDE'):].strip()
            if len(rest) >= 2 and rest[0] in ('"', "'") and rest[-1] == rest[0]:
                inc_name = rest[1:-1]
            else:
                inc_name = rest  # tolerate bare filenames

            candidates = [
                os.path.join(base_dir, inc_name),
                os.path.join(stdlib_dir, inc_name),
            ]

            inc_path = next((p for p in candidates if os.path.isfile(p)), None) # store the path that exists out of the two candi
            if inc_path is None: 
                raise FileNotFoundError(f"INCLUDE could not find {inc_name!r} (looked in {base_dir} and {stdlib_dir})")
            real = os.path.realpath(inc_path)
            if real in seen:
                continue  # already included; skip silently to allow header-style guards
            seen.add(real)
            with open(inc_path, 'r') as f:
                inc_code = f.read()
            
            # recursively preprocess any other includes. Append code to out_lines
            expanded = preprocess_includes(inc_code, os.path.dirname(real), seen)
            out_lines.append(f"# >>> begin include: {inc_name}")
            out_lines.append(expanded)
            out_lines.append(f"# <<< end include: {inc_name}")
        else:
            out_lines.append(raw)
    return '\n'.join(out_lines)


def run(code, input_stream=None):
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
    input_pos = 0
    output = []
    while pc < len(bf): # pc = program counter, akin to "instruction set"
        c = bf[pc]
        # perform operations
        if c == '>': ptr += 1
        elif c == '<': ptr -= 1
        elif c == '+': tape[ptr] = (tape[ptr] + 1) % 256
        elif c == '-': tape[ptr] = (tape[ptr] - 1) % 256
        elif c == '.': output.append(chr(tape[ptr])) # chr method converts ASCII to character
        elif c == ',':
            # LISTEN - read one byte of input into current cell
            if input_stream is not None:
                if input_pos < len(input_stream):
                    tape[ptr] = ord(input_stream[input_pos])
                    input_pos += 1
                else:
                    tape[ptr] = 0  # EOF
            else:
                ch = sys.stdin.read(1)
                tape[ptr] = ord(ch) if ch else 0
        elif c == '[' and tape[ptr] == 0: pc = jumps[pc]
        elif c == ']' and tape[ptr] != 0: pc = jumps[pc]
        pc += 1
    return ''.join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DriveScript Interpreter")
    parser.add_argument("file_name", help="Name of .ds file")
    parser.add_argument("--input", "-i", default=None,
                        help="Input string for LISTEN. If omitted, LISTEN reads from stdin.")

    args = parser.parse_args()

    if not args.file_name:
        raise Exception("Include the .ds program file!")

    # Read the .ds file, resolve includes, and execute it
    with open(args.file_name, 'r') as f:
        code = f.read()

    base_dir = os.path.dirname(os.path.abspath(args.file_name))
    code = preprocess_includes(code, base_dir)

    result = run(code, input_stream=args.input)
    # Use sys.stdout.write to avoid double-newlines when programs already emit them
    sys.stdout.write(result)

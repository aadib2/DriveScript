# DriveScript
[DriveScript](https://aadib2.github.io/DriveScript/) is an esoteric programming language created as part of SDSU CS 420: Advanced Programming Languages.

## What Is DriveScript

DriveScript turns driving actions into code. Instead of traditional keywords, programs are written with commands like `RIGHT`, `LEFT`, `GAS`, `BRAKE`, `HONK`, `LISTEN`, `PARK`, and `DRIVE`. The result is a small Brainfuck-like language that feels physical and playful while still being capable of real computation.

The language is intentionally minimal. Each command operates on a tape of memory cells, and programs usually build behavior by moving the pointer, changing cell values, printing ASCII characters, and looping.

## How the Language Works

DriveScript uses a tape of byte-sized cells initialized to zero. The pointer starts at cell 0 and moves across the tape as the program runs.

- `RIGHT` moves the pointer one cell to the right.
- `LEFT` moves the pointer one cell to the left.
- `GAS` increments the current cell.
- `BRAKE` decrements the current cell.
- `HONK` prints the ASCII character in the current cell.
- `LISTEN` reads one byte of input into the current cell.
- `GEAR N` repeats the next command `N` times.
- `GEAR R` reverses the next directional or value-changing command, so `RIGHT` becomes `LEFT` and `GAS` becomes `BRAKE`.
- `PARK ... DRIVE` creates a loop that repeats while the current cell is non-zero.

Most programs are written by combining these primitives into small reusable patterns for counters, conditionals, and output.

## How the Interpreter Works

The interpreter processes a `.ds` file in a few stages:

1. It removes comments and tokenizes the DriveScript words.
2. It applies `GEAR` repetition and reversal to expand each command into a plain instruction stream.
3. It maps DriveScript commands to a Brainfuck-style internal representation.
4. It builds a jump table for every `PARK ... DRIVE` loop before execution starts.
5. It executes the program against a byte tape and writes any output to standard out.

### Include Resolution

`INCLUDE` is resolved against two paths:

1. The directory of the file currently being processed.
2. The interpreter’s `stdlib` directory.

For example, if a program contains:

```ds
INCLUDE "helpers.ds"
```

the interpreter first looks for `helpers.ds` next to the current file. If it is not found there, it then checks the interpreter’s shared `stdlib` directory.

### Loop Jumps

`PARK` and `DRIVE` are translated to `[` and `]`. The interpreter walks the translated program once, using a stack to match each opening loop with its closing partner (similar to the palindrome problem). That lets it jump instantly when a loop should repeat or exit.

For example, this program:

```ds
GEAR 3 GAS PARK BRAKE DRIVE
```

becomes a loop over a cell that starts at `3`:

```text
++[-]
```

The loop keeps subtracting until the current cell reaches zero, then execution continues after `DRIVE`.

## Example Program

The `example_programs/` folder contains a few small programs that show different parts of the language in action:

- `simple_programs/hello.ds` and `simple_programs/hello_short.ds` show basic output.
- `simple_programs/listen_echo.ds` demonstrates input and output.
- `fizzbuzz/` contains a more complete multi-file example implementing FizzBuzz
- `complex_programs/if_stmt.ds` and `complex_programs/case_flip.ds` demonstrate branching-style logic.

If you want the quickest starting point, run `example_programs/simple_programs/hello.ds`.

## How to Run DriveScript Programs in the Terminal

Run a program with:

```bash
python3 drivescript_interpreter.py path/to/program.ds
```

If the program needs input for `LISTEN`, pass it with `--input`:

```bash
python3 drivescript_interpreter.py example_programs/simple_programs/listen_echo.ds --input "A"
```



# layout.ds - Canonical tape layout for the DriveScript Standard Library

All stdlib macros assume the following tape layout. If you INCLUDE multiple
stdlib files, they share this layout. Position values are absolute cell
indices. The convention is that every macro starts and ends with the pointer
at cell 0 (C_SCRATCH) unless otherwise noted.

- c0  C_SCRATCH   - print scratch (we put ASCII chars here and HONK)
- c1  C_HELPER    - multiplier helper for fast emit
- c2  -           - reserved spacer
- c3  C_ONES      - ones digit of current number (0-9)
- c4  C_UNTIL10   - 10 minus C_ONES (carry trigger when it hits 0)
- c5  C_TENS      - tens digit (0-10; 10 means we're at 100)
- c6  C_HELP_T    - temp for tests in counter region
- c7  C_FLAG_T    - zero-flag for counter-region tests
- c8  C_MOD3      - decreasing-from-3 mod-3 counter
- c9  C_HELP_3    - temp for mod-3 tests
- c10 C_FLAG_3    - zero-flag for mod-3 tests
- c11 C_MOD5      - decreasing-from-5 mod-5 counter
- c12 C_HELP_5    - temp for mod-5 tests
- c13 C_FLAG_5    - zero-flag for mod-5 tests
- c14 C_NEITHER   - 1 if no Fizz/Buzz printed this iteration (=> print number)
- c15 C_LOOPCNT   - outer-loop countdown (e.g. 100 for FizzBuzz)
- c16 C_HELP_L    - temp for loop-region tests
- c17 C_FLAG_L    - zero-flag for loop-region tests

This is a reference point when understanding how the STDLIB works.

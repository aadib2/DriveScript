from drivescript_interpreter import run


# Convert this BF program to DriveScript using gears for compactness
# Map: + GAS, - BRAKE, > RIGHT, < LEFT, [ PARK, ] DRIVE, . HONK
# Use GEAR N to compress runs
def bf_to_ds(bf):
    out = []
    i = 0
    inv = {'+':'GAS','-':'BRAKE','>':'RIGHT','<':'LEFT','[':'PARK',']':'DRIVE','.':'HONK',',':'LISTEN'}
    while i < len(bf):
        c = bf[i]
        if c not in inv:
            i += 1
            continue
        # Count run of same char (only for repeatable ones)
        run = 1
        if c in '+-<>':
            while i+run < len(bf) and bf[i+run] == c:
                run += 1
        if run >= 2 and run <= 5:
            out.append(f"GEAR {run} {inv[c]}")
        elif run > 5:
            # Break into chunks of 5
            full = run // 5
            rem = run % 5
            for _ in range(full):
                out.append(f"GEAR 5 {inv[c]}")
            for _ in range(rem):
                out.append(inv[c])
        else:
            out.append(inv[c])
        i += run
    return ' '.join(out)


if __name__ == "__main__":
    # Test 1: Hello World
    # Classic BF Hello World adapted: 
    # ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
    hello_bf = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    ds_hello = bf_to_ds(hello_bf) # translate
    print("Hello World DriveScript (length):", len(ds_hello), "chars")
    result = run(ds_hello) # interpret DS code
    print(f"Output: {repr(result)}")
    assert result == "Hello World!\n", f"FAIL: got {repr(result)}" # test if output matches
    print("Hello World: PASS")


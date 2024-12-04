import sys
import os.path

# Size of the memory. Should be more than enough for common programs
SIZE = 30000
memory = [0] * SIZE
ptr = 0
ASCII_mode = True

# Store all the instructions fetched from the file.
code_instructions = []

def bf_loader(script: str):
    scr =  open(script, 'r')
    while True:
        instruction = scr.read(1)
        if not instruction:
            break

        if instruction in ['<', '>', '+', '-', '.', ',', '[', ']']:
            code_instructions.append(instruction)
    scr.close()
    _bf_interpreter()


def _bf_interpreter():
    # keep track of the current instruction address
    curr_inst = 0
    # For loop ("[]"), push the instruction address of the "[" in a LIFO stack.
    loop_stack = []
    global memory
    global ptr
    global code_instructions
    if ASCII_mode:
        print("[i] ASCII mode selected")
    else:
        print("[i] Numeric mode selected")
    while curr_inst < len(code_instructions):
        instruction = code_instructions[curr_inst]
        if instruction == "<":
            if ptr >= 0:
                ptr -= 1
            else:
                print("[x] ERR: stack underflow at", curr_inst)
        if instruction == ">":
            if ptr < SIZE:
                ptr += 1
            else:
                print("[x] ERR: stack overflow at", curr_inst)
        if instruction == ".":
            if ASCII_mode:
                print(chr(memory[ptr]), end="")
            else:
                print(memory[ptr])
        if instruction == ",":
            memory[ptr] = ord(input()[0]) # Only one char read
        if instruction == "+":
            memory[ptr] += 1
        if instruction == "-":
            memory[ptr] -= 1

        if instruction == "[":
            if memory[ptr] != 0:
                # Append current memory address to the stack
                loop_stack.append(curr_inst + 1)
        if instruction == "]":
            if not len(loop_stack) == 0:
                if memory[ptr] > 0:
                    # Load memory address from stack
                    curr_inst = loop_stack[-1] - 1
                else:
                    # Pop memory address from the stack
                    loop_stack.pop()
        curr_inst += 1


if __name__ == "__main__":
    if len(sys.argv)-1 < 1:
        print("Usage: brainfuck.py <filename> [ascii_mode=<true/false>]")
    if len(sys.argv)-1 == 2 and "false" in sys.argv[2].lower():
        ASCII_mode = False
    if not os.path.isfile(sys.argv[1]):
        print("Error: file", sys.argv[1], " not found!")

    bf_loader(sys.argv[1])

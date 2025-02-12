# ***
# Assembler is sometimes buggy, if it doesnt work, try to remove any empty lines or whitespace in the .masm file you're trying to assemble
# If the assembler still doesnt work, try to remove any comments in the .masm file you're trying to assemble
# ***

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from libraries.binary_lib import mbin, mint, set_flag, check_flag

non_redundant_mnemonics = ["move", "add", "sub", "mult", "div", "and", "or", "xor", "not", "rol", "ror", "cmp", "shl", "shr", "push", "pop", "call", "ret"]
non_redundant_mnemonics_opcodes = {
    "move": "00001100",
    "add": "00001101",
    "sub": "00001110",
    "mult": "00001111",
    "div": "00010000",
    "and": "00010011",
    "or": "00010100",
    "xor": "00010101",
    "not": "00010110",
    "rol": "00010111",
    "ror": "00011000",
    "cmp": "00011001",
    "shl": "00011010",
    "shr": "00011011",
    "push": "00011100",
    "pop": "00011101",
    "call": "00011110",
    "ret": "00011111"
}

registers = {
            "r0": "0000",
            "r1": "0001",
            "r2": "0010",
            "r3": "0011",
            "r4": "0100",
            "r5": "0101",
            "r6": "0110",
            "r7": "0111",
            "pc": "1000",
            "ir": "1001",
            "sp": "1010",
            "bp": "1011",
            "acc": "1100",
            "flags": "1101",
            "mar": "1110",
            "mdr": "1111",
            "0000": "r0",
            "0001": "r1",
            "0010": "r2",
            "0011": "r3",
            "0100": "r4",
            "0101": "r5",
            "0110": "r6",
            "0111": "r7",
            "1000": "pc",
            "1001": "ir",
            "1010": "sp",
            "1011": "bp",
            "1100": "acc",
            "1101": "flags",
            "1110": "mar",
            "1111": "mdr",
        }

def collect_labels(assembly, reserved):
    print("Collecting labels...")
    labels = {}
    current_addresse = 0
    for i, line in enumerate(assembly):
        print("Entered loop")
        print(f"Line {i+1}: {line}")
        if line.endswith("\n"):
            line = line.split("\n")[0]
        if line.endswith(":"):
            print("Label found")
            if not line[0:] in reserved:
                print(f"Storing label {line[0:]} at address {current_addresse}")
                label = ">" + line[0:]
                labels[label] = mbin(current_addresse, 16, neg=False)
                    
            else:
                raise ValueError(f"Invalid label {line[1:]} at line {i+1}")
        else:
            print("No label found")
            current_addresse += 4
    return labels

def tokenize(line):
    if "\n" in line:
        line = line.split("\n")[0]
    if ";" in line:
        line = line.split(";")[0]
    if not line == "":
        tokens = line.split(" ")
        for token in tokens:
            if token == "":
                tokens.remove(token)
            if token == " ":
                tokens.remove(token)
            if token == "\n":
                tokens.remove(token)
            if token.endswith(","):
                tokens[tokens.index(token)] = token[:-1]
        return tokens
    return None

def register_to_bin(register):
    return registers[register]

def immediate_to_bin(immediate, bitsize):
    if immediate == "#":
        return mbin(0, bitsize, neg = False)
    return mbin(int(immediate), bitsize, neg = False)

def get_instruction(tokens, i, labels: dict):
    mnemonic = tokens[0]
    operands = tokens[1:]
    opcode_bin = ""
    operand1_bin = ""
    operand2_bin = ""
    operand3_bin = ""

    print(mnemonic, operands)
    match mnemonic:
        case "jmp":
            if len(operands) != 1:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[0].startswith("#"):
                opcode_bin = "00000000"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[0][1:]), 16, neg = False)
            elif operands[0].startswith(">"):
                if not str(operands[0]) + ":" in labels:
                    print("_________________________")
                    print("Error causing label: " + operands[0])
                    print("labels:", labels)
                    raise ValueError(f"Label {operands[0]} isn't defined at line {i+1}")
                opcode_bin = "00000000"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = labels[operands[0] + ":"]
            else:
                if not operands[0] in registers:
                    raise ValueError(f"Invalid register {operands[0]} at line {i+1}")
                opcode_bin = "00001000"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = "0000"
                operand3_bin = "0000000000000000"
        case "jeq":
            if len(operands) != 1:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[0].startswith("#"):
                opcode_bin = "00000001"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[0][1:]), 16, neg=False)
            elif operands[0].startswith(">"):
                if not operands[0] + ":" in labels:
                    print("_________________________")
                    print("labels:", labels)
                    raise ValueError(f"Label {operands[0]} isn't defined at line {i+1}")
                opcode_bin = "00000001"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = labels[operands[0] + ":"]
            else:
                if not operands[0] in registers:
                    raise ValueError(f"Invalid register {operands[0]} at line {i+1}")
                opcode_bin = "00001001"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = "0000"
                operand3_bin = "0000000000000000"
        case "jne":
            if len(operands) != 1:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[0].startswith("#"):
                    opcode_bin = "00000010"
                    operand1_bin = "0000"
                    operand2_bin = "0000"
                    operand3_bin = mbin(int(operands[0][1:]), 16, neg=False)
            elif operands[0].startswith(">"):
                if not operands[0] + ":" in labels:
                    raise ValueError(f"Label {operands[0]} isn't defined at line {i+1}")
                opcode_bin = "00000010"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = labels[operands[0] + ":"]
            else:
                if not operands[0] in registers:
                    raise ValueError(f"Invalid register {operands[0]} at line {i+1}")
                opcode_bin = "00001010"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = "0000"
                operand3_bin = "0000000000000000"
        case "inc":
            if len(operands) != 1:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[0].startswith("[") and operands[0].endswith("]"):
                opcode_bin = "00000011"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[0][1:-1]), 16, neg=False)
            else:
                opcode_bin = "00010001"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = "0000"
                operand3_bin = "0000000000000000"
        case "dec":
            if len(operands) != 1:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[0].startswith("[") and operands[0].endswith("]"):
                opcode_bin = "00000100"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[0][1:-1]), 16, neg=False)
            else:
                opcode_bin = "00010010"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = "0000"
                operand3_bin = "0000000000000000"
        case "load":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[1].startswith("#"):
                opcode_bin = "00000101"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[1][1:]), 16, neg=False)
            else:
                opcode_bin = "00000110"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[1][1:-1]), 16, neg=False)
        case "store":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[0].startswith("#"):
                opcode_bin = "00000111"
                operand1_bin = register_to_bin(operands[1])
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[0][1:]), 16, neg=False)
            else:
                opcode_bin = "00001011"
                operand1_bin = register_to_bin(operands[0][1:-1])
                operand2_bin = register_to_bin(operands[1])
                operand3_bin = "0000000000000000"
        case "move":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "add":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "sub":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "mult":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "div":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "and":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "or":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "xor":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "rol":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = immediate_to_bin(operands[1], 4)
            operand3_bin = "0000000000000000"
        case "ror":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = immediate_to_bin(operands[1], 4)
            operand3_bin = "0000000000000000"
        case "not":
            if len(operands) != 1:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = "0000"
            operand3_bin = "0000000000000000"
        case "cmp":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "shl":
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = immediate_to_bin(operands[1][:1], 4)
            operand3_bin = "0000000000000000"
        case "shr":
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = immediate_to_bin(operands[1][:1], 4)
            operand3_bin = "0000000000000000"
        case "push":
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = "0000"
            operand3_bin = "0000000000000000"
        case "pop":
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = "0000"
            operand3_bin = "0000000000000000"
        case "call":
            if len(operands) != 1:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[0].startswith("#"):
                opcode_bin = "00000000"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[0][1:]), 16, neg = False)
            elif operands[0].startswith(">"):
                if not str(operands[0]) + ":" in labels:
                    print("_________________________")
                    print("Error causing label: " + operands[0])
                    print("labels:", labels)
                    raise ValueError(f"Label {operands[0]} isn't defined at line {i+1}")
                opcode_bin = "00000000"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = labels[operands[0] + ":"]
        case "ret":
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = "0000"
            operand2_bin = "0000"
            operand3_bin = "0000000000000000"
        case "halt":
            opcode_bin = "11111111"
            operand1_bin = "0000"
            operand2_bin = "0000"
            operand3_bin = "0000000000000000"
        case "debug":
            opcode_bin = "debuggin"
            operand1_bin = "0000"
            operand2_bin = "0000"
            operand3_bin = "0000000000000000"
        case _:
            if not mnemonic.endswith(":"):
                raise ValueError(f"Invalid mnemonic '{mnemonic}' at line {i+1}")

    instruction = opcode_bin + operand1_bin + operand2_bin + operand3_bin
    return instruction

def cut_instruction(instruction):
    return [instruction[i:i+8] for i in range(0, len(instruction), 8)]

def write_to_file(binary, output_file):
    with open(output_file, "w") as file:
        for byte in binary:
            file.write(byte + "\n")

def read_from_file(input_file):
    with open(input_file, "r") as file:
        return file.readlines()

def assemble(assembly):
    binary = []
    reserved = ["jmp", "jeq", "jne", "inc", "dec", "load", "store", "move", "add", "sub", "mult", "div", "and", "or", "xor", "not", "rol", "ror", "cmp", "shl", "shr", "hlt", "nop", "ret", "", " ", "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "pc", "ir", "sp", "bp", "acc", "flags", "mar", "mdr"]
    labels = collect_labels(assembly, reserved)

    for i, line in enumerate(assembly):
        tokens = tokenize(line)
        if tokens == None or len(tokens) == 0:
            continue

        instruction = get_instruction(tokens, i, labels)
        for byte in cut_instruction(instruction):
            binary.append(byte)
    return binary

DIRECTORY_INPUT = "programs/asm/"
DIRECTORY_OUTPUT = "programs/bin/"

def main():
    input_file = DIRECTORY_INPUT +  str(input("Enter the name of the file to assemble: ")) + ".masm"
    output_file = DIRECTORY_OUTPUT + str(input("Enter the name of the output file: ")) + ".bin"
    assembly = read_from_file(input_file)
    binary = assemble(assembly)
    write_to_file(binary, output_file)

if __name__ == "__main__":
    main()
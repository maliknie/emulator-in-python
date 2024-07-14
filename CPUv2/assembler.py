# ISA
"""
Core instructions and syntax:
        32 bit:
             jmp #imd: | 00000000 | padding with zeros (4 bits) | padding with zeros (4 bits) | immediate value (16 bits) | Description: imd -> pc
             jeq #imd: | 00000001 | padding with zeros (4 bits) | padding with zeros (4 bits) | immediate value (16 bits) | Description: if zero flag = 1, imd -> pc
             jne #imd: | 00000010 | padding with zeros (4 bits) | padding with zeros (4 bits) | immediate value (16 bits) | Description: if zero flag != 1, imd -> pc
             inc [mem]: | 00000011 | padding with zeros (4 bits) | padding with zeros (4 bits) | memory address (16 bits) | Description: [mem] += 1
             dec [mem]: | 00000100 | padding with zeros (4 bits) | padding with zeros (4 bits) | memory address (16 bits) | Description: [mem] -= 1
             load #imd, reg : | 00000101 | reg1 (4 bits) | padding with zeros (4 bits) | immediate value (16 bits) | Description: imd -> reg1
             load [mem], reg: | 00000110 | reg1 (4 bits) | padding with zeros (4 bits) | memory address (16 bits) | Description: [mem] -> reg1
             store reg, [mem]: | 00000111 | reg1 (4 bits) | padding with zeros (4 bits) | memory address (16 bits) | Description: reg1 -> [mem] 
        16 bit + 16 bit padding:
             jmp reg: | 00001000 | reg1 (4 bits) | padding with zeros (4 bits) | padding with zeros (16 bits) | Description: reg1 -> pc
             jeq reg: | 00001001 | reg1 (4 bits) | padding with zeros (4 bits) | padding with zeros (16 bits) | Description: if zero flag = 1, reg1 -> pc
             jne reg: | 00001010 | reg1 (4 bits) | padding with zeros (4 bits) | padding with zeros (16 bits) | Description: if zero flag != 1, reg1 -> pc
             store reg1, reg2: | 00001011 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 -> [reg1]
             move reg1, reg2: | 00001100 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 -> reg1
             add reg1, reg2: | 00001101 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 + reg1 -> reg1
             sub reg1, reg2: | 00001110 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 - reg1 -> reg1
             mult reg1, reg2: | 00001111 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 * reg1 -> high 16 bits in reg1, low 16 bits in reg2
             div reg1, reg2: | 00010000 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 / reg1 -> result in reg1, mod in reg2
             inc reg: | 00010001 | reg1 (4 bits) | padding with zeros (4 bits) | padding with zeros (16 bits) | Description: reg1 += 1
             dec reg: | 00010010 | reg1 (4 bits) | padding with zeros (4 bits) | padding with zeros (16 bits) | Description: reg1 -= 1
             and reg1, reg2: | 00010011 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 & reg1 -> reg1
             or reg1, reg2: | 00010100 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 | reg1 -> reg1
             xor reg1, reg2: | 00010101 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 ^ reg1 -> reg1
             not reg 1: | 00010110 | reg1 (4 bits) | padding with zeros (4 bits) | padding with zeros (16 bits) | Description: ~reg1 -> reg1
             rol reg1, #imd: | 00010111 | reg1 (4 bits) | imd (4 bits) | padding with zeros (16 bits) | Description: reg1 << imd -> reg1
             ror reg1, #imd: | 00011000 | reg1 (4 bits) | imd (4 bits) | padding with zeros (16 bits) | Description: reg1 >> imd -> reg1
             cmp reg1, reg2: | 00011001 | reg1 (4 bits) | reg2 (4 bits) | padding with zeros (16 bits) | Description: reg2 - reg1 (only changes flags)

"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from libraries.binary_lib import mbin, mint, set_flag, check_flag

non_redundant_mnemonics = ["move", "add", "sub", "mult", "div", "and", "or", "xor", "not", "rol", "ror", "cmp"]
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
    return mbin(int(immediate), bitsize)

def get_instruction(tokens, i, labels: dict):
    mnemonic = tokens[0]
    operands = tokens[1:]
    opcode_bin = ""
    operand1_bin = ""
    operand2_bin = ""
    operand3_bin = ""

    match mnemonic:
        case "jmp":
            if len(operands) != 1:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[0].startswith("#"):
                opcode_bin = "00000000"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[0][1:]), 16)
            elif operands[0].startswith(">"):
                if not operands[0] in labels:
                    raise ValueError(f"Label {operands[0]} isn't defined at line {i+1}")
                opcode_bin = "00000000"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = labels[operands[0]]
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
                operand3_bin = mbin(int(operands[0][1:]), 16)
            elif operands[0].startswith(">"):
                if not operands[0] in labels:
                    raise ValueError(f"Label {operands[0]} isn't defined at line {i+1}")
                opcode_bin = "00000001"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = labels[operands[0]]
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
                    operand3_bin = mbin(int(operands[0][1:]), 16)
            elif operands[0].startswith(">"):
                if not operands[0] in labels:
                    raise ValueError(f"Label {operands[0]} isn't defined at line {i+1}")
                opcode_bin = "00000010"
                operand1_bin = "0000"
                operand2_bin = "0000"
                operand3_bin = labels[operands[0]]
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
                operand3_bin = mbin(int(operands[0][1:-1]), 16)
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
                operand3_bin = mbin(int(operands[0][1:-1]), 16)
            else:
                opcode_bin = "00010010"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = "0000"
                operand3_bin = "0000000000000000"
        case "load":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[0].startswith("#"):
                opcode_bin = "00000101"
                operand1_bin = register_to_bin(operands[1])
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[0][1:]), 16)
            else:
                opcode_bin = "00000110"
                operand1_bin = register_to_bin(operands[1])
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[0][1:-1]), 16)
        case "store":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            if operands[1].startswith("[") and operands[1].endswith("]"):
                opcode_bin = "00000111"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = "0000"
                operand3_bin = mbin(int(operands[1][1:-1]), 16)
            else:
                opcode_bin = "00001011"
                operand1_bin = register_to_bin(operands[0])
                operand2_bin = register_to_bin(operands[1])
                operand3_bin = "0000000000000000"
        case "move", "add", "sub", "mult", "div", "and", "or", "xor", "cmp":
            if len(operands) != 2:
                raise ValueError(f"Invalid number of operands for {mnemonic} at line {i+1}")
            opcode_bin = non_redundant_mnemonics_opcodes[mnemonic]
            operand1_bin = register_to_bin(operands[0])
            operand2_bin = register_to_bin(operands[1])
            operand3_bin = "0000000000000000"
        case "rol", "ror":
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
    reserved = ["jmp", "jeq", "jne", "inc", "dec", "load", "store", "move", "add", "sub", "mult", "div", "and", "or", "xor", "not", "rol", "ror", "cmp", "hlt", "nop", "ret", "", " ", "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "pc", "ir", "sp", "bp", "acc", "flags", "mar", "mdr"]
    labels = {}
    current_address = 0

    for i, line in enumerate(assembly):
        tokens = tokenize(line)
        if tokens == None or len(tokens) == 0:
            continue
        elif len(tokens) == 1:
            if tokens[0].startswith(":"):
                if not tokens[0][1:] in reserved:
                    labels[">" + tokens[0][1:]] = mbin(current_address, 16)
                else:
                    raise ValueError(f"Invalid label {tokens[0]} at line {i+1}")
                continue

        instruction = get_instruction(tokens, i, labels)
        for byte in cut_instruction(instruction):
            binary.append(byte)
            current_address += 1
    return binary

DIRECTORY_INPUT = "CPUv2/programs/asm/"
DIRECTORY_OUTPUT = "CPUv2/programs/bin/"

def main():
    input_file = DIRECTORY_INPUT +  str(input("Enter the name of the file to assemble: ")) + ".masm"
    output_file = DIRECTORY_OUTPUT + str(input("Enter the name of the output file: ")) + ".bin"
    assembly = read_from_file(input_file)
    binary = assemble(assembly)
    write_to_file(binary, output_file)

if __name__ == "__main__":
    main()
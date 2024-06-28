import os

input_file = "assembly.txt"
output_file = "program.bin"

input_file = "assembly_files/" + input_file
output_file = "binary_files/" + output_file


instruction_set = {
    "NOP": "0000000",
    "LDA": "0000001",
    "STA": "0000010",
    "ADD": "0000011",
    "SUB": "0000100",
    "JMP": "0000101",
    "JZ": "0000110",
    "JNZ": "0000111",
    "AND": "0001000",
    "OR": "0001001",
    "HLT": "0001010",
    "MOV": "0001011",
    "MOVT": "0001100",
    "MOVF": "0001101",
    "CLR": "0001110",
    "STAS": "0001111"
}

no_args = ["NOP", "HLT", "CLR"]
# amount of arguments when msb is 0
args0 = {
    'NOP': 0,
    'LDA': 2,
    'STA': 2,
    'ADD': 2,
    'SUB': 2,
    'JMP': 2,
    'JZ': 2,
    'JNZ': 2,
    'AND': 2,
    'OR': 2,
    'HLT': 0,
    'MOV': 2,
    'MOVT': 4,
    'MOVF': 4,
    'CLR': 0,
    'STAS': 2
}

# amount of arguments when msb is 1
args1 = {
    "NOP": 0,
    "LDA": 2,
    "STA": 2,
    "ADD": 2,
    "SUB": 2,
    "JMP": 2,
    "JZ": 2,
    "JNZ": 2,
    "AND": 2,
    "OR": 2,
    "HLT": 0,
    "MOV": 4,
    "MOVT": 4,
    "MOVF": 4,
    "CLR": 0,
    "STAS": 2
}

def assemble_from_string(assembly, output_file):
    lines = assembly.split("\n")
    code = []
    for line in lines:
        if ";" in line:
            line = line.split(";")[0]
        if line == "":
            continue

        tokens = line.split()
        if len(tokens) == 0:
            continue
        print(tokens)
        if tokens[0] in no_args:
            instruction = "0" + instruction_set[tokens[0]]
            code.append(instruction)
            continue
        if tokens[0] in instruction_set:
            instruction = instruction_set[tokens[0]]
            if tokens[1] == "#":
                instruction = "0" + instruction
            elif tokens[1] == "@":
                instruction = "1" + instruction
            elif tokens[1] == "-":
                instruction = "0" + instruction
            else:
                print("Expected # or @, got: ", tokens[1])
                continue
            code.append(instruction)
            if "," in tokens[2]:
                args = tokens[2].split(",")
                for arg in args:
                    arg = bin(int(arg))[2:].zfill(16)
                    code.append(arg[:8])
                    code.append(arg[8:])
            else:
                arg = bin(int(tokens[2]))[2:].zfill(16)
                code.append(arg[:8])
                code.append(arg[8:])
        else:
            print("Invalid instruction: ", tokens[0])
    return code, output_file

def assemble_from_file(input_file, output_file):
    with open(input_file, 'r') as f:
        assembly = f.read()
    return assemble_from_string(assembly, output_file)

if __name__ == "__main__":
    code, output_file = assemble_from_file(input_file, output_file)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in code:
            # Write each line to the file and add a newline character
            file.write(line + '\n')
    
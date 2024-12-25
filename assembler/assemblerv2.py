DIRECTORY_INPUT = "programs/asm/"
DIRECTORY_OUTPUT = "programs/bin/"

def read_from_file(input_file):
    with open(input_file, "r") as file:
        return file.readlines()

def preprocess_line(line):
    line = line.strip()
    if ";" in line:
        line = line.split(";")[0]
    if "\n" in line:
        line = line.split("\n")[0]
    while True:
        if line == "":
            break
        if line[0] == " ":
            line = line[1:]
        else:
            break
    return line

def tokenize_line(line):
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
        while True:
            if token == "":
                break
            if token[0] == " ":
                token = token[1:]
            else:
                break
    return tokens

def preprocess(assembly):
    processed_assembly = []
    for line in assembly:
        preprocessed_line = preprocess_line(line)
        if not preprocessed_line == "":
            processed_assembly.append(preprocessed_line)
    return processed_assembly

def tokenize(preprocessed_assembly):
    tokenized_assembly = []
    for  line in preprocessed_assembly:
        tokenized_line = tokenize_line(line)
        tokenized_assembly.append(tokenized_line)
    return tokenized_assembly

def check_line_for_labels(tokens):
    if tokens[0].endswith(":"):
        return tokens[0][:-1]

def collect_labels(tokenized_assembly):
    labels = {}
    address_counter = 0
    for tokens in tokenized_assembly:
        if check_line_for_labels(tokens):
            if check_line_for_labels(tokens) in labels:
                raise ValueError(f"Label {check_line_for_labels(tokens)} is already defined")
            labels[check_line_for_labels(tokens)] = "#" + str(address_counter)
        else:
            address_counter += 4
    return labels

def translate_label_in_tokens(tokens, labels):
    return [labels[token] if token in labels else token for token in tokens]

def translate_label(tokenized_assembly, labels):
    label_translated_tokens = []
    for tokens in tokenized_assembly:
        translated_tokens = translate_label_in_tokens(tokens, labels)
        label_translated_tokens.append(translated_tokens)
    return label_translated_tokens

def remove_labels(label_translated_tokens):
    label_removed_tokens = []
    for tokens in label_translated_tokens:
        remove_token = False
        for token in tokens:
            if token.endswith(":"):
                remove_token = True
        if not remove_token:
            label_removed_tokens.append(tokens)
    return label_removed_tokens

def hexadecimal_to_binary(hexadecimal):
    hexadecimal = hexadecimal[2:]
    return str(bin(int(hexadecimal, 16))[2:].zfill(16))

def decimal_to_binary(decimal):
    decimal = decimal[1:]
    return str(bin(int(decimal))[2:].zfill(16))

def adjust_binary(binary):
    binary = binary[2:]
    return str(bin(int(binary, 2))[2:].zfill(16))

def translate_numbers(label_removed_tokens):
    number_translated_tokens = []
    for tokens in label_removed_tokens:
        number_translated_token = []
        for token in tokens:
            if token.startswith("#"):
                number_translated_token.append(decimal_to_binary(token))
            elif token.startswith("0x"):
                number_translated_token.append(hexadecimal_to_binary(token))
            elif token.startswith("0b"):
                number_translated_token.append(adjust_binary(token))
            else:
                number_translated_token.append(token)
        number_translated_tokens.append(number_translated_token)
    return number_translated_tokens

def get_operand_types(label_removed_tokens):
    all_operand_types = []
    for line in label_removed_tokens:
        operand_types = get_operand_types_from_line(line)
        all_operand_types.append(operand_types)
    return tuple(all_operand_types)

def get_operand_types_from_line(line):
    types = []
    for token in line[1:]:
        if token in registers:
            types.append("reg")
        elif token.startswith("#") or token.startswith("0x") or token.startswith("0b"):
            types.append("imd")
        elif token.startswith("[") and token.endswith("]"):
            if token[1:-1] in registers:
                types.append("indirect reg")
            else:
                types.append("mem")
    return tuple(types)



def assemble(input_file):
    assembly = read_from_file(input_file)
    preprocessed_assembly = preprocess(assembly)
    tokenized_assembly = tokenize(preprocessed_assembly)
    labels = collect_labels(tokenized_assembly)
    label_translated_tokens = translate_label(tokenized_assembly, labels)
    label_removed_tokens = remove_labels(label_translated_tokens)
    number_translated_tokens = translate_numbers(label_removed_tokens)
    machine_code = None
    return machine_code

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
            "mdr": "1111"
        }

non_redundant_mnemonics_opcodes = non_redundant_mnemonics_opcodes = {
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
    "ret": "00011111",
    "halt": "11111111",
}

mnemonics_to_opcodes = {
    "jmp": [
        {("imd",): "00000000"},
        {("reg",): "00001000"}],
    "jeq": [
        {("imd",): "00000001"},
        {("reg",): "00001001"}],
    "jne": [
        {("imd",): "00000010"},
        {("reg",): "00001010"}],
    "inc": [
        {("mem",): "00000011"},
        {("reg",): "00010001"}],
    "dec": [
        {("mem",): "00000100"},
        {("reg",): "00010010"}],
    "load": [
        {("reg", "imd"): "00000101"},
        {("reg", "mem"): "00000110"}],
    "store": [
        {("mem", "reg"): "00000111"},
        {("indirect reg", "reg"): "00001011"}],
    "mov": [
        {("reg", "reg"): "00001100"}],
    "add": [
        {("reg", "reg"): "00001101"}],
    "sub": [
        {("reg", "reg"): "00001110"}],
    "mult": [
        {("reg", "reg"): "00001111"}],
    "div": [
        {("reg", "reg"): "00010000"}],
    "and": [
        {("reg", "reg"): "00010011"}],
    "or": [
        {("reg", "reg"): "00010100"}],
    "xor": [
        {("reg", "reg"): "00010101"}],
    "not": [
        {("reg",): "00010110"}],
    "rol": [
        {("reg", "imd"): "00010111"}],
    "ror": [
        {("reg", "imd"): "00011000"}],
    "cmp": [
        {("reg", "reg"): "00011001"}],
    "shl": [
        {("reg", "imd"): "00011010"}],
    "shr": [
        {("reg", "imd"): "00011011"}],
    "push": [
        {("reg",): "00011100"}],
    "pop": [
        {("reg",): "00011101"}],
    "call": [
        {("imd",): "00011110"}],
    "ret": [
        {(): "00011111"}],
    "halt": [
        {(): "11111111"}],
}

def translate_opcodes(number_translated_tokens, operand_types):
    all_opcode_translated_tokens = []
    for i, tokens in enumerate(number_translated_tokens):
        opcode_translated_tokens = translate_opcodes_from_line(tokens, operand_types[i])
        all_opcode_translated_tokens.append(opcode_translated_tokens)
    return all_opcode_translated_tokens

def translate_opcodes_from_line(tokens, operand_types):
    opcode_translated_tokens = []
    mnemonic = tokens[0]
    opcode = get_opcode(mnemonic, operand_types)
    opcode_translated_tokens.append(opcode)
    for token in tokens[1:]:
        opcode_translated_tokens.append(token)
    return opcode_translated_tokens


def get_opcode(mnemonic, operand_types):
    if mnemonic in mnemonics_to_opcodes:
        possible_opcodes = mnemonics_to_opcodes[mnemonic]
        for possible_opcode in possible_opcodes:
            if operand_types in possible_opcode:
                return possible_opcode[operand_types]
    raise ValueError(f"Invalid operand types '{operand_types}' for mnemonic '{mnemonic}' or mnemonic does not exist")

def translate_register(opcode_translated_tokens):
    all_register_translated_tokens = []
    for tokens in opcode_translated_tokens:
        register_translated_tokens = translate_register_from_line(tokens)
        all_register_translated_tokens.append(register_translated_tokens)
    return all_register_translated_tokens

def translate_register_from_line(tokens):
    register_translated_tokens = []
    for token in tokens:
        if token in registers:
            register_translated_tokens.append(registers[token])
        else:
            register_translated_tokens.append(token)
    return register_translated_tokens

def pad(register_translated_tokens):
    padded_tokens = []
    for tokens in register_translated_tokens:
        missing_tokens = 4 - len(tokens)
        match missing_tokens:
            case 0:
                padded_tokens.append(tokens[0])
                padded_tokens.append(tokens[1])
                padded_tokens.append(tokens[2])
                padded_tokens.append(tokens[3])
            case 1:
                present_lengths = []
                for token in tokens:
                    present_lengths.append(len(token))
                if present_lengths.count(4) == 1:
                    padded_tokens.append(tokens[0])
                    padded_tokens.append(tokens[1])
                    padded_tokens.append("0000")
                    padded_tokens.append(tokens[2])
                elif present_lengths.count(4) == 2:
                    padded_tokens.append(tokens[0])
                    padded_tokens.append(tokens[1])
                    padded_tokens.append(tokens[2])
                    padded_tokens.append("0000000000000000")
            case 2:
                present_lengths = []
                for token in tokens:
                    present_lengths.append(len(token))
                if present_lengths.count(4) == 0:
                    padded_tokens.append(tokens[0])
                    padded_tokens.append("0000")
                    padded_tokens.append("0000")
                    padded_tokens.append(tokens[1])
                elif present_lengths.count(4) == 1:
                    padded_tokens.append(tokens[0])
                    padded_tokens.append(tokens[1])
                    padded_tokens.append("0000")
                    padded_tokens.append("0000000000000000")
            case 3:
                padded_tokens.append(tokens[0])
                padded_tokens.append("0000")
                padded_tokens.append("0000")
                padded_tokens.append("0000000000000000")
            case _:
                raise Exception("Something went wrong...")
    sublists = []
    for i in range(0, len(padded_tokens), 4):
        sublists.append(padded_tokens[i:i+4])
    return sublists

def join_machine_code(machine_code):
    return ["".join(tokens) for tokens in machine_code]

def write_to_file(output_file, machine_code):
    with open(output_file, "w") as file:
        for line in machine_code:
            file.write(line[:8] + "\n")
            file.write(line[8:16] + "\n")
            file.write(line[16:24] + "\n")
            file.write(line[24:] + "\n")

if __name__ == "__main__":
    input_file = DIRECTORY_INPUT +  input("Enter the name of the file you want to assemble: ") + ".masm"
    assembly = read_from_file(input_file)
    preprocessed_assembly = preprocess(assembly)
    tokenized_assembly = tokenize(preprocessed_assembly)
    labels = collect_labels(tokenized_assembly)
    label_translated_tokens = translate_label(tokenized_assembly, labels)
    label_removed_tokens = remove_labels(label_translated_tokens)
    operand_types = get_operand_types(label_removed_tokens)
    number_translated_tokens = translate_numbers(label_removed_tokens)
    opcode_translated_tokens = translate_opcodes(number_translated_tokens, operand_types)
    register_translated_tokens = translate_register(opcode_translated_tokens)
    machine_code = pad(register_translated_tokens)
    machine_code = join_machine_code(machine_code)
    
    output_file = DIRECTORY_OUTPUT + input("Enter the name of your outputfile: ") + ".bin"
    write_to_file(output_file, machine_code)

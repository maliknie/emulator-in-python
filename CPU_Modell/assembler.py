code = []

index = 0
print("Enter values to store in mainmemory: ")
while True:
    value = input("Value (0-255): ")
    if value == "q":
        break
    if int(value) > 255 or int(value) < 0:
        print("Value too big")
        exit()
    value = str(bin(int(value))[2:])
    for i in range(8-len(value)):
        value = "0" + value
    code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('" + value + "'), " + str(index) + ")")
    index += 1 

code.append("controlunit.PC = " + str(index))

print("Enter instruction & operands: ")
while True:
    instruction = input("Instruction: ")
    if instruction == "q":
        break
    operand = input("Operand (for NOP, HLT: 0, for JMP, JZ, JNZ: 0-15, for LDA, STA, ADD, SUB, AND, OR: 0-15): ")
    if int(operand) > 15 or int(operand) < 0:
        print("Operand too big")
        exit()
    operand = str(bin(int(operand))[2:])
    for i in range(4-len(operand)):
        operand = "0" + operand
    match instruction:
        case "NOP":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), " + str(index) + ")")
        case "LDA":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('0001" + operand + "'), " + str(index) + ")")
        case "STA":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('0010" + operand + "')," + str(index) + ")")
        case "ADD":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('0011" + operand + "')," + str(index) + ")")
        case "SUB":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('0100" + operand + "')," + str(index) + ")")
        case "JMP":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('0101" + operand + "')," + str(index) + ")")
        case "JZ":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('0110" + operand + "')," + str(index) + ")")
        case "JNZ":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('0111" + operand + "')," + str(index) + ")")
        case "AND":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('1000" + operand + "')," + str(index) + ")")
        case "OR":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('1001" + operand + "')," + str(index) + ")")
        case "HLT":
            code.append("mainmemory.setValueAtIndex(byte.Byte().setByte('10100000')," + str(index) + ")")
        case _:
            print("Unknown instruction")
            index -= 1
    index += 1

for line in code:
    print(line)
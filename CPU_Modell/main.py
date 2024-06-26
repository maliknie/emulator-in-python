import RAM
import CPU
import byte
import register

RAM_SIZE = 65536 # 0 - 65536
FIRST_K = 10
PRINT_RAM = True
PRINT_FIRST_K = False

mainmemory = RAM.RAM(65536)
controlunit = CPU.CU()
arithmeticandlogicunit = CPU.ALU()
cpu = CPU.CPU(mainmemory, controlunit, arithmeticandlogicunit)



mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 0)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 1)
controlunit.PC = register.Register(byte.Byte().setByte('00000000'), byte.Byte().setByte('00000010'))

# Move x0 to xaaaa
mainmemory.setValueAtIndex(byte.Byte().setByte('10000100'), 2) # SUB
mainmemory.setValueAtIndex(byte.Byte().setByte('00000001'), 3) # Operand
print(mainmemory.getValueAtIndex(3).getByte())
mainmemory.setValueAtIndex(byte.Byte().setByte('10000011'), 4) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00000010'), 5) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('10000010'), 6) # STA
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 7) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('11111111'), 8) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00001010'), 9) # HLT
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 255) # 0x0
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 256) # 0x0

cpu.run()

k = 0
for value in mainmemory.registers:
    if (value.getByte() != "00000000" and PRINT_RAM) or (k < FIRST_K and PRINT_FIRST_K):
        if value.negative:
            print(hex(k), value.getByte(), "negative")
        else:
            print(hex(k), value.getByte())
    k += 1
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
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 3) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00000001'), 4) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('10000011'), 5) # ADD
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 6) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00000010'), 7) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('10000010'), 8) # STA
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 9) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 10) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00001010'), 11) # HLT

cpu.run()

k = 0
for value in mainmemory.registers:
    if (value.getByte() != "00000000" and PRINT_RAM) or (k < FIRST_K and PRINT_FIRST_K):
        if value.negative:
            print(hex(k), value.getByte(), "negative")
        else:
            print(hex(k), value.getByte())
    k += 1
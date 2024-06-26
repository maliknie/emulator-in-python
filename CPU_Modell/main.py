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
mainmemory.setValueAtIndex(byte.Byte().setByte('10000100'), 2)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 3)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000001'), 4)
mainmemory.setValueAtIndex(byte.Byte().setByte('10000011'), 5)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 6)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000010'), 7)
mainmemory.setValueAtIndex(byte.Byte().setByte('10000010'), 8)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 9)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 10)
mainmemory.setValueAtIndex(byte.Byte().setByte('00001010'), 11) 

cpu.run()

k = 0
for value in mainmemory.registers:
    if (value.getByte() != "00000000" and PRINT_RAM) or (k < FIRST_K and PRINT_FIRST_K):
        if value.negative:
            print(hex(k), value.getByte(), value.getInt(), "negative")
        else:
            print(hex(k), value.getByte(), value.getInt())
    k += 1
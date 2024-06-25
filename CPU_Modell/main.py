import RAM
import CPU
import byte
import register

RAM_SIZE = 65536 # 0 - 65536
PRINT_RAM = True

mainmemory = RAM.RAM(65536)
controlunit = CPU.CU()
arithmeticandlogicunit = CPU.ALU()
cpu = CPU.CPU(mainmemory, controlunit, arithmeticandlogicunit)



mainmemory.setValueAtIndex(byte.Byte().setByte('11110000'), 0)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 1)
controlunit.PC = register.Register(byte.Byte().setByte('00000000'), byte.Byte().setByte('00000010'))

# Move x0 to xaaaa
mainmemory.setValueAtIndex(byte.Byte().setByte('00001011'), 2) # MOV
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 3) # Address big to start index
mainmemory.setValueAtIndex(byte.Byte().setByte('01100100'), 4) # Address small to start index
mainmemory.setValueAtIndex(byte.Byte().setByte('00001010'), 5) # HLT

mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 100) # Adress big to the value we want to move (start index)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 101) # Adress small to the value we want to move
mainmemory.setValueAtIndex(byte.Byte().setByte('11111111'), 102) # Address big to the destination
mainmemory.setValueAtIndex(byte.Byte().setByte('11111111'), 103) # Address small to the destination

cpu.run()

k = 0
for value in mainmemory.registers:
    if (value.getByte() != "00000000" and PRINT_RAM) or k < 10:
        print(hex(k), value.getByte())
    k += 1
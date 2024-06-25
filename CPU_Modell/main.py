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



mainmemory.setValueAtIndex(byte.Byte().setByte('00000111'), 0)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000010'), 1)
controlunit.PC = register.Register(byte.Byte().setByte('00000000'), byte.Byte().setByte('00000010'))

# Move x0 to xaaaa
mainmemory.setValueAtIndex(byte.Byte().setByte('00001011'), 2) # MOV
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 3) # Operand 1 (x6)1 (aaf1)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000110'), 4) # Operand 2 (x6)2 (aaf2)
mainmemory.setValueAtIndex(byte.Byte().setByte('00001010'), 5) # HLT

mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 6) # x0 big (af1)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 7) # x0 small (af2)
mainmemory.setValueAtIndex(byte.Byte().setByte('10101010'), 8) # xaaaa big (at1)
mainmemory.setValueAtIndex(byte.Byte().setByte('10101010'), 9) # xaaaa small (at2)

cpu.run()

k = 0
for value in mainmemory.registers:
    if value.getByte() != "00000000" and PRINT_RAM:
        print(hex(k), value.getByte())
    k += 1
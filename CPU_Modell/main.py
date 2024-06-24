import RAM
import CPU
import byte

mainmemory = RAM.RAM(16)
controlunit = CPU.CU()
arithmeticandlogicunit = CPU.ALU()
cpu = CPU.CPU(mainmemory, controlunit, arithmeticandlogicunit)



mainmemory.setValueAtIndex(byte.Byte().setByte('00000001'), 0)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000010'), 1)
controlunit.PC = byte.Byte().setByte('00000010')
mainmemory.setValueAtIndex(byte.Byte().setByte('00000011'), 2) # ADD
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 3) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00000011'), 4) # ADD
mainmemory.setValueAtIndex(byte.Byte().setByte('00000001'), 5) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00000010'), 6) # STA
mainmemory.setValueAtIndex(byte.Byte().setByte('00001111'), 7) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00001010'), 8) # HLT

cpu.run()

k = 0
for value in mainmemory.registers:
    print(k, (int(value.getByte(), 2)))
    k += 1
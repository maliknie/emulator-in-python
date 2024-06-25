import RAM
import CPU
import byte
import register

RAM_SIZE = 65536 # 0 - 65536

mainmemory = RAM.RAM(65536)
controlunit = CPU.CU()
arithmeticandlogicunit = CPU.ALU()
cpu = CPU.CPU(mainmemory, controlunit, arithmeticandlogicunit)



mainmemory.setValueAtIndex(byte.Byte().setByte('00000001'), 0)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000010'), 1)
controlunit.PC = register.Register(byte.Byte().setByte('00000000'), byte.Byte().setByte('00000010'))
mainmemory.setValueAtIndex(byte.Byte().setByte('00000011'), 2) # ADD
mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 3) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00000011'), 4) # ADD
mainmemory.setValueAtIndex(byte.Byte().setByte('00000001'), 5) # Operand
mainmemory.setValueAtIndex(byte.Byte().setByte('00000010'), 6) # STA
mainmemory.setValueAtIndex(byte.Byte().setByte('11111111'), 7) # Operand 1
mainmemory.setValueAtIndex(byte.Byte().setByte('11111111'), 8) # Operand 2
mainmemory.setValueAtIndex(byte.Byte().setByte('00001010'), 9) # HLT

cpu.run()

k = 0
for value in mainmemory.registers:
    if value.getByte() != "00000000":
        print(hex(k), value.getByte())
    k += 1
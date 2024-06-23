import RAM
import CPU
import byte

mainmemory = RAM.RAM(16)
controlunit = CPU.CU()
arithmeticandlogicunit = CPU.ALU()
cpu = CPU.CPU(mainmemory, controlunit, arithmeticandlogicunit)



mainmemory.setValueAtIndex(byte.Byte().setByte('00000001'), 0)
mainmemory.setValueAtIndex(byte.Byte().setByte('00000010'), 1)
controlunit.PC = 2
mainmemory.setValueAtIndex(byte.Byte().setByte('00110000'), 2)
mainmemory.setValueAtIndex(byte.Byte().setByte('00110001'), 3)
mainmemory.setValueAtIndex(byte.Byte().setByte('00101111'), 4)
mainmemory.setValueAtIndex(byte.Byte().setByte('10100000'), 5)
for value in mainmemory.registers:
    print(value.getByte())

print("")
print("")
print("")

cpu.run()

for value in mainmemory.registers:
    print((int(value.getByte(), 2)))
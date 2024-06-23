import RAM
import byte
class CPU():
    def __init__(self, mainmemory, controlunit, alunit):
        if not isinstance(mainmemory, RAM.RAM) or not isinstance(controlunit, CU) or not isinstance(alunit, ALU):
            raise Exception("CPU Error: Arguments given aren't the correct objects.")
        self.mm = mainmemory
        self.cu = controlunit
        self.alu = alunit

    def run(self):
        while True:
            self.cu.fetch(self.mm)
            match self.cu.IR.getByte()[:4]:
                case "0000":
                    self.NOP()
                case "0001":
                    self.LDA(int(self.cu.IR.getByte()[4:], 2))
                case "0010":
                    self.STA(int(self.cu.IR.getByte()[4:], 2))
                case "0011":
                    self.ADD(int(self.cu.IR.getByte()[4:], 2))
                case "0100":
                    self.SUB(int(self.cu.IR.getByte()[4:], 2))
                case "0101":
                    self.JMP(int(self.cu.IR.getByte()[4:], 2))
                case "0110":
                    self.JZ(int(self.cu.IR.getByte()[4:], 2))
                case "0111":
                    self.JNZ(int(self.cu.IR.getByte()[4:], 2))
                case "1000":
                    self.AND(int(self.cu.IR.getByte()[4:], 2))
                case "1001":
                    self.OR(int(self.cu.IR.getByte()[4:], 2))
                case "1010":
                    break
                case _:
                    raise Exception("CPU Error: Unknown Instruction")


    def NOP(self):
        pass
    def LDA(self, adress):
        self.alu.accumulator = self.mm.getValueAtIndex
    def STA(self, adress):
        self.mm.setValueAtIndex(self.alu.accumulator, adress)
    def ADD(self, adress):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm.getValueAtIndex(adress), byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = (self.alu.accumulator).add(self.mm.getValueAtIndex(adress))
    def SUB(self, adress):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm.getValueAtIndex(adress), byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = (self.alu.accumulator).substract(self.mm.getValueAtIndex(adress))
    def JMP(self, value):
        self.cu.PC = value
    def JZ(self, value):
        if not isinstance(self.alu.accumulator, byte.Byte):
            raise Exception("Accumulator doesn't contain byte")
        if self.alu.accumulator.getByte() == "00000000":
            self.cu.PC = value
    def JNZ(self, value):
        if not isinstance(self.alu.accumulator, byte.Byte):
            raise Exception("Accumulator doesn't contain byte")
        if self.alu.accumulator.getByte() != "00000000":
            self.cu.PC = value
    def AND(self, adress):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm.getValueAtIndex(adress), byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = self.alu.accumulator.bitwise_and(self.mm.getValueAtIndex(adress))
    def OR(self, adress):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm.getValueAtIndex, byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = self.alu.accumulator.bitwise_or(self.mm.getValueAtIndex(adress))
    def HLT(self):
        exit()

class CU():
    def __init__(self):
        self.PC = 0
        self.IR = byte.Byte()
    def reset(self):
        self.PC = 0
        self.IR = byte.Byte()
    def fetch(self, memory):
        if not isinstance(memory, RAM.RAM):
            raise Exception("Fetch Error")
        self.IR = memory.getValueAtIndex(self.PC)
        self.PC += 1
        
        
class ALU():
    def __init__(self):
        self.accumulator = byte.Byte()
        
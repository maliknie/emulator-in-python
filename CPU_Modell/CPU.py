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
        print("Running CPU")
        while True:
            self.cu.fetch(self.mm)
            self.cu.inc_pc()

            match self.cu.IR.getByte():
                case "00000000":
                    self.NOP()
                case "00000001":
                    self.LDA(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.inc_pc()
                case "00000010":
                    self.STA(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.inc_pc()
                case "00000011":
                    self.ADD(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.inc_pc()
                case "00000100":
                    self.SUB(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.inc_pc()
                case "00000101":
                    self.JMP(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.inc_pc()
                case "00000110":
                    self.JZ(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.inc_pc()
                case "00000111":
                    self.JNZ(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.inc_pc()
                case "00001000":
                    self.AND(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.inc_pc()
                case "00001001":
                    self.OR(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.inc_pc()
                case "00001010":
                    break
                case _:
                    print("Problematic Byte: ", self.cu.IR.getByte())
                    raise Exception("CPU Error: Unknown command")
            

    def NOP(self):
        pass
    def LDA(self, adress: "byte.Byte"):
        self.alu.accumulator = self.mm.getValueAtIndex(adress.getInt())
    def STA(self, adress: "byte.Byte"):
        self.mm.setValueAtIndex(self.alu.accumulator, adress.getInt())
    def ADD(self, adress: "byte.Byte"):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm.getValueAtIndex(adress.getInt()), byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = (self.alu.accumulator).add(self.mm.getValueAtIndex(adress.getInt()))
    def SUB(self, adress: "byte.Byte"):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm.getValueAtIndex(adress.getInt()), byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = (self.alu.accumulator).substract(self.mm.getValueAtIndex(adress.getInt()))
    def JMP(self, adress: "byte.Byte"):
        self.cu.PC = adress
    def JZ(self, adress: "byte.Byte"):
        if not isinstance(self.alu.accumulator, byte.Byte):
            raise Exception("Accumulator doesn't contain byte")
        if self.alu.accumulator.getInt() == 0:
            self.cu.PC = adress
    def JNZ(self, adress: "byte.Byte"):
        if not isinstance(self.alu.accumulator, byte.Byte):
            raise Exception("Accumulator doesn't contain byte")
        if self.alu.accumulator.getInt() != 0:
            self.cu.PC = adress
    def AND(self, adress: "byte.Byte"):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm.getValueAtIndex(adress.getInt()), byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = self.alu.accumulator.bitwise_and(self.mm.getValueAtIndex(adress.getInt()))
    def OR(self, adress: "byte.Byte"):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm.getValueAtIndex(adress.getInt()), byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = self.alu.accumulator.bitwise_or(self.mm.getValueAtIndex(adress.getInt()))
    def HLT(self):
        exit()

class CU():
    def __init__(self):
        self.PC = byte.Byte()
        self.IR = byte.Byte()
    def reset(self):
        self.PC = byte.Byte()
        self.IR = byte.Byte()
    def fetch(self, memory: "RAM.RAM"):
        if not isinstance(memory, RAM.RAM):
            raise Exception("Fetch Error")
        self.IR = memory.getValueAtIndex(self.PC.getInt())
        print("Fetched: ", self.IR.getByte())
    def inc_pc(self):
        self.PC = self.PC.inc()
        return self.PC
            
class ALU():
    def __init__(self):
        self.accumulator = byte.Byte()
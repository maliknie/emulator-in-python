import RAM
import byte
import register

class CPU():
    def __init__(self, mainmemory: "RAM.RAM", controlunit: "CU", alunit: "ALU"):
        self.mm = mainmemory
        self.cu = controlunit
        self.alu = alunit

    def run(self):
        print("Running CPU")
        while True:
            self.cu.fetch(self.mm)
            self.cu.incPC()

            match self.cu.IR.getByte():
                case "00000000":
                    self.NOP()
                case "00000001":
                    self.LDA()
                case "00000010":
                    self.STA()
                case "00000011":
                    self.ADD(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.incPC()
                case "00000100":
                    self.SUB(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.incPC()
                case "00000101":
                    self.JMP(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.incPC()
                case "00000110":
                    self.JZ(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.incPC()
                case "00000111":
                    self.JNZ(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.incPC()
                case "00001000":
                    self.AND(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.incPC()
                case "00001001":
                    self.OR(self.mm.getValueAtIndex(self.cu.PC.getInt()))
                    self.cu.incPC()
                case "00001010":
                    print("HLT reached")
                    break
                case _:
                    print("Problematic Byte: ", self.cu.IR.getByte())
                    raise Exception("CPU Error: Unknown command")
            

    def NOP(self):
        pass
    def LDA(self):
        pc = self.cu.PC
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        self.alu.accumulator = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte))
        self.cu.incPC(2)
    def STA(self):
        pc = self.cu.PC
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        print("adress: ", big_adress_byte.getByte(), small_adress_byte.getByte())
        self.mm.setValueAtIndex(self.alu.accumulator, byte.joinBytesToInt(big_adress_byte, small_adress_byte))
        self.cu.incPC(2)
    def ADD(self, adress: "byte.Byte"):
        self.alu.accumulator = (self.alu.accumulator).add(self.mm.getValueAtIndex(adress.getInt()))
    def SUB(self, adress: "byte.Byte"):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm.getValueAtIndex(adress.getInt()), byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = (self.alu.accumulator).substract(self.mm.getValueAtIndex(adress.getInt()))
    def JMP(self, adress: "byte.Byte"):
        self.cu.PC = register.Register(self.mm.getValueAtIndex(adress.getInt()), self.mm.getValueAtIndex(adress.getInt() + 1))
    def JZ(self, adress: "byte.Byte"):
        if not isinstance(self.alu.accumulator, byte.Byte):
            raise Exception("Accumulator doesn't contain byte")
        if self.alu.accumulator.getInt() == 0:
            self.cu.PC = register.Register(self.mm.getValueAtIndex(adress.getInt()), self.mm.getValueAtIndex(adress.getInt() + 1))
    def JNZ(self, adress: "byte.Byte"):
        if not isinstance(self.alu.accumulator, byte.Byte):
            raise Exception("Accumulator doesn't contain byte")
        if self.alu.accumulator.getInt() != 0:
            self.cu.PC = register.Register(self.mm.getValueAtIndex(adress.getInt()), self.mm.getValueAtIndex(adress.getInt() + 1))
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
    def __init__(self) -> None:
        self.PC = register.Register()
        self.IR = byte.Byte()
    def reset(self) -> None:
        self.PC = register.Register()
        self.IR = byte.Byte()
    def fetch(self, memory: "RAM.RAM") -> None:
        if not isinstance(memory, RAM.RAM):
            raise Exception("Fetch Error")
        self.IR = memory.getValueAtIndex(self.PC.getInt())
        print("Fetched: ", self.IR.getByte())
    def incPC(self, amount: int = 1) -> "byte.Byte":
        self.PC.incRegister(amount)     
        return self.PC
            
class ALU():
    def __init__(self):
        self.accumulator = byte.Byte()
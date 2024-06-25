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
                    self.ADD()
                case "00000100":
                    self.SUB()
                case "00000101":
                    self.JMP()
                case "00000110":
                    self.JZ()
                case "00000111":
                    self.JNZ()
                case "00001000":
                    self.AND()
                case "00001001":
                    self.OR()
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
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1) # Bytes im nächsten und übernächsten Speicherplatz werden zusammengefügt
        self.alu.accumulator = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte))
        self.cu.incPC(2)
    def STA(self):
        pc = self.cu.PC
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        print("adress: ", big_adress_byte.getByte(), small_adress_byte.getByte())
        self.mm.setValueAtIndex(self.alu.accumulator, byte.joinBytesToInt(big_adress_byte, small_adress_byte))
        self.cu.incPC(2)
    def ADD(self):
        pc = self.cu.PC
        next_byte = self.mm.getValueAtIndex(pc.getInt())
        self.alu.accumulator = self.alu.accumulator.add(next_byte)
        self.cu.incPC()
    def SUB(self):
        pc = self.cu.PC
        next_byte = self.mm.getValueAtIndex(pc.getInt())
        self.alu.accumulator = self.alu.accumulator.substract(next_byte)
        self.cu.incPC()
    def JMP(self):
        pc = self.cu.PC
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        self.cu.PC.setRegisterFromBytes(big_adress_byte, small_adress_byte)
    def JZ(self):
        pc = self.cu.PC
        if self.alu.accumulator.getInt() == 0:
            big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
            small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            self.cu.PC.setRegisterFromBytes(big_adress_byte, small_adress_byte)
        else:
            self.cu.incPC(2)
    def JNZ(self):
        pc = self.cu.PC
        if self.alu.accumulator.getInt() != 0:
            big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
            small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            self.cu.PC.setRegisterFromBytes(big_adress_byte, small_adress_byte)
        else:
            self.cu.incPC(2)
    def AND(self):
        pc = self.cu.PC
        next_byte = self.mm.getValueAtIndex(pc.getInt())
        self.alu.accumulator = self.alu.accumulator.bitwise_and(next_byte)
        self.cu.incPC()
    def OR(self):
        pc = self.cu.PC
        next_byte = self.mm.getValueAtIndex(pc.getInt())
        self.alu.accumulator = self.alu.accumulator.bitwise_or(next_byte)
        self.cu.incPC()
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
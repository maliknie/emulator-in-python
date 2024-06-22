import RAM
import byte
class CPU():
    def __init__(self, mainmemory, controlunit, alunit):
        if not isinstance(mainmemory, RAM.RAM) or not isinstance(controlunit, CU) or not isinstance(alunit, ALU):
            raise Exception("CPU Error: Arguments given arem't the correct objects.")
        self.mm = mainmemory
        self.cu = controlunit
        self.alu = alunit

    def NOP(self):
        pass
    def LDA(self, adress):
        self.alu.accumulator = self.mm[adress]
    def STA(self, adress):
        self.mm[adress] = self.alu.accumulator
    def ADD(self, adress):
        self.alu.accumulator += self.mm[adress]
    def SUB(self, adress):
        self.alu.accumulator -= self.mm[adress]
    def JMP(self, value):
        self.cu.PC = value
    def JZ(self, value):
        if self.alu.accumulator == 0:   
            self.cu.PC = value
    def JNZ(self, value):
        if self.alu.accumulator != 0:   
            self.cu.PC = value
    def AND(self, adress):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm[adress]):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = self.alu.accumulator.bitwise_and(self.mm[adress])
    def OR(self, adress):
        if not isinstance(self.alu.accumulator, byte.Byte) or not isinstance(self.mm[adress], byte.Byte):
            raise Exception("Accumulator or adresse in main memory doesn't contain byte")
        self.alu.accumulator = self.alu.accumulator.bitwise_or(self.mm[adress])
    def HLT(self):
        exit()       

class CU(CPU):
    def __init__(self):
        super().__init__()
        self.PC = 0
        self.IR = ""
    def reset(self):
        self.PC = 0
        self.IR = ""
    def fetch(self, memory):
        if not isinstance(memory, RAM.RAM):
            raise Exception("Fetch Error")
        self.IR = memory[self.PC]
        self.PC += 1
        

        
class ALU(CPU):
    def __init__(self):
        super().__init__()
        self.mode = 0
        self.accumulator = 0
    def calculate(self, value):
        if self.mode == 0:
            self.accumulator = value
        elif self.mode == 1:
            self.accumulator += value
        
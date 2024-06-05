import RAM
import byte
class CPU():
    def __init__(self):
        pass

    def NOP(self):
        pass
    def LDA(self, alu, memory, adress):
        if not isinstance(alu, ALU) or not isinstance(memory, RAM.RAM):
            Exception("LDA Error")
        alu.accumulator = memory[adress]
    def STA(self, alu, memory, adress):
        if not isinstance(alu, ALU) or not isinstance(memory, RAM.RAM):
            Exception("STA Error")
        memory[adress] = alu.accumulator
    def ADD(self, alu, memory, adress):
        if not isinstance(alu, ALU) or not isinstance(memory, RAM.RAM):
            Exception("ADD Error")
        alu.accumulator += memory[adress]
    def SUB(self, alu, memory, adress):
        if not isinstance(alu, ALU) or not isinstance(memory, RAM.RAM):
            Exception("SUB Error")
        alu.accumulator -= memory[adress]
    def JMP(self, cu, value):
        if not isinstance(cu, CU):
            Exception("JMP Error")
        cu.PC = value
    def JZ(self, cu, value, alu):
        if not isinstance(cu, CU) or not isinstance(alu, ALU):
            Exception("JZ Error")
        if alu.accumulator == 0:   
            cu.PC = value
    def JNZ(self, cu, value, alu):
        if not isinstance(cu, CU) or not isinstance(alu, ALU):
            Exception("JZ Error")
        if alu.accumulator != 0:   
            cu.PC = value
    def AND(self, alu, memory, adresse):
        if not isinstance(alu, ALU) or not isinstance(memory, RAM.RAM):
            Exception("AND Error")
        if not isinstance(alu.accumulator, byte.Byte) or not isinstance(memory[adresse]):
            Exception("Accumulator doesn't contain byte")
        alu.accumulator = alu.accumulator.bitwise_and(memory[adresse])
    def OR(self, alu, memory, adresse):
        if not isinstance(alu, ALU) or not isinstance(memory, RAM.RAM):
            Exception("AND Error")
        if not isinstance(alu.accumulator, byte.Byte) or not isinstance(memory[adresse], byte.Byte):
            Exception("Accumulator doesn't contain byte")
        alu.accumulator = alu.accumulator.bitwise_or(memory[adresse])
    def HLT(self):
        pass
        
    



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
            Exception("Fetch Error")
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
        
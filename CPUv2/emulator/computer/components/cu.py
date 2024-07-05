class CU:
    def __init__(self, cpu) -> None:
        self.cpu = cpu

    def fetch(self):
        pc = int(self.cpu.pc, 2)
        instruction = self.cpu.memory.read(pc)
        self.cpu.ir = instruction
        pc += 4
        pc %= len(self.cpu.memory.memory_cells)
        self.cpu.pc = bin(pc)[2:].zfill(16)




    def decode(self):
        instruction = self.cpu.ir
        opcode = instruction[:8]
        operand1 = instruction[8:12]
        operand2 = instruction[12:16]
        operand3 = instruction[16:32]


    def callALU(self, op, a, b):
        self.cpu.alu.op = op
        self.cpu.alu.a = a
        self.cpu.alu.b = b
        self.cpu.alu.execute()

class Instructions:
    @staticmethod # jump #imd
    def i00000000(cpu, operand1, operand2, operand3):
        cpu.pc = operand3
    @staticmethod # jeq #imd
    def i00000001(cpu, operand1, operand2, operand3):
        if cpu.flags[15] == "1":
            cpu.pc = operand3
    @staticmethod # jnq #imd
    def i00000010(cpu, operand1, operand2, operand3):
        if cpu.flags[15] == "0":
            cpu.pc = operand3
    @staticmethod # inc [mem]
    def i00000011(cpu, opernad1, operand2, operand3):
        memory_address = int(operand3, 2)
        value = int(cpu.memory.read(memory_address), 2)
        value += 1
        value %= 256
        value = bin(value)[2:].zfill(8)
        cpu.memory.write(memory_address, value)
    @staticmethod # dec [mem]
    def i00000100(cpu, operand1, operand2, operand3):
        memory_address = int(operand3, 2)
        value = int(cpu.memory.read(memory_address), 2)
        value -= 1
        value %= 256
        value = bin(value)[2:].zfill(8)
        cpu.memory.write(memory_address, value)
    @staticmethod # load #imd
    def i00000101(cpu, operand1, operand2, operand3):
        value = int(operand3, 2)
        cpu.access_register(operand1, value)
    @staticmethod # load [mem]
    def i00000110(cpu, operand1, operand2, operand3):
        memory_address = int(operand3, 2)
        value = cpu.memory.read(memory_address)
        cpu.access_register(operand1, value)
    @staticmethod # store [mem]
    def i00000111(cpu, operand1, operand2, operand3):
        memory_address = int(operand3, 2)
        value = cpu.access_register(operand1)
        cpu.memory.write(memory_address, value)
    @staticmethod # jmp reg
    def i00001000(cpu, operand1, operand2, operand3):
        reg = cpu.access_register(operand1)
        cpu.pc = reg
    @staticmethod # jeq reg
    def i00001001(cpu, operand1, operand2, operand3):
        if cpu.flags[15] == "1":
            reg = cpu.access_register(operand1)
            cpu.pc = reg
    @staticmethod # jne reg
    def i00001010(cpu, operand1, operand2, operand3):
        if cpu.flags[15] == "0":
            reg = cpu.access_register(operand1)
            cpu.pc = reg
    @staticmethod # store [reg1] reg2
    def i00001011(cpu, operand1, operand2, operand3):
        address = cpu.access_register(operand1)
        address = int(address, 2)
        value = cpu.access_register(operand2)
        cpu.memory.write(value, address)

    @staticmethod # move reg1 reg 2
    def i00001100(cpu, operand1, operand2, operand3):
        reg2 = cpu.access_register(operand2)
        cpu.access_register(operand1, reg2)
    @staticmethod # add reg1 reg2
    def i00001101(cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        value = int(reg1, 2) + int(reg2, 2)
        negative_check = value < 0
        value %= 256
        value = value * (-1) if negative_check else value
        value = bin(value)[2:].zfill(16)
        cpu.access_register(operand1, value)
    @staticmethod # sub reg1 reg2
    def i00001110(cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        value = int(reg1, 2) - int(reg2, 2)
        negative_check = value < 0
        value %= 256
        value = value * (-1) if negative_check else value
        value = bin(value)[2:].zfill(16)
        cpu.access_register(operand1, value)
    @staticmethod # mult reg1 reg2
    def i00001111(cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        value = int(reg1, 2) * int(reg2, 2)
        negative_check = value < 0
        value %= 65536
        value = value * (-1) if negative_check else value
        value = bin(value)[2:].zfill(32)
        value_high = value[:16]
        value_low = value[16:]
        cpu.access_register(operand1, value_high)
        cpu.access_register(operand2, value_low)
    @staticmethod # div reg1 reg2
    def i00010000(cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        value = int(reg2, 2) / int(reg1, 2)
        modulo = int(reg2, 2) % int(reg1, 2)
        negative_check = value < 0
        value %= 256
        value = value * (-1) if negative_check else value
        value = bin(value)[2:].zfill(16)
        modulo %= 256
        modulo = bin(modulo)[2:].zfill(16)
        
        cpu.access_register(operand1, value)
        cpu.access_register(operand2, modulo)
    @staticmethod
    def i00010001(cpu, operand1, operand2, operand3):
        reg = cpu.access_register(operand1)
        value = int(reg, 2)
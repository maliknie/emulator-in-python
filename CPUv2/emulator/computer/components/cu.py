import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))
from libraries.binary_lib import mbin, mint, set_flag, check_flag

class CU:
    def __init__(self, cpu) -> None:
        self.cpu = cpu
    
    # Holt 4 Bytes aus dem Speicher und speichert sie im IR
    def fetch(self):
        pc = int(self.cpu.pc, 2)
        instruction = self.cpu.computer.memory.read(pc) + self.cpu.computer.memory.read(pc + 1) + self.cpu.computer.memory.read(pc + 2) + self.cpu.computer.memory.read(pc + 3)
        self.cpu.ir = instruction
        pc += 4
        pc %= len(self.cpu.computer.memory.memory_cells)
        self.cpu.pc = bin(pc)[2:].zfill(16)

    # Teilt die Instruktion in Opcode und Operanden auf
    def decode(self):
        instruction = self.cpu.ir
        self.opcode, self.operand1, self.operand2, self.operand3 = instruction[:8], instruction[8:12], instruction[12:16], instruction[16:32]
        """
        print("_________________________")
        print("Decoded instruction: ")
        print("Opcode: ", self.opcode)
        print("Operand1: ", self.operand1, mint(self.operand1))
        print("Operand2: ", self.operand2, mint(self.operand2))
        print("Operand3: ", self.operand3, mint(self.operand3))
        print("_________________________")"""
    
    # Führt die Instruktion aus
    def execute(self):
        match self.opcode:
            case "00000000":
                Instructions.i00000000(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00000001":
                Instructions.i00000001(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00000010":
                Instructions.i00000010(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00000011":
                Instructions.i00000011(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00000100":
                Instructions.i00000100(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00000101":
                Instructions.i00000101(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00000110":
                Instructions.i00000110(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00000111":
                Instructions.i00000111(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00001000":
                Instructions.i00001000(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00001001":
                Instructions.i00001001(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00001010":
                Instructions.i00001010(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00001011":
                Instructions.i00001011(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00001100":
                Instructions.i00001100(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00001101":
                Instructions.i00001101(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00001110":
                Instructions.i00001110(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00001111":
                Instructions.i00001111(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00010000":
                Instructions.i00010000(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00010001":
                Instructions.i00010001(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00010010":
                Instructions.i00010010(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00010011":
                Instructions.i00010011(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00010100":
                Instructions.i00010100(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00010101":
                Instructions.i00010101(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00010110":
                Instructions.i00010110(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00010111":
                Instructions.i00010111(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00011000":
                Instructions.i00011000(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00011001":
                Instructions.i00011001(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00011010":
                Instructions.i00011010(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "00011011":
                Instructions.i00011011(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "11111111":
                Instructions.i11111111(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case "debuggin":
                Instructions.print_registers(self, self.cpu, self.operand1, self.operand2, self.operand3)
            case _:
                raise ValueError("Invalid opcode: " + self.opcode + "\n" + "Program counter: " + str(int(self.cpu.pc, 2)))

    def callALU(self, op, a, b, bit_length = 16):
        self.cpu.alu.execute(op, a, b, bit_length)

# Implementation der Instruktionen
class Instructions:

    @staticmethod # jump #imd
    def i00000000(cu, cpu, operand1, operand2, operand3):
        cpu.pc = operand3
        
    @staticmethod # jeq #imd
    def i00000001(cu, cpu, operand1, operand2, operand3):
        if check_flag(cpu.flags, 15):
            cpu.pc = operand3

    @staticmethod # jne #imd
    def i00000010(cu, cpu, operand1, operand2, operand3):
        if not check_flag(cpu.flags, 15):
            cpu.pc = operand3

    @staticmethod # inc [mem]
    def i00000011(cu, cpu, opernad1, operand2, operand3):
        memory_address = int(operand3, 2)
        value = cpu.computer.memory.read(memory_address)
        cu.callALU("add", value, "00000001", 8)
        value = cpu.access_register("1100")[8:]
        cpu.computer.memory.write(memory_address, value)

    @staticmethod # dec [mem]
    def i00000100(cu, cpu, operand1, operand2, operand3):
        memory_address = int(operand3, 2)
        value = cpu.computer.memory.read(memory_address)
        cu.callALU("sub", value, "00000001", 8)
        value = cpu.access_register("1100")[8:]
        cpu.computer.memory.write(memory_address, value)

    @staticmethod # load #imd
    def i00000101(cu, cpu, operand1, operand2, operand3):
        if operand1 in cpu.reg32bit:
            operand3 = operand3.zfill(32)
        cpu.access_register(operand1, operand3)

    @staticmethod # load [mem]
    def i00000110(cu, cpu, operand1, operand2, operand3):
        memory_address = mint(operand3)
        value = cpu.computer.memory.read(memory_address) + cpu.computer.memory.read(memory_address + 1)
        if operand1 in cpu.reg32bit:
            value += cpu.computer.memory.read(memory_address + 2) + cpu.computer.memory.read(memory_address + 3)
        cpu.access_register(operand1, value)

    @staticmethod # store [mem]
    def i00000111(cu, cpu, operand1, operand2, operand3):
        memory_address = mint(operand3)
        value = cpu.access_register(operand1)
        cpu.computer.memory.write(memory_address, value[:8])
        cpu.computer.memory.write(memory_address + 1, value[8:16])
        if operand1 in cpu.reg32bit:
            cpu.computer.memory.write(memory_address + 2, value[16:24])
            cpu.computer.memory.write(memory_address + 3, value[24:32])

    @staticmethod # jmp reg
    def i00001000(cu, cpu, operand1, operand2, operand3):
        reg = cpu.access_register(operand1)
        cpu.pc = reg

    @staticmethod # jeq reg
    def i00001001(cu, cpu, operand1, operand2, operand3):
        if check_flag(cpu.flags, 15):
            reg = cpu.access_register(operand1)
            cpu.pc = reg

    @staticmethod # jne reg
    def i00001010(cu, cpu, operand1, operand2, operand3):
        if not check_flag(cpu.flags, 15):
            reg = cpu.access_register(operand1)
            cpu.pc = reg

    @staticmethod # store [reg1] reg2
    def i00001011(cu, cpu, operand1, operand2, operand3):
        address = cpu.access_register(operand1)
        address = mint(address)
        value = cpu.access_register(operand2)
        cpu.computer.memory.write(address, value[:8])
        cpu.computer.memory.write(address + 1, value[8:16])
        if operand2 in cpu.reg32bit:
            cpu.computer.memory.write(address + 2, value[16:24])
            cpu.computer.memory.write(address + 3, value[24:32])

    @staticmethod # move reg1 reg 2
    def i00001100(cu, cpu, operand1, operand2, operand3):
        if operand1 in cpu.reg32bit and operand2 in cpu.reg32bit:
            reg2 = cpu.access_register(operand2)
            cpu.access_register(operand1, reg2)
        elif operand1 in cpu.reg32bit and not operand2 in cpu.reg32bit:
            reg2 = cpu.access_register(operand2)
            reg2 = reg2.zfill(32)
            cpu.access_register(operand1, reg2)
        elif not operand1 in cpu.reg32bit and operand2 in cpu.reg32bit:
            reg2 = cpu.access_register(operand2)[:16]
            cpu.access_register(operand1, reg2)
        else:
            reg2 = cpu.access_register(operand2)
            cpu.access_register(operand1, reg2)

    @staticmethod # add reg1 reg2
    def i00001101(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("add", reg1, reg2, 16)
        value = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, value)

    @staticmethod # sub reg1 reg2
    def i00001110(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("sub", reg1, reg2, 16)
        value = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, value)

    @staticmethod # mult reg1 reg2
    def i00001111(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("mul", reg1, reg2, 32)
        value_high = cpu.access_register("1100")[:16]
        value_low = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value_high)
        cpu.access_register(operand2, value_low)

    @staticmethod # div reg1 reg2
    def i00010000(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("div", reg1, reg2, 16)
        value = cpu.access_register("1100")[16:]
        modulo = cpu.access_register("1100")[:16]
        
        cpu.access_register(operand1, value)
        cpu.access_register(operand2, modulo)

    @staticmethod # inc reg
    def i00010001(cu, cpu, operand1, operand2, operand3):
        reg = cpu.access_register(operand1)
        cu.callALU("add", reg, "00000001", 16)
        value = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, value)

    @staticmethod # dec reg
    def i00010010(cu, cpu, operand1, operand2, operand3):
        #print("dec reg", operand1)
        reg = cpu.access_register(operand1)
        cu.callALU("sub", reg, "00000001", 16)
        value = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, value)

    @staticmethod # and reg1 reg2
    def i00010011(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("and", reg1, reg2, 16)
        value = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, value)

    @staticmethod # or reg1 reg2
    def i00010100(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("or", reg1, reg2, 16)
        value = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, value)

    @staticmethod # xor reg1 reg2
    def i00010101(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("xor", reg1, reg2, 16)
        value = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, value)

    @staticmethod # not reg
    def i00010110(cu, cpu, operand1, operand2, operand3):
        #print("not", operand1)
        reg1 = cpu.access_register(operand1)
        cu.callALU("not", reg1, None, 16)
        value = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, value)

    @staticmethod # rol reg #imd
    def i00010111(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        cu.callALU("rol", reg1, operand2, 16)
        rolled = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, rolled)

    @staticmethod # ror reg #imd
    def i00011000(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        cu.callALU("ror", reg1, operand2, 16)
        rolled = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, rolled)

    @staticmethod # cmp reg1 reg2
    def i00011001(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        flags = cpu.access_register("1101")
        flags = set_flag(flags, "1", 14)
        cpu.access_register("1101", flags)
        cu.callALU("sub", reg1, reg2, 16)
    
    @staticmethod # shl reg #imd
    def i00011010(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        cu.callALU("shl", reg1, operand2, 16)
        shifted = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, shifted)
    
    @staticmethod # shr reg #imd
    def i00011011(cu, cpu, operand1, operand2, operand3):
        reg1 = cpu.access_register(operand1)
        cu.callALU("shr", reg1, operand2, 16)
        shifted = cpu.access_register("1100")[:16]
        cpu.access_register(operand1, shifted)

    @staticmethod # halt
    def i11111111(cu, cpu, operand1, operand2, operand3):
        print("halt")
        cu.cpu.running = False
    
    # Debugging Tools
    @staticmethod
    def print_registers(cu, cpu, operand1, operand2, operand3):
        cu.cpu.print_registers()

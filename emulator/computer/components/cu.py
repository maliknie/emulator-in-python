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

        self.cpu.computer.controller.add_event("CU: Fetching instruction " + instruction + " from address " + str(pc - 4))

    # Teilt die Instruktion in Opcode und Operanden auf
    def decode(self):
        instruction = self.cpu.ir
        self.opcode, self.operand1, self.operand2, self.operand3 = instruction[:8], instruction[8:12], instruction[12:16], instruction[16:32]

        self.cpu.computer.controller.add_event("CU: Decoding instruction " + instruction + " -> " + self.opcode + " " + self.operand1 + " " + self.operand2 + " " + self.operand3)
        """
        print("_________________________")
        print("Decoded instruction: ")
        print("Opcode: ", self.opcode)
        print("Operand1: ", self.operand1, mint(self.operand1))
        print("Operand2: ", self.operand2, mint(self.operand2))
        print("Operand3: ", self.operand3, mint(self.operand3))
        print("_________________________")"""
    
    def execute(self):
        try:
            Instructions.instruction_dict[self.opcode](self, self.cpu, self.operand1, self.operand2, self.operand3)
        except KeyError:
            self.cpu.computer.controller.add_event("CU: Unknown instruction " + self.opcode)
            self.cpu.computer.controller.add_event("Computer crashed")
            sys.exit(1)

    def reset(self):
        self.opcode = "00000000"
        self.operand1 = "0000000000000000"
        self.operand2 = "0000000000000000"
        self.operand3 = "0000000000000000"

    def callALU(self, op, a, b, bit_length = 16):
        self.cpu.alu.execute(op, a, b, bit_length)

# Implementation der Instruktionen
class Instructions:
    
    @staticmethod # jmp #imd
    def i00000000(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing jmp #" + str(mint(operand3)))

        cpu.pc = operand3
        
    @staticmethod # jeq #imd
    def i00000001(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing jeq #" + str(mint(operand3)))

        if check_flag(cpu.flags, 15):
            cpu.pc = operand3

    @staticmethod # jne #imd
    def i00000010(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing jne #" + str(mint(operand3)))

        if not check_flag(cpu.flags, 15):
            cpu.pc = operand3

    @staticmethod # inc [mem]
    def i00000011(cu, cpu, opernad1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing inc [" + str(mint(operand3)) + "]")


        memory_address = int(operand3, 2)
        value = cpu.computer.memory.read(memory_address)
        cu.callALU("add", value, "00000001", 8)
        value = cpu.access_register("1100")[24:]
        cpu.computer.memory.write(memory_address, value)

    @staticmethod # dec [mem]
    def i00000100(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing dec [" + str(mint(operand3)) + "]")

        memory_address = int(operand3, 2)
        value = cpu.computer.memory.read(memory_address)
        cu.callALU("sub", value, "00000001", 8)
        value = cpu.access_register("1100")[24:]
        cpu.computer.memory.write(memory_address, value)

    @staticmethod # load reg #imd
    def i00000101(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing load #" + str(mint(operand3)) + "," + cpu.registers[operand1])

        if operand1 in cpu.reg32bit:
            operand3 = operand3.zfill(32)
        cpu.access_register(operand1, operand3)

    @staticmethod # load reg [mem]
    def i00000110(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing load [" + str(mint(operand3)) + "], " + cpu.registers[operand1])

        memory_address = mint(operand3)
        value = cpu.computer.memory.read(memory_address) + cpu.computer.memory.read(memory_address + 1)
        if operand1 in cpu.reg32bit:
            value += cpu.computer.memory.read(memory_address + 2) + cpu.computer.memory.read(memory_address + 3)
        cpu.access_register(operand1, value)

    @staticmethod # store [mem] reg
    def i00000111(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing store " + cpu.registers[operand1] + ", [" + str(mint(operand3)) + "]")

        memory_address = mint(operand3)
        value = cpu.access_register(operand1)
        cpu.computer.memory.write(memory_address, value[:8])
        cpu.computer.memory.write(memory_address + 1, value[8:16])
        if operand1 in cpu.reg32bit:
            cpu.computer.memory.write(memory_address + 2, value[16:24])
            cpu.computer.memory.write(memory_address + 3, value[24:32])

    @staticmethod # jmp reg
    def i00001000(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing jmp [" + cpu.registers[operand1] + "]")

        reg = cpu.access_register(operand1)
        cpu.pc = reg

    @staticmethod # jeq reg
    def i00001001(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing jeq [" + cpu.registers[operand1] + "]")

        if check_flag(cpu.flags, 15):
            reg = cpu.access_register(operand1)
            cpu.pc = reg

    @staticmethod # jne reg
    def i00001010(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing jne [" + cpu.registers[operand1] + "]")

        if not check_flag(cpu.flags, 15):
            reg = cpu.access_register(operand1)
            cpu.pc = reg

    @staticmethod # store [reg1] reg2
    def i00001011(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing store [" + cpu.registers[operand1] + "], " + cpu.registers[operand2])

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
        cu.cpu.computer.controller.add_event("CU: Executing move " + cpu.registers[operand1] + ", " + cpu.registers[operand2])

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
        cu.cpu.computer.controller.add_event("CU: Executing add " + cpu.registers[operand1] + ", " + cpu.registers[operand2])

        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("add", reg1, reg2, 16)
        value = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value)

    @staticmethod # sub reg1 reg2
    def i00001110(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing sub " + cpu.registers[operand1] + ", " + cpu.registers[operand2])

        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("sub", reg1, reg2, 16)
        value = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value)

    @staticmethod # mult reg1 reg2
    def i00001111(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing mult " + cpu.registers[operand1] + ", " + cpu.registers[operand2])

        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("mul", reg1, reg2, 32)
        value_high = cpu.access_register("1100")[:16]
        value_low = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value_high)
        cpu.access_register(operand2, value_low)

    @staticmethod # div reg1 reg2
    def i00010000(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing div " + cpu.registers[operand1] + ", " + cpu.registers[operand2])

        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("div", reg1, reg2, 16)
        value = cpu.access_register("1100")[16:]
        modulo = cpu.access_register("1100")[:16]
        
        cpu.access_register(operand1, value)
        cpu.access_register(operand2, modulo)

    @staticmethod # inc reg
    def i00010001(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing inc " + cpu.registers[operand1])

        reg = cpu.access_register(operand1)
        cu.callALU("add", reg, "00000001", 16)
        value = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value)

    @staticmethod # dec reg
    def i00010010(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing dec " + cpu.registers[operand1])

        reg = cpu.access_register(operand1)
        cu.callALU("sub", reg, "00000001", 16)
        value = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value)

    @staticmethod # and reg1 reg2
    def i00010011(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing and " + cpu.registers[operand1] + ", " + cpu.registers[operand2])

        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("and", reg1, reg2, 16)
        value = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value)

    @staticmethod # or reg1 reg2
    def i00010100(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing or " + cpu.registers[operand1] + ", " + cpu.registers[operand2])

        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("or", reg1, reg2, 16)
        value = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value)

    @staticmethod # xor reg1 reg2
    def i00010101(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing xor " + cpu.registers[operand1] + ", " + cpu.registers[operand2])

        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        cu.callALU("xor", reg1, reg2, 16)
        value = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value)

    @staticmethod # not reg
    def i00010110(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing not " + cpu.registers[operand1])

        reg1 = cpu.access_register(operand1)
        cu.callALU("not", reg1, None, 16)
        value = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, value)

    @staticmethod # rol reg #imd
    def i00010111(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing rol " + cpu.registers[operand1] + ", #" + str(mint(operand2)))

        reg1 = cpu.access_register(operand1)
        cu.callALU("rol", reg1, operand3, 16)
        rolled = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, rolled)

    @staticmethod # ror reg #imd
    def i00011000(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing ror " + cpu.registers[operand1] + ", #" + str(mint(operand2)))

        reg1 = cpu.access_register(operand1)
        cu.callALU("ror", reg1, operand3, 16)
        rolled = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, rolled)

    @staticmethod # cmp reg1 reg2
    def i00011001(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing cmp " + cpu.registers[operand1] + ", " + cpu.registers[operand2])

        reg1 = cpu.access_register(operand1)
        reg2 = cpu.access_register(operand2)
        flags = cpu.access_register("1101")
        flags = set_flag(flags, "1", 14)
        cpu.access_register("1101", flags)
        cu.callALU("sub", reg1, reg2, 16)
    
    @staticmethod # shl reg #imd
    def i00011010(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing shl " + cpu.registers[operand1] + ", #" + str(mint(operand2)))

        reg1 = cpu.access_register(operand1)
        cu.callALU("shl", reg1, operand3, 16)
        shifted = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, shifted)
    
    @staticmethod # shr reg #imd
    def i00011011(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing shr " + cpu.registers[operand1] + ", #" + str(mint(operand2)))

        reg1 = cpu.access_register(operand1)
        cu.callALU("shr", reg1, operand3, 16)
        shifted = cpu.access_register("1100")[16:]
        cpu.access_register(operand1, shifted)

    @staticmethod # push reg
    def i00011100(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing push " + cpu.registers[operand1])

        reg1 = cpu.access_register(operand1)
        reg1_high = reg1[:8]
        reg1_low = reg1[8:]
        sp = int(cpu.access_register("1010"), 2)
        if sp - 2 < cpu.stack_lower_bound:
            raise Exception("Stack overflow")

        sp -= 2
        sp_bin = mbin(sp, 16, neg=False)
        cpu.access_register("1010", sp_bin)

        cpu.computer.memory.write(sp, reg1_high)
        cpu.computer.memory.write(sp + 1, reg1_low)
    
    @staticmethod # pop reg
    def i00011101(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing pop " + cpu.registers[operand1])

        sp = int(cpu.access_register("1010"), 2)
        if sp + 2 > cpu.stack_upper_bound:
            raise Exception("Stack underflow")

        sp += 2
        sp_bin = mbin(sp, 16, neg=False)
        cpu.access_register("1010", sp_bin)


        reg1_high = cpu.computer.memory.read(sp - 2)
        reg1_low = cpu.computer.memory.read(sp - 1)
        reg1 = reg1_high + reg1_low
        cpu.access_register(operand1, reg1)
    
    @staticmethod # call #imd (label)
    def i00011110(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing call " + cpu.registers[operand1])

        Instructions.i00011100(cu, cpu, "1000", "0000", "0000000000000000")
        Instructions.i00000000(cu, cpu, "0000", "0000", operand3)

    @staticmethod # ret
    def i00011111(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing ret")

        Instructions.i00011101(cu, cpu, "1000", "0000", "0000000000000000")



    @staticmethod # print reg
    def iwritestdout(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing print " + cpu.registers[operand1])
        
        #NEEDS IMPLEMENTATION

    @staticmethod # halt
    def i11111111(cu, cpu, operand1, operand2, operand3):
        cu.cpu.computer.controller.add_event("CU: Executing halt")
        print("halt")
        cu.cpu.running = False
    
    # Debugging Tools
    @staticmethod
    def print_registers(cu, cpu, operand1, operand2, operand3):
        cu.cpu.print_registers()

    instruction_dict = {
        "00000000": i00000000,
        "00000001": i00000001,
        "00000010": i00000010,
        "00000011": i00000011,
        "00000100": i00000100,
        "00000101": i00000101,
        "00000110": i00000110,
        "00000111": i00000111,
        "00001000": i00001000,
        "00001001": i00001001,
        "00001010": i00001010,
        "00001011": i00001011,
        "00001100": i00001100,
        "00001101": i00001101,
        "00001110": i00001110,
        "00001111": i00001111,
        "00010000": i00010000,
        "00010001": i00010001,
        "00010010": i00010010,
        "00010011": i00010011,
        "00010100": i00010100,
        "00010101": i00010101,
        "00010110": i00010110,
        "00010111": i00010111,
        "00011000": i00011000,
        "00011001": i00011001,
        "00011010": i00011010,
        "00011011": i00011011,
        "00011100": i00011100,
        "00011101": i00011101,
        "00011110": i00011110,
        "00011111": i00011111,
        "11111111": i11111111,
        "debuggin": print_registers,
        "writestd": iwritestdout          
    }

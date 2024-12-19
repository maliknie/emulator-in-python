from time import sleep
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))
from libraries.binary_lib import mbin, mint, set_flag, check_flag

class CPU:
    def __init__(self, alu, cu, computer) -> None:
        self.alu = alu
        self.cu = cu
        self.computer = computer

        self.running = False
        self.tick_mode = False

        # Allgemeine Register
        self.r0 = "0000000000000000"
        self.r1 = "0000000000000000"
        self.r2 = "0000000000000000"
        self.r3 = "0000000000000000"
        self.r4 = "0000000000000000"
        self.r5 = "0000000000000000"
        self.r6 = "0000000000000000"
        self.r7 = "0000000000000000"

        # Spezialregister
        self.pc = "0000000000000000"
        self.ir = "00000000000000000000000000000000"
        self.sp = "0000000000000000"
        self.bp = "0000000000000000"
        self.acc = "00000000000000000000000000000000"
        self.flags = "0000000000000000" # self.flags[15] = zero flag, self.flags[14] = cmp flag
        self.mar = "0000000000000000"
        self.mdr = "0000000000000000"

        self.reg32bit = ["1001", "1100"]

        # Register Mapping
        self.registers = {
            "0000": "r0",
            "0001": "r1",
            "0010": "r2",
            "0011": "r3",
            "0100": "r4",
            "0101": "r5",
            "0110": "r6",
            "0111": "r7",
            "1000": "pc",
            "1001": "ir",
            "1010": "sp",
            "1011": "bp",
            "1100": "acc",
            "1101": "flags",
            "1110": "mar",
            "1111": "mdr",
        }

        self.opcodes ={
            "00000000": "jmp",
            "00000001": "jeq",
            "00000010": "jne",
            "00000011": "inc",
            "00000100": "dec",
            "00000101": "load",
            "00000110": "load",
            "00000111": "store",
            "00001000": "jmp",
            "00001001": "jeq",
            "00001010": "jne",
            "00001011": "store",
            "00001100": "move",
            "00001101": "add",
            "00001110": "sub",
            "00001111": "mult",
            "00010000": "div",
            "00010001": "inc",
            "00010010": "dec",
            "00010011": "and",
            "00010100": "or",
            "00010101": "xor",
            "00010110": "not",
            "00010111": "rol",
            "00011000": "ror",
            "00011001": "cmp",
            "00011010": "shl",
            "00011011": "shr",
            "11111111": "halt"
        }



    def run(self):
        self.computer.clock.run()

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.tick_mode = False

        self.r0 = "0000000000000000"
        self.r1 = "0000000000000000"
        self.r2 = "0000000000000000"
        self.r3 = "0000000000000000"
        self.r4 = "0000000000000000"
        self.r5 = "0000000000000000"
        self.r6 = "0000000000000000"
        self.r7 = "0000000000000000"

        self.pc = "0000000000000000"
        self.ir = "00000000000000000000000000000000"
        self.sp = "0000000000000000"
        self.bp = "0000000000000000"
        self.acc = "00000000000000000000000000000000"
        self.flags = "0000000000000000" # self.flags[15] = zero flag, self.flags[14] = cmp flag
        self.mar = "0000000000000000"
        self.mdr = "0000000000000000"

        self.alu.reset()

    
    # Wird benutzt um von Register zu lesen und hinein zu schreiben
    def access_register(self, reg_code, value=None):
        if not reg_code in self.registers:
            raise ValueError("Invalid register code: ", reg_code)
        if value == None:
            return getattr(self, self.registers[reg_code])
        setattr(self, self.registers[reg_code], value)

    # Wechselt den Tick Mode (automatische oder manuelle Ausführung des Programms)
    def switch_tick_mode(self):
        self.tick_mode = not self.tick_mode
        print("Tick Mode: ", self.tick_mode)

    # Debugging Tools

    def print_registers(self):
        print("_________________________")
        print("Registers:")
        print("r0: ", self.r0)
        print("r1: ", self.r1)
        print("r2: ", self.r2)
        print("r3: ", self.r3)
        print("r4: ", self.r4)
        print("r5: ", self.r5)
        print("r6: ", self.r6)
        print("r7: ", self.r7)
        print("_________________________")
        print("pc: ", self.pc)
        print("ir: ", self.ir)
        print("sp: ", self.sp)
        print("bp: ", self.bp)
        print("acc: ", self.acc)
        print("flags: ", self.flags)
        print("mar: ", self.mar)
        print("mdr: ", self.mdr)
        print("_________________________")
        print("")
    
    def get_state(self):
        registers ={
            "r0": self.r0,
            "r1": self.r1,
            "r2": self.r2,
            "r3": self.r3,
            "r4": self.r4,
            "r5": self.r5,
            "r6": self.r6,
            "r7": self.r7,
            "pc": self.pc,
            "ir": self.ir,
            "sp": self.sp,
            "bp": self.bp,
            "acc": self.acc,
            "flags": self.flags,
            "mar": self.mar,
            "mdr": self.mdr
        }
        if not self.opcodes[self.ir[:8]] in ["rol", "ror", "shl", "shr"]:
            decoded_registers ={
                "r0": mint(self.r0),
                "r1": mint(self.r1),
                "r2": mint(self.r2),
                "r3": mint(self.r3),
                "r4": mint(self.r4),
                "r5": mint(self.r5),
                "r6": mint(self.r6),
                "r7": mint(self.r7),

                "pc": mint(self.pc),
                "ir": self.opcodes[self.ir[:8]] + " " + str(self.registers[self.ir[8:12]]) + " " + str(self.registers[self.ir[12:16]]) + " " + str(mint(self.ir[16:])),
                "sp": mint(self.sp),
                "bp": mint(self.bp),
                "acc": mint(self.acc),
                "flags": self.flags,
                "mar": mint(self.mar),
                "mdr": mint(self.mdr)
            }
        else:
            decoded_registers ={
                "r0": mint(self.r0),
                "r1": mint(self.r1),
                "r2": mint(self.r2),
                "r3": mint(self.r3),
                "r4": mint(self.r4),
                "r5": mint(self.r5),
                "r6": mint(self.r6),
                "r7": mint(self.r7),

                "pc": mint(self.pc),
                "ir": self.opcodes[self.ir[:8]] + " " + str(mint(self.ir[8:12])) + " " + str(mint(self.ir[12:16])) + " " + str(mint(self.ir[16:])),
                "sp": mint(self.sp),
                "bp": mint(self.bp),
                "acc": mint(self.acc),
                "flags": self.flags,
                "mar": mint(self.mar),
                "mdr": mint(self.mdr)
            }
        return (registers, decoded_registers)

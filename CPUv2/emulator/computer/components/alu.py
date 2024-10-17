import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from libraries.binary_lib import mbin, mint, set_flag, check_flag


class ALU:
    def __init__(self, cpu):
        self.cpu = cpu
        self.high = "0000000000000000"
        self.low = "0000000000000000"
        
    def reset(self):
        self.high = "0000000000000000"
        self.low = "0000000000000000"

    def execute(self, op, a, b, bit_length = 16):
        match op:
            case "add":
                self.high, self.low = "0000000000000000", Operations.add(a, b, bit_length)
            case "sub":
                self.high, self.low = "0000000000000000", Operations.sub(a, b, bit_length)
            case "mult":
                self.high, self.low = Operations.mult(a, b, bit_length)[:bit_length//2], Operations.mult(a, b, bit_length)[bit_length//2:]
            case "div":
                self.high, self.low = Operations.div(a, b, bit_length)[:bit_length//2], Operations.div(a, b, bit_length)[bit_length//2:]
            case "and":
                self.high, self.low = "0000000000000000", Operations.and_(a, b, bit_length)
            case "or":
                self.high, self.low = "0000000000000000", Operations.or_(a, b, bit_length)
            case "xor":
                self.high, self.low = "0000000000000000", Operations.xor(a, b, bit_length)
            case "not":
                self.high, self.low = "0000000000000000", Operations.not_(a, b, bit_length)
            case "rol":
                self.high, self.low = "0000000000000000", Operations.rol(a, b, bit_length)
            case "ror":
                self.high, self.low = "0000000000000000", Operations.ror(a, b, bit_length)
            case "shl":
                self.high, self.low = "0000000000000000", Operations.shl(a, b, bit_length)
            case "shr":
                self.high, self.low = "0000000000000000", Operations.shr(a, b, bit_length)
            case _:
                raise ValueError("Invalid operation: " + op)
            
        self.cpu.computer.controller.gui.update_alu_gui(op, a, b, self.high.zfill(16) + self.low.zfill(16))

        self.cpu.computer.controller.add_event("ALU: Executing " + a + " " + op + " " + b + " -> " + self.high.zfill(16) + self.low.zfill(16))

        # Wenn das Ergebnis einer Operation 0 ist, wird die Zero-Flag gesetzt
        if self.high.zfill(16) + self.low.zfill(16) == "00000000000000000000000000000000":
            flags = self.cpu.access_register("1101")
            flags = set_flag(flags, "1", 15)
            self.cpu.access_register("1101", flags)

        # Wenn das Ergebnis einer Operation nicht 0 ist, wird die Zero-Flag nicht gesetzt
        else:
            flags = self.cpu.access_register("1101")
            flags = set_flag(flags, "0", 15)
            self.cpu.access_register("1101", flags)


        # Wenn die cmp-Flag 1 ist, wird sie auf 0 gesetzt und das Ergebnis der Operation wird nicht in den Akkumulator geschrieben
        if not self.cpu == None and check_flag(self.cpu.access_register("1101"), 14):
            flags = self.cpu.access_register("1101")
            flags = set_flag(flags, "0", 14)
            self.cpu.access_register("1101", flags)

        # Wenn die cmp-Flag 0 ist, wird das Ergebnis der Operation in den Akkumulator geschrieben
        else:
            acc_value = self.high.zfill(16) + self.low.zfill(16)
            self.cpu.access_register("1100", acc_value)
            return self.low.zfill(16) + self.high.zfill(16)
        


# Implementation der Operationen der ALU
class Operations:
    @staticmethod
    def add(a, b, bit_length = 16):
        mod = 2**bit_length
        a = mint(a)
        b = mint(b)
        result = a + b
        result = ((result + mod//2) % mod) - mod//2
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def sub(a, b, bit_length = 16):
        mod = 2**bit_length
        a = mint(a)
        b = mint(b)
        result = a - b
        result = ((result + mod//2) % mod) - mod//2
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def mult(a, b, bit_length = 32):
        mod = 2**bit_length
        a = mint(a)
        b = mint(b)
        result = a * b
        result = ((result + mod//2) % mod) - mod//2
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def div(a, b, bit_length = 16):
        mod = 2**bit_length
        a = mint(a)
        b = mint(b)
        result = a // b
        result = ((result + mod//2) % mod) - mod//2
        mod = a % b
        return mbin(mod, bit_length).zfill(bit_length) + mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def and_(a, b, bit_length = 16):
        a = mint(a)
        b = mint(b)
        result = a & b
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def or_(a, b, bit_length = 16):
        a = mint(a)
        b = mint(b)
        result = a | b
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def xor(a, b, bit_length = 16):
        a = mint(a)
        b = mint(b)
        result = a ^ b
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def not_(a, b, bit_length = 16):
        a = mint(a)
        result = ~a
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def rol(a, b, bit_length = 16):
        a = mint(a)
        b = mint(b)
        result = (a << b) | (a >> (bit_length - b))
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def ror(a, b, bit_length = 16):
        a = mint(a)
        b = mint(b)
        result = (a >> b) | (a << (bit_length - b))
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def shl(a, b, bit_length = 16):
        a = mint(a)
        b = mint(b)
        result = a << b
        return mbin(result, bit_length).zfill(bit_length)
    @staticmethod
    def shr(a, b, bit_length = 16):
        a = mint(a)
        b = mint(b)
        result = a >> b
        return mbin(result, bit_length).zfill(bit_length)

def tests():
    assert Operations.add("0000000000000001", "0000000011110111") == "0000000011111000"
    assert Operations.add("0000000000000001", "0000000000000001") == "0000000000000010"
    assert Operations.add("0111111111111111", "0000000000000001") == "1000000000000000"
    assert Operations.sub("0000000000000010", "0000000000000001") == "0000000000000001"
    assert Operations.sub("0000000000000001", "0000000000000010") == "1111111111111111"
    assert Operations.sub("0000000000000000", "0000000000000000") == "0000000000000000"
    assert Operations.sub("0000000000000000", "1111111111111111") == "0000000000000001"
    assert Operations.mult("0000000000000010", "0000000000000010") == "00000000000000000000000000000100"
    assert Operations.mult("0000000000000010", "1111111111111110") == "11111111111111111111111111111100"
    assert Operations.mult("0000000000000001", "0000000000000001") == "00000000000000000000000000000001"
    assert Operations.mult("0000000000000000", "1100000000000000") == "00000000000000000000000000000000"
    assert Operations.div("0000000000000010", "0000000000000001") == "00000000000000000000000000000010"
    assert Operations.div("0000000000000001", "0000000000000010") == "00000000000000010000000000000000"
    assert Operations.div("0000100101001010", "1111111111111100") == "11111111111111101111110110101101"
    try:
        Operations.div("0000000000000001", "0000000000000000")
        assert False
    except ZeroDivisionError:
        assert True
    alu = ALU(None)
    alu.execute("add", "0000000000000001", "0000000000000001")
    assert alu.low == "0000000000000010"
    assert alu.high == "0000000000000000"
    
if __name__ == "__main__":
    tests()
    print(Operations.add("01111111", "00000001", 8))
    print("All tests passed!")
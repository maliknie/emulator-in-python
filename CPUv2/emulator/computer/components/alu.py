import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from libraries.binary_lib import mbin, mint


class ALU:
    def __init__(self, cpu):
        self.cpu = cpu
        self.high = "0000000000000000"
        self.low = "0000000000000000"
        
    
    def execute(self, op, a, b):
        match op:
            case "add":
                self.high, self.low = "0000000000000000", Operations.add(a, b)
            case "sub":
                self.high, self.low = "0000000000000000", Operations.sub(a, b)
            case "mult":
                self.high, self.low = Operations.mult(a, b)[:16], Operations.mult(a, b)[16:]
            case "div":
                self.high, self.low = Operations.div(a, b)[:16], Operations.div(a, b)[16:]

class Operations:
    @staticmethod
    def add(a, b):
        a = mint(a)
        b = mint(b)
        result = a + b
        result = ((result + 32768) % 65536) - 32768
        return mbin(result, 16).zfill(32)
    @staticmethod
    def sub(a, b):
        a = mint(a)
        b = mint(b)
        result = a - b
        result = ((result + 32768) % 65536) - 32768
        return mbin(result, 16).zfill(32)
    @staticmethod
    def mult(a, b):
        a = mint(a)
        b = mint(b)
        result = a * b
        result = ((result + 65536**2//2) % 65536**2) - 65536**2//2
        return mbin(result, 32).zfill(32)
    @staticmethod
    def div(a, b):
        a = mint(a)
        b = mint(b)
        result = a // b
        result = ((result + 32768) % 65536) - 32768
        mod = a % b
        return mbin(mod, 16).zfill(16) + mbin(result, 16).zfill(16)
    
if __name__ == "__main__":
    assert Operations.add("00000001", "11110111") == "1111111111111000"
    assert Operations.add("00000001", "00000001") == "0000000000000010"
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
    print("All tests passed!")
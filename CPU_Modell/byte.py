def AND(a, b):
    if a == 1 and b == 1:
        return 1
    return 0

def OR(a, b):
    if a == 1 or b == 1:
        return 1
    return 0

class Byte():
    def __init__(self) -> None:
        self.bits = [0, 0, 0, 0, 0, 0, 0, 0]
        self.negative = False
        
    def getByte(self) -> str:
        byte_string = ""
        if self.negative:
            byte_string += "-"
        for bit in self.bits[::-1]:
            byte_string += str(bit)
        return byte_string
    
    def getInt(self) -> int:
        return int(self.getByte(), 2)
    
    def setByte(self, byte_string: str) -> "Byte":
        byte_list = []
        byte_string = byte_string[::-1]
        for bit in byte_string:
            byte_list.append(int(bit))
        self.bits = byte_list
        return self
    
    def setBitInPos(self, bit: int, pos: int) -> None:
        current = self.bits[::-1]
        current[pos] = bit
        self.bits = current[::-1]
        
    def bitwise_and(self, value: "Byte") -> "Byte":
        new_bit = Byte()
        for i in range(len(self.bits)):
            new_bit.setBitInPos(AND(int(self.getByte()[i]), int(value.getByte()[i])), i)
        return new_bit
    
    def bitwise_or(self, value: "Byte") -> "Byte":
        new_bit = Byte()
        for i in range(len(self.bits)):
            new_bit.setBitInPos(OR(int(self.getByte()[i]), int(value.getByte()[i])), i)
        return new_bit
    
    def add(self, byte: "Byte") -> "Byte":        
        num1 = int(self.getByte(), 2)
        num2 = int(byte.getByte(), 2)
        result = num1 + num2
        result = str(bin(result)[2:]) # 0b weg schneiden
        if len(result) > 8:
            raise Exception("Overflow Error (Add)")
        for i in range(8-len(result)):
            result = "0" + result
        return Byte().setByte(result)

    def substract(self, byte: "Byte") -> "Byte":
        num1 = int(self.getByte(), 2)
        num2 = int(byte.getByte(), 2)
        result = num1 - num2
        new_byte = Byte()
        if result < 0:
            new_byte.negative = True
            result = result * -1

        result = str(bin(result)[2:])
        for i in range(8-len(result)):
            result = "0" + result
        
        new_byte.setByte(result)
        return new_byte

    def compare(self, byte: "Byte") -> int:      
        if int(self.getByte) > int(byte.getByte):
            return 0
        elif int(self.getByte) < int(byte.getByte):
            return 1
        else:
            return 2
    
    def inc(self) -> "Byte":
        return self.add(Byte().setByte("00000001"))
    
def joinBytesToInt(byte1: "Byte", byte2: "Byte") -> int:
    return int((byte1.getByte() + byte2.getByte()), 2)

if __name__ == "__main__":
    testbyte1 = Byte()
    testbyte1.setByte("00000001")

    testbyte2 = Byte()
    testbyte2.setByte("10000000")

    result = testbyte1.add(testbyte2)
    result2 = testbyte1.substract(testbyte2)
    print(result.getByte())
    print(result2.getByte())
    print(result2.negative)
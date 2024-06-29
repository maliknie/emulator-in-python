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
        for bit in self.bits[::-1]:
            byte_string += str(bit)
        return byte_string
    
    def getInt(self) -> int:
        if self.negative:
            return int(self.getByte(), 2) * -1
        return int(self.getByte(), 2)
    
    def setByte(self, byte_string: str, negative: bool = False) -> "Byte":
        # Keine Ahnung warum da immer ein b drin ist, aber jetzt funktioniert es
        for char in byte_string:
            if char != "0" and char != "1":
                byte_string = byte_string.replace(char, "")

        for i in range(8-len(byte_string)):
            byte_string = "0" + byte_string
        
        byte_list = []
        byte_string = byte_string[::-1]
        for bit in byte_string:
            byte_list.append(int(bit))
        self.bits = byte_list
        self.negative = negative
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
        if self.negative:
            num1 = num1 * -1
        if byte.negative:
            num2 = num2 * -1
        result = num1 + num2
        if result < 0:
            result = result * -1
            result = str(bin(result)[2:])
            for i in range(8-len(result)):
                result = "0" + result
            return Byte().setByte(result, True)
        result = str(bin(result)[2:]) # 0b weg schneiden
        for i in range(8-len(result)):
            result = "0" + result
        return Byte().setByte(result)

    def substract(self, byte: "Byte") -> "Byte":
        new_byte = Byte()
        num1 = self.getInt()
        print("num1: ", num1)
        num2 = byte.getInt()
        print("num2: ", num2)
        result = num1 - num2
        print("result: ", result)
        if result < 0:
            print("result is negative")
            result = result * -1
            result = str(bin(result)[2:])
            for i in range(8-len(result)):
                result = "0" + result
            return new_byte.setByte(result, True)
        result = str(bin(result)[2:])
        for i in range(8-len(result)):
            result = "0" + result
        return new_byte.setByte(result)
        

    def compare(self, byte: "Byte") -> int:
        num1 = int(self.getByte(), 2)
        num2 = int(byte.getByte(), 2)
        if self.negative:
            num1 = num1 * -1
        if byte.negative:
            num2 = num2 * -1   
        if num1 > num2:
            return 0
        elif num1 < num2:
            return 1
        else:
            return 2
    
    def inc(self) -> "Byte":
        return self.add(Byte().setByte("00000001"))
    
def joinBytesToInt(byte1: "Byte", byte2: "Byte") -> int:
    result = int((byte1.getByte() + byte2.getByte()), 2)
    if byte1.negative:
        result = result * -1
    return result

def testByte():
    testbyte1 = Byte()
    testbyte1.setByte("00000001", True)

    testbyte2 = Byte()
    testbyte2.setByte("00000001", True)

    result = testbyte1.add(testbyte2)
    result2 = testbyte1.substract(testbyte2)

    print(result.getByte(), result.negative)
    print(result2.getByte(), result2.negative)
if __name__ == "__main__":
    testByte()
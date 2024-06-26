import byte

# 16 Bit register class
class Register():
    def __init__(self, big_byte: byte.Byte=byte.Byte(), small_byte: byte.Byte=byte.Byte(), negative_flag: bool=False) -> None:
        self.bytes = (big_byte, small_byte)
        self.negative = negative_flag
    def getRegister(self) -> str:
        register_string = ""
        if self.negative:
            register_string += "-"
        register_string += self.bytes[0].getByte() + self.bytes[1].getByte()
        return register_string
    def getInt(self) -> int:
        if self.negative:
            print(self.getRegister())
            register_string = self.getRegister()
            register_string = register_string[1:]
            return int(register_string, 2) * -1
        return int(self.getRegister(), 2)
    def setRegisterFromString(self, big_byte_string: str, small_byte_string: str) -> "Register":
        self.bytes[0].setByte(big_byte_string)
        self.bytes[1].setByte(small_byte_string)
        return self
    def setRegisterFromBytes(self, big_byte: byte.Byte, small_byte: byte.Byte) -> "Register":
        self.bytes = (big_byte, small_byte)
        return self
    def addByteToRegister(self, byte: byte.Byte) -> "Register":
        result = self.getInt() + byte.getInt()
        if result >= 0:
            self.negative = False
        result = str(bin(result)[2:])
        for i in range(16-len(result)):
            result = "0" + result
        self.setRegisterFromString(result[:8], result[8:])
        return self
    def addDoubleByteToRegister(self, big_byte: byte.Byte, small_byte: byte.Byte) -> "Register":
        result = self.getInt() + byte.joinBytesToInt(big_byte, small_byte)
        if result >= 0:
            self.negative = False
        result = str(bin(result)[2:])
        for i in range(16-len(result)):
            result = "0" + result
        self.setRegisterFromString(result[:8], result[8:])
        return self
    def subByteFromRegister(self, byte: byte.Byte) -> "Register":
        result = self.getInt() - byte.getInt()
        if result < 0:
            self.negative = True
        result = str(bin(result)[2:])
        for i in range(16-len(result)):
            result = "0" + result
        self.setRegisterFromString(result[:8], result[8:])
        return self
    def subDoubleByteFromRegister(self, big_byte: byte.Byte, small_byte: byte.Byte) -> "Register":
        result = self.getInt() - byte.joinBytesToInt(big_byte, small_byte)
        if result < 0:
            self.negative = True
        result = str(bin(result)[2:])
        for i in range(16-len(result)):
            result = "0" + result
        self.setRegisterFromString(result[:8], result[8:])
        return self
    def incRegister(self, amount: int = 1) -> "Register":
        result = self.getInt() + amount
        if result >= 0:
            self.negative = False
        result = str(bin(result)[2:])
        for i in range(16-len(result)):
            result = "0" + result
        big_byte = byte.Byte().setByte(result[:8])
        small_byte = byte.Byte().setByte(result[8:])
        self.setRegisterFromBytes(big_byte, small_byte)
        return self
    def getBytes(self) -> tuple:
        return self.bytes
    def bitwiseAndWithDoubleByte(self, big_byte: byte.Byte, small_byte: byte.Byte) -> "Register":
        self.bytes[0] = self.bytes[0].bitwise_and(big_byte)
        self.bytes[1] = self.bytes[1].bitwise_and(small_byte)
        return self
    def bitwiseOrWithDoubleByte(self, big_byte: byte.Byte, small_byte: byte.Byte) -> "Register":
        self.bytes[0] = self.bytes[0].bitwise_or(big_byte)
        self.bytes[1] = self.bytes[1].bitwise_or(small_byte)
        return self
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
        return int(self.getRegister(), 2)
    def setRegisterFromString(self, register_string: str) -> "Register":
        self.bytes[0].setByte(register_string[:8])
        self.bytes[1].setByte(register_string[8:])
        return self
    def setRegisterFromBytes(self, big_byte: byte.Byte, small_byte: byte.Byte) -> "Register":
        self.bytes = (big_byte, small_byte)
        return self
    def addByteToRegister(self, byte: byte.Byte) -> "Register":
        result = self.getInt() + byte.getInt()
        if result > 65535:
            raise Exception("Overflow Error (Add to Register)")
        self.setRegisterFromString(bin(result)[2:])
        return self
    def incRegister(self, amount: int = 1) -> "Register":
        result = self.getInt() + amount
        if result > 65535:
            raise Exception("Overflow Error (Inc)")
        self.setRegisterFromString(bin(result)[2:])
        return self
    def getBytes(self) -> tuple:
        return self.bytes
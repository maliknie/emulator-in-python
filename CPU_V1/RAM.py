import byte

class RAM():
    def __init__(self, ram_size: int):
        self.registers = [byte.Byte() for x in range(ram_size)]
    def setValueAtIndex(self, value: "byte.Byte", index: int):
        self.registers[index] = value
        return True
    def getValueAtIndex(self, index: int):
        return self.registers[index]
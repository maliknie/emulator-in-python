import byte

class RAM():
    def __init__(self, ram_size):
        self.registers = [byte.Byte() for x in range(ram_size)]
    def setValueAtIndex(self, value, index):
        self.registers[index] = value
        return True
    def getValueAtIndex(self, index):
        return self.registers[index]
class RAM():
    def __init__(self):
        self.registers = 20 * []
    def setValueAtIndex(self, value, index):
        self.registers[index] = value
        return True
    def getValueAtIndex(self, index):
        return self.registers[index]
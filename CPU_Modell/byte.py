def AND(a, b):
    if a == 1 and b == 1:
        return 1
    return 0

def OR(a, b):
    if a == 1 or b == 1:
        return 1
    return 0

class Byte():
    def __init__(self):
        self.bits = [0, 0, 0, 0, 0, 0, 0, 0]
        
    def getByte(self):
        byte_string = ""
        for bit in self.bits[::-1]:
            byte_string += str(bit)
        return byte_string
    
    def setByte(self, byte_string):
        byte_list = []
        byte_string = byte_string[::-1]
        for bit in byte_string:
            byte_list.append(int(bit))
        self.bits = byte_list
    
    def setBitInPos(self, bit, pos):
        current = self.bits[::-1]
        current[pos] = bit
        self.bits = current[::-1]
        
    def bitwise_and(self, value):
        if not isinstance(value, Byte):
            Exception("Bitwise and Error")
        new_bit = Byte()
        for i in range(len(self.bits)):
            new_bit.setBitInPos(AND(int(self.getByte()[i]), int(value.getByte()[i])), i)
        return new_bit
    
    def bitwise_or(self, value):
        if not isinstance(value, Byte):
            Exception("Bitwise or Error")
        new_bit = Byte()
        for i in range(len(self.bits)):
            new_bit.setBitInPos(OR(int(self.getByte()[i]), int(value.getByte()[i])), i)
        return new_bit
    
    def add(self, value):
        pass
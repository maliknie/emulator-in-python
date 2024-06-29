import byte
import threading

class RAM():
    def __init__(self, ram_size: int):
        self.registers = [byte.Byte() for x in range(ram_size)]
        self.lock = threading.Lock()
    def setValueAtIndex(self, value: "byte.Byte", index: int):
        with self.lock:
            self.registers[index] = value
        return True
    def getValueAtIndex(self, index: int):
        with self.lock:
            return self.registers[index]
    def reset(self):
        with self.lock:
            self.registers = [byte.Byte() for x in range(len(self.registers))]
        return True
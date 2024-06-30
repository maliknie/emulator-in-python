class RAM:
    def __init__(self, size):
        self.size = size
        self.memory_cells = ["00000000" for _ in range(size)]
    
    def read(self, address):
        return self.memory_cells[address]
    
    def write(self, address, data):
        self.memory_cells[address] = data
class RAM:
    def __init__(self, size):
        self.size = size
        self.memory_cells = ["00000000" for _ in range(self.size)]
    
    def reset(self):
        self.memory_cells = ["00000000" for _ in range(self.size)]
    
    def read(self, address, triggered_by_gui=False):
        result = self.memory_cells[address]
        if not triggered_by_gui:
            self.computer.controller.add_event("RAM: Reading at address " + str(address) + " -> " + str(result))
        return result
    
    def write(self, address, data):
        self.computer.controller.add_event("RAM: Writing at address " + str(address) + " <- " + str(data))
        self.computer.controller.gui.update_ram_gui()
        self.memory_cells[address] = data
    
    def load_program(self, program_path):
        with open(program_path, "r") as f:
            program = f.readlines()
            for i, line in enumerate(program):
                self.memory_cells[i] = line.strip()
class Computer:
    def __init__(self, controller, cpu, memory, clock) -> None:
        self.controller = controller
        self.cpu = cpu
        self.memory = memory
        self.clock = clock
    
    def run(self):
        self.cpu.run()
    
    def shutdown(self):
        self.cpu.stop()
        self.memory.reset()
        self.cpu.reset()
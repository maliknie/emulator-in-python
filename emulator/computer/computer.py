# Hat wie in echt eine CPU, Memory und Clock, die zusammen einen Computer bilden

class Computer:
    def __init__(self, controller, cpu, memory, clock) -> None:
        self.controller = controller
        self.cpu = cpu
        self.memory = memory
        self.clock = clock
    
    def run(self):
        self.cpu.run()
    
    def reset(self):
       self.cpu.reset()
       self.memory.reset()
       self.clock.reset()

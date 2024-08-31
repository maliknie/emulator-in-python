from time import sleep
class Computer:
    def __init__(self, controller, cpu, memory, clock) -> None:
        self.controller = controller
        self.cpu = cpu
        self.memory = memory
        self.clock = clock
    
    def run(self):
        print("Computer is running")
        self.cpu.run()
    
    def shutdown(self):
        sleep(1)
        self.cpu.stop()
        self.memory.reset()
        self.cpu.alu.reset()
        print("Shutting down computer")
from time import sleep
class Computer:
    def __init__(self, controller, cpu, memory) -> None:
        self.controller = controller
        self.cpu = cpu
        self.memory = memory
    
    def run(self):
        print("Computer is running")
        self.cpu.run()
    
    def shutdown(self):
        self.cpu.stop()
        self.memory.reset()
        self.cpu.alu.reset()
        print("Shutting down computer")
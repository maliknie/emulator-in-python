from time import sleep
class Computer:
    def __init__(self, controller, cpu, memory) -> None:
        self.controller = controller
        self.cpu = cpu
        self.memory = memory
    
    def run(self):
        print("Computer is running")
        while True:
            sleep(10)
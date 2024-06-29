

class Computer:
    def __init__(self, cpu, memory, alu, cu) -> None:
        self.cpu = cpu(self, alu, cu)
        self.memory = memory(self)
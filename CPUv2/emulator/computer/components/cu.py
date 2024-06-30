class CU:
    def __init__(self, cpu) -> None:
        self.cpu = cpu

    def fetch(self):
        pass

    def decode(self):
        pass

    def callALU(self, op, a, b):
        self.cpu.alu.op = op
        self.cpu.alu.a = a
        self.cpu.alu.b = b
        self.cpu.alu.execute()
    
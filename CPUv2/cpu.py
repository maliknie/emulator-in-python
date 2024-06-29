class CPU:
    def __init__(self, alu, cu) -> None:
        self.alu = alu(self)
        self.cu = cu(self)

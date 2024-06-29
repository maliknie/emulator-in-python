class CU:
    def __init__(self, cpu) -> None:
        self.cpu = cpu
        self.program_counter = None
    def setProgramCounter(self, program_counter):
        self.program_counter = program_counter
    
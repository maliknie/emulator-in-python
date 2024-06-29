class ALU:
    def __init__(self, cpu):
        self.cpu = cpu
        self.op = None
        self.a = None
        self.b = None
        self.result = None
    
    def set_operation(self, op):
        self.op = op
    
    def load_operands(self, a, b=None):
        self.a = a
        self.b = b
    
    def execute(self):
        pass

    def get_result(self):
        return self.result
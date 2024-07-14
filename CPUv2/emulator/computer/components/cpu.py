from time import sleep

class CPU:
    def __init__(self, alu, cu, computer) -> None:
        self.alu = alu
        self.cu = cu
        self.computer = computer

        self.running = False

        self.r0 = "0000000000000000"
        self.r1 = "0000000000000000"
        self.r2 = "0000000000000000"
        self.r3 = "0000000000000000"
        self.r4 = "0000000000000000"
        self.r5 = "0000000000000000"
        self.r6 = "0000000000000000"
        self.r7 = "0000000000000000"

        self.pc = "0000000000000000"
        self.ir = "00000000000000000000000000000000"
        self.sp = "0000000000000000"
        self.bp = "0000000000000000"
        self.acc = "00000000000000000000000000000000"
        self.flags = "0000000000000000" # self.flags[15] = zero flag, self.flags[14] = cmp flag
        self.mar = "0000000000000000"
        self.mdr = "0000000000000000"

        self.reg32bit = ["1001", "1100"]

        self.registers = {
            "0000": "r0",
            "0001": "r1",
            "0010": "r2",
            "0011": "r3",
            "0100": "r4",
            "0101": "r5",
            "0110": "r6",
            "0111": "r7",
            "1000": "pc",
            "1001": "ir",
            "1010": "sp",
            "1011": "bp",
            "1100": "acc",
            "1101": "flags",
            "1110": "mar",
            "1111": "mdr",
        }

    def run(self):
        print("Running CPU")
        self.running = True
        while self.running:
            self.cu.fetch()
            self.cu.decode()
            self.cu.execute()

    def stop(self):
        self.running = False

    def access_register(self, reg_code, value=None):
        if not reg_code in self.registers:
            raise ValueError("Invalid register code: ", reg_code)
        if value == None:
            return getattr(self, self.registers[reg_code])
        setattr(self, self.registers[reg_code], value)
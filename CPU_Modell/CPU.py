import RAM
import byte
import register

class CPU():
    def __init__(self, mainmemory: "RAM.RAM", controlunit: "CU", alunit: "ALU"):
        self.mm = mainmemory
        self.cu = controlunit
        self.alu = alunit

    def run(self):
        print("Running CPU")
        while True:
            self.cu.fetch(self.mm)
            self.cu.incPC()
            instruction = self.cu.IR.getByte()
            # msb = 1 -> Operand ist in der nächsten Speicherzelle
            # msb = 0 -> Operand ist in der Speicherzelle, die durch die nächsten beiden Bytes definiert wird
            msb = int(instruction[0])
            match instruction[1:]:
                case "0000000":
                    self.NOP()
                case "0000001":
                    self.LDA(msb)
                case "0000010":
                    self.STA(msb)
                case "0000011":
                    self.ADD(msb)
                case "0000100":
                    self.SUB(msb)
                case "0000101":
                    self.JMP(msb)
                case "0000110":
                    self.JZ(msb)
                case "0000111":
                    self.JNZ(msb)
                case "0001000":
                    self.AND(msb)
                case "0001001":
                    self.OR(msb)
                case "0001011":
                    self.MOV(msb)
                case "0001010":
                    print("HLT reached")
                    break
                case _:
                    print("Problematic Byte: ", self.cu.IR.getByte())
                    raise Exception("CPU Error: Unknown command")
            

    def NOP(self):
        pass
    def LDA(self, msb: int):
        pc = self.cu.PC
        if msb:
            self.alu.accumulator = self.mm.getValueAtIndex(pc.getInt())
            self.cu.incPC()
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1) # Bytes im nächsten und übernächsten Speicherplatz werden zusammengefügt
        self.alu.accumulator = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte))
        self.cu.incPC(2)
    def STA(self, msb: int):
        pc = self.cu.PC
        if msb:
            self.mm.setValueAtIndex(self.alu.accumulator, pc.getInt())
            self.cu.incPC()
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        print("adress: ", big_adress_byte.getByte(), small_adress_byte.getByte())
        self.mm.setValueAtIndex(self.alu.accumulator, byte.joinBytesToInt(big_adress_byte, small_adress_byte))
        self.cu.incPC(2)
    def ADD(self, msb: int):
        pc = self.cu.PC
        if msb:
            next_byte = self.mm.getValueAtIndex(pc.getInt())
            self.alu.accumulator = self.alu.accumulator.add(next_byte)
            self.cu.incPC()
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        self.alu.accumulator = self.alu.accumulator.add(self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte)))
    def SUB(self, msb: int):
        pc = self.cu.PC
        if msb:
            next_byte = self.mm.getValueAtIndex(pc.getInt())
            self.alu.accumulator = self.alu.accumulator.substract(next_byte)
            self.cu.incPC()
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        self.alu.accumulator = self.alu.accumulator.substract(self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte)))
    def JMP(self, msb: int):
        pc = self.cu.PC
        if msb:
            big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
            small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            self.cu.PC.setRegisterFromBytes(big_adress_byte, small_adress_byte)
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        destination_big_byte = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte))
        destination_small_byte = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte) + 1)
        self.cu.PC.setRegisterFromBytes(destination_big_byte, destination_small_byte)
    def JZ(self, msb: int):
        if self.alu.accumulator.getInt() == 0:
            pc = self.cu.PC
            if msb:
                big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
                small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
                self.cu.PC.setRegisterFromBytes(big_adress_byte, small_adress_byte)
                return
            big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
            small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            destination_big_byte = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte))
            destination_small_byte = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte) + 1)
            self.cu.PC.setRegisterFromBytes(destination_big_byte, destination_small_byte)
        else:
            self.cu.incPC(2)
    def JNZ(self, msb: int):
        if self.alu.accumulator.getInt() != 0:
            pc = self.cu.PC
            if msb:
                big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
                small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
                self.cu.PC.setRegisterFromBytes(big_adress_byte, small_adress_byte)
                return
            big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
            small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            destination_big_byte = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte))
            destination_small_byte = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte) + 1)
            self.cu.PC.setRegisterFromBytes(destination_big_byte, destination_small_byte)
        else:
            self.cu.incPC(2)
    def AND(self, msb: int):
        pc = self.cu.PC
        if msb:
            next_byte = self.mm.getValueAtIndex(pc.getInt())
            self.alu.accumulator = self.alu.accumulator.bitwise_and(next_byte)
            self.cu.incPC()
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        goal_byte = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte))
        self.alu.accumulator = self.alu.accumulator.bitwise_and(goal_byte)
        self.cu.incPC(2)
    def OR(self, msb: int):
        pc = self.cu.PC
        if msb:
            next_byte = self.mm.getValueAtIndex(pc.getInt())
            self.alu.accumulator = self.alu.accumulator.bitwise_and(next_byte)
            self.cu.incPC()
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        goal_byte = self.mm.getValueAtIndex(byte.joinBytesToInt(big_adress_byte, small_adress_byte))
        self.alu.accumulator = self.alu.accumulator.bitwise_or(goal_byte)
        self.cu.incPC(2)
    def MOV(self, msb: int):
        pc = self.cu.PC
        print("Program Counter: ", self.cu.PC.getRegister())
        print("pc variable: ", pc.getRegister())
        if msb:
            from_adress_byte = self.mm.getValueAtIndex(pc.getInt())
            to_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            from_byte = self.mm.getValueAtIndex(from_adress_byte.getInt())
            self.mm.setValueAtIndex(from_byte, to_adress_byte.getInt())
            self.cu.incPC(2)
            return
        print("Test1: ok")
        aaf1 = self.mm.getValueAtIndex(pc.getInt())
        aaf2 = self.mm.getValueAtIndex(pc.getInt() + 1)
        print("aaf1, aaf2: ", aaf1.getByte(), aaf2.getByte())
        start_index = byte.joinBytesToInt(aaf1, aaf2)
        print("Start Index: ", hex(start_index))
        af1 = self.mm.getValueAtIndex(start_index)
        af2 = self.mm.getValueAtIndex(start_index + 1)
        print("af1, af2: ", af1.getByte(), af2.getByte())
        at1 = self.mm.getValueAtIndex(start_index + 2)
        at2 = self.mm.getValueAtIndex(start_index + 3)
        print("at1, at2: ", at1.getByte(), at2.getByte())
        value_to = self.mm.getValueAtIndex(byte.joinBytesToInt(at1, at2))
        print("Value to: ", value_to.getByte())
        value_from = self.mm.getValueAtIndex(byte.joinBytesToInt(af1, af2))
        print("Value from: ", value_from.getByte())
        self.mm.setValueAtIndex(value_from, value_to.getInt())
        self.cu.incPC(2)
        """
        from_adress_big = self.mm.getValueAtIndex(pc.getInt())
        print("Program Counter: ", self.cu.PC.getRegister())
        print("pc variable: ", pc.getRegister())
        from_adress_small = from_adress_big.add(byte.Byte().setByte('00000001'))
        to_adress_big = from_adress_big.add(byte.Byte().setByte('00000010'))
        to_adress_small = from_adress_big.add(byte.Byte().setByte('00000011'))
        value_to = self.mm.getValueAtIndex(byte.joinBytesToInt(to_adress_big, to_adress_small))
        value_from = self.mm.getValueAtIndex(byte.joinBytesToInt(from_adress_big, from_adress_small))
        self.mm.setValueAtIndex(value_from, value_to.getInt())
        self.cu.incPC(2)"""

    def HLT(self):
        exit()


class CU():
    def __init__(self) -> None:
        self.PC = register.Register()
        self.IR = byte.Byte()
    def reset(self) -> None:
        self.PC = register.Register()
        self.IR = byte.Byte()
    def fetch(self, memory: "RAM.RAM") -> None:
        if not isinstance(memory, RAM.RAM):
            raise Exception("Fetch Error")
        self.IR = memory.getValueAtIndex(self.PC.getInt())
        print("Fetched: ", self.IR.getByte())
    def incPC(self, amount: int = 1) -> "byte.Byte":
        self.PC.incRegister(amount)     
        return self.PC
            
class ALU():
    def __init__(self):
        self.accumulator = byte.Byte()
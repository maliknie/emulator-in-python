import RAM as RAM
import byte
import register
import time
import random
import copy

class CPU():
    def __init__(self, mainmemory: "RAM.RAM", controlunit: "CU", alunit: "ALU"):
        self.mm = mainmemory
        self.cu = controlunit
        self.alu = alunit

        self.running = False
    
    def testScreen(self):
        k = 0
        while True:
            k += 1
            print("Test Screen cycle: ", k)
            for i in range(len(self.mm.registers)):
                my_bytestring = "".join(random.choices("01", k=8))
                self.mm.registers[i] = byte.Byte().setByte(my_bytestring)

        
            
    
    def loadProgram(self, filename: str = "default.bin") -> None:
        if filename == "":
            filename = "default.bin"
        print("Loading program...")
        with open("binary_files/" + filename, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                line = line[:8]
                self.mm.setValueAtIndex(byte.Byte().setByte(line), i)
        print("Program loaded")

    def run(self):
        print("Running CPU")
        k = 0
        self.running = True
        while self.running:
            k += 1
            print("Cycle: ", k)
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
                case "0001100":
                    self.MOVT()
                case "0001101":
                    self.MOVF()
                case "0001110":
                    self.CLR()
                case "0001111":
                    self.STAS(msb)
                case "0001010":
                    print("HLT reached")
                    self.cu.PC.setRegisterFromInt(0)
                    break
                case _:
                    print("Problematic Byte: ", self.cu.IR.getByte())
                    print("PC: ", self.cu.PC.getInt())
                    raise Exception("CPU Error: Unknown command")
            
    def stop(self):
        print("Stopping CPU")
        self.running = False
        self.cu.reset()
        self.alu.reset()
        self.mm.reset()
        print("CPU stopped")

    def NOP(self):
        print("NOP")
        pass
    def LDA(self, msb: int):
        print("LDA")
        pc = self.cu.PC
        if msb:
            big_byte = self.mm.getValueAtIndex(pc.getInt())
            small_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            self.alu.accumulator.setRegisterFromBytes(copy.copy(big_byte), copy.copy(small_byte))
            self.cu.incPC(2)
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1) # Bytes im nächsten und übernächsten Speicherplatz werden zusammengefügt
        full_adress = byte.joinBytesToInt(big_adress_byte, small_adress_byte)
        big_byte = self.mm.getValueAtIndex(full_adress)
        small_byte = self.mm.getValueAtIndex(full_adress + 1)
        self.alu.accumulator.setRegisterFromBytes(copy.copy(big_byte), copy.copy(small_byte))
        self.cu.incPC(2)
    def STA(self, msb: int):
        print("STA")
        pc = self.cu.PC
        if msb:
            big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
            small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            full_adress = byte.joinBytesToInt(big_adress_byte, small_adress_byte)
            bytes_to_store = self.alu.accumulator.getBytes()
            for b in bytes_to_store:
                if not isinstance(b, byte.Byte):
                    pass
            self.mm.setValueAtIndex(copy.copy(bytes_to_store[0]), full_adress)
            self.mm.setValueAtIndex(copy.copy(bytes_to_store[1]), full_adress + 1)
            self.cu.incPC(2)
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        start_index = byte.joinBytesToInt(big_adress_byte, small_adress_byte)
        big_destination_byte = self.mm.getValueAtIndex(start_index)
        small_destination_byte = self.mm.getValueAtIndex(start_index + 1)
        full_adress = byte.joinBytesToInt(big_destination_byte, small_destination_byte)
        bytes_to_store = self.alu.accumulator.getBytes()
        self.mm.setValueAtIndex(copy.copy(bytes_to_store[0]), full_adress)
        self.mm.setValueAtIndex(copy.copy(bytes_to_store[1]), full_adress + 1)
        self.cu.incPC(2)
    def STAS(self, msb: int):
        print("STAS")
        pc = self.cu.PC
        if msb:
            big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
            small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            full_adress = byte.joinBytesToInt(big_adress_byte, small_adress_byte)
            bytes_to_store = self.alu.accumulator.getBytes()
            self.mm.setValueAtIndex(bytes_to_store[1], full_adress)
            self.cu.incPC(2)
            return
        big_index_byte = self.mm.getValueAtIndex(pc.getInt())
        small_index_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        index = byte.joinBytesToInt(big_index_byte, small_index_byte)
        big_destination_byte = self.mm.getValueAtIndex(index)
        small_destination_byte = self.mm.getValueAtIndex(index + 1)
        full_adress = byte.joinBytesToInt(big_destination_byte, small_destination_byte)
        bytes_to_store = self.alu.accumulator.getBytes()
        self.mm.setValueAtIndex(bytes_to_store[1], full_adress)
    def ADD(self, msb: int):
        print("ADD")
        pc = self.cu.PC
        if msb:
            big_byte = self.mm.getValueAtIndex(pc.getInt())
            small_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            self.alu.accumulator = self.alu.accumulator.addDoubleByteToRegister(big_byte, small_byte)
            self.cu.incPC(2)
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        full_adress = byte.joinBytesToInt(big_adress_byte, small_adress_byte)
        big_byte = self.mm.getValueAtIndex(full_adress)
        small_byte = self.mm.getValueAtIndex(full_adress + 1)
        self.alu.accumulator = self.alu.accumulator.addDoubleByteToRegister(big_byte, small_byte)
        self.cu.incPC(2)
    def SUB(self, msb: int):
        print("SUB")
        pc = self.cu.PC
        if msb:
            big_byte = self.mm.getValueAtIndex(pc.getInt())
            small_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            self.alu.accumulator = self.alu.accumulator.subDoubleByteFromRegister(big_byte, small_byte)
            self.cu.incPC(2)
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        full_adress = byte.joinBytesToInt(big_adress_byte, small_adress_byte)
        big_byte = self.mm.getValueAtIndex(full_adress)
        small_byte = self.mm.getValueAtIndex(full_adress + 1)
        self.alu.accumulator = self.alu.accumulator.subByteFromRegister(big_byte, small_byte)
    def JMP(self, msb: int):
        print("JMP")
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
        print("JZ")
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
        print("JNZ")
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
        print("AND")
        pc = self.cu.PC
        if msb:
            big_byte = self.mm.getValueAtIndex(pc.getInt())
            small_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            self.alu.accumulator = self.alu.accumulator.bitwiseAndWithDoubleByte(big_byte, small_byte)
            self.cu.incPC(2)
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        full_adress = byte.joinBytesToInt(big_adress_byte, small_adress_byte)
        big_byte = self.mm.getValueAtIndex(full_adress)
        small_byte = self.mm.getValueAtIndex(full_adress + 1)
        self.alu.accumulator = self.alu.accumulator.bitwiseAndWithDoubleByte(big_byte, small_byte)
        self.cu.incPC(2)
    def OR(self, msb: int):
        print("OR")
        pc = self.cu.PC
        if msb:
            big_byte = self.mm.getValueAtIndex(pc.getInt())
            small_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            self.alu.accumulator = self.alu.accumulator.bitwiseOrWithDoubleByte(big_byte, small_byte)
            self.cu.incPC(2)
            return
        big_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        full_adress = byte.joinBytesToInt(big_adress_byte, small_adress_byte)
        big_byte = self.mm.getValueAtIndex(full_adress)
        small_byte = self.mm.getValueAtIndex(full_adress + 1)
        self.alu.accumulator = self.alu.accumulator.bitwiseOrWithDoubleByte(big_byte, small_byte)
        self.cu.incPC(2)
    def MOV(self, msb: int):
        print("MOV")
        pc = self.cu.PC
        if msb:
            big_from_adress_byte = self.mm.getValueAtIndex(pc.getInt())
            small_from_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
            full_from_adress = byte.joinBytesToInt(big_from_adress_byte, small_from_adress_byte)
            big_to_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 2)
            small_to_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 3)
            full_to_adress = byte.joinBytesToInt(big_to_adress_byte, small_to_adress_byte)
            from_byte = self.mm.getValueAtIndex(full_from_adress)
            self.mm.setValueAtIndex(from_byte, full_to_adress)
            self.cu.incPC(4)
            return
        # Dieser Teil ist kompliziert, Erklärungsskizze in ../anderes/BilderUndSkizzen/mov.jpg
        big_byte = self.mm.getValueAtIndex(pc.getInt())
        small_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        start_index = byte.joinBytesToInt(big_byte, small_byte)
        big_from_adress_byte = self.mm.getValueAtIndex(start_index)
        small_from_adress_byte = self.mm.getValueAtIndex(start_index + 1)
        big_to_adress_byte = self.mm.getValueAtIndex(start_index + 2)
        small_to_adress_byte = self.mm.getValueAtIndex(start_index + 3)
        full_from_adress = byte.joinBytesToInt(big_from_adress_byte, small_from_adress_byte)
        full_to_adress = byte.joinBytesToInt(big_to_adress_byte, small_to_adress_byte)
        from_byte = self.mm.getValueAtIndex(full_from_adress)
        self.mm.setValueAtIndex(from_byte, full_to_adress)
        self.cu.incPC(2)
    def MOVT(self):
        print("MOVT")
        pc = self.cu.PC
        big_from_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_from_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        full_from_adress = byte.joinBytesToInt(big_from_adress_byte, small_from_adress_byte)
        big_index_byte = self.mm.getValueAtIndex(pc.getInt() + 2)
        small_index_byte = self.mm.getValueAtIndex(pc.getInt() + 3)
        index = byte.joinBytesToInt(big_index_byte, small_index_byte)
        big_to_adress_byte = self.mm.getValueAtIndex(index)
        small_to_adress_byte = self.mm.getValueAtIndex(index + 1)
        full_to_adress = byte.joinBytesToInt(big_to_adress_byte, small_to_adress_byte)
        from_byte = self.mm.getValueAtIndex(full_from_adress)
        self.mm.setValueAtIndex(from_byte, full_to_adress)
        self.cu.incPC(4)
    def MOVF(self):
        print("MOVF")
        pc = self.cu.PC
        big_to_adress_byte = self.mm.getValueAtIndex(pc.getInt())
        small_to_adress_byte = self.mm.getValueAtIndex(pc.getInt() + 1)
        full_to_adress = byte.joinBytesToInt(big_to_adress_byte, small_to_adress_byte)
        big_index_byte = self.mm.getValueAtIndex(pc.getInt() + 2)
        small_index_byte = self.mm.getValueAtIndex(pc.getInt() + 3)
        index = byte.joinBytesToInt(big_index_byte, small_index_byte)
        big_from_adress_byte = self.mm.getValueAtIndex(index)
        small_from_adress_byte = self.mm.getValueAtIndex(index + 1)
        full_from_adress = byte.joinBytesToInt(big_from_adress_byte, small_from_adress_byte)
        from_byte = self.mm.getValueAtIndex(full_from_adress)
        self.mm.setValueAtIndex(from_byte, full_to_adress)
        self.cu.incPC(4)
    def CLR(self):
        print("CLR")
        self.alu.accumulator.setRegisterFromBytes(byte.Byte().setByte('00000000'), byte.Byte().setByte('00000000'))
    def HLT(self):
        print("HLT")
        exit()


class CU():
    def __init__(self) -> None:
        self.PC = register.Register()
        self.IR = byte.Byte()
    def reset(self) -> None:
        self.PC = register.Register()
        self.IR = byte.Byte()
    def fetch(self, memory: "RAM.RAM") -> None:
        self.IR = memory.getValueAtIndex(self.PC.getInt())
    def incPC(self, amount: int = 1) -> "byte.Byte":
        self.PC.incRegister(amount)     
        return self.PC
            
class ALU():
    def __init__(self):
        self.accumulator = register.Register()
    def reset(self):
        self.__init__()
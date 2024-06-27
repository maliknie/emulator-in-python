import time
import threading
import byte
import RAM

class Display():
    def __init__(self, ram: RAM.RAM) -> None:
        self.mm = ram
        self.pixel_colors = ["#000000"] * 4096 # 4 Bits per Pixel = 16'384 Bits = 2'048 Bytes
    def setColor(self, index: int, color: str):
        self.pixel_colors[index] = color
    def translateRamToColor(self):
        color_bytes = self.mm.registers[63488:]
        print(len(color_bytes))

if __name__ == "__main__":
    mainmemory = RAM.RAM(65536)
    test_display = Display(mainmemory)
    test_display.translateRamToColor()
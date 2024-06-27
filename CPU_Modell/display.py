import time
import threading
import byte
import RAM
import tkinter as tk
import random

class Display():
    def __init__(self, ram: RAM.RAM, parentwindow: tk.Tk, canvas: tk.Canvas) -> None:
        self.parentwindow = parentwindow

        self.mm = ram
        self.canvas = canvas

        self.pixel_colors = ["#000000"] * 4096 # 4 Bits per Pixel = 16'384 Bits = 2'048 Bytes
        self.grid_size = 64

        self.color_bytes = [byte.Byte() for i in range(2048)]
        self.split_bytes = ["0000" for i in range(4096)]
    def setColor(self, index: int, color: str):
        self.pixel_colors[index] = color
    def splitBytes(self):
        for i in range(4096, 2):
            self.split_bytes[i] = self.color_bytes[i/2].getByte()[:4]
            self.split_bytes[i+1] = self.color_bytes[i/2].getByte()[4:]
    def translateRamToColor(self):
        print("Translating RAM to Color...")
        self.color_bytes = self.mm.registers[63488:]
        self.splitBytes()
        for i in range(4096):
            match self.split_bytes[i]:
                case "0000":
                    self.setColor(i, "#000000")
                case "1111":
                    self.setColor(i, "#FFFFFF")
                case _:
                    self.setColor(i, "#0000FF")
    def renderCanvas(self):
        print("Rendering Canvas...")

        for i in range(64):
            for j in range(64):
                pixel_index = i * 64 + j
                pixel_color = self.pixel_colors[pixel_index]
                top_left_x = j * 8
                top_left_y = i * 8
                bottom_right_x = top_left_x + 8
                bottom_right_y = top_left_y + 8
                self.canvas.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill=pixel_color, outline="")
        self.canvas.pack()
    def thread(self):
        print("Starting Thread...")
        
        while True:
            start_time = time.time()
            for _ in range(100):
                pixel_index = random.randint(0, self.grid_size**2 - 1)
                color = "#" + "".join(random.choices("0123456789ABCDEF", k=6))
                self.setColor(pixel_index, color)
            self.renderCanvas()
            time.sleep(1)
            elapsed_time = time.time() - start_time
            print(f"Time elapsed since last thread call: ", elapsed_time, " seconds")


if __name__ == "__main__":
    mainmemory = RAM.RAM(65536)

    window = tk.Tk()
    window.title("Pixel Display")
    window.geometry("1080x1080")

    canvas = tk.Canvas(window, width=1024, height=1024)

    screen = Display(mainmemory, window, canvas)
    update_thread = threading.Thread(target=screen.thread)
    update_thread.daemon = True
    update_thread.start()

    window.mainloop()
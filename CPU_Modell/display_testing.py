import tkinter as tk
import random
import threading
import time
import display
import CPU_V1.RAM as RAM

GRID_SIZE = 64
mainmemory = RAM.RAM(65536)

window = tk.Tk()
window.title("Pixel Display")
window.geometry("1080x1080")

canvas = tk.Canvas(window, width=1024, height=1024)
canvas.pack()

screen = display.Display(mainmemory, canvas)


RECTANGLE_SIZE = 8  # funktioniert endlich !!!
print(1)

update_thread = threading.Thread(target=screen.thread)
update_thread.daemon = True
update_thread.start()

window.mainloop()
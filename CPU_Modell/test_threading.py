import time
import threading
import random
import tkinter as tk

class Pixel():
    def __init__(self, color: str, top_left_x: int, top_left_y: int, bottom_right_x: int, bottom_right_y: int) -> None:
        self.color = color
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y

grid_size = 64

pixels = [Pixel("#000000", 0, 0, 8, 8) for i in range(4096)]

def preparePixels():
    while True:
        time.sleep(2)
        pixel_color = "#000000"
        pixel_top_left_x = 0
        pixel_top_left_y = 0
        pixel_bottom_right_x = 8
        pixel_bottom_right_y = 8
        # prepare colors
        for i in range(64):
            for j in range(64):
                pixel_index = i * 64 + j
                pixel_color = "#" + "".join(random.choices("0123456789ABCDEF", k=6))
                pixel_top_left_x = j * 8
                pixel_top_left_y = i * 8
                pixel_bottom_right_x = pixel_top_left_x + 8
                pixel_bottom_right_y = pixel_top_left_y + 8
                pixel = Pixel(pixel_color, pixel_top_left_x, pixel_top_left_y, pixel_bottom_right_x, pixel_bottom_right_y)
                pixel_color = "#" + "".join(random.choices("0123456789ABCDEF", k=6))
                pixels[pixel_index] = pixel
        #        canvas.create_rectangle(pixel_top_left_x, pixel_top_left_y, pixel_bottom_right_x, pixel_bottom_right_y, fill=pixel_color, outline="")
        #canvas.pack()
        print("Pixels prepared")
        draw(canvas)
        

def draw(canvas: tk.Canvas):
    start = time.time()
    for pixel in pixels:
        canvas.create_rectangle(pixel.top_left_x, pixel.top_left_y, pixel.bottom_right_x, pixel.bottom_right_y, fill=pixel.color, outline="")
    canvas.pack()
    time_elapsed = time.time() - start
    print("Time elapsed: ", time_elapsed)
    time.sleep(1)
    











root = tk.Tk()
root.title("Test")

canvas = tk.Canvas(root, width=1024, height=1024)

draw_button = tk.Button(root, text="Draw", command=lambda: draw(canvas))
draw_button.pack()

prepare_thread = threading.Thread(target=preparePixels)
prepare_thread.daemon = True
prepare_thread.start()

root.mainloop()
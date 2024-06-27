import tkinter as tk
import random
import threading
import time

AMOUNT_OF_PIXELS = 64

window = tk.Tk()
window.title("Pixel Display")
window.geometry("1080x1080")

canvas = tk.Canvas(window, width=1024, height=1024)
canvas.pack()


pixel_colors = ["#DD9aFF"] * AMOUNT_OF_PIXELS**2

RECTANGLE_SIZE = 8  # funktioniert endlich !!!

def update_display():
    for i in range(AMOUNT_OF_PIXELS):
        for j in range(AMOUNT_OF_PIXELS):
            pixel_index = i * AMOUNT_OF_PIXELS + j
            pixel_color = pixel_colors[pixel_index]
            # positionen der Pixel berechnen basierend auf RECTANGLE_SIZE

            top_left_x = j * RECTANGLE_SIZE
            top_left_y = i * RECTANGLE_SIZE
            bottom_right_x = top_left_x + RECTANGLE_SIZE
            bottom_right_y = top_left_y + RECTANGLE_SIZE
            canvas.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill=pixel_color, outline="")

def set_pixel_color(pixel_index, color):
    pixel_colors[pixel_index] = color

def continuous_update():
    while True:
        for _ in range(100):
            pixel_index = random.randint(0, AMOUNT_OF_PIXELS**2 - 1)
            color = "#" + "".join(random.choices("0123456789ABCDEF", k=6))
        set_pixel_color(pixel_index, color)
        update_display()
        time.sleep(1)

update_thread = threading.Thread(target=continuous_update)
update_thread.daemon = True
update_thread.start()

window.mainloop()
import time
import threading
import random
import tkinter as tk
grid_size = 64

colors = ["#000000"] * 4096

def setColor(index: int, color: str):
    colors[index] = color

def prepareColor():
    while True:
        start_time = time.time()
        for _ in range(100):
            pixel_index = random.randint(0, grid_size**2 - 1)
            color = "#" + "".join(random.choices("0123456789ABCDEF", k=6))
            setColor(pixel_index, color)
        print("Colors prepared")
        time.sleep(2)
        elapsed_time = time.time() - start_time
        print(f"Time elapsed since last thread call: ", elapsed_time, " seconds")

def draw(colors, canvas: tk.Canvas):
    start = time.time()
    for i in range(64):
        for j in range(64):
            pixel_index = i * 64 + j
            pixel_color = colors[pixel_index]
            top_left_x = j * 8
            top_left_y = i * 8
            bottom_right_x = top_left_x + 8
            bottom_right_y = top_left_y + 8
            canvas.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill=pixel_color, outline="")
    canvas.pack()
    elapsed_time = time.time() - start
    print(f"Drawing time: ", elapsed_time, " seconds")
    
root = tk.Tk()
root.title("Test")

canvas = tk.Canvas(root, width=1024, height=1024)


draw_button = tk.Button(root, text="Draw", command=lambda: draw(colors, canvas))
draw_button.pack()

update_thread = threading.Thread(target=prepareColor)
update_thread.daemon = True
update_thread.start()

root.mainloop()
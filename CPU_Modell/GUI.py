import tkinter as tk
import display
import RAM
import threading
import time
import queue

class Window():
    def __init__(self, title, geometry):
        self.isopen = False
        self.isbuilt = False
        self.title = title
        self.geometry = geometry
    def build(self):
        openWindow(self)
        print("Class: Window")

class displayWindow(Window):
    def __init__(self, title, geometry, ram: RAM.RAM):
        super().__init__(title, geometry)
        self.mm = ram
        self.window = None
    def build(self):
        newwindow = openWindow(self)
        self.window = newwindow
        if not self.isbuilt:
            self.isbuilt = True
            exitbutton = tk.Button(newwindow, text="exit", command=lambda: self.close(newwindow), height=1, width=3)
            exitbutton.pack()
            canvas = tk.Canvas(newwindow, width=1024, height=1024)

            screen = display.Display(self.mm, newwindow, canvas)
            update_thread = threading.Thread(target=screen.thread)
            update_thread.daemon = True
            update_thread.start()

            
    def close(self, newwindow):
        if not isinstance(newwindow, tk.Tk):
            exit()
        newwindow.destroy()
        self.isopen = False
        self.isbuilt = False

class clockWindow(Window):
    def __init__(self, title, geometry):
        super().__init__(title, geometry)
    def build(self):
        newwindow = openWindow(self)
        if not self.isbuilt:
            self.isbuilt = True
            button1 = tk.Button(newwindow, text="exit", command=lambda: self.close(newwindow))
            button1.pack()
    def close(self, newwindow):
        if not isinstance(newwindow, tk.Tk):
            exit()
        newwindow.destroy()
        self.isopen = False
        self.isbuilt = False

class rootWindow(Window):
    def __init__(self, title, geometry, root: tk.Tk, displaywindow: displayWindow, clockwindow: clockWindow):
        super().__init__(title, geometry)
        self.tkwindow = root
        self.displaywindow = displaywindow
        self.clockwindow = clockwindow
    def build(self):
        self.tkwindow.title(self.title)
        self.tkwindow.geometry(self.geometry)
        if not self.isbuilt:
            self.isbuilt = True
            exitbutton = tk.Button(self.tkwindow, text="exit", command=lambda: self.close(), height=1, width=3)
            exitbutton.pack()
            displaybutton = tk.Button(self.tkwindow, text="Display", command=self.displaywindow.build)
            displaybutton.pack()
            clockbutton = tk.Button(self.tkwindow, text="Clock", command=self.clockwindow.build)
            clockbutton.pack()
    def close(self):
        self.tkwindow.destroy()
        self.isopen = False
        self.isbuilt = False



def openWindow(window):
    if not isinstance(window, Window):
        exit()
    if not window.isopen:
        newwindow = tk.Tk()
        newwindow.title(window.title)
        newwindow.geometry(window.geometry)
        window.isopen = True
        return newwindow

def build_gui(mainmemory: RAM.RAM):
    displaywindow = displayWindow("Pixel Display", "1080x1080", mainmemory)
    clockwindow = clockWindow("Clock", "200x200")
    root = rootWindow("CPU Modell", "500x500", tk.Tk(), displaywindow, clockwindow)
    root.build()

    root.tkwindow.mainloop()
if __name__ == "__main__":
    mainmemory = RAM.RAM(65536)
    build_gui(mainmemory)
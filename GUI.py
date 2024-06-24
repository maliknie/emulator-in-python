import tkinter as tk


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
    def __init__(self, title, geometry, resolution):
        super().__init__(title, geometry)
        self.resolution = resolution
    def build(self):
        newwindow = openWindow(self)
        if not self.isbuilt:
            self.isbuilt = True
            buttonframe = tk.Frame(newwindow)
            buttonframe.columnconfigure(0)
            buttonframe.rowconfigure(0)
            exitbuttonframe = tk.Frame(newwindow)
            exitbuttonframe.columnconfigure(1)
            exitbuttonframe.rowconfigure(0)
            exitbutton = tk.Button(exitbuttonframe, text="exit", command=lambda: self.close(newwindow), height=1, width=3)
            exitbutton.grid(row=0, column=0, sticky="nw")
            exitbuttonframe.pack()
            pixelframe = tk.Frame(newwindow, height=1, width=1)
            
            for i in range(self.resolution):
                pixelframe.columnconfigure(i, weight=0)
                pixelframe.rowconfigure(i, weight=0)
                for j in range(self.resolution):
                    button = tk.Button(pixelframe, text="", height=1, width=1, background="black")
                    button.grid(row=i, column=j, sticky="wens")
            pixelframe.pack(fill="x") 
            
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
def openWindow(window):
    if not isinstance(window, Window):
        exit()
    if not window.isopen:
        newwindow = tk.Tk()
        newwindow.title(window.title)
        newwindow.geometry(window.geometry)
        window.isopen = True
        return newwindow

displaywindow = displayWindow("Display", "500x500", 20)
clockwindow = clockWindow("Clock", "200x200")

root = tk.Tk()
root.title("root")
root.geometry("500x500")

"""
heading = tk.Label(root, text="Heading")
heading.pack()
textbox = tk.Text(root, height=3, width=18)
textbox.pack()
"""

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0,weight=1)
buttonframe.columnconfigure(1,weight=1)
buttonframe.columnconfigure(2,weight=1)
buttonframe.rowconfigure(0, weight = 1)
buttonframe.rowconfigure(1, weight = 1)
buttonframe.rowconfigure(2, weight = 1)
button1 = tk.Button(buttonframe, text="open display", command=lambda: displaywindow.build())
button1.grid(row=0, column=0, sticky=tk.W+tk.E)
button2 = tk.Button(buttonframe, text="open clock", command=lambda: clockwindow.build())
button2.grid(row=0, column=1, sticky=tk.W+tk.E)
button3 = tk.Button(buttonframe, text="exit", command=lambda: root.destroy())
button3.grid(row=0, column=2, sticky=tk.W+tk.E)
button4 = tk.Button(buttonframe, text="test", command=exit)
button4.grid(row=1, column=0, sticky=tk.W+tk.E)
button5 = tk.Button(buttonframe, text="test", command=exit)
button5.grid(row=1, column=1, sticky=tk.W+tk.E)
button6 = tk.Button(buttonframe, text="test", command=exit)
button6.grid(row=1, column=2, sticky=tk.W+tk.E)
buttonframe.pack(fill="x")


root.mainloop()
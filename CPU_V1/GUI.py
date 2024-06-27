import tkinter as tk

class GUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("CPU Emulator")

        self.setup_ui()
    
    def setup_ui(self):
        self.start_cpu_button = tk.Button(self.root, text="Start CPU", command=self.start_cpu)
        self.start_cpu_button.pack()
    
    def start_cpu(self):
        self.controller.start_cpu()
    
    def update_gui(self, data):
        pass

    def main_loop(self):
        self.root.mainloop()
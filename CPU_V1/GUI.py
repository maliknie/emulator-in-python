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

        self.open_display_window_button = tk.Button(self.root, text="Open Display Window", command=self.open_display_window)
        self.open_display_window_button.pack()
    
    def start_cpu(self):
        self.controller.start_cpu()
    
    def update_gui(self, data):
        pass

    def open_display_window(self):
        self.controller.start_screen()

    def main_loop(self):
        self.root.mainloop()
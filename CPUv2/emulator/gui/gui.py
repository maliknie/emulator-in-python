import tkinter as tk

class GUI:
    def __init__(self, controller):
        self.controller = controller
        

    def start(self):
        self.root = tk.Tk()
        self.root.title("CPU Emulator")
        self.root.geometry("200x200")
        self.root.iconphoto(True, tk.PhotoImage(file='anderes/images/tk.png'))

        self.setup_ui()
        self.main_loop()
    
    def setup_ui(self):

        self.start_cpu_button = tk.Button(self.root, text="Start Computer", command=self.start_computer)
        self.start_cpu_button.pack()

        self.open_display_window_button = tk.Button(self.root, text="Open Screen", command=self.start_screen)
        self.open_display_window_button.pack()

    def main_loop(self):
        self.root.mainloop()

    def start_computer(self):
        self.controller.start_computer()

    def start_screen(self):
        self.controller.start_screen()
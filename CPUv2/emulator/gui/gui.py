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
        self.load_program_entry = tk.Entry(self.root)
        self.load_program_entry.pack()

        self.load_program_button = tk.Button(self.root, text="Load Program", command=self.load_program)
        self.load_program_button.pack()

        self.start_cpu_button = tk.Button(self.root, text="Start Computer", command=self.start_computer)
        self.start_cpu_button.pack()

        self.shutdown_cpu_button = tk.Button(self.root, text="Shutdown Computer", command=self.shutdown_computer)
        self.shutdown_cpu_button.pack()

        self.open_display_window_button = tk.Button(self.root, text="Open Screen", command=self.start_screen)
        self.open_display_window_button.pack()

    def main_loop(self):
        self.root.mainloop()

    def load_program(self):    
        name = self.load_program_entry.get()
        self.load_program_entry.delete(0, len(name))
        path = "CPUv2/programs/bin/" + name + ".bin"
        self.controller.load_program(path)

    def start_computer(self):
        self.controller.start_computer()

    def start_screen(self):
        self.controller.start_screen()
    
    def shutdown_computer(self):
        self.controller.shutdown_computer()
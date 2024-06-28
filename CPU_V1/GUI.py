import tkinter as tk

class GUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("CPU Emulator")
        self.root.geometry("200x200")

        self.setup_ui()
    
    def setup_ui(self):
        self.load_program_entry = tk.Entry(self.root)
        self.load_program_entry.pack()

        self.load_program_button = tk.Button(self.root, text="Load Program", command=self.load_program)
        self.load_program_button.pack()

        self.start_cpu_button = tk.Button(self.root, text="Start CPU", command=self.start_cpu)
        self.start_cpu_button.pack()

        self.open_display_window_button = tk.Button(self.root, text="Open Display Window", command=self.open_display_window)
        self.open_display_window_button.pack()

        self.test_screen_button = tk.Button(self.root, text="Test Screen",  command=self.testScreen)
        self.test_screen_button.pack()

    def load_program(self):
        program = self.load_program_entry.get()
        self.load_program_entry.delete(0, len(program))
        self.controller.load_program(program)
    def start_cpu(self):
        self.controller.start_cpu()
    
    def update_gui(self, data):
        pass

    def open_display_window(self):
        self.controller.start_screen()
    
    def testScreen(self):
        self.controller.test_screen()

    def main_loop(self):
        self.root.mainloop()
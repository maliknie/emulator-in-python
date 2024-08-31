import tkinter as tk

class GUI:
    def __init__(self, controller):
        self.controller = controller
        

    def start(self):
        self.root = tk.Tk()
        self.root.title("CPU Emulator")
        self.root.geometry("200x200")
        self.root.iconphoto(True, tk.PhotoImage(file='anderes/images/tk.png'))

        self.cpu_open = False
        self.clock_open = False

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

        self.cpu_gui_button = tk.Button(self.root, text="Open CPU", command=self.cpu_loop)
        self.cpu_gui_button.pack()

        self.clock_gui_button = tk.Button(self.root, text="Open Clock", command=self.clock_loop)
        self.clock_gui_button.pack()
    def main_loop(self):
        self.root.mainloop()

    def cpu_loop(self):
        if self.cpu_open:
            return
        
        self.cpu_open = True
        self.cpu_gui = tk.Tk()
        self.cpu_gui.title("CPU")
        self.cpu_gui.geometry("500x300")
        self.cpu_gui.bind("<Destroy>",  self.cpu_gui_destroyed)

        self.tick_mode_button = tk.Button(self.cpu_gui, text="Switch Tick Mode", command=self.switch_tick_mode)
        self.tick_mode_button.pack()

        self.register_header = tk.Label(self.cpu_gui, text="Registers")
        self.register_header.pack()

        self.cpu_state = self.controller.get_cpu_state()
        print(self.cpu_state)

        self.running_label = tk.Label(self.cpu_gui, text="Running: " + str(self.cpu_state[1]["running"]))
        self.running_label.pack()

        #change running_label text:

        self.register_labels = []

        for key in self.cpu_state[0]:
            label = tk.Label(self.cpu_gui, text=key + ": " + str(self.cpu_state[0][key]))
            self.register_labels.append(label)
        
        for label in self.register_labels:
            label.pack()

        ###

        self.cpu_gui.mainloop()
    
    def clock_loop(self):
        if self.clock_open:
            return
        
        self.clock_open = True
        self.clock_gui = tk.Tk()
        self.clock_gui.title("Clock")
        self.clock_gui.geometry("200x200")
        self.clock_gui.bind("<Destroy>",  self.clock_gui_destroyed)

        self.tick_button = tk.Button(self.clock_gui, text="Tick", command=self.controller.tick_button_pressed)
        self.tick_button.pack()

        self.clock_gui.mainloop()

    def cpu_gui_destroyed(self, event):
        print("CPU GUI Destroyed")
        self.cpu_open = False
        return event
    
    def clock_gui_destroyed(self, event):
        print("Clock GUI Destroyed")
        self.clock_open = False
        return event

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

    def switch_tick_mode(self):
        self.controller.switch_tick_mode()
    
    def update_cpu_gui(self):
        print("Updating CPU GUI (GUI)")
    
        state = self.controller.get_cpu_state()
        self.running_label.config(text="Running: " + str(state[1]["running"]))
        for label in self.register_labels:
            label_name = label.cget("text").split(":")[0]
            label.config(text=label_name + ": " + str(state[0][label_name]))
        
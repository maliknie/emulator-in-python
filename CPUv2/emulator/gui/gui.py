import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self, controller):
        self.controller = controller

        # GUI Settings
        self.header_font = ("Calibri 24 bold")
        self.standard_font = ("Calibri 18")
        self.padding_x = 5
        self.padding_y = 5

        self.cpu_window_open = False
        self.clock_window_open = False
        
        

    def start(self):
        self.root = tk.Tk()
        self.root.title("CPU Emulator")
        self.root.geometry("500x500")
        self.root.iconphoto(True, tk.PhotoImage(file='anderes/images/tk.png'))

        self.setup_ui()
        self.main_loop()
    
    def setup_ui(self):
        
        #Configure Grid Layout

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)


        # Load Program Frame
        self.load_program_frame = ttk.Frame(self.root) 
        self.load_program_frame_label = ttk.Label(self.load_program_frame, text="Load Program", font=self.header_font)
        self.load_program_frame_label.grid(row=0, column=0)
        self.load_program_input_frame = ttk.Frame(self.load_program_frame)

        self.load_program_label = ttk.Label(self.load_program_input_frame, text="Enter Program Name: ", font=self.standard_font)
        self.load_program_label.grid(row=1, column=0,)
        self.load_program_entry = ttk.Entry(self.load_program_input_frame)
        self.load_program_entry.grid(row=1, column=1, padx=self.padding_x)
        self.load_program_button = ttk.Button(self.load_program_input_frame, text="Load Program", command=self.load_program)
        self.load_program_button.grid(row=1, column=2, padx=self.padding_x)

        self.load_program_input_frame.grid(row=1, column=0, padx=self.padding_x)
        self.load_program_frame.grid(row=0, column=0)

        # Computer Buttons Frame
        self.computer_buttons_frame = ttk.Frame(self.root)
        self.computer_buttons_frame_label = ttk.Label(self.computer_buttons_frame, text="Computer Controls", font=self.header_font)
        self.computer_buttons_frame_label.grid(row=0, column=0)

        self.computer_buttons_button_frame = ttk.Frame(self.computer_buttons_frame)
        self.start_cpu_button = ttk.Button(self.computer_buttons_button_frame, text="Start Computer", command=self.start_computer)
        self.start_cpu_button.grid(row=1, column=0, padx=self.padding_x)
        self.shutdown_cpu_button = ttk.Button(self.computer_buttons_button_frame, text="Shutdown Computer", command=self.shutdown_computer)
        self.shutdown_cpu_button.grid(row=1, column=1, padx=self.padding_x)

        self.computer_buttons_button_frame.grid(row=1, column=0, pady=10)
        self.computer_buttons_frame.grid(row=1, column=0)

        # GUI Buttons Frame
        self.gui_buttons_frame = ttk.Frame(self.root)
        self.gui_buttons_frame_label = ttk.Label(self.gui_buttons_frame, text="GUI Controls", font=self.header_font)
        self.gui_buttons_frame_label.grid(row=0, column=0)

        self.gui_buttons_button_frame = ttk.Frame(self.gui_buttons_frame)
        self.open_display_window_button = ttk.Button(self.gui_buttons_button_frame, text="Open Screen", command=self.start_screen)
        self.cpu_gui_button = ttk.Button(self.gui_buttons_button_frame, text="Open CPU", command=self.cpu_loop)
        self.clock_gui_button = ttk.Button(self.gui_buttons_button_frame, text="Open Clock", command=self.clock_loop)
        self.open_display_window_button.grid(row=1, column=0, padx=self.padding_x)  
        self.cpu_gui_button.grid(row=1, column=1, padx=self.padding_x)
        self.clock_gui_button.grid(row=1, column=2, padx=self.padding_x)
        self.gui_buttons_button_frame.grid(row=1, column=0, pady=10)
        self.gui_buttons_frame.grid(row=2, column=0)

    def main_loop(self):
        self.root.tk.call("source", "CPUv2/libraries/Azure-ttk-theme-main/azure.tcl")
        self.root.tk.call("set_theme", "dark")
        self.root.mainloop()

    def cpu_loop(self):
        if self.cpu_window_open:
            return
        
        self.cpu_window_open = True

        self.cpu_open = True
        self.cpu_gui = tk.Tk()
        self.cpu_gui.title("CPU")
        self.cpu_gui.geometry("500x300")
        self.cpu_gui.bind("<Destroy>",  self.cpu_gui_destroyed)

        self.tick_mode_button = ttk.Checkbutton(self.cpu_gui, text="Tick Mode", style="Switch.TCheckbutton", command=self.switch_tick_mode)
        self.tick_mode_button.pack()

        self.register_header = tk.Label(self.cpu_gui, text="Registers")
        self.register_header.pack()

        self.cpu_state = self.controller.get_cpu_state()

        self.running_label = tk.Label(self.cpu_gui, text="Running: " + str(self.cpu_state[1]["running"]))
        self.running_label.pack()

        #change running_label text:

        self.all_purpose_register_labels = []
        self.special_purpose_register_labels = []

        self.all_purpose_register_frame = ttk.Frame(self.cpu_gui)
        self.special_purpose_register_frame = ttk.Frame(self.cpu_gui)

        counter = 0
        for key in self.cpu_state[0]:
            counter += 1
            if counter < 9:
                label = ttk.Label(self.all_purpose_register_frame, text=key + ": " + str(self.cpu_state[0][key]))
                self.all_purpose_register_labels.append(label)
            else:
                label = ttk.Label(self.special_purpose_register_frame, text=key + ": " + str(self.cpu_state[0][key]))
                self.special_purpose_register_labels.append(label)
        
        for label in self.all_purpose_register_labels:
            label.pack()
        for label in self.special_purpose_register_labels:
            label.pack()
        
        self.all_purpose_register_frame.pack(side="left")
        self.special_purpose_register_frame.pack(side="left")

        ###

        self.cpu_gui.tk.call("source", "CPUv2/libraries/Azure-ttk-theme-main/azure.tcl")
        self.cpu_gui.tk.call("set_theme", "dark")
        self.cpu_gui.mainloop()
    
    def clock_loop(self):
        if self.clock_window_open:
            return
        
        self.clock_open = True
        self.clock_gui = tk.Tk()
        self.clock_gui.title("Clock")
        self.clock_gui.geometry("300x100")
        self.clock_gui.bind("<Destroy>",  self.clock_gui_destroyed)


        self.operation_label = ttk.Label(self.clock_gui, text="Current Operation: " + self.controller.computer.clock.current_operation, font=self.standard_font)
        self.operation_label.pack(pady=self.padding_y)

        self.tick_button = ttk.Button(self.clock_gui, text="Tick", command=self.controller.tick_button_pressed)
        self.tick_button.pack()


        self.clock_gui.tk.call("source", "CPUv2/libraries/Azure-ttk-theme-main/azure.tcl")
        self.clock_gui.tk.call("set_theme", "dark")
        self.clock_gui.mainloop()

    def cpu_gui_destroyed(self, event):
        self.cpu_window_open = False
        #self.cpu_open = False
        return (event,)
    
    def clock_gui_destroyed(self, event):
        self.cpu_window_open = False
        #self.clock_open = False
        return (event,)

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

        if not self.cpu_window_open and not self.controller.computer.cpu.tick_mode:
            return

        state = self.controller.get_cpu_state()
        self.running_label.config(text="Running: " + str(state[1]["running"]))

        for label in self.all_purpose_register_labels:
            label_name = label.cget("text").split(":")[0]
            label.config(text=label_name + ": " + str(state[0][label_name]))
        
        for label in self.special_purpose_register_labels:
            label_name = label.cget("text").split(":")[0]
            label.config(text=label_name + ": " + str(state[0][label_name]))

    
    def update_clock_gui(self):
        if not self.cpu_window_open and not self.controller.computer.cpu.tick_mode:
            return
        self.operation_label.config(text="Current Operation: " + self.controller.computer.clock.current_operation)

        
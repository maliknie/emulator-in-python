import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))
from libraries.binary_lib import mbin, mint, set_flag, check_flag


class GUI:
    def __init__(self, controller):
        self.controller = controller

        # GUI Settings
        self.header_font = ("Calibri 24 bold")
        self.standard_font = ("Calibri 18")
        self.small_font = ("Monospace 10")
        self.padding_x = 5
        self.padding_y = 5

        self.cpu_window_open = False
        self.clock_window_open = False
        self.alu_window_open = False
        self.ram_window_open = False
        self.log_window_open = False

        self.memory_address_entry = None
        self.new_ram_result = None
        self.current_ram_address = None
        
        self.new_events = []
        
    # Startet das root Fenster
    def start(self):
        self.root = tk.Tk()
        self.root.title("CPU Emulator")
        self.root.geometry("600x600")
        self.root.iconphoto(True, tk.PhotoImage(file='anderes/images/tk.png'))

        self.setup_ui()
        self.main_loop()
    
    # Setzt das Layout des root Fensters
    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)


        # Load Program Frame
        self.load_program_frame = ttk.Frame(self.root) 
        self.load_program_frame_label = ttk.Label(self.load_program_frame, text="Load Program", font=self.header_font)
        self.load_program_frame_label.grid(row=0, column=0, sticky="n", pady=self.padding_y, padx=self.padding_x)
        self.load_program_input_frame = ttk.Frame(self.load_program_frame)

        self.load_program_label = ttk.Label(self.load_program_input_frame, text="Enter Program Name: ", font=self.standard_font)
        self.load_program_label.grid(row=1, column=0, padx=self.padding_x, pady=self.padding_y)
        self.load_program_entry = ttk.Entry(self.load_program_input_frame)
        self.load_program_entry.grid(row=1, column=1, padx=self.padding_x, pady=self.padding_y)
        self.load_program_button = ttk.Button(self.load_program_input_frame, text="Load Program", command=self.load_program)
        self.load_program_button.grid(row=1, column=2, padx=self.padding_x, pady=self.padding_y)

        self.load_program_input_frame.grid(row=1, column=0, padx=self.padding_x, pady=self.padding_y)
        self.load_program_frame.grid(row=0, column=0, sticky="n", pady=self.padding_y, padx=self.padding_x)

        # Computer Buttons Frame
        self.computer_buttons_frame = ttk.Frame(self.root)
        self.computer_buttons_frame_label = ttk.Label(self.computer_buttons_frame, text="Computer Controls", font=self.header_font)
        self.computer_buttons_frame_label.grid(row=0, column=0, pady=self.padding_y, padx=self.padding_x)

        self.computer_buttons_button_frame = ttk.Frame(self.computer_buttons_frame)
        self.start_cpu_button = ttk.Button(self.computer_buttons_button_frame, text="Start Computer", command=self.start_computer)
        self.start_cpu_button.grid(row=1, column=0, padx=self.padding_x, pady=self.padding_y)
        self.shutdown_cpu_button = ttk.Button(self.computer_buttons_button_frame, text="Shutdown Computer", command=self.shutdown_computer)
        self.shutdown_cpu_button.grid(row=1, column=1, padx=self.padding_x, pady=self.padding_y)

        self.computer_buttons_button_frame.grid(row=1, column=0, pady=self.padding_y, padx=self.padding_x)
        self.computer_buttons_frame.grid(row=1, column=0, pady=self.padding_y, padx=self.padding_x)

        # GUI Buttons Frame
        self.gui_buttons_frame = ttk.Frame(self.root)
        self.gui_buttons_frame_label = ttk.Label(self.gui_buttons_frame, text="GUI Controls", font=self.header_font)
        self.gui_buttons_frame_label.grid(row=0, column=0)

        self.gui_buttons_button_frame = ttk.Frame(self.gui_buttons_frame)
        self.open_display_window_button = ttk.Button(self.gui_buttons_button_frame, text="Open Screen", command=self.start_screen)
        self.cpu_gui_button = ttk.Button(self.gui_buttons_button_frame, text="Open CPU", command=self.cpu_loop)
        self.clock_gui_button = ttk.Button(self.gui_buttons_button_frame, text="Open Clock", command=self.clock_loop)
        self.alu_gui_button = ttk.Button(self.gui_buttons_button_frame, text="Open ALU", command=self.alu_loop)
        self.ram_gui_button = ttk.Button(self.gui_buttons_button_frame, text="Open RAM", command=self.ram_loop)
        self.log_gui_button = ttk.Button(self.gui_buttons_button_frame, text="Open Log", command=self.log_loop)

        self.open_display_window_button.grid(row=1, column=0, padx=self.padding_x, pady=self.padding_y)  
        self.cpu_gui_button.grid(row=1, column=1, padx=self.padding_x, pady=self.padding_y)
        self.clock_gui_button.grid(row=1, column=2, padx=self.padding_x, pady=self.padding_y)
        self.alu_gui_button.grid(row=2, column=0, padx=self.padding_x, pady=self.padding_y)
        self.ram_gui_button.grid(row=2, column=1, padx=self.padding_x, pady=self.padding_y)
        self.log_gui_button.grid(row=2, column=2, padx=self.padding_x, pady=self.padding_y)
        self.gui_buttons_button_frame.grid(row=1, column=0, pady=10)
        self.gui_buttons_frame.grid(row=2, column=0)

    # Startet die main Schleife des root Fensters
    def main_loop(self):
        self.root.tk.call("source", "CPUv2/libraries/Azure-ttk-theme-main/azure.tcl")
        self.root.tk.call("set_theme", "dark")
        self.root.mainloop()



    # Startet das CPU Fenster
    def cpu_loop(self):
        if self.cpu_window_open:
            return
        
        self.cpu_window_open = True

        self.cpu_open = True
        self.cpu_gui = tk.Tk()
        self.cpu_gui.title("CPU")
        self.cpu_gui.geometry("550x300")
        self.cpu_gui.protocol("WM_DELETE_WINDOW", self.cpu_gui_destroyed)

        self.register_header = tk.Label(self.cpu_gui, text="Registers", font=self.header_font)
        self.register_header.grid(sticky="w")

        self.cpu_state = self.controller.get_cpu_state()

        self.all_purpose_register_labels = []
        self.special_purpose_register_labels = []
        self.register_32_bit_frame_labels = []

        self.all_purpose_register_frame = ttk.Frame(self.cpu_gui)
        self.special_purpose_register_frame = ttk.Frame(self.cpu_gui)
        self.register_32_bit_frame = ttk.Frame(self.cpu_gui)

        counter = 0
        for key in self.cpu_state[0]:
            counter += 1
            if counter < 9:
                content = str(self.cpu_state[0][key])
                label = ttk.Label(self.all_purpose_register_frame, text=key + ": " + content + " (" +str(mint(content)) + ")", font=self.small_font)
                self.all_purpose_register_labels.append(label)
            else:
                content = str(self.cpu_state[0][key])
                if not key in ["ir", "flags"]:
                    message = key + ": " + content + " (" + str(mint(content)) + ")"
                elif key == "ir":
                    message = key + ": " + content + " (" + self.decode_instruction(content) + ") "
                else:
                    message = key + ": " + content

                if key in ["ir", "acc"]:
                    label = ttk.Label(self.register_32_bit_frame, text=message, font=self.small_font)
                    self.register_32_bit_frame_labels.append(label)
                    continue
                label = ttk.Label(self.special_purpose_register_frame, text=message, font=self.small_font)
                self.special_purpose_register_labels.append(label)
        
    

        
        for i, label in enumerate(self.all_purpose_register_labels):
            label.grid(sticky="w", row=i, column=0)
        for i, label in enumerate(self.special_purpose_register_labels):
            label.grid(sticky="w", row=i, column=0)
        for i, label in enumerate(self.register_32_bit_frame_labels):
            label.grid(sticky="w", row=i, column=0)
        
        self.all_purpose_register_frame.grid(row=1, column=0, pady=self.padding_y, sticky="w")
        self.special_purpose_register_frame.grid(row=1, column=1, pady=self.padding_y, sticky="w")
        self.register_32_bit_frame.grid(row=2, column=0, pady=self.padding_y, sticky="w")

        self.cpu_gui.tk.call("source", "CPUv2/libraries/Azure-ttk-theme-main/azure.tcl")
        self.cpu_gui.tk.call("set_theme", "dark")
        self.cpu_gui.mainloop()
    
    # Startet das Clock Fenster
    def clock_loop(self):
        if self.clock_window_open:
            return
        
        self.clock_window_open = True
        self.clock_gui = tk.Tk()
        self.clock_gui.title("Clock")
        self.clock_gui.geometry("350x150")
        self.clock_gui.protocol("WM_DELETE_WINDOW", self.clock_gui_destroyed)

        self.operation_and_tick_frame = ttk.Frame(self.clock_gui)
        self.tick_mode_frame = ttk.Frame(self.clock_gui)

        self.operation_label = ttk.Label(self.operation_and_tick_frame, text="Current Operation: " + self.controller.computer.clock.current_operation, font=self.standard_font)
        self.operation_label.grid(pady=self.padding_y, padx=self.padding_x, sticky="w", row=0, column=0)
        self.tick_button = ttk.Button(self.operation_and_tick_frame, text="Tick", command=self.controller.tick_button_pressed)
        self.tick_button.grid(pady=self.padding_y, padx=self.padding_x, sticky="w", row=1, column=0)

        self.tick_mode_on_button = ttk.Button(self.tick_mode_frame, text="Tick Mode On", command=self.controller.tick_mode_on)
        self.tick_mode_off_button = ttk.Button(self.tick_mode_frame, text="Tick Mode Off", command=self.controller.tick_mode_off)
        self.tick_mode_on_button.grid(row=0, column=0, padx=self.padding_x, pady=self.padding_y, sticky="w")
        self.tick_mode_off_button.grid(row=0, column=1, padx=self.padding_x, pady=self.padding_y, sticky="w")

        self.operation_and_tick_frame.grid(row=0, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.tick_mode_frame.grid(row=1, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")

        self.clock_gui.tk.call("source", "CPUv2/libraries/Azure-ttk-theme-main/azure.tcl")
        self.clock_gui.tk.call("set_theme", "dark")
        self.clock_gui.mainloop()

    def alu_loop(self):
        if self.alu_window_open:
            return
        
        self.alu_window_open = True

        self.alu_gui = tk.Tk()
        self.alu_gui.title("ALU")
        self.alu_gui.geometry("750x100")
        self.alu_gui.protocol("WM_DELETE_WINDOW", self.alu_gui_destroyed)

        self.alu_operand_frame = ttk.Frame(self.alu_gui)
        self.alu_operation_frame = ttk.Frame(self.alu_gui)
        self.alu_result_frame = ttk.Frame(self.alu_gui)
        self.alu_arrow_1_frame = ttk.Frame(self.alu_gui)
        self.alu_arrow_2_frame = ttk.Frame(self.alu_gui)

        self.alu_arrow_1 = ttk.Label(self.alu_arrow_1_frame, text="→", font=self.standard_font)
        self.alu_arrow_2 = ttk.Label(self.alu_arrow_2_frame, text="→", font=self.standard_font)
        self.alu_arrow_1.grid(row=0, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.alu_arrow_2.grid(row=0, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")

        self.alu_operand_a_label = ttk.Label(self.alu_operand_frame, text="Operand a: None", font=self.standard_font)
        self.alu_operand_b_label = ttk.Label(self.alu_operand_frame, text="Operand b: None", font=self.standard_font)
        self.alu_operand_a_label.grid(row=0, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.alu_operand_b_label.grid(row=2, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")

        self.alu_operation_label = ttk.Label(self.alu_operation_frame, text="Operation: None", font=self.standard_font)
        self.alu_operation_label.grid(row=1, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")

        self.alu_result_label = ttk.Label(self.alu_result_frame, text="Result: None", font=self.standard_font)
        self.alu_result_label.grid(row=2, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")


        self.alu_operand_frame.grid(row=0, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.alu_arrow_1_frame.grid(row=0, column=1, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.alu_operation_frame.grid(row=0, column=2, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.alu_arrow_2_frame.grid(row=0, column=3, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.alu_result_frame.grid(row=0, column=4, pady=self.padding_y, padx=self.padding_x, sticky="w")

        self.alu_gui.tk.call("source", "CPUv2/libraries/Azure-ttk-theme-main/azure.tcl")
        self.alu_gui.tk.call("set_theme", "dark")
        self.alu_gui.mainloop()

    def ram_loop(self):
        if self.ram_window_open:
            return
        
        self.ram_window_open = True

        self.ram_gui = tk.Tk()
        self.ram_gui.title("RAM")
        self.ram_gui.geometry("600x200")
        self.ram_gui.protocol("WM_DELETE_WINDOW", self.ram_gui_destroyed)

        self.ram_label_frame = ttk.Frame(self.ram_gui)
        self.ram_entry_frame = ttk.Frame(self.ram_gui)
        self.ram_result_frame = ttk.Frame(self.ram_gui)

        self.ram_label = ttk.Label(self.ram_label_frame, text="Memory", font=self.header_font)
        self.ram_label.grid(row=0, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")

        self.ram_entry_label = ttk.Label(self.ram_entry_frame, text="Enter Memory Address: ", font=self.standard_font)
        self.ram_entry_label.grid(row=1, column=0)
        self.ram_entry = ttk.Entry(self.ram_entry_frame)
        self.ram_entry.grid(row=1, column=1)
        self.ram_entry_button = ttk.Button(self.ram_entry_frame, text="Read Memory", command=lambda: self.controller.read_memory(self.ram_entry.get(), triggered_by_gui=True))
        self.ram_entry_button.grid(row=1, column=2, padx=self.padding_x, pady=self.padding_y, sticky="w")

        self.ram_result_label = ttk.Label(self.ram_result_frame, text="Result: None", font=self.standard_font)
        self.ram_result_label.grid(row=2, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")

        self.ram_label_frame.grid(row=0, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.ram_entry_frame.grid(row=1, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.ram_result_frame.grid(row=2, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")


        self.ram_gui.tk.call("source", "CPUv2/libraries/Azure-ttk-theme-main/azure.tcl")
        self.ram_gui.tk.call("set_theme", "dark")
        self.ram_gui.mainloop()

    def log_loop(self):
        if self.log_window_open:
            return
        
        self.log_window_open = True

        self.log_gui = tk.Tk()
        self.log_gui.title("Log")
        self.log_gui.geometry("800x300")
        self.log_gui.protocol("WM_DELETE_WINDOW", self.log_gui_destroyed)

        self.log_label_frame = ttk.Frame(self.log_gui)
        self.log_text_frame = ttk.Frame(self.log_gui)

        self.log_label = ttk.Label(self.log_label_frame, text="Last Log Entries: ", font=self.header_font)
        self.log_text = ttk.Label(self.log_text_frame, text="None", font=self.small_font)
        self.log_label.grid(row=0, column=0, padx=self.padding_x, pady=self.padding_y, sticky="w")
        self.log_text.grid(row=0, column=0, padx=self.padding_x, pady=self.padding_y, sticky="w")


        self.log_label_frame.grid(row=0, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")
        self.log_text_frame.grid(row=1, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")

        self.log_gui.tk.call("source", "CPUv2/libraries/Azure-ttk-theme-main/azure.tcl")
        self.log_gui.tk.call("set_theme", "dark")
        self.log_gui.mainloop()


    # Wird ausgeführt, wenn das CPU Fenster geschlossen wird
    def cpu_gui_destroyed(self):
        self.cpu_window_open = False
        self.cpu_gui.destroy()
    
    # Wird ausgeführt, wenn das Clock Fenster geschlossen wird
    def clock_gui_destroyed(self):
        self.clock_window_open = False
        self.clock_gui.destroy()

    # Wird ausgeführt, wenn das ALU Fenster geschlossen wird
    def alu_gui_destroyed(self):
        self.alu_window_open = False
        self.alu_gui.destroy()
    
    # Wird ausgeführt, wenn das RAM Fenster geschlossen wird
    def ram_gui_destroyed(self):
        self.ram_window_open = False
        self.ram_gui.destroy()
    
    # Wird ausgeführt, wenn das Log Fenster geschlossen wird
    def log_gui_destroyed(self):
        self.log_window_open = False
        self.log_gui.destroy()
    

    
    # Aktualisiert das CPU Fenster
    def update_cpu_gui(self):
        if not self.cpu_window_open:
            return
        try:
            state = self.controller.get_cpu_state()
            

            for label in self.all_purpose_register_labels:
                if not label.winfo_exists():
                    continue
                label_name = label.cget("text").split(":")[0]
                message = label_name + ": " + str(state[0][label_name]).zfill(16) + " (" + str(mint(state[0][label_name])) + ")"
                label.config(text=message)
            
            for label in self.special_purpose_register_labels:
                if not label.winfo_exists():
                    continue
                label_name = label.cget("text").split(":")[0]
                if label_name == "flags":
                    message = label_name + ": " + str(state[0][label_name]).zfill(16)
                else:
                    message = label_name + ": " + str(state[0][label_name]).zfill(16) + " (" + str(mint(state[0][label_name])) + ")"
                label_name = label.cget("text").split(":")[0]
                label.config(text=message)
            
            for label in self.register_32_bit_frame_labels:
                if not label.winfo_exists():
                    continue
                label_name = label.cget("text").split(":")[0]
                if label_name == "ir":
                    message = label_name + ": " + str(state[0][label_name]).zfill(32) + " (" + self.decode_instruction(state[0][label_name]) + ")"
                else:
                    message = label_name + ": " + str(state[0][label_name]).zfill(32) + " (" + str(mint(state[0][label_name])) + ")"
                label.config(text=message)
        except tk.TclError:
            pass
        
            

    # Aktualisiert das Clock Fenster
    def update_clock_gui(self):
        if not self.clock_window_open:
            return
        try: 
            if self.operation_label.winfo_exists():
                self.operation_label.config(text="Current Operation: " + self.controller.computer.clock.current_operation)
        except tk.TclError:
            pass

    # Aktualisiert das ALU Fenster
    def update_alu_gui(self, op, a, b, result):
        if not self.alu_window_open:
            return
        
        try:
            if self.alu_operand_a_label.winfo_exists():
                self.alu_operand_a_label.config(text="Operand a: " + str(a) + " (" + str(mint(a)) + ")")
            if self.alu_operand_b_label.winfo_exists():
                self.alu_operand_b_label.config(text="Operand b: " + str(b) + " (" + str(mint(b)) + ")")
            if self.operation_label.winfo_exists():
                self.alu_operation_label.config(text="Operation: " + op)
            if self.alu_result_label.winfo_exists():
                self.alu_result_label.config(text="Result: " + result + " (" + str(mint(result)) + ")")
        except tk.TclError:
            pass

    # Aktualisiert das RAM Fenster
    def update_ram_gui(self, triggered_by_gui=False):
        if not self.ram_window_open:
            return
        try:
            if self.current_ram_address == None:
                if self.ram_result_label.winfo_exists():
                    self.ram_result_label.config(text="Result: Invalid Address")
                return
            if triggered_by_gui:
                self.new_ram_result = self.controller.computer.memory.read(self.current_ram_address, triggered_by_gui=True)
            else:
                self.new_ram_result = self.controller.computer.memory.read(self.current_ram_address)
            if self.ram_result_label.winfo_exists():
                self.ram_result_label.config(text="Result: " + str(self.new_ram_result) + " (" + str(mint(self.new_ram_result)) + ")")
        except tk.TclError:
            pass

    # Aktualisiert das Log Fenster
    def update_log_gui(self):
        if not self.log_window_open:
            return
        try: 
            for widget in self.log_text_frame.winfo_children():
                widget.destroy()
            
            for i, event in enumerate(self.new_events):
                label = ttk.Label(self.log_text_frame, text=event, font=self.small_font)
                label.grid(row=i, column=0, padx=self.padding_x, pady=self.padding_y, sticky="w")
            self.log_text_frame.grid(row=1, column=0, pady=self.padding_y, padx=self.padding_x, sticky="w")
        except tk.TclError:
            pass

        
        self.new_events = []




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

    def decode_instruction(self, instruction):
        reg_dict = self.controller.computer.cpu.registers
        opcode = instruction[:8]
        operand1 = instruction[8:12]
        operand2 = instruction[12:16]
        operand3 = instruction[16:32]
        
        match opcode:
            case "00000000":
                return "jmp #" + str(mint(operand3))
            case "00000001":
                return "jeq #" + str(mint(operand3))
            case "00000010":
                return "jne #" + str(mint(operand3))
            case "00000011":
                return "inc [" + str(mint(operand3)) + "]"
            case "00000100":
                return "dec [" + str(mint(operand3)) + "]"
            case "00000101":
                return "load #" + str(mint(operand3)) + ", " + reg_dict[operand1]
            case "00000110":
                return "load [" + str(mint(operand3)) + "], " + reg_dict[operand1]
            case "00000111":
                return "store " + reg_dict[operand1] + ", [" + str(mint(operand3)) + "]"
            case "00001000":
                return "jmp " + reg_dict[operand1]
            case "00001001":
                return "jeq " + reg_dict[operand1]
            case "00001010":
                return "jne " + reg_dict[operand1]
            case "00001011":
                return "store [" + reg_dict[operand1] + "], " + reg_dict[operand2]
            case "00001100":
                return "move " + reg_dict[operand1] + ", " + reg_dict[operand2]
            case "00001101":
                return "add " + reg_dict[operand1] + ", " + reg_dict[operand2]
            case "00001110":
                return "sub " + reg_dict[operand1] + ", " + reg_dict[operand2]
            case "00001111":
                return "mult " + reg_dict[operand1] + ", " + reg_dict[operand2]
            case "00010000":
                return "div " + reg_dict[operand1] + ", " + reg_dict[operand2]
            case "00010001":
                return "inc " + reg_dict[operand1]
            case "00010010":
                return "dec " + reg_dict[operand1]
            case "00010011":
                return "and " + reg_dict[operand1] + ", " + reg_dict[operand2]
            case "00010100":
                return "or " + reg_dict[operand1] + ", " + reg_dict[operand2]
            case "00010101":
                return "xor " + reg_dict[operand1] + ", " + reg_dict[operand2]
            case "00010110":
                return "not " + reg_dict[operand1]
            case "00010111":
                return "rol " + reg_dict[operand1] + ", #" + str(mint(operand2))
            case "00011000":
                return "ror " + reg_dict[operand1] + ", #" + str(mint(operand2))
            case "00011001":
                return "cmp " + reg_dict[operand1] + ", " + reg_dict[operand2]
            case "00011010":
                return "shl " + reg_dict[operand1] + ", #" + str(mint(operand2))
            case "00011011":
                return "shr " + reg_dict[operand1] + ", #" + str(mint(operand2))
            case "11111111":
                return "hlt"

            case _:
                return "None"
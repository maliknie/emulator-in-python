import threading

# Vermittlerklasse, die die Kommunikation zwischen GUI, Computer und Bildschirm steuert

class AppController:
    def __init__(self, gui, computer, screen):
        self.gui = gui
        self.computer = computer
        self.screen = screen

    def load_program(self, program_path):
        self.computer.memory.load_program(program_path)
    
    def start_computer(self):
        self.computer_thread = threading.Thread(target=self.computer.run, daemon=True)
        self.computer_thread.start()
    
    def reset(self):
        self.computer.reset()
        self.gui.new_events = []
        self.update_gui()

    def start_screen(self):
        self.screen_thread = threading.Thread(target=self.screen.run, daemon=True)
        self.screen_thread.start()
    
    def start_gui(self):
        self.gui.start()
    
    def get_cpu_state(self):
        return self.computer.cpu.get_state()
    
    def tick_button_pressed(self):
        self.computer.clock.tick_button_pressed()
    
    def tick_mode_on(self):
        self.computer.cpu.tick_mode = True
    
    def tick_mode_off(self):
        self.computer.cpu.tick_mode = False
    
    def update_gui(self):
        self.gui.update_cpu_gui()
        self.gui.update_clock_gui()
        self.gui.update_ram_gui()
        self.gui.update_alu_gui()
        self.gui.update_stdout_gui()
        self.gui.update_log_gui()
    
    def add_event(self, event):
        self.gui.new_events.append(event)

    # work in progress, everything should be encoded in UTF-16
    def write_to_stdout(self, data):
        self.gui.data = data
        self.gui.update_stdout_gui()
    
    def read_memory(self, address, triggered_by_gui=False):
        if address.isdigit():
            address = int(address)
            self.gui.current_ram_address = address
            self.gui.update_ram_gui(triggered_by_gui=triggered_by_gui)
            return
        
        self.gui.current_ram_address = None
        self.gui.update_ram_gui()
        return
    
    def destroy_screen(self):
        self.screen.stop()
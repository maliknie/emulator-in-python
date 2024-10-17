import threading

# Vermittlerklass, die die Kommunikation zwischen GUI, Computer und Bildschirm steuert

class AppController:
    def __init__(self, gui, computer, screen):
        self.gui = gui
        self.computer = computer
        self.screen = screen

    def load_program(self, program_path):
        self.computer.memory.load_program(program_path)
    
    def start_computer(self):
        print("Starting computer")
        self.computer_thread = threading.Thread(target=self.computer.run, daemon=True)
        self.computer_thread.start()
    
    def shutdown_computer(self):
        print("Shutting down computer")
        self.computer.shutdown()

    def start_screen(self):
        print("Starting screen")
        self.screen_thread = threading.Thread(target=self.screen.run, daemon=True)
        self.screen_thread.start()
    
    def start_gui(self):
        self.gui.start()
    
    def get_cpu_state(self):
        return self.computer.cpu.get_state()
    
    def tick_button_pressed(self):
        self.computer.clock.tick_button_pressed()
    
    def switch_tick_mode(self):
        print("Switching tick mode")
        self.computer.cpu.switch_tick_mode()
    
    def update_gui(self):
        self.gui.update_cpu_gui()
        self.gui.update_clock_gui()
    
    def read_memory(self, address):
        if address.isdigit():
            address = int(address)
            self.gui.current_ram_address = address
            self.gui.update_ram_gui()
            return
        
        self.gui.current_ram_address = None
        self.gui.update_ram_gui()
        return

        
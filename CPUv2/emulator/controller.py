import threading

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
    
    def shutdown_computer(self):
        self.computer.shutdown()

    def start_screen(self):
        self.screen_thread = threading.Thread(target=self.screen.run, daemon=True)
        self.screen_thread.start()
    
    def start_gui(self):
        self.gui.start()
    
    def get_cpu_state(self):
        return self.computer.cpu.get_state()
    
    def tick_button_pressed(self):
        self.computer.clock.tick_button_pressed()
    
    def switch_tick_mode(self):
        self.computer.cpu.switch_tick_mode()
    
    def update_cpu_state(self):
        print("Updating CPU State (Controller)")
        self.gui.update_cpu_gui()
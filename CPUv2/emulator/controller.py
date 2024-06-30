import threading

class AppController:
    def __init__(self, gui, computer, screen):
        self.gui = gui
        self.computer = computer
        self.screen = screen
    
    def start_computer(self):
        self.computer_thread = threading.Thread(target=self.computer.run, daemon=True)
        self.computer_thread.start()

    def start_screen(self):
        self.screen_thread = threading.Thread(target=self.screen.run, daemon=True)
        self.screen_thread.start()
    
    def start_gui(self):
        self.gui.start()
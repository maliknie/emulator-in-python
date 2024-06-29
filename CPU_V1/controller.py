import threading

class AppController:
    def __init__(self, gui_class, cpu_instance, pygamedisplay_instance):
        self.gui = gui_class(self)
        self.cpu = cpu_instance
        self.pygamedisplay = pygamedisplay_instance
    
    def start_cpu(self):
        self.cpu_thread = threading.Thread(target=self.cpu.run, daemon=True)
        self.cpu_thread.start()
    
    def stop_cpu(self):
        self.cpu.stop()

    def start_screen(self):
        self.screen_thread = threading.Thread(target=self.pygamedisplay.run, daemon=True)
        self.screen_thread.start()

    def load_program(self, program):
        self.cpu.loadProgram(program)
    
    def test_screen(self):
        self.test_screen_thread = threading.Thread(target=self.cpu.testScreen, daemon=True)
        self.test_screen_thread.start()
    
    def update_gui(self, data):
        pass
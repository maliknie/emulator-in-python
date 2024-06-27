import threading
class AppController:
    def __init__(self, gui_class, cpu_instance):
        self.gui = gui_class(self)
        self.cpu = cpu_instance
    
    def start_cpu(self):
        self.cpu_thread = threading.Thread(target=self.cpu.run, daemon=True)
        self.cpu_thread.start()
    
    def update_gui(self, data):
        pass
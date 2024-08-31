import threading

class Clock():
    def __init__(self, computer) -> None:
        self.computer = computer
        self.tick_event = threading.Event()

    def tick(self):
        print("Ticking")
        if self.computer.cpu.tick_mode:
            self.computer.cpu.cu.fetch()
            self.computer.controller.gui.update_cpu_gui()
            self.wait_for_tick()
            self.computer.cpu.cu.decode()
            self.computer.controller.gui.update_cpu_gui()
            self.wait_for_tick()
            self.computer.cpu.cu.execute()
            self.computer.controller.gui.update_cpu_gui()
            self.wait_for_tick()

        else:
            self.computer.cpu.cu.fetch()
            self.computer.controller.gui.update_cpu_gui()
            self.computer.cpu.cu.decode()
            self.computer.controller.gui.update_cpu_gui()
            self.computer.cpu.cu.execute()
            self.computer.controller.gui.update_cpu_gui()
        
        
            
    def wait_for_tick(self):
        self.tick_event.clear()
        self.tick_event.wait()

    def run(self):
        self.computer.cpu.running = True
        while self.computer.cpu.running:
            self.tick()

    def tick_button_pressed(self):
        self.tick_event.set()
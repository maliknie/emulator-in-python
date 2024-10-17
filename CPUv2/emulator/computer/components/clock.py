import threading

class Clock():
    def __init__(self, computer) -> None:
        self.computer = computer
        self.current_operation = "None"
        self.tick_event = threading.Event()

    def tick(self):
        if self.computer.cpu.tick_mode:
            self.current_operation = "Fetch"
            self.computer.cpu.cu.fetch()
            self.computer.controller.update_gui()
            self.wait_for_tick()
            self.current_operation = "Decode"
            self.computer.cpu.cu.decode()
            self.computer.controller.update_gui()
            self.wait_for_tick()
            self.current_operation = "Execute"
            self.computer.cpu.cu.execute()
            self.computer.controller.update_gui()
            self.wait_for_tick()

        else:
            self.current_operation = "Fetch"
            self.computer.cpu.cu.fetch()
            self.computer.controller.update_gui()
            self.current_operation = "Decode"
            self.computer.cpu.cu.decode()
            self.computer.controller.update_gui()
            self.current_operation = "Execute"
            self.computer.cpu.cu.execute()
            self.computer.controller.update_gui()
        
        
            
    def wait_for_tick(self):
        self.tick_event.clear()
        self.tick_event.wait()

    def run(self):
        self.computer.cpu.running = True
        while self.computer.cpu.running:
            self.tick()

    def tick_button_pressed(self):
        self.tick_event.set()
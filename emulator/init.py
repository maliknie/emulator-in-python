from controller import AppController as Controller


from computer.components.cpu import CPU
from computer.components.cu import CU
from computer.components.alu import ALU
from computer.components.memory import RAM
from computer.computer import Computer
from computer.components.clock import Clock

from devices.screen import PixelDisplay

from gui.gui import GUI

def initialize_system(ram_size):
    controller = Controller(None, None, None)

    memory = RAM(size=ram_size)
    cpu = CPU(None, None, None)
    alu = ALU(cpu)
    cu = CU(cpu)
    clock = Clock(None)
    cpu.alu = alu
    cpu.cu = cu

    
    computer = Computer(controller, cpu, memory, clock)
    cpu.computer = computer
    clock.computer = computer
    memory.computer = computer

    controller.computer = computer

    screen = PixelDisplay(controller)

    gui = GUI(controller)
    
    controller.screen = screen
    controller.gui = gui




    
    return controller
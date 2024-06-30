from controller import AppController as Controller


from computer.components.cpu import CPU
from computer.components.cu import CU
from computer.components.alu import ALU
from computer.components.memory import RAM
from computer.computer import Computer

from devices.screen import pixelDisplay

from gui.gui import GUI

def initialize_system():
    controller = Controller(None, None, None)

    memory = RAM(size=65536)
    cpu = CPU(None, None)
    alu = ALU(cpu)
    cu = CU(cpu)
    cpu.alu = alu
    cpu.cu = cu
    
    computer = Computer(cpu=cpu, memory=memory)

    screen = pixelDisplay(memory)

    gui = GUI(controller)

    controller.computer = computer
    controller.screen = screen
    controller.gui = gui




    
    return controller
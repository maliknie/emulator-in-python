from GUI import GUI
from CPU import CPU
from CPU import CU
from CPU import ALU
from RAM import RAM
from screen import pixelDisplay
from controller import AppController

if __name__ == "__main__":
    ram_instance = RAM(100000)
    cu_instance = CU()
    alu_instance = ALU()
    cpu_instance = CPU(ram_instance, cu_instance, alu_instance)
    pygame_instance = pixelDisplay(ram_instance)
    controller = AppController(GUI, cpu_instance, pygame_instance)
    controller.gui.main_loop()
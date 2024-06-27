# standard libraries
import tkinter as tk
import random
import threading
import time

# custom libraries
import RAM
import CPU
import byte
import register
import GUI
import display

RAM_SIZE = 65536 # 0 - 65536
FIRST_K = 10
PRINT_RAM = True
PRINT_FIRST_K = False

def build_computer(ram_size: int = 65536):
    mainmemory = RAM.RAM(ram_size)
    controlunit = CPU.CU()
    arithmeticandlogicunit = CPU.ALU()
    cpu = CPU.CPU(mainmemory, controlunit, arithmeticandlogicunit)
    return mainmemory, controlunit, arithmeticandlogicunit, cpu

def load_program(mainmemory: RAM.RAM):
    print("Initiating RAM...")
    mainmemory.setValueAtIndex(byte.Byte().setByte('00000011'), 2)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 3)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00010000'), 4)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00000011'), 5)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 6)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00010000'), 7)
    mainmemory.setValueAtIndex(byte.Byte().setByte('10000010'), 8)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 9)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 10)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00001010'), 11)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00000000'), 16)
    mainmemory.setValueAtIndex(byte.Byte().setByte('00000001'), 17)

def set_pc(controlunit: CPU.CU, start_index: int):
    new_register = register.Register()
    new_register.setRegisterFromInt(start_index)
    controlunit.PC = new_register

def build_gui():
    displaywindow = GUI.displayWindow("Pixel Display", "1080x1080")
    clockwindow = GUI.clockWindow("Clock", "200x200")
    root = GUI.rootWindow("CPU Modell", "500x500")
    root.build(displaywindow, clockwindow)

    canvas = tk.Canvas(displaywindow, width=1024, height=1024)
    canvas.pack()

    screen = display.Display(mainmemory, canvas)


"""
RUN PROGRAM
"""

mainmemory, controlunit, arithmeticandlogicunit, cpu = build_computer(RAM_SIZE)
set_pc(controlunit, 2)
load_program(mainmemory)
build_gui()
cpu.run()


"""
DEBUG OUTPUT
"""
k = 0
for value in mainmemory.registers:
    if (value.getByte() != "00000000" and PRINT_RAM) or (k < FIRST_K and PRINT_FIRST_K):
        if value.negative:
            print(hex(k), value.getByte(), value.getInt(), "negative")
        else:
            print(hex(k), value.getByte(), value.getInt())
    k += 1
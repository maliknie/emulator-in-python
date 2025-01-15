# Custom Emulator Project

This repository contains a custom-built emulator that simulates a simplified CPU architecture. The project includes a custom instruction set architecture (ISA), an assembler, and example programs to demonstrate functionality.

## Features

- **Custom ISA:** Supports arithmetic, control flow, memory manipulation, and bitwise operations.
- **Assembler:** Converts assembly programs into machine code executable by the emulator.
- **Pixel-based Display:** Uses `pygame==2.6.1` to create a pixel-based display for graphical output.
- **Example Programs:** Includes example programs like Fibonacci sequence generation.

## File Structure

```
.
├── assembler
│   ├── assembler.py
│   └── assemblerv2.py
├── docs
│   └── isa.md
├── emulator
│   ├── computer
│   │   ├── components
│   │   │   ├── alu.py
│   │   │   ├── clock.py
│   │   │   ├── cpu.py
│   │   │   ├── cu.py
│   │   │   ├── memory.py
│   │   │   └── __pycache__
│   │   │       ├── alu.cpython-311.pyc
│   │   │       ├── clock.cpython-311.pyc
│   │   │       ├── cpu.cpython-311.pyc
│   │   │       ├── cu.cpython-311.pyc
│   │   │       └── memory.cpython-311.pyc
│   │   ├── computer.py
│   │   └── __pycache__
│   │       └── computer.cpython-311.pyc
│   ├── controller.py
│   ├── devices
│   │   ├── __pycache__
│   │   │   └── screen.cpython-311.pyc
│   │   └── screen.py
│   ├── gui
│   │   ├── gui.py
│   │   └── __pycache__
│   │       └── gui.cpython-311.pyc
│   ├── init.py
│   ├── main.py
│   └── __pycache__
│       ├── controller.cpython-311.pyc
│       └── init.cpython-311.pyc
├── images
│   ├── icon.png
│   └── tk.png
├── libraries
│   ├── Azure-ttk-theme-main
│   │   ├── azure.tcl
│   │   ├── Dark screenshot.png
│   │   ├── example.py
│   │   ├── LICENSE
│   │   ├── Light screenshot.png
│   │   ├── README.md
│   │   ├── screenshot.png
│   │   └── theme
│   │       ├── dark
│   │       │   ├── box-accent.png
│   │       │   ├── box-basic.png
│   │       │   ├── box-hover.png
│   │       │   ├── box-invalid.png
│   │       │   ├── button-hover.png
│   │       │   ├── card.png
│   │       │   ├── check-accent.png
│   │       │   ├── check-basic.png
│   │       │   ├── check-hover.png
│   │       │   ├── check-tri-accent.png
│   │       │   ├── check-tri-basic.png
│   │       │   ├── check-tri-hover.png
│   │       │   ├── circle-accent.png
│   │       │   ├── circle-basic.png
│   │       │   ├── circle-hover.png
│   │       │   ├── combo-button-basic.png
│   │       │   ├── combo-button-focus.png
│   │       │   ├── combo-button-hover.png
│   │       │   ├── down-accent.png
│   │       │   ├── down.png
│   │       │   ├── empty.png
│   │       │   ├── hor-accent.png
│   │       │   ├── hor-basic.png
│   │       │   ├── hor-hover.png
│   │       │   ├── notebook.png
│   │       │   ├── off-basic.png
│   │       │   ├── on-accent.png
│   │       │   ├── on-basic.png
│   │       │   ├── outline-basic.png
│   │       │   ├── outline-hover.png
│   │       │   ├── radio-accent.png
│   │       │   ├── radio-basic.png
│   │       │   ├── radio-hover.png
│   │       │   ├── radio-tri-accent.png
│   │       │   ├── radio-tri-basic.png
│   │       │   ├── radio-tri-hover.png
│   │       │   ├── rect-accent-hover.png
│   │       │   ├── rect-accent.png
│   │       │   ├── rect-basic.png
│   │       │   ├── rect-hover.png
│   │       │   ├── right.png
│   │       │   ├── scale-hor.png
│   │       │   ├── scale-vert.png
│   │       │   ├── separator.png
│   │       │   ├── size.png
│   │       │   ├── tab-basic.png
│   │       │   ├── tab-disabled.png
│   │       │   ├── tab-hover.png
│   │       │   ├── tick-hor-accent.png
│   │       │   ├── tick-hor-basic.png
│   │       │   ├── tick-hor-hover.png
│   │       │   ├── tick-vert-accent.png
│   │       │   ├── tick-vert-basic.png
│   │       │   ├── tick-vert-hover.png
│   │       │   ├── tree-basic.png
│   │       │   ├── tree-pressed.png
│   │       │   ├── up-accent.png
│   │       │   ├── up.png
│   │       │   ├── vert-accent.png
│   │       │   ├── vert-basic.png
│   │       │   └── vert-hover.png
│   │       ├── dark.tcl
│   │       ├── light
│   │       │   ├── box-accent.png
│   │       │   ├── box-basic.png
│   │       │   ├── box-hover.png
│   │       │   ├── box-invalid.png
│   │       │   ├── button-hover.png
│   │       │   ├── card.png
│   │       │   ├── check-accent.png
│   │       │   ├── check-basic.png
│   │       │   ├── check-hover.png
│   │       │   ├── check-tri-accent.png
│   │       │   ├── check-tri-basic.png
│   │       │   ├── check-tri-hover.png
│   │       │   ├── circle-accent.png
│   │       │   ├── circle-basic.png
│   │       │   ├── circle-hover.png
│   │       │   ├── combo-button-basic.png
│   │       │   ├── combo-button-focus.png
│   │       │   ├── combo-button-hover.png
│   │       │   ├── down-accent.png
│   │       │   ├── down.png
│   │       │   ├── empty.png
│   │       │   ├── hor-accent.png
│   │       │   ├── hor-basic.png
│   │       │   ├── hor-hover.png
│   │       │   ├── notebook.png
│   │       │   ├── off-basic.png
│   │       │   ├── off-hover.png
│   │       │   ├── on-accent.png
│   │       │   ├── on-basic.png
│   │       │   ├── on-hover.png
│   │       │   ├── outline-basic.png
│   │       │   ├── outline-hover.png
│   │       │   ├── radio-accent.png
│   │       │   ├── radio-basic.png
│   │       │   ├── radio-hover.png
│   │       │   ├── radio-tri-accent.png
│   │       │   ├── radio-tri-basic.png
│   │       │   ├── radio-tri-hover.png
│   │       │   ├── rect-accent-hover.png
│   │       │   ├── rect-accent.png
│   │       │   ├── rect-basic.png
│   │       │   ├── rect-hover.png
│   │       │   ├── right.png
│   │       │   ├── scale-hor.png
│   │       │   ├── scale-vert.png
│   │       │   ├── separator.png
│   │       │   ├── size.png
│   │       │   ├── tab-basic.png
│   │       │   ├── tab-disabled.png
│   │       │   ├── tab-hover.png
│   │       │   ├── tick-hor-accent.png
│   │       │   ├── tick-hor-basic.png
│   │       │   ├── tick-hor-hover.png
│   │       │   ├── tick-vert-accent.png
│   │       │   ├── tick-vert-basic.png
│   │       │   ├── tick-vert-hover.png
│   │       │   ├── tree-basic.png
│   │       │   ├── tree-pressed.png
│   │       │   ├── up-accent.png
│   │       │   ├── up.png
│   │       │   ├── vert-accent.png
│   │       │   ├── vert-basic.png
│   │       │   └── vert-hover.png
│   │       └── light.tcl
│   ├── binary_lib.py
│   └── __pycache__
│       └── binary_lib.cpython-311.pyc
├── LICENSE
├── programs
│   ├── asm
│   │   ├── add.masm
│   │   ├── calltest.masm
│   │   ├── default.masm
│   │   ├── fibonacci.masm
│   │   ├── ips.masm
│   │   ├── pixel.masm
│   │   └── stacktest.masm
│   └── bin
│       ├── add.bin
│       ├── ct.bin
│       ├── default.bin
│       ├── fibonacci.bin
│       ├── ips.bin
│       ├── pixel.bin
│       ├── st2.bin
│       ├── st3.bin
│       └── stacktest.bin
├── project_structure.txt
├── README.md
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maliknie/emulator-in-python
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Emulator

1. Assemble your program:
   ```bash
   python assembler/assemblerv2.py
   ```

2. Run the emulator with the binary file:
   ```bash
   python emulator/main.py
   ```

### Writing Your Own Programs

1. Write your program in assembly using the custom ISA. (You can find supported instruction in docs/isa.md)
2. Save the program in the `programs/asm/` directory.
3. Assemble and execute it using the steps above.

## Example Program: Fibonacci

```assembly
load #1, r0      ; n-1 (first Fibonacci number)
load #1, r1      ; n-2 (second Fibonacci number)
load #5, r3      ; Total numbers to calculate
load #1, r4      ; Base counter value
dec r3           ; Adjust counter
jmp >fib_loop

end:
move r7, r0      ; Store final result in r7
halt             ; End program

fib_loop:
move r6, r0      ; Backup n-1
add r0, r1       ; Calculate n = n-1 + n-2
move r1, r6      ; Update n-2
dec r3           ; Decrement counter
cmp r3, r4       ; Check if complete
jne >fib_loop    ; Repeat if not
jmp >end
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements or new features.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
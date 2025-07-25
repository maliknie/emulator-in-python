# Custom Emulator Project

This repository contains a custom-built emulator that simulates a simplified CPU architecture. The project includes a custom instruction set architecture (ISA), an assembler, and example programs to demonstrate functionality.

# Blog
If you're curious to learn more about this project you can read more about it on my [blog](https://malik.lilo.page/posts/grH24N8Lll/).

## Features

- [**Custom ISA:**](docs/isa.md) Supports arithmetic, control flow, memory manipulation, and bitwise operations.
- **Assembler:** Converts assembly programs into machine code executable by the emulator.
- **Pixel-based Display:** Uses `pygame==2.6.1` to create a pixel-based display for graphical output.
- **Example Programs:** Includes example programs like Fibonacci sequence generation.

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

1. Write your program in assembly using the custom ISA. (You can find supported instruction in [docs/isa.md](docs/isa.md))
2. Save the program in the `programs/asm/` directory.
3. Assemble and execute it using the steps above.

## Example Program: Fibonacci

```assembly
load r0, #1      ; n-1 (first Fibonacci number)
load r1, #1      ; n-2 (second Fibonacci number)
load r3, #5      ; Total numbers to calculate
load r4, #1      ; Base counter value
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

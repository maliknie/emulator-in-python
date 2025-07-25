# CUSTOM ISA

This document outlines the entire instruction set architecture (ISA) for the emulator project. It includes descriptions, formats, and examples for each supported instruction.

---

## Instruction Format

### Binary Format
```
[Opcode (8 bits)] [Operand 1 (4 bits)] [Operand 2 (4 bits)] [Operand 3 (16 bits)]
```

### Assembly Format
```
<OPCODE> <OPERAND 1>, <OPERAND 2>, <OPERAND 3>
```
- Unused operands are padded with zeros in binary.
- Registers are named as `r0, r1, ..., r7`.
- Immediate values are unsigned integers.

---

## Registers

### General Purpose Registers

Registers `r0-r7` are 16-bit general purpose registers that can be used when writing code for the emulator.

### Special Registers

- `pc`: program counter (16-bit)
- `ir`: instruction register (32-bit)
- `sp`: stack pointer (16-bit)
- `bp`: base pointer (16-bit)
- `acc`: accumulator (32-bit)
- `flags`: register containing 16 flags (16-bit)
- `mar`: memory adress register (16-bit)
- `mdr`: memory data register (16-bit)

Take note that:
1. `mar` and `mdr`aren't correctly implemented yet
2. technically all registers - even special registers - can be used when writing code although this may result in crashes if you don't know what you're doing 

## Flags

The CPU maintains a 16-bit flags register to store the outcomes of various operations. Each bit in the register represents a specific condition. The flags are indexed from 0 to 15, with the following notable flags:

### Zero Flag (Index 15)
- **Description:** Set to `1` if the result of the previous arithmetic or logical operation is zero. Otherwise, it is set to `0`.
- **Affected Instructions:** All arithmetic and logical operations (e.g., `ADD`, `SUB`, `AND`, `OR`, etc.).
- **Example:** 
  - `SUB r1, r2` (if `r1 - r2 = 0`, the zero flag is set to `1`).

### Carry Flag (Index 14)
- **Description:** Set to `1` if the result of an addition operation exceeds the register size and wraps around. Otherwise, it is set to `0`.
- **Affected Instructions:** `ADD`
- **Example:**
  - `ADD r1, r2` (if the sum of `r1` and `r2` is greater than the maximum value the register can hold, the carry flag is set to `1`).

### Borrow Flag (Index 13)
- **Description:** Set to `1` if the result of a subtraction operation is negative and wraps around. Otherwise, it is set to `0`.
- **Affected Instructions:** `SUB`
- **Example:**
  - `SUB r1, r2` (if `r2` is greater than `r1`, causing a wrap-around, the borrow flag is set to `1`).

Other bits in the flags register may be reserved for future use or not implemented. For the purposes of this ISA, only the zero, carry, and borrow flags are actively utilized.

---

## Instruction Set

### Control Flow

#### JMP
- **Opcode:** `00000000`
- **Description:** Jumps to the specified address.
- **Assembly Format:** `JMP <#IMMEDIATE>`
- **Binary Example:** `00000000 0000 0000 0000000000001000` (Jumps to address 8)

#### JEQ
- **Opcode:** `00000001`
- **Description:** Jumps to the address if the zero flag is set.
- **Assembly Format:** `JEQ <#IMMEDIATE>`
- **Binary Example:** `00000001 0000 0000 0000000000001000` (Jumps to address 8 if zero flag is 1)

#### JNE
- **Opcode:** `00000010`
- **Description:** Jumps to the address if the zero flag is not set.
- **Assembly Format:** `JNE <#IMMEDIATE>`
- **Binary Example:** `00000010 0000 0000 0000000000001000` (Jumps to address 8 if zero flag is 0)

#### JMP (Register)
- **Opcode:** `00001000`
- **Description:** Jumps to the address stored in the specified register.
- **Assembly Format:** `JMP <REGISTER>`
- **Binary Example:** `00001000 0001 0000 0000000000000000` (Jumps to address in `r1`)

#### JEQ (Register)
- **Opcode:** `00001001`
- **Description:** Jumps to the address in the register if the zero flag is set.
- **Assembly Format:** `JEQ <REGISTER>`
- **Binary Example:** `00001001 0001 0000 0000000000000000` (Jumps to address in `r1` if zero flag is 1)

#### JNE (Register)
- **Opcode:** `00001010`
- **Description:** Jumps to the address in the register if the zero flag is not set.
- **Assembly Format:** `JNE <REGISTER>`
- **Binary Example:** `00001010 0001 0000 0000000000000000` (Jumps to address in `r1` if zero flag is 0)

#### CALL 
- **Opcode:** `0001111`
- **Description:** Jumps to the specified address and pushes the program counter onto the stack.
- **Assembly Format:** `CALL <#IMMEDIATE>`
- **Binary Example:** `00011110 0000 0000 0000000000001000` (Jumps to address 8 and pushes the program counter onto the stack)

#### RET 
- **Opcode:** `00011111`
- **Description:** Pops the top element of the stack into the program counter.
- **Assembly Format:** `RET`
- **Binary Example:** `00011111 0000 0000 0000000000000000` (Pops the top element of the stack into the program counter)

---

### Memory Operations

#### LOAD
- **Opcode:** `00000101`
- **Description:** Loads an immediate value into a register.
- **Assembly Format:** `LOAD <REGISTER>, <#IMMEDIATE>`
- **Binary Example:** `00000101 0001 0000 0000000000001010` (Loads 10 into `r1`)

#### LOAD (Memory)
- **Opcode:** `00000110`
- **Description:** Loads the value from a memory address into a register. Depending on the register size (16 or 32 bit) 2 or 4 conscutive memory cells are loaded into the register.
- **Assembly Format:** `LOAD <REGISTER>, [MEMORY]`
- **Binary Example:** `00000110 0001 0000 0000000000010000` (Loads value from address 16 and 17 into `r1`)

#### STORE
- **Opcode:** `00000111`
- **Description:** Stores the value of a register into a specified memory address.
- **Assembly Format:** `STORE <REGISTER>, <#IMMEDIATE>`
- **Binary Example:** `00000111 0001 0000 0000000000010000` (Stores value in `r1` into address 16)

#### STORE (Register)
- **Opcode:** `00000111`
- **Description:** Stores the value of a source register to the memory address stored in the destination register.
- **Assembly Format:** `STORE [DST], <SRC>`
- **Binary Example:** `00000111 0001 0010 0000000000000000` (Stores value in `r2` to the adress stored in `r1`)

#### MOVE
- **Opcode:** `00001100`
- **Description:** Moves the value from one register to another.
- **Assembly Format:** `MOVE <DEST>, <SRC>`
- **Binary Example:** `00001100 0001 0010 0000000000000000` (Moves value from `r2` to `r1`)

---

### Stack Operations

#### PUSH
- **Opcode:** `00011100`
- **Description:** Pushes a register onto the stack.
- **Assembly Format:** `PUSH <REGISTER>`
- **Binary Example:** `00011100 0001 0000 0000000000000000` (Pushes the value in `r1`onto the stack)

#### PUSH
- **Opcode:** `00011101`
- **Description:** Pops a value from the stack and stores it in a register.
- **Assembly Format:** `POP <REGISTER>`
- **Binary Example:** `00011101 0001 0000 0000000000000000` (Pops the top value from the stack and stores it in `r1`)

---

### Arithmetic Operations

#### ADD
- **Opcode:** `00001101`
- **Description:** Adds the values of two registers and stores the result in the first register.
- **Assembly Format:** `ADD <DEST>, <SRC>`
- **Binary Example:** `00001101 0001 0010 0000000000000000` (Adds `r2` to `r1` and stores in `r1`)

#### SUB
- **Opcode:** `00001110`
- **Description:** Subtracts the value of the second register from the first and stores the result in the first register.
- **Assembly Format:** `SUB <DEST>, <SRC>`
- **Binary Example:** `00001110 0001 0010 0000000000000000` (Subtracts `r2` from `r1` and stores in `r1`)

#### MULT
- **Opcode:** `00001111`
- **Description:** Multiplies two registers and stores the high and low bits in two registers.
- **Assembly Format:** `MULT <REG1>, <REG2>`
- **Binary Example:** `00001111 0001 0010 0000000000000000` (Multiplies `r1` and `r2`, stores high in `r1`, low in `r2`)

#### DIV
- **Opcode:** `00010000`
- **Description:** Divides the first register by the second and stores the quotient and remainder.
- **Assembly Format:** `DIV <REG1>, <REG2>`
- **Binary Example:** `00010000 0001 0010 0000000000000000` (Divides `r1` by `r2`, stores quotient in `r1`, remainder in `r2`)

---

### Increment/Decrement Operations

#### INC (Register)
- **Opcode:** `00010001`
- **Description:** Increments the value in a register by 1.
- **Assembly Format:** `INC <REGISTER>`
- **Binary Example:** `00010001 0001 0000 0000000000000000` (Increments `r1` by 1)

#### DEC (Register)
- **Opcode:** `00010010`
- **Description:** Decrements the value in a register by 1.
- **Assembly Format:** `DEC <REGISTER>`
- **Binary Example:** `00010010 0001 0000 0000000000000000` (Decrements `r1` by 1)

#### INC (Memory)
- **Opcode:** `00000011`
- **Description:** Increments the value at a specified memory address by 1.
- **Assembly Format:** `INC [MEMORY]`
- **Binary Example:** `00000011 0000 0000 0000000000010000` (Increments value at address 16 by 1)

#### DEC (Memory)
- **Opcode:** `00000100`
- **Description:** Decrements the value at a specified memory address by 1.
- **Assembly Format:** `DEC [MEMORY]`
- **Binary Example:** `00000100 0000 0000 0000000000010000` (Decrements value at address 16 by 1)

---

### Bitwise Operations

#### AND
- **Opcode:** `00010011`
- **Description:** Performs a bitwise AND on two registers.
- **Assembly Format:** `AND <DEST>, <SRC>`
- **Binary Example:** `00010011 0001 0010 0000000000000000` (ANDs `r1` and `r2`, stores in `r1`)

#### OR
- **Opcode:** `00010100`
- **Description:** Performs a bitwise OR on two registers.
- **Assembly Format:** `OR <DEST>, <SRC>`
- **Binary Example:** `00010100 0001 0010 0000000000000000` (ORs `r1` and `r2`, stores in `r1`)

#### XOR
- **Opcode:** `00010101`
- **Description:** Performs a bitwise XOR on two registers.
- **Assembly Format:** `XOR <DEST>, <SRC>`
- **Binary Example:** `00010101 0001 0010 0000000000000000` (XORs `r1` and `r2`, stores in `r1`)

#### NOT
- **Opcode:** `00010110`
- **Description:** Inverts all bits in a register.
- **Assembly Format:** `NOT <REGISTER>`
- **Binary Example:** `00010110 0001 0000 0000000000000000` (Inverts bits in `r1`)

#### ROL
- **Opcode:** `00010111`
- **Description:** Performs a bitwise left rotation by the specified immediate value.
- **Assembly Format:** `ROL <REGISTER>, <#IMMEDIATE>`
- **Binary Example:** `00010111 0001 0000 0000000000000010` (Rotates `r1` left by 2 bits)

#### ROR
- **Opcode:** `00011000`
- **Description:** Performs a bitwise right rotation by the specified immediate value.
- **Assembly Format:** `ROR <REGISTER>, <#IMMEDIATE>`
- **Binary Example:** `00011000 0001 0000 0000000000000010` (Rotates `r1` right by 2 bits)

#### SHL
- **Opcode:** `00011010`
- **Description:** Shifts the value in a register left by the specified immediate value.
- **Assembly Format:** `SHL <REGISTER>, <#IMMEDIATE>`
- **Binary Example:** `00011010 0001 0000 0000000000000010` (Shifts `r1` left by 2 bits)

#### SHR
- **Opcode:** `00011011`
- **Description:** Shifts the value in a register right by the specified immediate value.
- **Assembly Format:** `SHR <REGISTER>, <#IMMEDIATE>`
- **Binary Example:** `00011011 0001 0000 0000000000000010` (Shifts `r1` right by 2 bits)

---

### Program Control

#### CMP
- **Opcode:** `00011001`
- **Description:** Compares two registers and sets flags accordingly.
- **Assembly Format:** `CMP <REG1>, <REG2>`
- **Binary Example:** `00011001 0001 0010 0000000000000000` (Compares `r1` and `r2`)

#### HALT
- **Opcode:** `11111111`
- **Description:** Stops program execution.
- **Assembly Format:** `HALT`
- **Binary Example:** `11111111 0000 0000 0000000000000000` (Halts the program)

---

This ISA supports a range of operations for control flow, memory handling, arithmetic, and bitwise logic. Each instruction adheres to a fixed 32-bit format for consistency and simplicity.

# OpenByte
A hackable, lightweight, 8-bit computer emulator written in python.

GENERAL INFORMATION
---
An 8-bit computer emulator written in python. It's based off of 8-bit systems of the late 70's and early 90's. It uses a custom CPU with it's own instruction set

GETTING STARTED
--- 
Python 3+ required<br>
dearpygui required

### Running a program
You can run a program by typing the following in a terminal from the root folder: `python3 .\src\main.py (path to an assembled program)`


### Assembling a program
Once finished writing a program, type the following into a terminal from the root folder: `python3 .\src\assembler\assembler.py (path to .asm file) (path to export .bin)`


CPU INFO
---
Architecture: 8-Bit

Endianness - Little Endian

Registers: 
- A : 8-bit
- X : 8-bit
- Y : 8-bit
- Program Counter : 16-bit
- Instruction Register : 8-bit
- Stack Pointer : 8-bit
- Flags : 8-bit

Instruction Version: OPENBYTE v1.0.0


EMULATOR INFORMATION
---
Language: Python

Version: v1.0.0


MEMORY LAYOUT
---
0x0000 - 0x00FF : Stack                 - Important data like the program counter when jumping to a subroutine

0x0100 - 0x8FFF : WRAM                  - General Purpose Memory

0x9000 - 0xFFFD : PROM                  - Program Rom

0xFFFE - 0xFFFF : Program Start Pointer - Reset Vector


FLAGS
---
The FLAG register is an 8-bit register that represents the current state/status of the processor.

Currently, Flags have not been implemented yet.


INSTRUCTION SET
---

Register Specific
- A Register
    - 0x01 : LDA : Load A register with a value from the next memory address
    - 0x02 : STA : Store A register to a value in memory specified by the next two memory values
    - 0x03 : ADA : Adds to the A register by the value in the next memory address
    - 0x04 : INA : Increments the A register by one
- X Register
    - 0x11 : LDX : Loads X register with a value from the next memory address
    - 0x12 : STX : Stores X register to a value in memory specified by the next two memory values
    - 0x13 : ADX : Adds to the X register by the value in the next memory address
    - 0x14 : INX : Increments the X register by one
- Y Registers
    - 0x21 : LDY : Loads Y register with a value from the next memory address
    - 0x22 : STY : Stores Y register to a value in memory specified by the next two memory values
    - 0x23 : ADY : Adds to the Y register by the value in the next memory address

Flow Control
- 0x00 : NOP : No Operation
- Jumping
    - 0x61 : JMP : Moves the Program Counter to a position in memory specified by the next two memory addresses
    - 0x62 : JSR : Pushes current program counter to stack, then jumps to subroutine specified by the next two memory addresses
    - 0x63 : RSR : Pulls program counter from stack, and returns from the subroutine

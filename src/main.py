from modules.components import *
from modules.gui import GUI
import sys

debug=True

print('OpenByte Emulator v1.0.0')

# Get the program from the argument
if len(sys.argv) == 2:
    compiledprog = sys.argv[1]
else: # Else print a usage message
    print("Usage: python main.py <path to compiled program>")
    sys.exit(0)

memory = Memory() # Initilize Memory

# Push program into memory
with open(compiledprog, 'rb') as program:
    content = program.read()
    print(f'Loaded {len(content)} bytes from {compiledprog}')
    for i, byte in enumerate(content):
        memory.write(i, byte, True)

program.close()

# Initilize the cpu
cpu = CPU(memory)
cpu.reset() # and reset it

# Create the GUI
gui = GUI(cpu, memory)

# Loop
while gui.running():
    cpu.decode_instructions()
    gui.update()

gui.shutdown()



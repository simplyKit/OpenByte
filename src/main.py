from modules.components import *
from modules.gui import GUI
import sys
import os

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

# Create the GUI only if display is available
gui = None
if os.environ.get('DISPLAY'):
    try:
        gui = GUI(cpu, memory)
    except Exception as e:
        print(f'Warning: Could not initialize GUI: {e}')
        print('Running in headless mode')
else:
    print('No display available. Running in headless mode')

# Loop
if gui:
    while gui.running():
        cpu.decode_instructions()
        gui.update()
    gui.shutdown()
else:
    # Headless execution - just run for a limited number of cycles
    print('Running 100 instruction cycles...')
    for i in range(100):
        try:
            cpu.decode_instructions()
        except Exception as e:
            print(f'Instruction {i}: {e}')
            break
    print('Headless execution complete')



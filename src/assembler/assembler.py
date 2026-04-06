import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Fix for an import bug cuz im too lazy
from modules.instructions import *

# Grab arguments
if len(sys.argv) == 3:
    assemprogpath = sys.argv[1]
    binaryprogpath = sys.argv[2]
else:
    print("Usage: python3 compiler.py <assembly program> <binary output>")
    sys.exit()

# Generate the Mnemonic map
MNEMONIC_MAP = {f.__name__: (op, OPERAND_SIZE.get(f.__name__, 0)) 
                for op, f in INSTRUCTIONS.items()}

def assemble():
    memory_image = bytearray(0x10000)
    labels = {}
    current_pc = 0

    if not os.path.exists(assemprogpath):
        print (f"Error: File {assemprogpath} not found")
        return

    # Pass 1
    with open(assemprogpath, "rt") as file:
        temp_pc = 0
        for line_number, line in enumerate(file, 1):
            clean = line.split(';')[0].strip().lower()
            if not clean: continue

            # Label identification
            if clean.endswith(":"):
                labels[clean[:-1]] = temp_pc
                continue

            tokens = clean.split()
            mnemonic = tokens[0]

            if mnemonic == ".org": 
                temp_pc = int(tokens[1], 16) if tokens[1].startswith("0x") else int(tokens[1])
            elif mnemonic == "db":
                temp_pc += len(tokens) - 1
            elif mnemonic in MNEMONIC_MAP:
                _, size = MNEMONIC_MAP[mnemonic]
                temp_pc += 1 + (size or 0)

    # Pass 2
    with open(assemprogpath, "rt") as file:
        for line_number, line in enumerate(file, 1):
            clean = line.split(';')[0].strip().lower()
            if not clean or clean.endswith(":"): continue

            tokens = clean.split()
            mnemonic = tokens[0]

            if mnemonic == ".org": # .org
                current_pc = int(tokens[1], 16) if tokens[1].startswith("0x") else int(tokens[1])

            elif mnemonic == "db": # direct byte
                for val_str in tokens[1:]:
                    val = int(val_str, 16) if val_str.startswith("0x") else int(val_str)
                    memory_image[current_pc] = val & 0xFF
                    current_pc += 1

            elif mnemonic in MNEMONIC_MAP:
                opcode, size = MNEMONIC_MAP[mnemonic]
                memory_image[current_pc] = opcode
                current_pc += 1
                
                if size and size > 0:
                    operand_str = tokens[1]
                    # Check if operand is a label
                    val = int(labels[operand_str]) if operand_str in labels else \
                          (int(operand_str, 16) if operand_str.startswith("0x") else int(operand_str))
                    
                    for byte in val.to_bytes(size, 'little'):
                        memory_image[current_pc] = byte
                        current_pc += 1
            else:
                print(f"Unknown command: {mnemonic} at line: {line_number}")
            
            
    
    with open(binaryprogpath, "wb") as file:
        file.write(memory_image)
    print(f"Binary wrote to {binaryprogpath}")

if __name__ == "__main__":
    assemble()


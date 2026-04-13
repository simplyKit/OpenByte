from __future__ import annotations

from . import instructions

class Memory:
    def __init__(self, size:int=0x10000):
        self.memory:list[int] = [0x00]*size
        self.size = size

    def write(self, address:int, value:int, force:bool=False):
        '''Writes to a place in memory\n
        Use force if trying to write to an unwritable piece of memory (ROM)'''
        if address > 0x9000 and not force:
            print(f'Unable to write to: {address}. Reason: Read Only.')
        else:
            self.memory[address%self.size] = value % 0x100
    
    def read(self, address:int):
        '''Reads a place in memory'''
        return self.memory[address%self.size] % 0x100

class CPU:
    def __init__(self, memory:Memory):
        self.memory = memory

        # Register Creation
        self.a:int # Accumulator
        self.x:int # X Register
        self.y:int # Y Register

        self.pc:int # Program Counter
        self.ir:int # Instruction Register
        self.sp:int # Stack Pointer

        self.flags:int # Flag Register
    
    def reset(self):
        '''Resets the CPU's variables'''
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00

        self.pc = (self.memory.read(0xFFFF) << 8) | self.memory.read(0xFFFE)
        self.ir = 0x00
        self.sp = 0xFF

        self.flags = 0b00000000

    def decode_instructions(self):
        '''Decodes instructions inside of Memory'''
        self.ir = self.memory.read(self.pc)

        if self.ir in instructions.INSTRUCTIONS:
            self.pc = (self.pc + 1) % 0x10000
            instructions.INSTRUCTIONS[self.ir](self)
        else:
            raise Exception(f"Unknown instruction: {self.ir}")
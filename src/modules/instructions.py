from collections.abc import Callable
from typing import Literal
from . import components


class HelperFuncs:
    '''Class that contains a bunch of functions that make most operations easier!'''
    @staticmethod
    def incrementRegister(cpu:components.CPU, register:Literal["A", "X", "Y", "PC", "SP"], amount:int):
        '''Increments a register'''
        if register == "A":
            cpu.a = (cpu.a + amount) % 0x100
        elif register == "X":
            cpu.x = (cpu.x + amount) % 0x100
        elif register == "Y":
            cpu.y = (cpu.y + amount) % 0x100
        elif register == "PC":
            cpu.pc = (cpu.pc + amount) % 0x10000
        elif register == "SP":
            cpu.sp = (cpu.sp + amount) % 0x100
        else:
            raise ValueError("Selected Register is Invalid")
    
    @staticmethod
    def fetchByte(cpu:components.CPU):
        val = cpu.memory.read(cpu.pc)
        HelperFuncs.incrementRegister(cpu, "PC", 1)
        return val
    
    @staticmethod
    def fetchAddr(cpu:components.CPU):
        low = cpu.memory.read(cpu.pc)
        high = cpu.memory.read((cpu.pc + 1) % 0x10000)
        HelperFuncs.incrementRegister(cpu, "PC", 2)
        return (high << 8) | low
    
# -- No Operation
def nop(cpu:components.CPU):
    '''No Operation'''
    pass

# -- A register modification
def lda(cpu:components.CPU):
    '''Load the Accumulator with the next value in memory'''
    cpu.a = HelperFuncs.fetchByte(cpu)

def sta(cpu:components.CPU):
    '''Stores the accumulator at a memory address specified by the next two memory addresses'''
    cpu.memory.write(HelperFuncs.fetchAddr(cpu), cpu.a)

def ada(cpu:components.CPU):
    '''Adds to the A register'''
    HelperFuncs.incrementRegister(cpu, "A", HelperFuncs.fetchByte(cpu))

# -- X register modification
def ldx(cpu:components.CPU):
    '''Load the X register with the next value in memory'''
    cpu.x = HelperFuncs.fetchByte(cpu)

def stx(cpu:components.CPU):
    '''Stores the X register at a memory address specified by the next two memory addresses'''
    cpu.memory.write(HelperFuncs.fetchAddr(cpu), cpu.x)

def adx(cpu:components.CPU):
    '''Adds to the X register'''
    HelperFuncs.incrementRegister(cpu, "X", HelperFuncs.fetchByte(cpu))

# -- Y register modification
def ldy(cpu:components.CPU):
    '''Load the Y register with the next value in memory'''
    cpu.y = HelperFuncs.fetchByte(cpu)

def sty(cpu:components.CPU):
    '''Stores the Y register at a memory address specified by the next two memory addresses'''
    cpu.memory.write(HelperFuncs.fetchAddr(cpu), cpu.y)

def ady(cpu:components.CPU):
    '''Adds to the Y register'''
    HelperFuncs.incrementRegister(cpu, "Y", HelperFuncs.fetchByte(cpu))

# -- Address jumping
def jmp(cpu:components.CPU):
    '''Jump to the address defined in the next two bytes'''
    cpu.pc = HelperFuncs.fetchAddr(cpu)

def jsr(cpu:components.CPU):
    '''Jump to a subroutine'''
    target = HelperFuncs.fetchAddr(cpu)

    cpu.memory.write(cpu.sp, (cpu.pc >> 8) & 0xFF)
    HelperFuncs.incrementRegister(cpu, "SP", -1)
    
    cpu.memory.write(cpu.sp, cpu.pc & 0xFF)
    HelperFuncs.incrementRegister(cpu, "SP", -1)

    cpu.pc = target

def rsr(cpu:components.CPU):
    '''Return from subroutine'''
    HelperFuncs.incrementRegister(cpu, "SP", 1)
    low = cpu.memory.read(cpu.sp)
    
    HelperFuncs.incrementRegister(cpu, "SP", 1)
    high = cpu.memory.read(cpu.sp)
    
    cpu.pc = (high << 8) | low

INSTRUCTIONS:dict[int,Callable[[components.CPU], None]] = {
                0x00:nop,
                0x01:lda,
                0x02:sta,
                0x03:ada,
                0x11:ldx,
                0x12:stx,
                0x13:adx,
                0x21:ldy,
                0x22:sty,
                0x23:ady,
                0x61:jmp, 
                0x62:jsr,
                0x63:rsr,
                }

# =========================================== Metadata - Used with the Compiler ===========================================
OPERAND_SIZE:dict[str,int] = {
    "nop": 0, "lda": 1, "sta": 2, "ada": 1,
    "ldx": 1, "stx": 2, "adx": 1, "ldy": 1,
    "sty": 2, "ady": 1, "jmp": 2, "jsr": 2, "rsr": 0
}
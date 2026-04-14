'''
GUI
sorry bout the little comments.
'''

import dearpygui.dearpygui as dpg
from . import components

class GUI:
    '''Basic GUI for editing RAM and ROM values, looking at CPU register values, and overall clock execution'''
    def __init__(self, cpu:components.CPU, memory:components.Memory):
        self.cpu = cpu
        self.memory = memory

        # Memory Window Settings
        self.rows = 16
        self.columns = 16

        self.memory_offset = 0

        dpg.create_context() # Create the GUI context
        self._init_layout() # Create the GUI layout
        dpg.create_viewport(title="Debugger", width=1000, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def _init_layout(self):
        # Create CPU status window
        with dpg.window(label="CPU Status", width=250, height=250, pos=(0, 0), no_close=True):
            dpg.add_text("PC: 0x000", tag="pc")
            dpg.add_text("Stack: 0x00", tag="stack")
            dpg.add_text("A: 0x00", tag="a")
            dpg.add_text("X: 0x00", tag="x")
            dpg.add_text("Y: 0x00", tag="y")
            dpg.add_text("Flags: 0b00000000", tag="flags")
        
            with dpg.window(label="Memory", width=750, height=500, pos=(250, 0), no_close=True):
                dpg.add_text("Jump to: ")

                dpg.add_input_text(tag="jump_addr", width=100, on_enter=True, callback=self._jump_to_address)
                dpg.add_slider_int(label="Scroll", min_value=0, max_value=0xFF00, 
                                tag="mem_scroll", callback=self._scroll, width=300)
                dpg.add_separator()

                with dpg.table(header_row=True, borders_innerH=True, borders_innerV=True, 
                            borders_outerH=True, borders_outerV=True, resizable=True):
                    # Address column
                    dpg.add_table_column(label="Addr")
                    for i in range(self.columns): dpg.add_table_column(label=f"{i:01x}")

                    for r in range(self.rows):
                        with dpg.table_row():
                            # Address row
                            dpg.add_text("0000", tag=f"row_addr_{r}", color=(100, 200, 255))
                            for c in range(self.columns):
                                idx = r * self.columns + c
                                dpg.add_text("00", tag=f"mem_{idx}")
    
    def _scroll(self, sender, app_data):
        new_offset = (app_data // 16) * 16
        max_safe_offset = len(self.memory.memory) - 256
        self.memory_offset = max(0, min(new_offset, max_safe_offset))
    
    def _jump_to_address(self, sender, app_data):
        try:
            new_addr = int(app_data, 16)
            new_offset = (new_addr // 16) * 16
            self.memory_offset = max(0, min(new_offset, 0xFF00))
            dpg.set_value("mem_scroll", self.memory_offset)
        except ValueError:
            pass
    
    def update(self):
        # Update CPU and Memory objects
        dpg.set_value("pc", f"PC: {hex(self.cpu.pc)}")
        dpg.set_value("stack", f"Stack: {hex(self.cpu.sp)}")
        dpg.set_value("a", f"A: {hex(self.cpu.a)}")
        dpg.set_value("x", f"X: {hex(self.cpu.x)}")
        dpg.set_value("y", f"Y: {hex(self.cpu.y)}")
        dpg.set_value("flags", f"Flags: {bin(self.cpu.flags)}")

        # Memory update logic
        for r in range(16):
            row_addr = (self.memory_offset + (r * 16)) & 0xFFFF
            dpg.set_value(f"row_addr_{r}", f"{row_addr:04X}:")
            
            for c in range(16):
                byte_addr = row_addr + c
                val = self.memory.memory[byte_addr]
                dpg.set_value(f"mem_{r*16+c}", f"{val:02X}")

        # Render
        dpg.render_dearpygui_frame()

    def running(self):
        return dpg.is_dearpygui_running()

    def shutdown(self):
        dpg.destroy_context()
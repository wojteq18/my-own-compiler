from register_manager import reg_manager

free_memory_address = 8
symbols_table = {}
procedures_table = {}

def get_addr(variable_name):
    global free_memory_address
    global symbols_table
    if variable_name not in symbols_table:
        symbols_table[variable_name] = {'addr': free_memory_address}
        free_memory_address += 1
    return symbols_table[variable_name]['addr']

def generate_number(number_value, buffer):
    buffer.add_instr("RST a")
    if number_value == 0:
        return
    binary_repr = bin(number_value)[2:]
    buffer.add_instr("INC a")
    for bit in binary_repr[1:]:
        buffer.add_instr("SHL a")
        if bit == '1':
            buffer.add_instr("INC a")
      
def gen_multiply(buffer, reg_m1):
    reg_m2 = reg_manager.get_register()   
    reg_res = reg_manager.get_register()  
    reg_temp = reg_manager.get_register() 
    l_start = buffer.get_new_label()
    l_add = buffer.get_new_label()
    l_end = buffer.get_new_label()
    buffer.add_instr(f"SWP {reg_m2}")     
    buffer.add_instr(f"RST {reg_res}")   
    buffer.set_label(l_start)
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_m2}")
    buffer.add_instr(f"JZERO LABEL_{l_end}") 
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_m2}")
    buffer.add_instr("SHR a")
    buffer.add_instr("SHL a")
    buffer.add_instr(f"RST {reg_temp}") 
    buffer.add_instr(f"SWP {reg_temp}") 
    buffer.add_instr(f"ADD {reg_m2}")
    buffer.add_instr(f"SUB {reg_temp}") 
    buffer.add_instr(f"JZERO LABEL_{l_add}") 
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_res}")
    buffer.add_instr(f"ADD {reg_m1}")
    buffer.add_instr(f"SWP {reg_res}")
    buffer.set_label(l_add)
    buffer.add_instr(f"SHL {reg_m1}")     
    buffer.add_instr(f"SHR {reg_m2}")    
    buffer.add_instr(f"JUMP LABEL_{l_start}") 
    buffer.set_label(l_end)
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_res}")    
    reg_manager.release_register()
    reg_manager.release_register()
    reg_manager.release_register()

def get_divide(buffer, reg_m1, operator):
    reg_m2 = reg_manager.get_register()      
    reg_q = reg_manager.get_register()       
    reg_b_shift = reg_manager.get_register() 
    reg_mult = reg_manager.get_register()    
    reg_temp = reg_manager.get_register()    
    l_div_zero = buffer.get_new_label()
    l_align_start = buffer.get_new_label()
    l_align_end = buffer.get_new_label()
    l_loop_start = buffer.get_new_label()
    l_skip_sub = buffer.get_new_label()
    l_end = buffer.get_new_label()
    buffer.add_instr(f"SWP {reg_m2}") 
    buffer.add_instr(f"RST {reg_q}")  
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_m2}")
    buffer.add_instr(f"JZERO LABEL_{l_div_zero}")
    buffer.add_instr(f"RST a")
    buffer.add_instr(f"RST {reg_b_shift}")
    buffer.add_instr(f"ADD {reg_m2}")
    buffer.add_instr(f"SWP {reg_b_shift}")
    buffer.add_instr(f"RST a") 
    buffer.add_instr(f"RST {reg_mult}")
    buffer.add_instr("INC a")  
    buffer.add_instr(f"SWP {reg_mult}")
    buffer.set_label(l_align_start)
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_b_shift}")
    buffer.add_instr("SHL a")
    buffer.add_instr(f"RST {reg_temp}")
    buffer.add_instr(f"SWP {reg_temp}") 
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_temp}")
    buffer.add_instr(f"SUB {reg_m1}") 
    buffer.add_instr(f"JPOS LABEL_{l_align_end}") 
    buffer.add_instr(f"SHL {reg_b_shift}")
    buffer.add_instr(f"SHL {reg_mult}")
    buffer.add_instr(f"JUMP LABEL_{l_align_start}")
    buffer.set_label(l_align_end)
    buffer.set_label(l_loop_start)
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_b_shift}")
    buffer.add_instr(f"SUB {reg_m1}")
    buffer.add_instr(f"JPOS LABEL_{l_skip_sub}") 
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_m1}")
    buffer.add_instr(f"SUB {reg_b_shift}")
    buffer.add_instr(f"SWP {reg_m1}")
    buffer.add_instr("RST a") 
    buffer.add_instr(f"ADD {reg_q}")
    buffer.add_instr(f"ADD {reg_mult}")
    buffer.add_instr(f"SWP {reg_q}")
    buffer.set_label(l_skip_sub)
    buffer.add_instr(f"SHR {reg_b_shift}")
    buffer.add_instr(f"SHR {reg_mult}")
    buffer.add_instr("RST a")
    buffer.add_instr(f"ADD {reg_mult}")
    buffer.add_instr(f"JPOS LABEL_{l_loop_start}")
    buffer.add_instr(f"JUMP LABEL_{l_end}")
    buffer.set_label(l_div_zero)
    buffer.add_instr(f"RST {reg_q}")
    buffer.add_instr(f"RST {reg_m1}")
    buffer.set_label(l_end)
    buffer.add_instr("RST a")
    if operator == "DIVIDE":
        buffer.add_instr(f"ADD {reg_q}")
    else:
        buffer.add_instr(f"ADD {reg_m1}")
    for _ in range(5):
        reg_manager.release_register()

def get_array_addr(name, start, end):
    global free_memory_address
    global symbols_table
    if name in symbols_table:
        import sys
        sys.exit(f"Error: Variable/Array '{name}' already declared")
    start = int(start)
    end = int(end)
    if start > end:
        import sys
        sys.exit(f"Error: Invalid array range [{start}:{end}]") 
    size = end - start + 1
    base_addr = free_memory_address
    symbols_table[name] = {'type': 'array', 'addr': base_addr, 'start': start, 'end': end}
    free_memory_address += size
    return base_addr

def get_proc_param_addr(proc_name, param_index):
    global free_memory_address
    global symbols_table
    key = f"__proc_{proc_name}_param_{param_index}"
    if key not in symbols_table:
        symbols_table[key] = {'addr': free_memory_address, 'type': 'pointer'}
        free_memory_address += 1
    return symbols_table[key]['addr']

class CodeBuffer: 
    def __init__(self):
        self.instructions = []
        self.labels = {}
        self.label_counter = 0
    def get_new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"
    def add_instr(self, instr):
        self.instructions.append(instr)
    def set_label(self, label_name):
        self.labels[label_name] = len(self.instructions)
    def finalize(self):
        final_output = []
        sorted_labels = sorted(self.labels.items(), key=lambda x: len(x[0]), reverse=True)
        for instr in self.instructions:
            processed_instr = instr
            for label, line_num in sorted_labels:
                placeholder = f"LABEL_{label}"
                if placeholder in processed_instr:
                    processed_instr = processed_instr.replace(placeholder, str(line_num))    
            final_output.append(processed_instr)
        return "\n".join(final_output)
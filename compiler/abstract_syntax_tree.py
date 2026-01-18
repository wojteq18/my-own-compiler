import sys
from register_manager import reg_manager
from compiler_utils import generate_number, get_addr, gen_multiply, get_divide, symbols_table, procedures_table

class Node:
    def generate(self, buffer):
        raise NotImplementedError("Subclasses must implement generate method")
    
class NumberNode(Node):
    def __init__(self, value):
        self.value = value
    def generate(self, buffer):
        generate_number(int(self.value), buffer)
    
class VariableNode(Node):
    def __init__(self, name):
        self.name = name
    def generate(self, buffer):
        info = symbols_table[self.name]
        addr = info['addr']
        if info.get('is_param'):
            reg_ptr = reg_manager.get_register()
            buffer.add_instr(f"LOAD {addr}")
            buffer.add_instr(f"SWP {reg_ptr}")
            buffer.add_instr(f"RLOAD {reg_ptr}")
            reg_manager.release_register()
        else:
            buffer.add_instr(f"LOAD {addr}")
    
class BinaryOperationNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def generate(self, buffer):
        self.left.generate(buffer)
        reg_left = reg_manager.get_register()
        buffer.add_instr(f"SWP {reg_left}")
        self.right.generate(buffer)
        if self.operator == "ADD":
            buffer.add_instr(f"ADD {reg_left}")
        elif self.operator == "MINUS":
            buffer.add_instr(f"SWP {reg_left}")
            buffer.add_instr(f"SUB {reg_left}")
        elif self.operator == "MULTIPLY":
            gen_multiply(buffer, reg_left)
        elif self.operator == "DIVIDE":        
            get_divide(buffer, reg_left, "DIVIDE")
        elif self.operator == "MODULO":
            get_divide(buffer, reg_left, "MODULO")    
        reg_manager.release_register()

class AssignmentNode(Node):
    def __init__(self, target, expression):
        self.target = target 
        self.expression = expression
    def generate(self, buffer):
        self.expression.generate(buffer)
        if isinstance(self.target, VariableNode):
            info = symbols_table[self.target.name]
            if info.get('is_param'):
                reg_val = reg_manager.get_register()
                buffer.add_instr(f"SWP {reg_val}")
                reg_ptr = reg_manager.get_register()
                buffer.add_instr(f"LOAD {info['addr']}")
                buffer.add_instr(f"SWP {reg_ptr}")
                buffer.add_instr("RST a")
                buffer.add_instr(f"ADD {reg_val}")
                buffer.add_instr(f"RSTORE {reg_ptr}")
                reg_manager.release_register()
                reg_manager.release_register()
            else:
                buffer.add_instr(f"STORE {info['addr']}")
        else:
            reg_val = reg_manager.get_register()
            buffer.add_instr(f"SWP {reg_val}")
            reg_addr = reg_manager.get_register()
            self.target.generate_address(buffer, reg_addr)
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_val}")
            buffer.add_instr(f"RSTORE {reg_addr}")
            reg_manager.release_register()
            reg_manager.release_register()

class ReadNode(Node):
    def __init__(self, target):
        self.target = target
    def generate(self, buffer):
        if isinstance(self.target, VariableNode):
            info = symbols_table[self.target.name]
            buffer.add_instr("READ") 
            if info.get('is_param'):
                reg_val = reg_manager.get_register()
                buffer.add_instr(f"SWP {reg_val}")
                reg_ptr = reg_manager.get_register()
                buffer.add_instr(f"LOAD {info['addr']}")
                buffer.add_instr(f"SWP {reg_ptr}")
                buffer.add_instr("RST a")
                buffer.add_instr(f"ADD {reg_val}")
                buffer.add_instr(f"RSTORE {reg_ptr}")
                reg_manager.release_register()
                reg_manager.release_register()
            else:
                buffer.add_instr(f"STORE {info['addr']}") 
        elif isinstance(self.target, ArrayElementNode):
            reg_addr = reg_manager.get_register()
            self.target.generate_address(buffer, reg_addr)
            buffer.add_instr("READ")
            buffer.add_instr(f"RSTORE {reg_addr}")
            reg_manager.release_register()

class WriteNode(Node):
    def __init__(self, value_node):
        self.value_node = value_node
    def generate(self, buffer):
        self.value_node.generate(buffer)
        buffer.add_instr("WRITE")    

class ConditionNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def generate(self, buffer, label_false):
        self.left.generate(buffer)
        reg_left = reg_manager.get_register()
        buffer.add_instr(f"SWP {reg_left}")
        self.right.generate(buffer)
        reg_right = reg_manager.get_register()
        buffer.add_instr(f"SWP {reg_right}")
        
        if self.operator == '>':
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_left}")
            buffer.add_instr(f"SUB {reg_right}")
            buffer.add_instr(f"JZERO LABEL_{label_false}")
        elif self.operator == '<':
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_right}")
            buffer.add_instr(f"SUB {reg_left}")
            buffer.add_instr(f"JZERO LABEL_{label_false}")
        elif self.operator == '=':
            label_ok = buffer.get_new_label()
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_left}")
            buffer.add_instr(f"SUB {reg_right}")
            buffer.add_instr(f"JPOS LABEL_{label_false}")
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_right}")
            buffer.add_instr(f"SUB {reg_left}")
            buffer.add_instr(f"JPOS LABEL_{label_false}")
        elif self.operator == '!=':
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_left}")
            buffer.add_instr(f"SUB {reg_right}")
            buffer.add_instr(f"JPOS LABEL_TEMP_{label_false}")
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_right}")
            buffer.add_instr(f"SUB {reg_left}")
            buffer.add_instr(f"JZERO LABEL_{label_false}")
            buffer.set_label(f"TEMP_{label_false}")
        elif self.operator == '>=':
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_right}")
            buffer.add_instr(f"SUB {reg_left}")
            buffer.add_instr(f"JPOS LABEL_{label_false}")
        elif self.operator == '<=':
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_left}")
            buffer.add_instr(f"SUB {reg_right}")
            buffer.add_instr(f"JPOS LABEL_{label_false}")
            
        reg_manager.release_register()
        reg_manager.release_register()

class IfNode(Node):
    def __init__(self, condition, then_commands, else_commands=None):
        self.condition = condition
        self.then_commands = then_commands
        self.else_commands = else_commands
    def generate(self, buffer):
        label_else = buffer.get_new_label()
        label_end = buffer.get_new_label()
        self.condition.generate(buffer, label_else)
        for cmd in self.then_commands:
            cmd.generate(buffer)
        buffer.add_instr(f"JUMP LABEL_{label_end}")
        buffer.set_label(label_else)
        if self.else_commands:
            for cmd in self.else_commands:
                cmd.generate(buffer)
        buffer.set_label(label_end)

class WhileNode(Node):
    def __init__(self, condition, commands):
        self.condition = condition
        self.commands = commands   
    def generate(self, buffer):
        label_start = buffer.get_new_label()
        label_end = buffer.get_new_label()  
        buffer.set_label(label_start)
        self.condition.generate(buffer, label_end)  
        for cmd in self.commands:
            cmd.generate(buffer) 
        buffer.add_instr(f"JUMP LABEL_{label_start}")
        buffer.set_label(label_end)

class ForNodeTo(Node):
    def __init__(self, var_name, start_value, end_value, commands):
        self.var_name = var_name
        self.start_value = start_value
        self.end_value = end_value
        self.commands = commands
    def generate(self, buffer):
        addr_i = get_addr(self.var_name)
        addr_limit = get_addr(f"limit_{buffer.get_new_label()}")
        self.start_value.generate(buffer)
        buffer.add_instr(f"STORE {addr_i}")
        self.end_value.generate(buffer)
        buffer.add_instr(f"STORE {addr_limit}")
        l_start = buffer.get_new_label()
        l_end = buffer.get_new_label()
        buffer.set_label(l_start)
        buffer.add_instr(f"LOAD {addr_i}")   
        reg_limit = reg_manager.get_register()
        buffer.add_instr(f"SWP {reg_limit}")    
        buffer.add_instr(f"LOAD {addr_limit}") 
        buffer.add_instr(f"SWP {reg_limit}") 
        buffer.add_instr(f"SUB {reg_limit}")    
        buffer.add_instr(f"JPOS LABEL_{l_end}")
        reg_manager.release_register()
        for cmd in self.commands:
            cmd.generate(buffer)
        buffer.add_instr(f"LOAD {addr_i}")
        buffer.add_instr("INC a")
        buffer.add_instr(f"STORE {addr_i}")
        buffer.add_instr(f"JUMP LABEL_{l_start}")
        buffer.set_label(l_end)

class ForNodeDownTo(Node):
    def __init__(self, var_name, start_value, end_value, commands):
        self.var_name = var_name
        self.start_value = start_value
        self.end_value = end_value
        self.commands = commands       
    def generate(self, buffer):
        addr_i = get_addr(self.var_name)
        addr_limit = get_addr(f"limit_{buffer.get_new_label()}")
        self.start_value.generate(buffer)
        buffer.add_instr(f"STORE {addr_i}")
        self.end_value.generate(buffer)
        buffer.add_instr(f"STORE {addr_limit}")
        l_start = buffer.get_new_label()
        l_end = buffer.get_new_label()
        buffer.set_label(l_start)
        buffer.add_instr(f"LOAD {addr_i}")   
        reg_limit = reg_manager.get_register()
        buffer.add_instr(f"SWP {reg_limit}")    
        buffer.add_instr(f"LOAD {addr_limit}")  
        buffer.add_instr(f"SUB {reg_limit}")    
        buffer.add_instr(f"JPOS LABEL_{l_end}")
        reg_manager.release_register()
        for cmd in self.commands:
            cmd.generate(buffer)
        buffer.add_instr(f"LOAD {addr_i}")
        buffer.add_instr(f"JZERO LABEL_{l_end}")
        buffer.add_instr("DEC a")
        buffer.add_instr(f"STORE {addr_i}")
        buffer.add_instr(f"JUMP LABEL_{l_start}")
        buffer.set_label(l_end)

class RepeatNode(Node):
    def __init__(self, commands, condition):
        self.commands = commands
        self.condition = condition
    def generate(self, buffer):
        label_start = buffer.get_new_label()
        buffer.set_label(label_start)
        for cmd in self.commands:
            cmd.generate(buffer)
        self.condition.generate(buffer, label_start)    

class ArrayElementNode(Node):
    def __init__(self, name, index_node):
        self.name = name
        self.index_node = index_node
    def generate_address(self, buffer, target_reg):
        info = symbols_table[self.name]
        if info.get('is_param'):
            self.index_node.generate(buffer)
            reg_idx = reg_manager.get_register()
            buffer.add_instr(f"SWP {reg_idx}")
            buffer.add_instr(f"LOAD {info['addr']}")
            buffer.add_instr(f"ADD {reg_idx}")
            buffer.add_instr(f"SWP {target_reg}")
            reg_manager.release_register()
        else:
            self.index_node.generate(buffer) 
            reg_index_val = reg_manager.get_register()
            buffer.add_instr(f"SWP {reg_index_val}")
            generate_number(info['start'], buffer)
            reg_start = reg_manager.get_register()
            buffer.add_instr(f"SWP {reg_start}") 
            buffer.add_instr("RST a")
            buffer.add_instr(f"ADD {reg_index_val}")
            buffer.add_instr(f"SUB {reg_start}")     
            reg_manager.release_register() 
            buffer.add_instr(f"SWP {reg_index_val}") 
            generate_number(info['addr'], buffer)   
            buffer.add_instr(f"ADD {reg_index_val}")
            buffer.add_instr(f"SWP {target_reg}")
            reg_manager.release_register()
    def generate(self, buffer):
        reg_addr = reg_manager.get_register()
        self.generate_address(buffer, reg_addr)
        buffer.add_instr(f"RLOAD {reg_addr}") 
        reg_manager.release_register()  

class ProcedureNode(Node):
    def __init__(self, name, params, commands): 
        self.name = name
        self.params = params  
        self.commands = commands
    def generate(self, buffer):
        buffer.set_label(f"PROC_{self.name}")
        ret_addr_cell = get_addr(f"__ret_addr_{self.name}")
        buffer.add_instr(f"STORE {ret_addr_cell}") 
    
        for cmd in self.commands:
            cmd.generate(buffer)
        
        buffer.add_instr(f"LOAD {ret_addr_cell}") 
        buffer.add_instr("RTRN")

class CallNode(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def generate(self, buffer):
        proc_info = procedures_table[self.name]
        for i, arg_node in enumerate(self.args):
            param_cell_addr = proc_info['param_addrs'][i]
            arg_info = symbols_table[arg_node.name]
            
            if arg_info.get('is_param'):
                buffer.add_instr(f"LOAD {arg_info['addr']}")
            else:
                if 'T' in proc_info['params'][i][1]:
                    vba = arg_info['addr'] - arg_info['start']
                    generate_number(vba, buffer)
                else:
                    generate_number(arg_info['addr'], buffer)
            
            buffer.add_instr(f"STORE {param_cell_addr}")
        
        buffer.add_instr(f"CALL LABEL_PROC_{self.name}")
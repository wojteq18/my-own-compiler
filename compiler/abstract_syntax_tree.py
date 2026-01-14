import sys
from register_manager import reg_manager
from compiler_utils import generate_number, get_addr, gen_multiply, get_divide

class Node:
    def generate(self):
        raise NotImplementedError("Subclasses must implement generate method")
    
class NumberNode(Node): #dziedziczy po Node
    def __init__(self, value):
        self.value = value

    def generate(self, buffer):
        generate_number(int(self.value), buffer)
    
class VariableNode(Node): #dziedziczy po Node
    def __init__(self, name):
        self.name = name    

    def generate(self, buffer):
        addr = get_addr(self.name)
        buffer.add_instr(f"LOAD {addr}")  
    
class BinaryOperationNode(Node): #dziedziczy po Node
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
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def generate(self, buffer):
        self.expression.generate(buffer)
        addr = get_addr(self.name)
        buffer.add_instr(f"STORE {addr}")

class ReadNode(Node):
    def __init__(self, name):
        self.name = name
    def generate(self, buffer):
        addr = get_addr(self.name)
        buffer.add_instr("READ")
        buffer.add_instr(f"STORE {addr}")

class WriteNode(Node):
    def __init__(self, value_node):
        self.value_node = value_node
    def generate(self, buffer):
        self.value_node.generate(buffer)
        buffer.add_instr("WRITE")            




    

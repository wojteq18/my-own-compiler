import sys
from register_manager import reg_manager
from compiler_utils import generate_number, get_addr

class Node:
    def generate(self):
        raise NotImplementedError("Subclasses must implement generate method")
    
class NumberNode(Node): #dziedziczy po Node
    def __init__(self, value):
        self.value = value

    def generate(self):
        return generate_number(int(self.value))
    
class VariableNode(Node): #dziedziczy po Node
    def __init__(self, name):
        self.name = name    

    def generate(self):
        addr = get_addr(self.name)
        code = f"LOAD {addr}\n"
        return code    
    
class BinaryOperationNode(Node): #dziedziczy po Node
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def generate(self):
        code = self.left.generate() #obliczamy lewą stronę - wynik ląduje w rejestrze 'a'
        reg = reg_manager.get_register()
        code += f"SWP {reg}\n"  # Przechowujemy wynik lewej strony w rejestrze pomocniczym

        code += self.right.generate() #obliczamy prawą stronę - wynik ląduje w rejestrze 'a'

        if self.operator == 'ADD':
            code += f"ADD {reg}\n"  # Dodajemy wartość z rejestru pomocniczego do akumulatora
        elif self.operator == 'MINUS':    
            code += f"SWP {reg}\n"
            code += f"SUB {reg}\n"  # Odejmujemy wartość z rejestru pomocniczego od akumulatora

        reg_manager.release_register()
        return code




    

import sys

class RegisterManager:
    def __init__(self):
        self.registers = ['b', 'c', 'd', 'e', 'f', 'g', 'h'] # Lista dostępnych rejestrów oprócz 'a', a traktujemy jako akumulator
        self.register_pointer = 0

    def get_register(self):
        if self.register_pointer >= len(self.registers):
            sys.exit("Error: Out of registers")
        else:
            reg = self.registers[self.register_pointer]
            self.register_pointer += 1
            return reg

    def release_register(self):
        if self.register_pointer > 0:
            self.register_pointer -= 1  

reg_manager = RegisterManager()              
from register_manager import reg_manager

free_memory_address = 0
symbols_table = {}

def get_addr(variable_name): #Przyporządkowuje unikalny adres w pamięci dla zmiennej
    global free_memory_address
    global symbols_table
    if variable_name not in symbols_table:
        symbols_table[variable_name] = free_memory_address
        free_memory_address += 1
    return symbols_table[variable_name]

def generate_number(number_value):
    code = f"RST a\n"
    if number_value == 0:
        return code
    elif number_value == 1:
        code += f"INC a\n"
        return code
    else:
        binary_value = bin(number_value)[2:]  # Konwertuj na binarny i usuń prefiks '0b'
        code += f"INC a\n"  # Ustaw na jeden
        for bit in binary_value[1:]:
            code += f"SHL a\n"  # Przesuń w lewo (mnożenie przez 2)
            if bit == '1':
                code += f"INC a\n"  # Dodaj jeden, jeśli bit to 1
    return code   
  
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


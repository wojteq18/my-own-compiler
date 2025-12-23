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
    code = "RST a\n"
    if number_value == 0:
        return code
    elif number_value == 1:
        code += "INC a\n"
        return code
    else:
        binary_value = bin(number_value)[2:]  # Konwertuj na binarny i usuń prefiks '0b'
        code += "INC a\n"  # Ustaw na jeden
        for bit in binary_value[1:]:
            code += "SHL a\n"  # Przesuń w lewo (mnożenie przez 2)
            if bit == '1':
                code += "INC a\n"  # Dodaj jeden, jeśli bit to 1
    code += "SWP a\n"
    return code            


from parser import parser

def run():
    while True:
        try:
            s = input('calc> ')
        except EOFError:
            break
        if s.lower() == 'exit':
            break
        result = parser.parse(s)
        if result is not None:
            print(result)    


if __name__ == "__main__":
    run()
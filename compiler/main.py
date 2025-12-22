from parser import parser
import sys

def run():
    if len(sys.argv) != 3:
        print("Usage: python main.py <source_file> <output_file>")
        return
    
    source_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(source_file, 'r') as f:
            source_code = f.read()
            result = parser.parse(source_code)

            if result:
                with open(output_file, 'w') as out_f:
                    out_f.write(result)
                print(f"Compilation successful! Output written to {output_file}")
            else:
                print("Compilation failed due to syntax errors.")
                
    except FileNotFoundError:
        print(f"Source file '{source_file}' not found.")
        return


if __name__ == "__main__":
    run()
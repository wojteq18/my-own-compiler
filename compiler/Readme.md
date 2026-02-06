# Imperative Language Compiler

A Python-based compiler designed to translate imperative source code into machine-readable instructions. This project features a modular architecture, including a custom lexer, parser, and code optimization stages.

## 🚀 Features

* **Modular Pipeline**: Separate stages for Lexical Analysis, Syntax Analysis, and Code Generation.
* **Peephole Optimization**: Basic instruction-level optimizations for better performance.
* **Easy Interface**: Simple CLI wrapper to run the compiler as an executable.
* **Error Reporting**: Clear feedback for syntax errors or missing files.

## 📂 Project Structure

* `kompilator` - The main executable wrapper (entry point).
* `lexer.py` - Tokenizes the source input.
* `parser.py` - Performs syntax analysis (using PLY or similar).
* `code_buffer.py` - Manages intermediate instruction storage.
* `register_manager.py` - Handles low-level register allocation logic.
* `compiler_utils.py` - Shared utilities and helper functions.
* `Makefile` - Automation for setting up permissions and cleanup.

## 🛠 Getting Started

### Prerequisites
* **Python 3.x**
* **Make** (usually pre-installed on Linux/macOS)


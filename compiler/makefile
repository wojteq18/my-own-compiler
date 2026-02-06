# Nazwa pliku wynikowego
APP_NAME = kompilator

.PHONY: all clean

all:
	@# Nadajemy uprawnienia do wykonywania
	chmod +x $(APP_NAME)
	@echo "Kompilator gotowy. Możesz go uruchomić przez: ./$(APP_NAME) <input> <output>"

clean:
	rm -rf __pycache__
	rm -f parsetab.py parser.out
	@echo "Wyczyszczono."
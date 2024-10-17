from init import initialize_system

RAM_SIZE_IN_KIB = 64

RAM_SIZE = RAM_SIZE_IN_KIB * 1024

def main():
    # Erstellt eine Instanz aller Klassen und startet das GUI
    controller = initialize_system(RAM_SIZE)
    controller.gui.start()

if __name__ == "__main__":
    main()
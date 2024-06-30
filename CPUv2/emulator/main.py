from init import initialize_system

def main():
    controller = initialize_system()

    controller.gui.start()

if __name__ == "__main__":
    main()
    
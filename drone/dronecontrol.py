from djitellopy import Tello


# Functie om de drone te besturen
def control_drone(tello):
    while True:
        try:
            command = input("Enter a command (takeoff/land/quit/w/s/a/d/u/j/l/r): ").strip().lower()
            if command == "takeoff":
                tello.takeoff()
            elif command == "land":
                tello.land()
            elif command == "quit":
                tello.land()
                break
            elif command == "flip":
                tello.flip("f")
            elif command == "w":
                tello.move_forward(50)
            elif command == "s":
                tello.move_back(50)
            elif command == "a":
                tello.move_left(50)
            elif command == "d":
                tello.move_right(50)
            elif command == "u":
                tello.move_up(50)
            elif command == "j":
                tello.move_down(50)
            elif command == "l":
                tello.rotate_clockwise(45)
            elif command == "r":
                tello.rotate_counter_clockwise(45)
            else:
                print("Invalid command. Please enter a valid command.")

        except KeyboardInterrupt:
            tello.land()
            break


# Hoofdprogramma
if __name__ == "__main__":
    try:
        # Verbind met de Tello-drone
        tello = Tello()
        tello.connect()

        # Start de controlefunctie
        control_drone(tello)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Sluit de verbinding met de drone
        tello.end()
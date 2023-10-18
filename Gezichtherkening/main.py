import cv2
import socket
import keyboard
from djitellopy import Tello

# Maak een TCP/IP socket
sock_dashboard = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind de socket aan een specifiek adres en poort
server_adres = ('localhost', 12345)
sock_dashboard.bind(server_adres)

# Luister naar inkomende verbindingen
sock_dashboard.listen(1)

# Initialiseer de Tello drone
tello = Tello()
tello.connect()
tello.streamon()

# Laad een vooraf getraind model voor gezichtsdetectie
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# IP- en poortinformatie voor de Tello
tello_adres = ('192.168.10.1', 8889)

# Maak een UDP-socket voor het verzenden van commando's
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind de socket aan een lokale poort om reacties te ontvangen
sock.bind(('', 9000))

# Functie om een commando naar de Tello Drone te sturen
def stuur_commando(commando):
    try:
        sock.sendto(commando.encode('utf-8'), tello_adres)
        reactie, ip = sock.recvfrom(1024)
        return reactie.decode('utf-8')
    except Exception as e:
        return str(e)

# Definieer de dronebesturingscommando's op basis van toetsenbordinvoer
def bestuur_drone(tello, toets):
    if toets == 'w':
        tello.send_rc_control(0, 20, 0, 0)  # Vooruit bewegen
    elif toets == 's':
        tello.send_rc_control(0, -20, 0, 0)  # Achteruit bewegen
    elif toets == 'a':
        tello.send_rc_control(-20, 0, 0, 0)  # Links bewegen
    elif toets == 'd':
        tello.send_rc_control(20, 0, 0, 0)   # Rechts bewegen
    if toets == 'i':
        tello.send_rc_control(0, 0, 20, 0)  # Omhoog bewegen
    elif toets == 'k':
        tello.send_rc_control(0, 0, -20, 0)  # Omlaag bewegen
    elif toets == 'h':
        tello.send_rc_control(0, 0, 0, 0)  # Zweven
    elif toets == 'l':
        tello.send_rc_control(0, 0, 0, 20)  # Met de klok mee draaien
    elif toets == 'j':
        tello.send_rc_control(0, 0, 0, -20)  # Tegen de klok in draaien
    elif toets == 'q':
        tello.land()  # Landen

def main():
    try:
        # Opstijgen
        tello.takeoff()

        # Voeg sneltoetsen toe om de drone te besturen
        keyboard.add_hotkey('w', lambda: bestuur_drone(tello, 'w'))
        keyboard.add_hotkey('s', lambda: bestuur_drone(tello, 's'))
        keyboard.add_hotkey('a', lambda: bestuur_drone(tello, 'a'))
        keyboard.add_hotkey('d', lambda: bestuur_drone(tello, 'd'))
        keyboard.add_hotkey('i', lambda: bestuur_drone(tello, 'i'))
        keyboard.add_hotkey('k', lambda: bestuur_drone(tello, 'k'))
        keyboard.add_hotkey('j', lambda: bestuur_drone(tello, 'j'))
        keyboard.add_hotkey('l', lambda: bestuur_drone(tello, 'l'))
        keyboard.add_hotkey('h', lambda: bestuur_drone(tello, 'h'))
        keyboard.add_hotkey('q', tello.land)

        # Wacht op verbinding
        verbinding, client_adres = sock_dashboard.accept()
        
        #wanneer de loop true is dan gaat hij pas de code gebruiken
        while True:

            try:
                print('Verbinding van', client_adres)

                frame = tello.get_frame_read().frame
                grijs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                gezichten = face_cascade.detectMultiScale(grijs, scaleFactor=1.3, minNeighbors=5)

                for (x, y, w, h) in gezichten:
                    if w * h < 4000:  # Pas de groottegrens indien nodig aan
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Rode kleur voor kleinere gezichten
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Groene kleur voor andere gezichten

                print(frame.shape)

                # Wacht op opdracht van LabVIEW
                data = verbinding.recv(16)

                # Toon het frame met gezichtsdetectie
                if data:
                    verbinding.sendall(frame)
                else:
                    print('Geen gegevens van', client_adres)
                    break
            except Exception as e:
                print(e)

    except KeyboardInterrupt:
        tello.land()
    finally:
        # Sluit de verbinding
        verbinding.close()
        tello.land()
        tello.streamoff()
        cv2.destroyAllWindows()
        tello.end()

if __name__ == "__main__":
    main()
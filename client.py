import socket
import os

id = input("Nummer: ")
if len(id) == 1:
  id = "0" + id

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(f"vlg-bibl-{id}.local"), 8000))

print("""
a: Alert
w: Write
h: Hotkey
s: Sleep
pr: Print
c: Close
sc: Super-Close
ADVANCED:
p: PyAutogui
""")

while True:
    print()
    print()
    commands = []
    print("Schreibe Befehle, zum Senden Ctrl-D, zum Abbrechen Ctrl-C:\n")
    send = True
    while True:
        try:
            c = input()
        except EOFError:
            send = True
            break
        except KeyboardInterrupt:
            send = False
            break
        commands.append(c)
    if not send:
        continue
    command = "\n".join(commands)
    if "c()" in commands or "sc()" in commands:
        client.send(command.encode("utf-8"))
        client.close()
        break
    if len(command) > 1024:
        print("Befehlkette zu lang!")
        continue
    client.send(command.encode("utf-8"))
os.system("clear")
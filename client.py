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
    print("Schreibe Befehle, zum Schluss X:\n")
    while True:
      try:
          c = input()
      except EOFError:
          break
      commands.append(c)
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
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5978))

msg = s.recv(2048).decode("utf-8")

print(msg)

s.close()
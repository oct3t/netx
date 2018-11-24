import socket

target_host = "0.0.0.0"
target_port = 9999

# Create a socket obj
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client
client.connect((target_host, target_port))

# Send some data
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# Receivie some data
response = client.recv(1024)

print response

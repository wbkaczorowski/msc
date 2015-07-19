#UDP client broadcasts to server(s)
import socket, time

address = ('<broadcast>', 9001)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

data = "Test testowy "
tick = 0

while True:
    print data + format(tick)
    client_socket.sendto(data + format(tick), address)
    tick = tick + 1
    time.sleep(6)

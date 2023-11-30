########################## BOB is the receiver(server)
# import main as aes
# import diffie as dh
import socket


HOST = '127.0.0.1'
PORT = 56565




#################################### main ######################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
clientSocket,address=server.accept()
print("Connection Established!!!!!")

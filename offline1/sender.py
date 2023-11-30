###################### Alice is the sender (Client) ###################

# import main as aes
# import diffie as dh
import socket


HOST = '127.0.0.1'
PORT = 56565



#########################  main #######################

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Client side okay!!")

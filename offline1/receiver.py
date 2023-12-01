########################## BOB is the receiver(server)
# import main as aes
import diffie as dh
import socket


HOST = '127.0.0.1'
PORT = 56565

def generate_own_private_key(p):
    x=dh.get_random_number(p)
    return x

def get_final_key(rcvedPublicKey,private_key,p):
    computed_key=dh.compute_R(private_key,rcvedPublicKey,p)
    return computed_key

def generate_public_key(own_private_key,g_x,g_y,p,a):
    rx, ry = dh.scaler_point_mult(g_x, g_y, own_private_key, a, p)
    publicKey_Bob = rx % p  #### k_a*G mod p
    return publicKey_Bob



#################################### main ######################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
client,address=server.accept()
print("Connection Established!!!!!")

length = client.recv(1024).decode()
gotItems = client.recv(int(length)).decode()
#print(gotItems)
a, b, p,g_x,g_y,rcvedPublicKey = int(gotItems.split()[0]), int(gotItems.split()[1]), int(gotItems.split()[2]), int(gotItems.split()[3]),int(gotItems.split()[4]),int(gotItems.split()[5])
print(a)
print(b)
print(p)
print(g_x)
print(g_y)
print(rcvedPublicKey)
bob_private_key=generate_own_private_key(p)
computed_key=get_final_key(rcvedPublicKey,bob_private_key,p)
print(computed_key)

publicKey_Bob=generate_public_key(bob_private_key,g_x,g_y,p,a)
client.sendall(str(publicKey_Bob).encode())  ############## sending bob's public key
print("hereeeeeeee")
print(publicKey_Bob)



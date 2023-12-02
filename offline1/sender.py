###################### Alice is the sender (Client) ###################

# import main as aes
import diffie_hellman as dh
import socket


HOST = '127.0.0.1'
PORT = 56565
########### send a,b, p, G(point), k_a*G mod p
def generate_what_to_send_initially(bit):
    p=dh.generate_random_prime(bit)
    a=dh.a
    b=dh.b
    g_x,g_y=dh.generate_random_x_y(a,b)
    own_secretKey=dh.get_random_number(p)
    rx, ry = dh.scaler_point_mult(g_x, g_y, own_secretKey, a,p)
    publicKey_A_x = rx % p  #### k_a*G mod p
    publicKey_A_y =ry % p
    return p,a,b,g_x,g_y,publicKey_A_x,publicKey_A_y,own_secretKey


# def get_final_key(rcvedPublicKey,private_key,p):
#     computed_key=dh.compute_R(private_key,rcvedPublicKey,p)
#     return computed_key

def get_final_key(rcvedPublicKey_x,rcvedPublicKey_y,private_key,p):
    computed_key=dh.compute_R(private_key,rcvedPublicKey_x,rcvedPublicKey_y,p)
    return computed_key



#########################  main #######################

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Client side okay!!")
p,a,b,g_x,g_y,publicKey_A_x,publicKey_A_y,own_private_key=generate_what_to_send_initially(128)
#print(p,a,b,g_x,g_y,publicKey_A)
items = str(a) + " " + str(b) + " " + str(p) + " " + str(g_x) + " " + str(g_y) + " " + str(publicKey_A_x)+ " " + str(publicKey_A_y)
client.sendall(str(len(items)).encode())
client.sendall(items.encode())
# print(a)
# print(b)
# print(p)
# print(g_x)
# print(g_y)
#print(publicKey_A_x)
#print(publicKey_A_y)


length = client.recv(1024).decode()
gotItems = client.recv(int(length)).decode()
bob_key_x,bob_key_y = int(gotItems.split()[0]), int(gotItems.split()[1])


final_key=get_final_key(bob_key_x,bob_key_y,own_private_key,p)
print("hereeeeeeee")
print(final_key)

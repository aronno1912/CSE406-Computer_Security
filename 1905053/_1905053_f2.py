######################### implementation of diffie-hellman #################################
import random
from sympy import isprime
from Crypto.Util import number
import math
import os
import time

global P, x, y
a = 3
b = 4


def is_perfect_square(n):
    root = int(math.sqrt(n))
    return root * root == n


###################### G generation ########################3
def generate_random_x_y(a, b):
    while True:
        x = random.randint(1, 500)
        expression_result = x ** 3 + a * x + b

        if is_perfect_square(expression_result):
            y = int(math.sqrt(expression_result))
            return x, y


############# P generation ###########################
def generate_random_prime(bits):
    while True:
        # Generate a random number with the specified number of bits
        p = random.getrandbits(bits)

        # Ensure the number has the correct bit length
        p |= (1 << (bits - 1)) | 1

        # Check if the number is prime
        if isprime(p):
            return p


def get_random_number(p):
    random_number = random.randint(2, p - 1)
    return random_number


def generate_parameter_a_b(p):
    while True:
        # Generate random numbers a and b
        a = random.randint(1, p - 1)
        b = random.randint(1, p - 1)

        # Calculate the expression 4a^3 + 27b^2 mod p
        result = (4 * (a ** 3) + 27 * (b ** 2)) % p

        # Check if the result is not equal to 0 mod p
        if result != 0:
            return a, b
        else:
            generate_parameter_a_b(P)


#
def point_doubling(x1, y1, a, P):
    s = ((3 * x1 ** 2 + a) * pow(2 * y1, -1, P)) % P
    x3 = (s ** 2 - (2 * x1)) % P
    y3 = ((s * (x1 - x3) - y1) % P)
    return x3, y3


########################## use this ########################
def point_addition(x1, y1, x2, y2, P):
    s = ((y2 - y1) * pow(x2 - x1, -1, P)) % P
    x3 = (s ** 2 - (x2 + x1)) % P
    y3 = (s * (x1 - x3) - y1) % P
    return x3, y3


################## algorithm for point multiplication.........if bit is 1 perform both add and doubling!!!!!
def scaler_point_mult(x1, y1, secretKey, a, p):
    secretKey_bin = bin(secretKey)[3:]  # used to remove the '0b' prefix and the msb
    final_x = x1
    final_y = y1
    for i, bit in enumerate(secretKey_bin):
        (x1, y1) = point_doubling(x1, y1, a, p)
        if bit == '1':
            x1, y1 = point_addition(x1, y1, final_x, final_y, p)
    return x1, y1


def get_y_from_elliptic_curve(x):
    y2 = x ** 3 + a * x + b
    y = (math.sqrt(y2))
    print("Y is  ", y)
    return y


def compute_R(ownPrivateKey, recvPublicKeyx, recvPublicKey_y, P):
    pub_x = recvPublicKeyx
    pub_y = recvPublicKey_y
    tempx, tempy = scaler_point_mult(pub_x, pub_y, ownPrivateKey, a, P)
    R = tempx % P
    return R


def all_calculation(howManyBit):
    global P, x, y
    P = generate_random_prime(howManyBit)
    #print(P)
    x, y = generate_random_x_y(a, b)
    time_A = 0.0000
    time_B = 0.0000
    time_R = 0.0000
    for i in range(1, 6):
        start_A = time.time()
        secretKey_A = get_random_number(P)  # K_a
        rx, ry = scaler_point_mult(x, y, secretKey_A, a, P)
        publicKey_Ax = rx % P  # K_a*G mod P which is x component of A
        publicKey_Ay = ry % P   # y component of A
        end_A = time.time()
        start_B = time.time()
        secretKey_B = get_random_number(P)  # K_b
        rrx, rry = scaler_point_mult(x, y, secretKey_B, a, P)
        publicKey_Bx = rrx % P  # K_b*G mod P   which is B
        publicKey_By = rry % P
        end_B = time.time()
        start_R = time.time()
        #print("alice")
        R = compute_R(secretKey_A, publicKey_Bx, publicKey_By, P)
        #print(R)
        # print("Bob")
        # print("Bob er private ,",secretKey_B)
        # print("rcv ",publicKey_Ax)

        R2 = compute_R(secretKey_B, publicKey_Ax, publicKey_Ay, P)
        #print(R2)
        #print()
        end_R = time.time()
        time_A = time_A + (end_A - start_A)
        time_B = time_B + (end_B - start_B)
        time_R = time_R + (end_R - start_R)

    time_A = time_A / 5
    time_B = time_B / 5
    time_R = time_R / 5
    print("A", time_A * 1000)
    print("B", time_B * 1000)
    print("R", time_R * 1000)


#####################################  main    ###########################################
def main():
    print("For 128 bit :")
    all_calculation(128)
    print()
    print("For 192 bit :")
    all_calculation(192)
    print()
    print("For 256 bit :")
    all_calculation(256)


if __name__ == "__main__":
    main()


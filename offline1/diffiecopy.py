import random
from sympy import isprime
from Crypto.Util import number
import math
import os
import time

global P,x,y
a=3
b=4



def is_perfect_square(n):
    root = int(math.sqrt(n))
    return root*root == n

###################### G generation ########################3
def generate_random_x_y(a, b):
    while True:
        x = random.randint(1, 500)
        expression_result = x**3 + a*x + b

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
    random_number = random.randint(2, p-1)
    return random_number
#
# def generate_parameter_a_b(p):
#     while True:
#         # Generate random numbers a and b
#         a = random.randint(1, p - 1)
#         b = random.randint(1, p - 1)
#
#         # Calculate the expression 4a^3 + 27b^2 mod p
#         result = (4 * (a**3) + 27 * (b**2)) % p
#
#         # Check if the result is not equal to 0 mod p
#         if result != 0:
#             return a, b
#         else:
#             generate_parameter_a_b(P)
#
def point_doubling(x1,y1,a):
    t1=number.inverse(2*y1, P)
    s=((3*x1**2 +a)*t1)%P
    x3=(s**2-(2*x1))%P
    y3=((s*(x1-x3)-y1)%P)
    return x3,y3

# def point_double(x,y, a,p):
#     # Point doubling operation
#     s = (3 * x * x + a) % p
#     inv_s = pow(s, -1, p)
#     m = (2 * y * inv_s) % p
#     x_result = (m * m - 2 * x) % p
#     y_result = (m * (x - x_result) - y) % p
#     return x_result, y_result

def point_addition(x1,y1,x2,y2):
    t1 = number.inverse(x2 - x1, P)
    s=((y2-y1)*t1)%P
    x3 = (s ** 2 - (x2+ x1)) % P
    y3 = (s * (x1 - x3) - y1) % P
    return x3, y3



# def point_doubling(x1, y1, a):
#     numerator = (3 * x1**2 + a)
#     denominator = 2 * y1
#
#     # Ensure integer division
#     ss = numerator // denominator
#
#     x3 = (ss**2 - 2*x1) % P
#     y3 = (ss * (x1 - x3) - y1) % P
#
#     return x3, y3
def scaler_point_mult(x1,y1,secretKey,a):
    bitNum=secretKey.bit_length()
    finalx,finaly=x1,y1
    for i in reversed(range(0,bitNum-1)):
        finalx, finaly = point_doubling(finalx, finaly, a)
        #if the current bit in the binary representation of the scalar secretKey is 1,
        # perform point addition using the add function.
        if secretKey & 1 << i:
            finalx, finalx = point_addition(finalx, finaly, x1, y1)
    return finalx, finaly


def get_y_from_elliptic_curve(x):
    y2=x**3 + a*x + b
    y=int(math.sqrt(y2))
    return y

def compute_R(ownPrivateKey,recvPublicKey_x,recvPublicKey_y):
    pub_x=recvPublicKey_x
    pub_y=recvPublicKey_y
    tempx,tempy=scaler_point_mult(pub_x,pub_y,ownPrivateKey,a)
    R=tempx%P
    return R




def all_calculation(howManyBit):
    global P,x,y
    P = generate_random_prime(howManyBit)
    print(P)
    x, y = generate_random_x_y(a, b)
    time_A = 0.0000
    time_B = 0.0000
    time_R = 0.0000
    for i in range(1, 6):
        start_A = time.time()
        secretKey_A = get_random_number(P)  # K_a
        rx, ry = scaler_point_mult(x, y, secretKey_A, a)
        publicKey_Ax = rx % P  # K_a*G mod P which is A
        publicKey_Ay = ry % P
        end_A = time.time()
        start_B = time.time()
        secretKey_B = get_random_number(P)  # K_b
        rrx, rry = scaler_point_mult(x, y, secretKey_B, a)
        publicKey_Bx = rrx % P  # K_b*G mod P   which is B
        publicKey_By = rry % P
        end_B = time.time()
        start_R = time.time()
        R = compute_R(secretKey_A, publicKey_Bx,publicKey_By)
        R2 = compute_R(secretKey_B, publicKey_Ax, publicKey_Ay)
        print(R)
        print(R2)
        end_R = time.time()
        time_A = time_A + (end_A - start_A)
        time_B = time_B + (end_B - start_B)
        time_R = time_R + (end_R - start_R)

    time_A = time_A / 5
    time_B = time_B / 5
    time_R = time_R / 5
    print("A",time_A * 1000)
    print("B",time_B * 1000)
    print("R",time_R * 1000)

#####################################  main    ###########################################
print("For 128 bit :")
all_calculation(128)
# print()
# print("For 192 bit :")
# all_calculation(192)
# print()
# print("For 256 bit :")
# all_calculation(256)



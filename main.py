# import os
#
## def generate_random_iv_matrix():
#     # Generate a random 16-byte IV
#     iv = os.urandom(16)
#
#     # Convert the IV to a 4x4 matrix of hex strings
#     iv_hex_array = [format(byte, '02x') for byte in iv]
#     iv_matrix = [iv_hex_array[i:i+4] for i in range(0, len(iv_hex_array), 4)]
#
#     return iv_matrix
#
# # Example usage:
# iv_matrix = generate_random_iv_matrix()
# for row in iv_matrix:
#     print(row)

import random
from sympy import isprime


def generate_random_prime(bits):
    while True:
        # Generate a random number with the specified number of bits
        candidate = random.getrandbits(bits)

        # Ensure the number has the correct bit length
        candidate |= (1 << (bits - 1)) | 1

        # Check if the number is prime
        if isprime(candidate):
            return candidate


# Generate a random prime with 128 bits
prime_128_bits = generate_random_prime(128)

print(f"Random prime with 128 bits: {prime_128_bits}")

import random

def generate_nonzero_mod_p(p):
    while True:
        # Generate random numbers a and b
        a = random.randint(1, p - 1)
        b = random.randint(1, p - 1)

        # Calculate the expression 4a^3 + 27b^2 mod p
        result = (4 * (a**3) + 27 * (b**2)) % p

        # Check if the result is not equal to 0 mod p
        if result != 0:
            return a, b, result

# Example usage with p = 13 (you can replace 13 with any prime number)
p_value = 13
a_result, b_result, expression_result = generate_nonzero_mod_p(prime_128_bits)

print(f"a: {a_result}")
print(f"b: {b_result}")
print(f"4a^3 + 27b^2 mod {prime_128_bits}: {expression_result}")

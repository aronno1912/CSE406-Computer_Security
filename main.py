import os

def generate_random_iv_matrix():
    # Generate a random 16-byte IV
    iv = os.urandom(16)

    # Convert the IV to a 4x4 matrix of hex strings
    iv_hex_array = [format(byte, '02x') for byte in iv]
    iv_matrix = [iv_hex_array[i:i+4] for i in range(0, len(iv_hex_array), 4)]

    return iv_matrix

# Example usage:
iv_matrix = generate_random_iv_matrix()
for row in iv_matrix:
    print(row)
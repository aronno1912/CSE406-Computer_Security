# def print_ascii_hex(sentence):
#     for char in sentence:
#         if char.isalpha():
#             ascii_value = ord(char)
#             hex_value = hex(ascii_value)[2:].upper()
#             print(hex_value, end=' ')
#         elif char.isspace():
#             print('20', end=' ')  # ASCII value for space
#     print()  # Print a newline at the end
key=[]
ptWithPad = []


def print_ascii_hex(sentence):
    for char in sentence:
        ascii_value = ord(char)
        hex_value = hex(ascii_value)[2:].upper()
        key.append(hex_value)
        print(key, end=' ')
    print()  # Print a newline at the end


def plain_text_handling(sentence,array):
    for char in sentence:
            ascii_value = ord(char)
            hex_value = hex(ascii_value)[2:].upper()
            array.append(hex_value)


    # Pad with '00' until the length is 16
    while len(array) % 16 != 0:
        array.append('00')

    # Split into blocks of length 16 and print
    for i in range(0, len(array), 16):
        block = array[i:i+16]
        print(' '.join(block))

######################## make matrix ##################################
def convert_to_matrix(ptWithPad):
    matrices = []
    num_matrices = len(ptWithPad) // 16

    for i in range(num_matrices):
        matrix = [[ptWithPad[j], ptWithPad[j + 1], ptWithPad[j + 2], ptWithPad[j + 3]] for j in
                  range(i * 16, (i + 1) * 16, 4)]
        matrices.append(matrix)

    return matrices

# Example usage:
sentence = "Never gonna give you up"
plain_text_handling(sentence,ptWithPad)

################# print matrices###############
matrices = convert_to_matrix(ptWithPad)
for i, matrix in enumerate(matrices, start=1):
    print(f"Matrix p{i}:")
    for row in matrix:
        print(row)
    print()
#####################################################

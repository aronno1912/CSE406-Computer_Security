from util import *

key = []
ptWithPad = []
roundKeyMatrices = []


def convert_str_array_to_int(input_array):
    int_array = [int(element) for element in input_array]
    return int_array

def convert_str_array_to_hex(input_array):
    hex_array = [hex(int(element))[2:] for element in input_array]
    return hex_array

def convert_int_list_to_hex(int_list):
    hex_list = [hex(num)[2:] for num in int_list]
    return hex_list

def print_ascii_hex(sentence):
    for char in sentence:
        ascii_value = ord(char)
        hex_value = hex(ascii_value)[2:].upper()
        key.append(hex_value)
        print(key, end=' ')
    print()  # Print a newline at the end


def plain_text_handling(sentence, array):
    for char in sentence:
        ascii_value = ord(char)
        hex_value = hex(ascii_value)[2:].upper()
        array.append(hex_value)

    # Pad with '00' until the length is 16
    while len(array) % 16 != 0:
        array.append('00')

    # Split into blocks of length 16 and print
    for i in range(0, len(array), 16):
        block = array[i:i + 16]
        print(' '.join(block))


######################## make matrix ##################################
msgMatrices = []


def convert_to_matrix(ptWithPad, listOfMat):
    num_matrices = len(ptWithPad) // 16

    for i in range(num_matrices):
        matrix = [[ptWithPad[j], ptWithPad[j + 1], ptWithPad[j + 2], ptWithPad[j + 3]] for j in
                  range(i * 16, (i + 1) * 16, 4)]
        transposed_matrix = list(map(list, zip(*matrix)))
        listOfMat.append(transposed_matrix)

    return listOfMat


############################### key ############################
def convert_to_matrix_row_major(ptWithPad):
    num_matrices = len(ptWithPad) // 16

    for i in range(num_matrices):
        matrix = [[ptWithPad[j], ptWithPad[j + 1], ptWithPad[j + 2], ptWithPad[j + 3]] for j in
                  range(i * 16, (i + 1) * 16, 4)]
        # transposed_matrix = list(map(list, zip(*matrix)))
        # listOfMat.append(transposed_matrix)

    return matrix


def byteSubstitutionFromS_Box(row, flag):

    for i in range(len(row)):
        if flag:
            row[i]=hex(Sbox[int(row[i], 16)])
        else:
            row[i] = hex(InvSbox[int(row[i], 16)])
        row[i]=row[i][2:]
    #print(row)

#######################################################################
def xor_rows(row1, row2):
    if len(row1) != len(row2):
        raise ValueError("Rows must have the same length for XOR operation.")

    result_row = [element1 ^ element2 for element1, element2 in zip(row1, row2)]
    return result_row

def xor_hex_rows(hex_row1, hex_row2):
    if len(hex_row1) != len(hex_row2):
        raise ValueError("Rows must have the same length for XOR operation.")

    result_row = [hex(int(element1, 16) ^ int(element2, 16))[2:] for element1, element2 in zip(hex_row1, hex_row2)]
    return result_row

def circular_left_shift(row):
    if not row:
        return row  # Return an empty row as is

    shifted_row = row[1:] + [row[0]]
    return shifted_row


def roundConsRow(idx):
    row = [roundConstant[idx], 0x00, 0x00, 0x00]
    return row

########################## Round key###########################################
def roundKey(mat,ind):
    new_matrix = []
    shifted_row=circular_left_shift(mat[3])
    byteSubstitutionFromS_Box(shifted_row, True)
    rc=roundConsRow(ind)
    rc=convert_int_list_to_hex(rc)
    g=xor_hex_rows(rc,shifted_row)
    row1=xor_hex_rows(mat[0],g)
    row2=xor_hex_rows(row1,mat[1])
    row3=xor_hex_rows(row2,mat[2])
    row4=xor_hex_rows(row3,mat[3])

    # Construct the new matrix
    new_matrix.append(row1)
    new_matrix.append(row2)
    new_matrix.append(row3)
    new_matrix.append(row4)

    # Transpose the matrix before returning
    transposed_matrix = [list(row) for row in zip(*new_matrix)]
    return transposed_matrix

def generateAllRoundKeyMatrices(initial_matrix):
    transposed_matrix = [list(row) for row in zip(*initial_matrix)]
    roundKeyMatrices.append(transposed_matrix)

    for i in range(1, 11):
        # Call your roundKey function here with the appropriate arguments
        new_matrix = roundKey(initial_matrix,i)
        roundKeyMatrices.append(new_matrix)
        transposed_matrix = [list(row) for row in zip(*new_matrix)]
        initial_matrix=transposed_matrix




# Example usage:
sentence = "Thats my Kung Fu"
plain_text_handling(sentence, key)

################# print matrices###############
originalKeyMat = []
originalKeyMat = convert_to_matrix_row_major(key)
generateAllRoundKeyMatrices(originalKeyMat)


###################################### debug ###################
def print_matrix(matrix):
    for row in matrix:
        print(row)

def print_list_of_matrices(matrix_list):
    for idx, matrix in enumerate(matrix_list, start=1):
        print(f"Matrix {idx}:")
        print_matrix(matrix)
        print()

##################################################################################################
print_list_of_matrices(roundKeyMatrices)


#####################################################

from util import *
import os

key = []
ptWithPad = []
roundKeyMatrices = []
msgMatrices = []
cipherTextMatrices = []
initializationVector=[]

def generate_random_iv_hex_array():
    # Generate a random 16-byte IV
    iv = os.urandom(16)

    # Convert the IV to a 1D array of hex strings
    iv_hex_array = [format(byte, '02x') for byte in iv]

    return iv_hex_array

def convert_str_array_to_int(input_array):
    int_array = [int(element) for element in input_array]
    return int_array

def convert_str_array_to_hex(input_array):
    hex_array = [hex(int(element))[2:] for element in input_array]
    return hex_array

def convert_int_list_to_hex(int_list):
    hex_list = [hex(num)[2:] for num in int_list]
    return hex_list

def convert_2d_to_1d_column_major(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    array = []
    for col in range(cols):
        for row in range(rows):
            array.append(matrix[row][col])

    return array

def hex_array_to_sentence(hex_array):
    sentence = ''.join([chr(int(hex_str, 16)) for hex_str in hex_array])
    return sentence

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


### col major
def convert_to_matrix(ptWithPad, listOfMat):
    num_matrices = len(ptWithPad) // 16

    for i in range(num_matrices):
        matrix = [[ptWithPad[j], ptWithPad[j + 1], ptWithPad[j + 2], ptWithPad[j + 3]] for j in
                  range(i * 16, (i + 1) * 16, 4)]
        transposed_matrix = list(map(list, zip(*matrix)))
        listOfMat.append(transposed_matrix)




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


def byte_substitution_matrix(matrix,flag):
    new_matrix = []

    for row in matrix:
        byteSubstitutionFromS_Box(row, flag)
        new_matrix.append(row.copy())  # Copy the modified row to the new matrix

    return new_matrix

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


def xor_matrices(mat1, mat2):
    if len(mat1) != len(mat2) or any(len(row1) != len(row2) for row1, row2 in zip(mat1, mat2)):
        raise ValueError("Matrices must have the same dimensions for XOR operation.")

    result_matrix = []
    for row1, row2 in zip(mat1, mat2):
        result_row = xor_hex_rows(row1, row2)
        result_matrix.append(result_row)

    return result_matrix

def circular_left_shift(row):
    if not row:
        return row  # Return an empty row as is

    shifted_row = row[1:] + [row[0]]
    return shifted_row

def cyclic_left_shift_whole_mat(matrix):
    # Cyclic left shift the 2nd row by 1
    matrix[1] = matrix[1][1:] + matrix[1][:1]

    # Cyclic left shift the 3rd row by 2
    matrix[2] = matrix[2][2:] + matrix[2][:2]

    # Cyclic left shift the 4th row by 3
    matrix[3] = matrix[3][3:] + matrix[3][:3]

    return matrix

def cyclic_right_shift_whole_mat(matrix):
    # Cyclic right shift the 2nd row by 1
    matrix[1] = matrix[1][-1:] + matrix[1][:-1]

    # Cyclic right shift the 3rd row by 2
    matrix[2] = matrix[2][-2:] + matrix[2][:-2]

    # Cyclic right shift the 4th row by 3
    matrix[3] = matrix[3][-3:] + matrix[3][:-3]

    return matrix

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

def mix_column(matrix1, matrix2):
    result_matrix = [[0 for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                bv1 = matrix1[i][k]
                bv2 = BitVector(hexstring=matrix2[k][j])
                bv3=bv1.gf_multiply_modular(bv2, AES_modulus, 8)
                result_matrix[i][j] = result_matrix[i][j]^bv3.intValue()


    # # Convert the result back to hexadecimal strings
    # result_matrix = [[bv.getHexStringFromBitVector() for bv in row] for row in result_matrix]
  # Convert the result back to hexadecimal strings
    result_matrix = [[format(value, 'x') for value in row] for row in result_matrix]

    return result_matrix


# Example usage:



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



##################################################### main() ###############################

sentence = "Thats my Kung Fu"
plain_text_handling(sentence, key)
originalKeyMat = []
originalKeyMat = convert_to_matrix_row_major(key)
generateAllRoundKeyMatrices(originalKeyMat)
#print_list_of_matrices(roundKeyMatrices)
msg="Two One Nine Two"
plain_text_handling(msg, ptWithPad)
convert_to_matrix(ptWithPad,msgMatrices)
#print_matrix(msgMatrices[0])

########## round 0 ########################
state_mat=xor_matrices(msgMatrices[0],roundKeyMatrices[0])

############### round 1 to 9##############################
for i in range(1,10):
    state_mat = byte_substitution_matrix(state_mat,True)
    state_mat = cyclic_left_shift_whole_mat(state_mat)
    state_mat = mix_column(Mixer, state_mat)
    state_mat = xor_matrices(state_mat, roundKeyMatrices[i])
####################### round 10 ################################

state_mat = byte_substitution_matrix(state_mat,True)
state_mat = cyclic_left_shift_whole_mat(state_mat)
state_mat = xor_matrices(state_mat, roundKeyMatrices[10])
print_matrix(state_mat)
cipherTextMatrices.append(state_mat)

############################## done with encryption ##################

############################## start decryption ##############################

########## round 0 ########################
inv_state_mat=xor_matrices(cipherTextMatrices[0],roundKeyMatrices[10])
for i in range(1,10):
    inv_state_mat = cyclic_right_shift_whole_mat(inv_state_mat)
    inv_state_mat = byte_substitution_matrix(inv_state_mat,False)
    inv_state_mat = xor_matrices(inv_state_mat, roundKeyMatrices[10 - i])
    inv_state_mat = mix_column(InvMixer, inv_state_mat)

########### round 10 ########################
inv_state_mat = cyclic_right_shift_whole_mat(inv_state_mat)
inv_state_mat = byte_substitution_matrix(inv_state_mat,False)
inv_state_mat = xor_matrices(inv_state_mat, roundKeyMatrices[0])
print()
cipher_in_1d=convert_2d_to_1d_column_major(inv_state_mat)
sen=hex_array_to_sentence(cipher_in_1d)
print(sen)










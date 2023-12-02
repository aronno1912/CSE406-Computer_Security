from util import *
import os
import time

key = []
ptWithPad = []
roundKeyMatrices = []
msgMatrices = []
cipherTextMatrices = []
initializationVector=[['46', 'ce', '24', 'e4'], ['79', 'e1', '63', 'a3'], ['24', '5a', '29', '03'], ['a1', 'c9', '98', '74']]
afterDecryptionSentences=[]



############################### key ############################
def convert_to_matrix_row_major(ptWithPad):
    num_matrices = len(ptWithPad) // 16

    for i in range(num_matrices):
        matrix = [[ptWithPad[j], ptWithPad[j + 1], ptWithPad[j + 2], ptWithPad[j + 3]] for j in
                  range(i * 16, (i + 1) * 16, 4)]
        # transposed_matrix = list(map(list, zip(*matrix)))
        # listOfMat.append(transposed_matrix)

    return matrix

###### takes a list of matries of hex strings a returns a string with ascii chars
def matrices_to_string(matrix_list):
    result_string = ""

    for matrix in matrix_list:
        hex_array = [element for row in matrix for element in row]
        sentence = hex_array_to_sentence(hex_array)
        result_string += sentence

    return result_string

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


def hex_matrices_to_sentence(matrix_list):
    for matrix in matrix_list:
        hex_array = [element for row in matrix for element in row]
        sentence = hex_array_to_sentence(hex_array)
        print(sentence, end="")


def plain_text_handling(sentence, array):
    for char in sentence:
        ascii_value = ord(char)
        hex_value = hex(ascii_value)[2:].upper()
        array.append(hex_value)

    # Pad with '00' until the length is 16
    while len(array) % 16 != 0:
        array.append('20')         ########################       space padding!!!!!!!!!



######################## make matrix ##################################


### col major
def convert_to_matrix(ptWithPad, listOfMat):
    num_matrices = len(ptWithPad) // 16

    for i in range(num_matrices):
        matrix = [[ptWithPad[j], ptWithPad[j + 1], ptWithPad[j + 2], ptWithPad[j + 3]] for j in
                  range(i * 16, (i + 1) * 16, 4)]
        transposed_matrix = list(map(list, zip(*matrix)))
        listOfMat.append(transposed_matrix)

##### row major
def convert_to_matrix2(ptWithPad, listOfMat):
    num_matrices = len(ptWithPad) // 16

    for i in range(num_matrices):
        matrix = [[ptWithPad[j], ptWithPad[j + 1], ptWithPad[j + 2], ptWithPad[j + 3]] for j in
                  range(i * 16, (i + 1) * 16, 4)]
        #transposed_matrix = list(map(list, zip(*matrix)))
        listOfMat.append(matrix)


def byteSubstitutionFromS_Box(row, flag):

    for i in range(len(row)):
        if flag:
            row[i]=hex(Sbox[int(row[i], 16)])
        else:
            row[i] = hex(InvSbox[int(row[i], 16)])
        row[i]=row[i][2:]


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
    s=time.time()
    rc=roundConsRow(ind)
    rc=convert_int_list_to_hex(rc)
    e=time.time()
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
  # Convert the result back to hexadecimal strings
    result_matrix = [[format(value, 'x') for value in row] for row in result_matrix]

    return result_matrix


#################################### ENCRYPTION ##############################################################


def do_encryption(sharedKey,msg):
    global initializationVector
    plain_text_handling(sharedKey, key)
    originalKeyMat = convert_to_matrix_row_major(key)
    generateAllRoundKeyMatrices(originalKeyMat)
    plain_text_handling(msg, ptWithPad)
    convert_to_matrix(ptWithPad, msgMatrices)
    tempIV = initializationVector
    # Iterate over the size of msgMatrices list
    for iter in range(len(msgMatrices)):

        tempMat = xor_matrices(msgMatrices[iter], tempIV)
        ###################### round 0 #####################################################
        state_mat = xor_matrices(tempMat, roundKeyMatrices[0])

        #####################Rounds 1 to 9 ################################
        for i in range(1, 10):
            state_mat = byte_substitution_matrix(state_mat, True)
            state_mat = cyclic_left_shift_whole_mat(state_mat)
            state_mat = mix_column(Mixer, state_mat)
            state_mat = xor_matrices(state_mat, roundKeyMatrices[i])

        #####################Round 10#########################################
        state_mat = byte_substitution_matrix(state_mat, True)
        state_mat = cyclic_left_shift_whole_mat(state_mat)
        state_mat = xor_matrices(state_mat, roundKeyMatrices[10])
        tempIV = state_mat

        # print_matrix(state_mat)
        cipherTextMatrices.append(state_mat)
    str=matrices_to_string(cipherTextMatrices)
    cipherTextMatrices.clear()
    msgMatrices.clear()
    afterDecryptionSentences.clear()
    ptWithPad.clear()
    return str

#################################### DECRYPTION ##############################################################

def do_decryption(sharedKey,msg):
    global initializationVector
    plain_text_handling(sharedKey, key)
    originalKeyMat = convert_to_matrix_row_major(key)
    generateAllRoundKeyMatrices(originalKeyMat)
    plain_text_handling(msg, ptWithPad)
    convert_to_matrix2(ptWithPad, msgMatrices)
    tempIV = initializationVector
    for d in range(len(msgMatrices)):

        inv_state_mat = xor_matrices(msgMatrices[d], roundKeyMatrices[10])
        for i in range(1, 10):
            inv_state_mat = cyclic_right_shift_whole_mat(inv_state_mat)
            inv_state_mat = byte_substitution_matrix(inv_state_mat, False)
            inv_state_mat = xor_matrices(inv_state_mat, roundKeyMatrices[10 - i])
            inv_state_mat = mix_column(InvMixer, inv_state_mat)

        ########### round 10 ########################
        inv_state_mat = cyclic_right_shift_whole_mat(inv_state_mat)
        inv_state_mat = byte_substitution_matrix(inv_state_mat, False)
        inv_state_mat = xor_matrices(inv_state_mat, roundKeyMatrices[0])
        tempInv = xor_matrices(inv_state_mat, tempIV)  ############################## just for iv
        tempIV = msgMatrices[d]
        #print("ekhane")
        cipher_in_1d = convert_2d_to_1d_column_major(tempInv)
        #print(' '.join(map(str, cipher_in_1d)))
        sen = hex_array_to_sentence(cipher_in_1d)
        afterDecryptionSentences.append(sen)

    result_string = ''.join(afterDecryptionSentences)
    cipherTextMatrices.clear()
    msgMatrices.clear()
    afterDecryptionSentences.clear()
    ptWithPad.clear()
    return result_string






import pandas as pd
from decimal import Decimal
import time
import struct
import sys

def native_binary(num, visualize=True):
    '''
    Function:
        Prints out the native binary representation of a float

    Params:
        num: float number
    '''

    x = ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))
    if visualize:
        print("Sign - Exponent - Mantissa")
        return x [0] + " - " + x[1:9] + " - " + x[9:]
    else:
        return x
    

def pack_float(num, visualize=True):
    '''
    Function:
        Converts a floating point number to the IEEE 754 32-bit base-2 floating-point variable format
    
    Params:
        num: floating point number to pack
        visualize: return in a form that is easier to read
    '''
    
    if num >= 0:
        sign = '0'
    else:
        sign = '1'
        num  = abs(num)
    ### Convert float number to binary representation
    binary_num = convert_float_to_binary(num)
    ### Normalize the mantissa
    try:
        cur_decimal = binary_num.find('.')
        shifted_decimal = binary_num.index('1') + 1
    except ValueError:
        shifted_decimal = cur_decimal
        shift = -127
    else:
        shift = cur_decimal - shifted_decimal
        if shift < 0:
            shift+=1
    ### Find the final exponent and mantissa
    exponent = convert_whole_to_binary(shift + 127)
    exponent = "".join(['0']*(8 - len(exponent))) + exponent
    mantissa = binary_num[shifted_decimal:].replace(".", "")
    mantissa = mantissa + "".join(['0']*(23 - len(mantissa)))
    mantissa = mantissa[0:23]
    if visualize:
        print("Sign - Exponent - Mantissa")
        return sign + " - " + exponent + " - " + mantissa
    else:
        return sign + exponent + mantissa

def convert_float_to_binary(num):
    '''
    Function:
        Converts a number to its binary equivalent

    Params:
        num: float number
    '''

    num_split = str(num).split(".")
    try:
        num_split[1] = "0." + num_split[1]
    except IndexError:
        num_split.append("0.0")
    num_split = list(map(lambda x : float(x), num_split))
    binary_whole = convert_whole_to_binary(num_split[0])
    binary_fraction = convert_fraction_to_binary(num_split[1])
    return binary_whole + "." + binary_fraction

def convert_whole_to_binary(num):
    '''
    Function:
        Converts an integer to its binary equivalent

    Params:
        num: integer number
    '''

    binary = [0]*128
    length = 0
    quotient = int(num)
    while True:
        remainder = str(quotient % 2)
        quotient = int(quotient / 2)
        binary[length] = remainder
        length+=1
        if quotient == 0:
            break
    binary = binary[0:length]
    binary.reverse()
    return "".join(binary)

def convert_fraction_to_binary(num):
    '''
    Function:
        Converts the fractional portion of a float to its binary equivalent
    
    Params:
        num: fractional portion of float number
    '''

    binary = []
    product = num
    while True:
        product = product * 2
        carry = int(product)
        product = product - carry
        binary.append(str(carry))
        if product == 0:
            break
    return "".join(binary)

def test_packing_time(test, test_range=1000000):
    '''
    Function:
        Test the average time to pack a float using the pack_float() method with 1,000,000 iterations

    Params:
        test: float number to test
        test_range: number of tests to run
    '''

    total = 0
    for i in range(test_range):
        start = time.time()
        pack_float(test)
        total+=time.time() - start
    return total / test_range

def convert_binary_to_int(binary):
    binary = str(binary)
    length = len(binary)-1
    sum_total = 0
    for bit in binary:
        sum_total+=int(bit) * math.pow(2, length)
        length-=1
    return sum_total

def compare_floats(float1, float2, max_ULPs=4):
    # Numbers have different signs, return false
    if float1 < 0 != float2 < 0:
        return False

    # Get binary form of floats
    float1 = int(native_binary(float1, False))
    float2 = int(native_binary(float2, False))

    # Convert binary to int
    float1 = int(convert_binary_to_int(float1))
    float2 = int(convert_binary_to_int(float2))

    # Compare integer representations
    return abs(float2 - float1) < max_ULPs

if __name__ == "__main__":

    num = float(sys.argv[1])

    print(pack_float(num))
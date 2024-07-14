def mbin(num, length):
    match length:
        case 8:
            if num > 127 or num < -128:
                raise ValueError("num must be between -128 and 127 for length 8, got " + str(num) + " instead.")
        case 16:
            if num > 32767 or num < -32768:
                raise ValueError("num must be between -32768 and 32767 for length 16, got " + str(num) + " instead.")
        case 32:
            if num > 2147483647 or num < -2147483648:
                raise ValueError("num must be between -2147483648 and 2147483647 for length 32, got " + str(num) + " instead.")
        case _:
            raise ValueError("length must be 8, 16, or 32, got " + str(length) + " instead.")
    if num >= 0:
        return "0" + bin(num)[2:].zfill(length-1)
    else:
        bin_num = num + 2**length
        return "1" + bin(bin_num)[3:].zfill(length-1)
def mint(bin_num):
    if not type(bin_num) == str:
        raise ValueError("bin_num must be a string, got " +  str(type(bin_num)) + " instead (" + str(bin_num) + ")")
    length = len(bin_num)
    num = 0
    bin_num = bin_num[::-1]
    for i, bit in enumerate(bin_num):
        if i == length - 1:
            if bit == "1":
                num -= 2**i
        else:
            if bit == "1":
                num += 2**i
    return num

def set_flag(flags, bit, pos):
    return flags[:pos] + bit + flags[pos+1:]

def check_flag(flags, pos):
    return flags[pos] == "1"
        
    
def test_mint():
    assert mint("0000000000000001") == 1
    assert mint("1111111111111111") == -1
    assert mint("0000000000000010") == 2
    assert mint("1111111111111110") == -2
    assert mint("0000000000000100") == 4
    assert mint("1111111111111100") == -4
    assert mint("0000000000001000") == 8
    assert mint("1111111111111000") == -8
    assert mint("0000000000010000") == 16
    assert mint("1111111111110000") == -16
    assert mint("1111000000000000") == -4096
    assert mint("0010000000000000") == 8192
    assert mint("001") == 1
    assert mint("111") == -1
    assert mint("0010") == 2
    assert mint("1110") == -2
    assert mint("00000000000000000000000000000000") == 0
    assert mint("10000000000000000000000000000000") == -2147483648
    assert mint("01111111111111111111111111111111") == 2147483647
    assert mint("00001111") == 15
    assert mint("11110001") == -15

def test_mbin():
    assert mbin(1, 8) == "00000001"
    assert mbin(-1, 8) == "11111111"
    assert mbin(2, 8) == "00000010"
    assert mbin(-2, 8) == "11111110"
    assert mbin(4, 8) == "00000100"
    assert mbin(-4, 8) == "11111100"
    assert mbin(8, 8) == "00001000"
    assert mbin(-8, 8) == "11111000"
    assert mbin(16, 8) == "00010000"
    assert mbin(-16, 8) == "11110000"
    assert mbin(32, 8) == "00100000"
    assert mbin(-32, 8) == "11100000"
    assert mbin(64, 8) == "01000000"
    assert mbin(-64, 8) == "11000000"
    assert mbin(127, 8) == "01111111"
    assert mbin(-128, 8) == "10000000"
    try:
        mbin(128, 8)
        assert False
    except ValueError:
        assert True

    assert mbin(1, 16) == "0000000000000001"
    assert mbin(-1, 16) == "1111111111111111"
    assert mbin(2, 16) == "0000000000000010"
    assert mbin(-2, 16) == "1111111111111110"
    assert mbin(4, 16) == "0000000000000100"
    assert mbin(-4, 16) == "1111111111111100"
    assert mbin(8, 16) == "0000000000001000"
    assert mbin(-8, 16) == "1111111111111000"
    assert mbin(16, 16) == "0000000000010000"
    assert mbin(-16, 16) == "1111111111110000"
    assert mbin(32, 16) == "0000000000100000"
    assert mbin(-32, 16) == "1111111111100000"
    assert mbin(64, 16) == "0000000001000000"
    assert mbin(-64, 16) == "1111111111000000"
    assert mbin(128, 16) == "0000000010000000"
    assert mbin(-128, 16) == "1111111110000000"
    assert mbin(32767, 16) == "0111111111111111"
    assert mbin(-32768, 16) == "1000000000000000"
    assert mbin(283, 16) == "0000000100011011"
    assert mbin(-2378, 16) == "1111011010110110"
    try:
        mbin(32768, 16)
        assert False
    except ValueError:
        assert True
    
    assert mbin(1, 32) == "00000000000000000000000000000001"
    assert mbin(-1, 32) == "11111111111111111111111111111111"
    assert mbin(2, 32) == "00000000000000000000000000000010"
    assert mbin(-2, 32) == "11111111111111111111111111111110"
    assert mbin(4, 32) == "00000000000000000000000000000100"
    assert mbin(-4, 32) == "11111111111111111111111111111100"
    assert mbin(8, 32) == "00000000000000000000000000001000"
    assert mbin(-8, 32) == "11111111111111111111111111111000"
    assert mbin(16, 32) == "00000000000000000000000000010000"
    assert mbin(-16, 32) == "11111111111111111111111111110000"
    assert mbin(32, 32) == "00000000000000000000000000100000"
    assert mbin(-32, 32) == "11111111111111111111111111100000"
    assert mbin(64, 32) == "00000000000000000000000001000000"
    assert mbin(-64, 32) == "11111111111111111111111111000000"
    assert mbin(128, 32) == "00000000000000000000000010000000"
    assert mbin(-128, 32) == "11111111111111111111111110000000"
    assert mbin(2147483647, 32) == "01111111111111111111111111111111"
    assert mbin(-2147483648, 32) == "10000000000000000000000000000000"
    try:
        mbin(2147483648, 32)
        assert False
    except ValueError:
        assert True

    




if __name__ == "__main__":
    test_mint()
    test_mbin()
    print("binary_lib.py is correct")
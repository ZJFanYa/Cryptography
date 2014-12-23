import sys
import math

def checkParam(paramsNum, arguments):
    if (paramsNum != 5):
        print "There is wrong number of parameters. Main string was entered incorrectly."
        return False
    
    if(sys.argv[4] != "-c" and sys.argv[4] != "-d"):
        print "Wrong operation"
        return False
    
    return True
	
def PrintStart():
    print "This programme encodes and decodes the plaintext according\
        to AES-128 or Rijndael algorithm "
    print "Main string should be in a such way: "
    print "[source file name] [key file name] [result file name] [encode or decode]"
    print "	source file name - file with the plain text"
    print "	key file name - file with the text of key for algorithm"
    print "	result file name - file with the result of encryption"
    print " encode or decode "
    print "		""-c"" - encode the plain text according to AES-128 algorithm"
    print "		""-d"" - decode the cipher text according to AES-128 algorithm"
	
def mulBy2(symbol):
    if(symbol < 0x80):
        symbol = symbol * 2
    else:
        symbol = (((symbol * 2) ^ 0x1b) % 0x100)
    return symbol
		
def mulBy3(symbol):
    return mulBy2(symbol) ^ symbol
	
def mulBy4(symbol):
    return mulBy2(mulBy2(symbol))
	
def mulBy8(symbol):
    return mulBy2(mulBy4(symbol))
	
def mulBy09(symbol):
    return mulBy8(symbol) ^ symbol

def mulBy0b(symbol):
    return mulBy8(symbol) ^ mulBy2(symbol) ^ symbol
	
def mulBy0d(symbol):
    return mulBy8(symbol) ^ mulBy4(symbol) ^ symbol
	
def mulBy0e(symbol):
    return mulBy8(symbol) ^ mulBy4(symbol) ^ mulBy2(symbol)
				
def SubBytes(array, inverse):
    if not inverse:
        Sbox = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
        ]
		
        for i in range(4):
            array[i] = Sbox[array[i]]
			
    else:
        InvSbox = [
            0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
            0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
            0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
            0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
            0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
            0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
            0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
            0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
            0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
            0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
            0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
            0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
            0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
            0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
            0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
            0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
        ]
		
        for i in range(4):
            array[i] = InvSbox[array[i]]
    return array
	
def KeyExpansion(key, inverse):
    RCon = []
    for i in range(4):
        RCon.append([])
        for j in range(10):
            RCon[i].append([])
				
    RCon[0] = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    for i in range(1, 4):
        for j in range(10):
            RCon[i][j] = 0x00
		
    KeySchedule =[]
    LastColumn = []
    for i in range(4):
        LastColumn.append([])
    for i in range(4):
        KeySchedule.append([])
        for j in range(11 * 4):
            KeySchedule[i].append([])
			
    for i in range(4):
        for j in range(4):
            KeySchedule[j][i] = ord(key[j + 4 * i])
			
    for i in range(4, 11 * 4):
        if not (i % 4):
            for j in range(3):
                LastColumn[j] = KeySchedule[j + 1][i - 1]
            LastColumn[3] = KeySchedule[0][i - 1]
			
            LastColumn = SubBytes(LastColumn, False)
			
            for j in range(4):
                KeySchedule[j][i] = KeySchedule[j][i - 4] ^ LastColumn[j] ^\
                    RCon[j][i / 4 - 1]
		
        else:
            for j in range(4):
                KeySchedule[j][i] = KeySchedule[j][i - 4] ^ KeySchedule[j][i - 1]
				
    return KeySchedule
	
def ShiftRows(array, inverse):
    if not inverse:
        for i in range(4):
            for j in range(i):
                tempValue = array[i][0]
                for m in range(3):
                    array[i][m] = array[i][m + 1]
                array[i][3] = tempValue
				
    else:
        for i in range(4):
            for j in range(i):
                tempValue = array[i][3]
                for m in range(3, 0, -1):
                    array[i][m] = array[i][m - 1]
                array[i][0] = tempValue
			
    return array

def MixColumns(array, inverse):
    mixColumnedArr = []
    for i in range(4):
        mixColumnedArr.append([])
        for j in range(4):
            mixColumnedArr[i].append([])
    
    if not inverse:
        for i in range(4):
            mixColumnedArr[0][i] = mulBy2(array[0][i]) ^ mulBy3(array[1][i]) ^\
                array[2][i] ^ array[3][i]
            mixColumnedArr[1][i] = array[0][i] ^ mulBy2(array[1][i]) ^\
                mulBy3(array[2][i]) ^ array[3][i]
            mixColumnedArr[2][i] = array[0][i] ^ array[1][i] ^\
                mulBy2(array[2][i]) ^ mulBy3(array[3][i])
            mixColumnedArr[3][i] = mulBy3(array[0][i]) ^ array[1][i] ^\
                array[2][i] ^ mulBy2(array[3][i])
	
    else:
        for i in range(4):
            mixColumnedArr[0][i] = mulBy0e(array[0][i]) ^ mulBy0b(array[1][i]) ^\
                mulBy0d(array[2][i]) ^ mulBy09(array[3][i])
            mixColumnedArr[1][i] = mulBy09(array[0][i]) ^ mulBy0e(array[1][i]) ^\
                mulBy0b(array[2][i]) ^ mulBy0d(array[3][i])
            mixColumnedArr[2][i] = mulBy0d(array[0][i]) ^ mulBy09(array[1][i]) ^\
                mulBy0e(array[2][i]) ^ mulBy0b(array[3][i])
            mixColumnedArr[3][i] = mulBy0b(array[0][i]) ^ mulBy0d(array[1][i]) ^\
                mulBy09(array[2][i]) ^ mulBy0e(array[3][i])
		
    return mixColumnedArr
	
def AddAroundKey(array, RoundKey, cipherRound, inverse):
    if not inverse:
        for i in range(4):
            for j in range(4):
                array[i][j] = array[i][j] ^ RoundKey[i][cipherRound * 4 + j]
				
    else:
        for i in range(4):
            for j in range(4):
                array[i][j] = array[i][j] ^ RoundKey[i][(10 - cipherRound) * 4 + j]

    return array

def AESCoding(plainText, key, inverse):
    plainTextLen = len(plainText)
    keyLen = len(key)
    if not plainTextLen:
        print "The plain text file is empty. Error!"
        sys.exit(-1)

    if not keyLen:
        print "The key text file is empty. Error!"
        sys.exit(-1)
		
    elif (keyLen > 16):
        print "Only the first 16 symbols of the key will be used\
            as a key. Key in the AES algorithm consists of 16 symbols!"
		
    elif (keyLen < 16):
        print "Key in the AES algorithm consists of 16 symbols! \
            Deficient symbols will be filled '01'"
        while(keyLen != 16):
            key = key + chr(0x01)
            keyLen = keyLen + 1
		
    cipherRound = 0

    if not plainTextLen % 0x10:
        stateBlocksNum = int(plainTextLen / 0x10)

        state = []
        for i in range(stateBlocksNum):
            state.append([])
            for j in range(4):
                state[i].append([])
                for m in range(4):
                    state[i][j].append(ord(plainText[j + 4 * m + 16 * i]))
						
    else:
        stateBlocksNum = plainTextLen / 0x10 + 1
		
        state = []
        for i in range(stateBlocksNum):
            state.append([])
            for j in range(4):
                state[i].append([])
                for m in range(4):
                    state[i][j].append([])
						
        for i in range(plainTextLen):
            state[i / 0x10][i % 4][(i % 0x10) / 4] = ord(plainText[i])
				
        for i in range(plainTextLen, stateBlocksNum * 0x10 - 1):
            state[i / 0x10][i % 4][(i % 0x10) / 4] = 0
				
        state[stateBlocksNum - 1][3][3] = 0x01

    RoundKey = KeyExpansion(key, inverse)
					
    for i in range(stateBlocksNum):
        state[i] = AddAroundKey(state[i], RoundKey, cipherRound, inverse)
		
    for i in range(9):
        cipherRound = cipherRound + 1
        for i in range(stateBlocksNum):
            for j in range(4):
                state[i][j] = SubBytes(state[i][j], inverse)
				
        for i in range(stateBlocksNum):
            state[i] = ShiftRows(state[i], inverse)
			
        if not inverse:
            for i in range(stateBlocksNum):
                state[i] = MixColumns(state[i], inverse)
					
            for i in range(stateBlocksNum):
                state[i] = AddAroundKey(state[i], RoundKey, cipherRound, inverse)
					
        else:
            for i in range(stateBlocksNum):
                state[i] = AddAroundKey(state[i], RoundKey, cipherRound, inverse)
			
            for i in range(stateBlocksNum):
                state[i] = MixColumns(state[i], inverse)

    cipherRound = cipherRound + 1
    for i in range(stateBlocksNum):
        for j in range(4):
            state[i][j] = SubBytes(state[i][j], inverse)
				
    for i in range(stateBlocksNum):
        state[i] = ShiftRows(state[i], inverse)

    for i in range(stateBlocksNum):
        state[i] = AddAroundKey(state[i], RoundKey, cipherRound, inverse)

    result = ""
    for i in range(stateBlocksNum * 0x10):
        result = result + chr(state[i / 0x10][i % 4][(i % 16) / 4])
		
    if inverse:
        if ord(result[len(result) - 1]) == 0x01:
            resLength = len(result) - 1
            pointer = len(result) - 2
            while ord(result[pointer]) == 0x00:
                pointer = pointer - 1
                resLength = resLength - 1
            resCopy = ""
            for i in range(resLength):
                resCopy = resCopy + result[i]
            return resCopy

    return result
        
def main():
    paramsNum = len(sys.argv)
    if not checkParam(paramsNum, sys.argv):
        sys.exit(-1)
		
    sourceFileName = sys.argv[1]
    keyFileName = sys.argv[2]
    destinFileName = sys.argv[3]
    operation = sys.argv[4]

    PrintStart()

    with open(sourceFileName, 'rb') as sourceFile:
        plainText = sourceFile.read()
		
    with open(keyFileName, 'rb') as keyFile:
        key = keyFile.read()

    if(operation == "-c"):
        inverse = False
    else:
        inverse = True

    result = AESCoding(plainText, key, inverse)			
	
    with open(destinFileName, 'wb') as resFile:
        resFile.write(result)
	
if __name__ == "__main__":
    main()

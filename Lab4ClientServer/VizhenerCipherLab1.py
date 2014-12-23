import sys

def checkParam(paramsNum, arguments):
    if (paramsNum != 5):
        print "There is wrong number of parameters.\
            Main string was entered incorrectly."
        return False
    if(sys.argv[4] != "-c" and sys.argv[4] != "-d"):
        print "Wrong operation"
        return False
    return True
	
def PrintStart():
    print "This programme encodes and decodes the plaintext\
        according to Vizhener encryption algorithm"
    print "Main string should be in a such way: "
    print "[source file name] [key file name] [result file name] [encode or decode]"
    print "	source file name - file with the plain text"
    print "	key file name - file with the text of key for algorithm"
    print "	result file name - file with the result of encryption"
    print " encode or decode "
    print "		""-c"" - encode the plain text according to Vizhener algorithm"
    print "		""-d"" - decode the cipher text according to Vizhener algorithm"
	
def encrypt(plainText, cipherKey):
    alphabet = ""
    for i in range(256):
        alphabet = alphabet + chr(i)
        
    plainTextLen = len(plainText)
    keyLen = len(cipherKey)
    shift = keyLen
        
    while(keyLen < plainTextLen):
        cipherKey = cipherKey + cipherKey[-shift]
        keyLen = keyLen + 1
		
    result = ""
    for index, symbol in enumerate(plainText):
        result = result + (alphabet[(alphabet.find(plainText[index])\
                + alphabet.find(cipherKey[index]) + 1) % len(alphabet)])

    return result

def decrypt(plainText, cipherKey):
    alphabet = ""
    for i in range(256):
        alphabet = alphabet + chr(i)
        
    plainTextLen = len(plainText)
    keyLen = len(cipherKey)
    shift = keyLen
        
    while(keyLen < plainTextLen):
        cipherKey = cipherKey + cipherKey[-shift]
        keyLen = keyLen + 1
		
    result = ""
    for index, symbol in enumerate(plainText):
        result = result + (alphabet[(alphabet.find(plainText[index])\
                - alphabet.find(cipherKey[index]) - 1) % len(alphabet)])

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
		
    if not plainText:
        print "The plain text file is empty. Error!"
        sys.exit(-1)
        
    with open(keyFileName, 'rb') as keyFile:
        key = keyFile.read()
    if not key:
        print "The key text file is empty. Error!"
        sys.exit(-1)

    if (operation == "-c"):
        result = encrypt(plainText, key)
     
    else:
        result = decrypt(plainText, key)

    with open(destinFileName, 'wb') as resFile:
        resFile.write(result)

if __name__ == "__main__":
    main()
	
	
	

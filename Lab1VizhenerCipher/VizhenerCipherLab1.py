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
	
def main():
    paramsNum = len(sys.argv)
    if not checkParam(paramsNum, sys.argv):
        sys.exit(-1)
		
    sourceFileName = sys.argv[1]
    keyFileName = sys.argv[2]
    destinFileName = sys.argv[3]
    operation = sys.argv[4]

    PrintStart()
    alphabet = ""
    for i in range(256):
        alphabet = alphabet + chr(i)

    with open(sourceFileName, 'r') as sourceFile:
        plainText = sourceFile.read()
		
    plainTextLen = len(plainText)
    if not plainText:
        print "The plain text file is empty. Error!"
        sys.exit(-1)
		
    with open(keyFileName, 'r') as keyFile:
        key = keyFile.read()
	
    keyLen = len(key)
    if not key:
        print "The key text file is empty. Error!"
        sys.exit(-1)
		
    while(keyLen < plainTextLen):
        key = key + key[-4]
        keyLen = keyLen + 1
		
    with open(destinFileName, 'w') as resFile:
        if (operation == "-c"):
            for index, symbol in enumerate(plainText):
                resFile.write(alphabet[(alphabet.find(plainText[index])\
                    + alphabet.find(key[index]) + 1) % len(alphabet)])
				
        else:
            for index, symbol in enumerate(plainText):
                resFile.write(alphabet[(alphabet.find(plainText[index])\
                    - alphabet.find(key[index]) - 1) % len(alphabet)])

if __name__ == "__main__":
    main()
	
	
	
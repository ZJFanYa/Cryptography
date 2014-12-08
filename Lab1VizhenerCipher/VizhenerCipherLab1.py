import sys

def checkParam(paramsNum, arguments):
	if (paramsNum != 5):
		print "There is wrong number of parameters. Main string was entered incorrectly."
		return False

	if(sys.argv[4] != "-c" and sys.argv[4] != "-d"):
		print "Wrong operation"
		return False

	return True
	
def PrintStart():
	print "This programme encodes and decodes the plaintext according to Vizhener encryption algorithm"
	print "Main string should be in a such way: "
	print "[source file name] [key file name] [result file name] [encode or decode]"
	print "	source file name - file with the plain text"
	print "	key file name - file with the text of key for algorithm"
	print "	result file name - file with the result of encryption"
	print " encode or decode "
	print "		""-c"" - encode the plain text according to Vizhener algorithm"
	print "		""-d"" - decode the cipher text according to Vizhener algorithm"
	
paramsNum = len(sys.argv)
if not checkParam(paramsNum, sys.argv):
	sys.exit(-1)
	
sourceFileName = sys.argv[1]
keyFileName = sys.argv[2]
destinFileName = sys.argv[3]
operation = sys.argv[4]

PrintStart()
alphabet = "abcdefghijklmnopqrstuvwxyz"

sourceFile = open(sourceFileName, 'r')
	
plainText = sourceFile.read()
plainTextLen = len(plainText)
if not plainTextLen:
	print "The plain text file is empty. Error!"
	sourceFile.close()
	sys.exit(-1)

for i in range(0, plainTextLen):
	if(plainText[i] < 'a' or plainText[i] > 'z'):
		print "In the plaintext there are symbols that are not in English alphabet. Error!"
		sourceFile.close()
		sys.exit(-1)
		
sourceFile.close()
	
keyFile = open(keyFileName, 'r')
key = keyFile.read()
keyLen = len(key)
if not keyLen:
	print "The key text file is empty. Error!"
	sourceFile.close()
	sys.exit(-1)
	
for i in range(0, keyLen):
	if(key[i] < 'a' or key[i] > 'z'):
		print "In the text of key for algorithm there are symbols that are not in English alphabet. Error!"
		keyFile.close()
		sys.exit(-1)
keyFile.close()
	
while(keyLen < plainTextLen):
	key = key + key[-4]
	keyLen = keyLen + 1
	
resFile = open(destinFileName, 'w')
	
if (operation == "-c"):
	for i in range(0, plainTextLen):
		resFile.write(alphabet[(alphabet.find(plainText[i]) + alphabet.find(key[i]) + 1) % len(alphabet)])
		
else:
	for i in range(0, plainTextLen):
		resFile.write(alphabet[(alphabet.find(plainText[i]) - alphabet.find(key[i]) - 1) % len(alphabet)])
	
resFile.close()
	
	
	
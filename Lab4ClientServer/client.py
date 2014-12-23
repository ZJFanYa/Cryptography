import sys
import math
import VizhenerCipherLab1
import AESLab2
import StegoLSBLab3
import socket

def checkParam(paramsNum, arguments):
    if (paramsNum != 6):
        print "There is wrong number of parameters. Main string was entered incorrectly."
        return False
    
    return True
	
def PrintStart():
    print "This programme is client application which encrypts\
        the data in a such way that server never can decrypt this :)"
    print "Main string should be in a such way: "
    print "[name of .py file] [source file name] [key file name] [secondKey file name] [picture file name]\
        [file for cheking result]"
    print "	source file name - file with the plain text"
    print "	key file name - file with the text of key for Vizhener algorithm"
    print "     secondKey file name - file with the text of key for AES-128 algorithm"
    print "	picture file name - file with the image for keeping of data"
	
def main():
    paramsNum = len(sys.argv)
    if not checkParam(paramsNum, sys.argv):
        sys.exit(-1)
		
    sourceFileName = sys.argv[1]
    keyFileName = sys.argv[2]
    secondKeyFileName = sys.argv[3]
    pictureFileName = sys.argv[4]
    chkResFile = sys.argv[5]

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
		
    with open(secondKeyFileName, 'rb') as secKeyFile:
        secKey = secKeyFile.read()

    if not secKey:
        print "The second key text file is empty. Error!"
        sys.exit(-1)

    vizhResult = VizhenerCipherLab1.encrypt(plainText, key)
    AESResult = AESLab2.AESCoding(vizhResult, secKey, False)
    craftyPic = StegoLSBLab3.encrypt(pictureFileName, AESResult)
    craftyPic.save(pictureFileName, "BMP")
	
    with open(pictureFileName, 'rb') as picFile:
        picture = picFile.read()
    
    mySocket = socket.socket()
    mySocket.connect(('localhost', 1408))
    dataNum = mySocket.send(picture)
    mySocket.close()

    print("Data has sent successfully!")
    sourceText = ""
    newSocket = socket.socket()
    newSocket.connect(('localhost', 1408))
    
    while(True):
        newData = newSocket.recv(1024)
        if not newData:
            break
        sourceText = sourceText + newData
    newSocket.close()

    with open(chkResFile, 'wb') as chkRes:
        chkRes.write(sourceText)
    
if __name__ == "__main__":
    main()

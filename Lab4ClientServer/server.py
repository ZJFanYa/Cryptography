import sys
import math
import VizhenerCipherLab1
import AESLab2
import StegoLSBLab3
import socket

def checkParam(paramsNum, arguments):
    if (paramsNum != 4):
        print "There is wrong number of parameters. Main string was entered incorrectly."
        return False
    
    return True
	
def PrintStart():
    print "This programme is server application which decrypts\
        any cipher that humanity thought :)"
    print "Main string should be in a such way: "
    print "[name of .py file] [name of got picture] [key file name] [secondKey file name]"
    print "     name of .py file - file of server application"
    print "     name of got picture - file for picture from client with the data"
    print "	key file name - file with the text of key for Vizhener algorithm"
    print "     secondKey file name - file with the text of key for AES-128 algorithm"
	
def main():
    paramsNum = len(sys.argv)
    if not checkParam(paramsNum, sys.argv):
        sys.exit(-1)
		
    pictureFileName = sys.argv[1]
    keyFileName = sys.argv[2]
    secondKeyFileName = sys.argv[3]

    PrintStart()
        
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

    mySocket = socket.socket()
    mySocket.bind(('', 1408))
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    smartPic = ""
    round = 0
    while True:
        newData = conn.recv(1024)
        if not newData:
            break
        smartPic = smartPic + newData

    print "Data has got successfully!"
    conn.close()
    with open(pictureFileName, 'wb') as pictureFile:
        pictureFile.write(smartPic)
	
    stegoRes = StegoLSBLab3.decrypt(pictureFileName)
    AESResult = AESLab2.AESCoding(stegoRes, secKey, True)
    vizhResult = VizhenerCipherLab1.decrypt(AESResult, key)

    conn, addr = mySocket.accept()
    conn.send(vizhResult) 

if __name__ == "__main__":
    main()

import sys
import math
from PIL import Image, ImageDraw

def checkParam(paramsNum, arguments):
    if (paramsNum != 4 and paramsNum != 3):
        print "There is wrong number of parameters. Main string was entered incorrectly."
        return False

    return True
	
def PrintStart():
    print "This programme encodes and decodes the plaintext in the\
        image according to LSB algorithm"
    print "If you want hide the text in the picture you should write 4 parameters:"
    print "[name of .py file] [source image file name] [plaintext file name] [result image file name]"
    print "	source file name - file with the source image"
    print "	plaintext file name - file with the text which is hidden"
    print "	result file name - image file with the result of encryption"
    print "If you should fins the text which is hidden in the picture\
        you should use 3 parameters:"
    print "[name of .py file] [name of image file with the hidden text] [name of file with the text]"

def encrypt(sourcePicture, plainText):
    imagine = Image.open(sourcePicture)
    draw = ImageDraw.Draw(imagine)
    width = imagine.size[0]
    height = imagine.size[1]
    pixels = imagine.load()
		
    widthIndex = 0
    heightIndex = 0	
			
    plainTextLen = len(plainText)
    if not plainText:
        print "The plain text file is empty. Error!"
        sys.exit(-1)
		
    hiddenBits = []
    for i in range((plainTextLen + 4) * 3):         
        hiddenBits.append([])

    hiddenBits[0] = plainTextLen >> 30                        
    hiddenBits[1] = (plainTextLen & 0b111000000000000000000000000000) >> 27    
    hiddenBits[2] = (plainTextLen & 0b111000000000000000000000000) >> 24
    hiddenBits[3] = (plainTextLen & 0b110000000000000000000000) >> 22
    hiddenBits[4] = (plainTextLen & 0b1110000000000000000000) >> 19
    hiddenBits[5] = (plainTextLen & 0b1110000000000000000) >> 16		
    hiddenBits[6] = (plainTextLen & 0b1100000000000000) >> 14                        
    hiddenBits[7] = (plainTextLen & 0b11100000000000) >> 11    
    hiddenBits[8] = (plainTextLen & 0b11100000000) >> 8
    hiddenBits[9] = (plainTextLen & 0b11000000) >> 6
    hiddenBits[10] = (plainTextLen & 0b111000) >> 3
    hiddenBits[11] = plainTextLen & 0b111
			
    for index, symbol in enumerate(plainText):
        hiddenBits[(index + 4) * 3] = ord(symbol) >> 6                      
        hiddenBits[(index + 4) * 3 + 1] = (ord(symbol) & 0b00111000) >> 3   
        hiddenBits[(index + 4) * 3 + 2] = ord(symbol) & 0b00000111           
			
    for i in range(plainTextLen + 4):
        if heightIndex >= height:
            heightIndex = 0
            widthIndex = widthIndex + 1
            if widthIndex >= width:
                print "Content of file with a picture is over,\
                    we can't record new data to the picture"
                sys.exit(-1)
			
        pixelNow = pixels[widthIndex, heightIndex]                           
        rSegm = ((pixelNow[0] >> 2) << 2) + hiddenBits[i * 3]
        gSegm = ((pixelNow[1] >> 3) << 3) + hiddenBits[i * 3 + 1]
       	bSegm = ((pixelNow[2] >> 3) << 3) + hiddenBits[i * 3 + 2]
        imagine.putpixel((widthIndex, heightIndex), (rSegm, gSegm, bSegm))   
        heightIndex = heightIndex + 1

    return imagine

def decrypt(picture):
    imagine = Image.open(picture)
    draw = ImageDraw.Draw(imagine)
    width = imagine.size[0]
    height = imagine.size[1]
    pixels = imagine.load()
    text = ""
		
    widthIndex = 0
    heightIndex = 4

    Byte = []
    for i in range(4):
        Byte.append([])
        firPart = pixels[0, i][0] & 0b00000011                       
        secPart = pixels[0, i][1] & 0b00000111
        thirPart = pixels[0, i][2] & 0b00000111
        Byte[i] = (firPart << 6) + (secPart << 3) + thirPart

    textVolume = 0
    for i in range(4):
        textVolume = textVolume + (Byte[i] << ((3 - i) * 8))
    	
    for i in range(textVolume):
        if heightIndex >= height:
            heightIndex = 0
            widthIndex = widthIndex + 1
		     
        firPart = pixels[widthIndex, heightIndex][0] & 0b00000011
        secPart = pixels[widthIndex, heightIndex][1] & 0b00000111
        thirPart = pixels[widthIndex, heightIndex][2] & 0b00000111
        symbol = chr((firPart << 6) + (secPart << 3) + thirPart)
        heightIndex = heightIndex + 1
        text = text + symbol

    return text
    
def main():
    paramsNum = len(sys.argv)
    if not checkParam(paramsNum, sys.argv):
        sys.exit(-1)
		
    PrintStart()
	
    sourceFileName = sys.argv[1]
    plainTextFileName = sys.argv[2]
    operation = sys.argv[3]
    
    if operation == "-c":
        with open(plainTextFileName, 'rb') as plainTextFile:
            plainText = plainTextFile.read()
        cipherImage = encrypt(sourceFileName, plainText)
        cipherImage.save(sourceFileName, "BMP")
    else:
        text = decrypt(sourceFileName)        
        with open(plainTextFileName, 'wb') as resFile:
            resFile.write(text)
	
if __name__ == "__main__":
    main()
		
		

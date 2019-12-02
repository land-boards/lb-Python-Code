inputFile = open('5-InputT.txt', 'r')
inputFile = str(inputFile.read())
length = len(inputFile)
box = [0 for x in xrange(1000000)] #1000x1000 Box to fill with lengths per space
dellength = 0
inpt = ["" for x in xrange(length)]
for x in xrange(length):
    inpt[x] = inputFile[x]
# print(length)
# print(inpt)
deleting = True
x = 0
ctr = 0

notAtEnd = True

while(length >= x+1):
    currLetter = inpt[x]
    if((currLetter == 'A') or (currLetter == 'a')):
        inpt.pop(x)
        # print("Popped: ", end =" ")
        # print(x)
    else:
        x += 1
    length = len(inpt)
    # print(length)
    # print(x)
    if(x >= length):
        notAtEnd == False



while(ctr <= 15000000):
    currLetter = inpt[x]
    nextLetter = inpt[x+1]
    #print(currLetter)
    #print(nextLetter)
    if(currLetter == "a"):
        if(nextLetter == "A"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "b"):
        if(nextLetter == "B"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "c"):
        if(nextLetter == "C"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "d"):
        if(nextLetter == "D"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "e"):
        if(nextLetter == "E"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "f"):
        if(nextLetter == "F"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "g"):
        if(nextLetter == "G"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "h"):
        if(nextLetter == "H"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "i"):
        if(nextLetter == "I"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1 
    elif(currLetter == "j"):
        if(nextLetter == "J"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "k"):
        if(nextLetter == "K"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "l"):
        if(nextLetter == "L"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "m"):
        if(nextLetter == "M"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "n"):
        if(nextLetter == "N"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "o"):
        if(nextLetter == "O"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "p"):
        if(nextLetter == "P"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "q"):
        if(nextLetter == "Q"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "r"):
        if(nextLetter == "R"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "s"):
        if(nextLetter == "S"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "t"):
        if(nextLetter == "T"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "u"):
        if(nextLetter == "U"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "v"):
        if(nextLetter == "V"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "w"):
        if(nextLetter == "W"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "x"):
        if(nextLetter == "X"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "y"):
        if(nextLetter == "Y"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "z"):
        if(nextLetter == "Z"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "A"):
        if(nextLetter == "a"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "B"):
        if(nextLetter == "b"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "C"):
        if(nextLetter == "c"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "D"):
        if(nextLetter == "d"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "E"):
        if(nextLetter == "e"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "F"):
        if(nextLetter == "f"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "G"):
        if(nextLetter == "g"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "H"):
        if(nextLetter == "h"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "I"):
        if(nextLetter == "i"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "J"):
        if(nextLetter == "j"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "K"):
        if(nextLetter == "k"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "L"):
        if(nextLetter == "l"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "M"):
        if(nextLetter == "m"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "N"):
        if(nextLetter == "n"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "O"):
        if(nextLetter == "o"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "P"):
        if(nextLetter == "p"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "Q"):
        if(nextLetter == "q"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "R"):
        if(nextLetter == "r"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "S"):
        if(nextLetter == "s"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "T"):
        if(nextLetter == "t"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "U"):
        if(nextLetter == "u"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "V"):
        if(nextLetter == "v"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "W"):
        if(nextLetter == "w"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "X"):
        if(nextLetter == "x"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "Y"):
        if(nextLetter == "y"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1
    elif(currLetter == "Z"):
        if(nextLetter == "z"):
            inpt.pop(x)
            inpt.pop(x)
            length = length - 2
            x -= 1

    x = x+1
    ctr += 1
    if(x >= length-1):
        x = 0
    #print(inpt)
    #print(".", end =" ")

#print(inpt)
print(len(inpt))






















    

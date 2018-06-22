import cmath
import numpy as np
from matplotlib import pyplot as plt
import math

def pgm_to_mat(s):
    fread = open(s, 'r')
    b = fread.read()
    lines = b.split("\n")
    print(lines[:4])
    n = lines[2].split(" ")
    row = np.int16(n[0])
    col = np.int16(n[1])
    a = np.zeros((row, col), dtype=np.int16)
    ind = 4
    for i in range(row):
        for j in range(col):
            a[i][j] = np.int16(lines[ind])
            ind += 1
    return a

def embed(cover,secret,pos,skip):
    file = open("out2.txt", 'w')
    coverMatrix=pgm_to_mat(cover)
    secretMatrix=pgm_to_mat(secret)
    stegoMatrix=np.zeros(np.shape(coverMatrix), dtype=np.complex_)
    np.copyto(stegoMatrix,coverMatrix)
    index=0
    for a in range(0,len(secretMatrix)):
        for b in range(0,len(secretMatrix)):
            binaryNumber=np.binary_repr(secretMatrix[a][b])
            file.write(str(secretMatrix[a][b])+"\t"+str(int(binaryNumber,2))+"\n")
            for digit in binaryNumber:
                coln=int(index/len(coverMatrix))
                rown=int(index%len(coverMatrix))
                coverNumber=np.binary_repr(int(coverMatrix[coln][rown]))
                coverNumber=coverNumber[:-1]+digit

                for a in range(len(coverNumber),8):
                    coverNumber="0"+coverNumber
                stegoMatrix[coln][rown]=int(coverNumber,2)
                index+=skip
    return stegoMatrix

def getSecret(stegoMatrix,pos,skip):
    index=True
    file = open('out.txt', 'w')
    secret=int(math.sqrt(len(stegoMatrix)*len(stegoMatrix)/(8*skip)))
    dummy=""
    secretMatrix=np.zeros((secret,secret),dtype=np.complex_)
    for a in range(0,len(stegoMatrix)):
        for b in range(0,len(stegoMatrix)):
            c=str(np.binary_repr(int(stegoMatrix[a][b])))
            #print(c)
            if(index):
                dummy+=c[len(c)-1:]
                file.write(c[len(c)-1:]+ "\n")
            index=not index
    sindex=0
    for a in range(0,len(dummy),8):
        secretMatrix[int(sindex/secret)][int(sindex%secret)]=int(dummy[a:a+8],2)
        sindex+=1
    return secretMatrix

plt.figure(1)
stegoMatrix=embed("images/f16.pgm","secrets/Hide0.5.pgm",0,2)
plt.imshow(stegoMatrix.astype(float),cmap="gray")
plt.show()
secretMatrix=getSecret(stegoMatrix,0,2)
plt.imshow(secretMatrix.astype(float),cmap="gray")
plt.show()
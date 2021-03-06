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
    file=open("out2.txt","w")
    coverMatrix=pgm_to_mat(cover)
    secretMatrix=pgm_to_mat(secret)
    stegoMatrix=np.zeros(np.shape(coverMatrix), dtype=np.complex_)
    np.copyto(stegoMatrix,coverMatrix)
    dummy=""
    for a in range(0,len(secretMatrix)):
        for b in range(0,len(secretMatrix)):
            dummy+=np.binary_repr(secretMatrix[a][b],width=8)
            file.write(str(int(np.binary_repr(secretMatrix[a][b],width=8),2))+"\n")
    index=0
    for a in range(0,len(stegoMatrix)*len(stegoMatrix),skip):
        #print(stegoMatrix[int(a/len(stegoMatrix))][int(a%len(stegoMatrix))],"\t",)
        #stegoMatrix[int(a/len(stegoMatrix))][int(a%len(stegoMatrix))]=int(stegoMatrix[int(a/len(stegoMatrix))][int(a%len(stegoMatrix))])^int(dummy[index])
        stegoMatrix[int(a / len(stegoMatrix))][int(a % len(stegoMatrix))] = ( int(coverMatrix[int(a / len(stegoMatrix))][int(a % len(stegoMatrix))]) & ~1) | int(dummy[index],2)
        index+=1
        #print(stegoMatrix[int(a/len(stegoMatrix))][int(a%len(stegoMatrix))])
    return stegoMatrix

def getSecret(stegoMatrix,pos,skip):
    index=True
    secret=int(math.sqrt(len(stegoMatrix)*len(stegoMatrix)/(8*skip)))
    dummy=""
    secretMatrix=np.zeros((secret,secret),dtype=np.complex_)
    for a in range(0,len(stegoMatrix)):
        for b in range(0,len(stegoMatrix)):
            c=np.binary_repr(int(stegoMatrix[a][b]))
            #print(c)
            if(index):
                dummy+=c[len(c)-1:]
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
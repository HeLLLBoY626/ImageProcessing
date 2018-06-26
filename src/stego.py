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
    file=open("in.txt","w")
    coverMatrix=pgm_to_mat(cover)
    secretMatrix=pgm_to_mat(secret)
    stegoMatrix=np.zeros(np.shape(coverMatrix), dtype=np.complex_)
    np.copyto(stegoMatrix,coverMatrix)
    dummy=""
    for a in range(0,len(secretMatrix)):
        for b in range(0,len(secretMatrix)):
            dummy+=np.binary_repr(secretMatrix[a][b],width=8)
            #file.write(np.binary_repr(secretMatrix[a][b],width=8)+"\n")
    index=0
    rskip=0
    if(skip<1):
        rskip=int(np.round(skip*10))
        skip=1
    for a in range(0,len(stegoMatrix)*len(stegoMatrix),skip):
        rown=int(a % len(stegoMatrix))
        coln=int(a / len(stegoMatrix))
        stegoMatrix[coln][rown] = ( int(coverMatrix[coln][rown]) & ~(1 << hash(coln,rown,pos) )) | (int(dummy[index],2) << hash(coln,rown,pos))
        index+=1
        file.write(np.binary_repr(int(stegoMatrix[coln][rown]),8)+"\t"+"\n")
    return stegoMatrix

def getSecret(stegoMatrix,pos,skip):
    file = open("out.txt", "w")
    index=0
    secret=int(math.sqrt(len(stegoMatrix)*len(stegoMatrix)/(8*skip)))
    dummy=""
    secretMatrix=np.zeros((secret,secret),dtype=np.complex_)
    rskip=0
    if (skip < 1):
        rskip = int(np.round(skip * 10))
        skip = 1
    for a in range(0,len(stegoMatrix)):
        for b in range(0,len(stegoMatrix)):
            c=np.binary_repr(int(stegoMatrix[a][b]),8)
            if(index%skip==0):
                dummy+=c[7-hash(a,b,pos)]
            file.write(c+"\t"+"\n")
            index+=1
    sindex=0
    for a in range(0,len(dummy),8):
        secretMatrix[int(sindex/secret)][int(sindex%secret)]=int(dummy[a:a+8],2)
        sindex+=1
    return secretMatrix

def hash(i,j,pos):
    if(pos<8):
        return pos
    if(pos==8):
        return (i+j)%8
    elif (pos==9):
        return (i*j)%8

plt.figure(1)
stegoMatrix=embed("images/tree.pgm","secrets/Hide0.5.pgm",4,2)
plt.imshow(stegoMatrix.astype(float),cmap="gray")
plt.show()
secretMatrix=getSecret(stegoMatrix,4,2)
plt.imshow(secretMatrix.astype(float),cmap="gray")
plt.show()
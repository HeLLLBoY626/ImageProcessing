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
    multiple=False
    coverMatrix=pgm_to_mat(cover)
    secretMatrix=pgm_to_mat(secret)
    stegoMatrix=np.zeros(np.shape(coverMatrix), dtype=np.complex_)
    np.copyto(stegoMatrix,coverMatrix)
    dummy=""
    if(skip<1):
        skip=1
        multiple=True
    for a in range(0,len(secretMatrix)):
        for b in range(0,len(secretMatrix)):
            dummy+=np.binary_repr(secretMatrix[a][b],width=8)
            #file.write(np.binary_repr(secretMatrix[a][b],width=8)+"\n")
    index=0
    for a in range(0,len(stegoMatrix)*len(stegoMatrix),skip):
        rown=int(a % len(stegoMatrix))
        coln=int(a / len(stegoMatrix))
        if(index>=len(dummy)):
            break
        stegoMatrix[coln][rown] = ( int(coverMatrix[coln][rown]) & ~(1 << hash(coln,rown,pos) )) | (int(dummy[index],2) << hash(coln,rown,pos))
        index += 1
        if(multiple):
            stegoMatrix[coln][rown] = (int(stegoMatrix[coln][rown]) & ~(1 << (3-hash(coln, rown, pos)))) | ( int(dummy[index], 2) << (3-hash(coln, rown, pos)))
            index += 1
        file.write(np.binary_repr(int(stegoMatrix[coln][rown]), 8) + "\n")
    return stegoMatrix

def getSecret(stegoMatrix,pos,skip,x=None):
    file = open("out.txt", "w")
    index=0
    if(x==None):
        secret=int(math.sqrt(len(stegoMatrix)*len(stegoMatrix)/(8*skip)))
    else:
        secret=x
    dummy=""
    multiple=False
    if(skip<1):
        skip=1
        multiple=True
    secretMatrix=np.zeros((secret,secret),dtype=np.complex_)
    for a in range(0,len(stegoMatrix)):
        for b in range(0,len(stegoMatrix)):
            c=np.binary_repr(int(stegoMatrix[a][b]),8)
            if(index%skip==0):
                dummy+=c[7-hash(a,b,pos)]
                if(multiple):
                    dummy += c[4+hash(a, b, pos)]
            file.write(c+"\t"+"\n")
            index+=1

    sindex=0
    for a in range(0,min(len(dummy),secret*secret*8),8):
        secretMatrix[int(sindex/secret)][int(sindex%secret)]=int(dummy[a:a+8],2)
        sindex+=1
    return secretMatrix

def hash(i,j,pos):
    if(pos<4):
        return pos
    elif(pos==4):
        return (i+j)%4
    else:
        return (i*j)%4

def PSNR(matrix,image):
    original=pgm_to_mat(image).astype(float)
    mse=0
    for a in range(0,len(matrix)):
        for b in range(0,len(matrix)):
            mse+=math.pow(original[a][b]-matrix[a][b],2)
    return 10*np.log10( (math.inf if (mse==0.0) else (math.pow(int(open(image, 'r').read().split("\n")[3]),2)/mse))*len(matrix)*len(matrix))

def IF(matrix,image):
    original=pgm_to_mat(image).astype(float)
    sum1=0
    sum2=0
    for a in range(0,len(matrix)):
        for b in range(0,len(matrix)):
            sum1+=math.pow(original[a][b]-matrix[a][b],2)
            sum2+=math.pow(original[a][b],2)
    return 1-sum1/sum2

plt.figure(1)
stegoMatrix=embed("images/f16.pgm","secrets/Hide0.5.pgm",2,1)
plt.imshow(stegoMatrix.astype(float),cmap="gray")
plt.show()
secretMatrix=getSecret(stegoMatrix,2,1,len(pgm_to_mat("secrets/Hide0.5.pgm")))
plt.imshow(secretMatrix.astype(float),cmap="gray")
plt.show()
print(PSNR(stegoMatrix.astype(float),"images/f16.pgm"))
print(IF(stegoMatrix.astype(float),"images/f16.pgm"))
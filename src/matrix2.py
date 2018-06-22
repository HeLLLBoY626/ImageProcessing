import cmath
import numpy as np
from matplotlib import pyplot as plt

from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean,rotate

def dft(n,normalize):
    matrix = np.zeros((n, n), dtype=np.complex_)
    identity = np.zeros((n, n), dtype=np.complex_)
    omega=cmath.exp(-2j*cmath.pi/n)
    factor=1
    for a in range(n):
        value=1
        for b in range(n):
            matrix[a][b]=value
            value=value*factor
            if normalize:
               matrix[a][b]=matrix[a][b]/cmath.sqrt(n)
            factor = factor * omega
    #for a in range(n):
        #print("\n")
        #for b in range(n):
            #print(matrix[a][b],end="\t")

    #print("\n")
    for a in range(n):
        for b in range(n):
            if a is b:
                identity[a][a]=1
    f_matrix=np.dot(np.dot(matrix.transpose(),identity),matrix)
    #for a in range(n):
        #print("\n")
        #for b in range(n):
            #print(f_matrix[a][b],end="\t")
    return f_matrix


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

def translate(matrix,x,y,crop,top,left):
    height=np.shape(matrix)[0] if crop else (np.shape(matrix)[0]+y)
    width = np.shape(matrix)[1] if crop else (np.shape(matrix)[1] + x)
    mShift=np.zeros((height,width),dtype=np.complex_)
    if (crop):
        if (top and left):
            for a in range(y, height):
                for b in range(x, width):
                    mShift[a][b] = matrix[a - y][b - x]
        if (top and not left):
            for a in range(y, height):
                for b in range(0,width-x):
                    mShift[a][b]=matrix[a][b+x]
        if (not top and left):
            for a in range(0, height - y):
                for b in range(x, width):
                    mShift[a][b] = matrix[a+y][b - x]
        if (not top and not left):
            for a in range(0, height - y):
                for b in range(0, width - x):
                    mShift[a][b] = matrix[a+y][b+x]
    else:
        if(top and left):
            for a in range(y,height):
                for b in range(x,width):
                    mShift[a][b]=matrix[a-y][b-x]
        if( top and not left):
            for a in range(y,height):
                for b in range(0,width-x):
                    mShift[a][b]=matrix[a-y][b]
        if (not top and left):
            for a in range(0, height-y):
                for b in range(x, width):
                    mShift[a][b] = matrix[a][b - x]
        if (not top and not left):
            for a in range(0, height-y):
                for b in range(0, width-x):
                    mShift[a][b] = matrix[a][b]
    return mShift

def histogram(matrix):
    plt.figure(1)
    plt.hist(matrix, bins="auto")
    plt.show()

def binary(matrix):
    biMatrix=np.zeros(np.shape(matrix),dtype=np.byte)
    for a in range(0,np.shape(matrix)[0]):
        for b in range(0,np.shape(matrix)[1]):
            biMatrix[a][b]=1 if matrix[a][b]>=127 else 0
    return biMatrix

def ceil(matrix):
    cMatrix=np.zeros(np.shape(matrix),dtype=np.int16)
    for a in range(0,np.shape(matrix)[0]):
        for b in range(0,np.shape(matrix)[1]):
            cMatrix[a][b]=np.ceil(matrix[a][b])
    return cMatrix

def reflect_vertical(matrix):
    midline=int(np.shape(matrix)[0]/2)
    for a in range(1,midline):
        for b in range(0,len(matrix)):
            temp=matrix[midline+a][b]
            matrix[midline+a][b]=matrix[midline-a][b]
            matrix[midline-a][b]=temp
    return matrix

def reflect_lateral(matrix):
    midline=int(np.shape(matrix)[1]/2)
    for b in range(1,midline):
        for a in range(0,len(matrix)):
            temp=matrix[a][midline+b]
            matrix[a][midline+b]=matrix[a][midline-b]
            matrix[a][midline-b]=temp
    return matrix

m=pgm_to_mat("images/tree.pgm")
print("height=\t"+str(np.shape(m)[0]))
print("width=\t"+str(np.shape(m)[1]))
#m=translate(m,50,50,False,True,True)
#m=rotate(m,10,True)
#m=resize(m,(256,256))
m=reflect_lateral(m)
plt.figure(1)
#m=binary(m)
plt.imshow(m.astype(float),cmap="gray")
plt.show()

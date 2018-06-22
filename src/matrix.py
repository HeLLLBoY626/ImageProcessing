import cmath
import numpy as np
from matplotlib import pyplot as plt


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

m=pgm_to_mat("images/tree.pgm")
'''dft_matrix=dft(len(m),False)
for a in range(len(m)):
    for b in range(len(m)):
        dft_matrix[a][b]=np.log10(abs(dft_matrix[a][b]))
print(type(dft_matrix))'''
t=np.fft.fft(m)
t=np.fft.fftshift(t)
t1=np.log10(abs(t))
plt.figure(1)
plt.imshow(t1,cmap="gray")
plt.show()

import numpy as np
from matplotlib import pyplot as plt

def pgm_to_mat(s):
     fread= open(s,'r')
     b=fread.read()
     lines=b.split("\n")
     print(lines[:4])
     n=lines[2].split(" ")
     row=np.int16(n[0])
     col=np.int16(n[1])
     a=np.zeros((row,col),dtype=np.int16)
     ind=4
     for i in range(row):
          for j in range(col):
               a[i][j]=np.int16(lines[ind])
               ind+=1
     return a

img=pgm_to_mat('images/peppers.pgm')
plt.figure(1)
plt.imshow(img,cmap="gray")
plt.show()

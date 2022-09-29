import sys
import re
import numpy as np
import matplotlib.pyplot as plt

f = open('./NN_HW1_DataSet/2ring.txt', 'r')
for l in f:
    m = re.findall(r'\d+\.*\d*', l)
    x = float(m[0])
    y = float(m[1])
    d = int(m[2])
    if d == 1:
        plt.plot(x, y, 'x', color='red')
    else:
        plt.plot(x, y, 'o', color='blue')
plt.show()

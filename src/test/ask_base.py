import matplotlib.pyplot as plt
import numpy as np
import random

n = input("nombre de signes")
d = [] #d=dot parce que la flemme
s = [] #s=signe

for x in range (n):
    amp = random.randint(1,2)
    si = np.linspace(x * np.pi, (x+1) * np.pi, 100) #si = signal
    p1, = plt.plot(si, np.sin(si*4)*amp)
    d.append(p1)
    s.append(str(amp-1))

plt.title("Modulation d'amplitude")
plt.legend(d,s)
plt._show()


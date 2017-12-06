import matplotlib.pyplot as plt
import numpy as np
import random



n = input("nombre de signes")

for x in range (n):
    freq = random.randint(1,2)
    if freq == 2:
        freq = 4

    si = np.linspace(x * np.pi, (x+1) * np.pi, 100)
    p1, = plt.plot(si, np.sin(si*2*freq))

plt.title("Modulation de frequences")
plt._show()
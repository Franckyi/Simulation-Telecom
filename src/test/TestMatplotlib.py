import matplotlib.pyplot as plt
import numpy as np

#  Ce site explique bien le fonctionnement de Numpy et Matplotlib : http://math.mad.free.fr/depot/numpy/essai.html

x = np.linspace(-2 * np.pi, 2 * np.pi, 100)  # 100 points repartis de -2pi a 2pi
p1, = plt.plot(x, np.sin(x))  # tracer la fonction sin(x)
p2, = plt.plot(x, np.cos(x))  # tracer la fonction cos(x)
plt.title("Fonctions trigo")  # titre du graphique
plt.legend([p1, p2], ["Sinus", "Cosinus"])  # legende du graphique
plt.show()  # afficher

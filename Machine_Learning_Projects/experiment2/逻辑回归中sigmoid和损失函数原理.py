import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 100)


def y(x):
    return 1 / (1 + np.exp(-x))


y = y(x)
plt.plot(x, y)
plt.show()

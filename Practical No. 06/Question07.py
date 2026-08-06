import matplotlib.pyplot as plt
import numpy as np

data = np.random.normal(0, 1, 100)

plt.hist(data, bins=20, color="purple", edgecolor="black")

plt.title("Histogram")
plt.xlabel("Values")
plt.ylabel("Frequency")

plt.grid(True)

plt.show()

print("Shravan Ramesh Vishwakarma")
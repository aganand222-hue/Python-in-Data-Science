import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.plot(x, y, marker="o")
plt.title("Line Plot")

plt.subplot(1,2,2)
plt.bar(x, y)
plt.title("Bar Chart")

plt.tight_layout()
plt.show()

print("Shravan Ramesh Vishwakarma")
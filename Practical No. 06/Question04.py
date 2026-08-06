import matplotlib.pyplot as plt

categories = ["Data Structures", "Scala for DS", "Operating System", "Python for DS"]
scores = [65, 70, 74, 60]

plt.barh(categories, scores, color="orange")

plt.title("Student Scores")
plt.xlabel("Scores")
plt.ylabel("Subjects")

plt.show()

print("Shravan Ramesh Vishwakarma")
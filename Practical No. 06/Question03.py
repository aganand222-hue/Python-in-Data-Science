import matplotlib.pyplot as plt

categories = ["Data Structures", "Scala for DS", "Operating System", "Python for DS"]
scores = [65, 70, 74, 60]

plt.bar(categories, scores, color="skyblue")

plt.title("Student Scores")
plt.xlabel("Subjects")
plt.ylabel("Scores")

plt.show()

print("Shravan Ramesh Vishwakarma")
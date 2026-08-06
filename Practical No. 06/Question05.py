import matplotlib.pyplot as plt

categories = ["Data Structures", "Scala for DS", "Operating System", "Python for DS"]
scores = [65, 70, 74, 60]

explode = (0, 0, 0, 0.2)

plt.pie(scores,
        labels=categories,
        autopct="%1.1f%%",
        explode=explode,
        shadow=True)

plt.title("Student Scores")

plt.show()

print("Shravan Ramesh Vishwakarma")
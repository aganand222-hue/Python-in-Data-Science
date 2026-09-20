import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("food_delivery.csv")

plt.figure(figsize=(8, 5))

plt.bar(df["Order_ID"].astype(str), df["Order_Value"])

plt.xlabel("Order ID")
plt.ylabel("Order Value")
plt.title("Food Delivery Order Value")

plt.show()

plt.figure(figsize=(8, 5))

plt.plot(
    df["Order_ID"].astype(str),
    df["Delivery_Time"],
    marker="o"
)

plt.xlabel("Order ID")
plt.ylabel("Delivery Time (minutes)")
plt.title("Food Delivery Time")

plt.show()

plt.figure(figsize=(8, 5))

plt.hist(df["Order_Value"], bins=5)

plt.xlabel("Order Value")
plt.ylabel("Number of Orders")
plt.title("Distribution of Order Values")

plt.show()

restaurant_count = df["Restaurant_Type"].value_counts()

plt.figure(figsize=(7, 7))

plt.pie(
    restaurant_count,
    labels=restaurant_count.index,
    autopct="%1.1f%%"
)

plt.title("Orders by Restaurant Type")

plt.show()

print("S117 Shravan Ramesh Vishwakarma")
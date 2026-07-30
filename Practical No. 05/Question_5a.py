import pandas as pd

data = {
    "Name": ["Shravan", "Rohit", "Anand"],
    "Age": [18, 19, 19],
    "Marks": [85, 90, 88]
}

df = pd.DataFrame(data)

print(df)
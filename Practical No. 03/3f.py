from datetime import datetime

date_str1 = input("Enter the first date (YYYY-MM-DD): ")
date_str2 = input("Enter the second date (YYYY-MM-DD): ")

date1 = datetime.strptime(date_str1, "%Y-%m-%d")
date2 = datetime.strptime(date_str2, "%Y-%m-%d")

if date1 < date2:
    print(f"{date_str1} is earlier than {date_str2}.")
elif date1 > date2:
    print(f"{date_str1} is later than {date_str2}.")
else:
    print("Both dates are the same.")
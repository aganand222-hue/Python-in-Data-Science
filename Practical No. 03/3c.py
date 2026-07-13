from datetime import datetime
now = datetime.now()
print("Different date formats:")
print("1. YYYY-MM-DD :", now.strftime("%Y-%m-%d"))
print("2. DD-MM-YYYY :", now.strftime("%d-%m-%Y"))
print("3. Month Day, Year :", now.strftime("%B %d, %Y"))
print("4. Day Month, Year :", now.strftime("%d %B, %Y"))
print("5. MM/DD/YYYY :", now.strftime("%m/%d/%Y"))
print("6. Weekday, Month Day, Year:", now.strftime("%A, %B %d, %Y"))
from datetime import datetime

today = datetime.now()

print("YYYY-MM-DD :", today.strftime("%Y-%m-%d"))
print("DD-MM-YYYY :", today.strftime("%d-%m-%Y"))
print("Month Day, Year :", today.strftime("%B %d, %Y"))
print("Weekday, Month Day, Year :", today.strftime("%A, %B %d, %Y"))
from datetime import datetime

now = datetime.now()

print("Month Number:", now.month)
print("Month Name:", now.strftime("%B"))
from datetime import datetime

timestamp = float(input("Enter a timestamp (e.g., 1690915200): "))

date = datetime.fromtimestamp(timestamp)

print("Converted date:", date.strftime("%Y-%m-%d %H:%M:%S"))
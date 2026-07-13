import calendar

def show_full_year_calendar(year):
    print(f"\nFull Calendar for {year}:\n")
    print(calendar.calendar(year))

def show_month_calendar(year, month):
    print(f"\nCalendar for {calendar.month_name[month]} {year}:\n")
    print(calendar.month(year, month))

def is_leap_year(year):
    if calendar.isleap(year):
        print(f"\n{year} is a leap year.")
    else:
        print(f"\n{year} is not a leap year.")

print("Calendar Module")

year = int(input("Enter the year: "))

show_full_year_calendar(year)

month = int(input("\nEnter the month number (1-12) to view that month's calendar: "))

show_month_calendar(year, month)

is_leap_year(year)
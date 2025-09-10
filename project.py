# Classic Expense tracker in python

# Importing libraries
import datetime

# Everything will be added to this variable: 
expenses = []

def added_expense():
    desc = input("Enter expense description: ")
    amount = float(input("Enter amount (in Rs): "))
    category = input("Enter category (Food/Study/Shopping/Transport/House Stuff/Other): ")

    # Now we gotta add the date and stuff ya know.
    date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if date_input.strip() == "": 
        date = datetime.date.today()
    else: 
        date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()

    expenses.append({"desc" : desc, "amount" : amount, "category" : category, "date" : date})
    print("✅ Expense added successfully!\n")

# Now for the expense review

def view_expenses(filter_type="all"):
    total = 0
    today = datetime.date.today()

    print("\n--- Your Expenses ---")
    for e in expenses: 
        if filter_type == "day" and e["date"].isocalendar()[1] !=today.isocalendar()[1]:
            continue
        elif filter_type == "week" and e["date"].isocalendar()[1] !=today.isocalendar()[1]:
            continue
        elif filter_type == "month" and e["date"].month !=today.month:
            continue

        print(f"{e['date']} | {e['category']} | {e['amount']}")
        total += e["amount"]

        print(f"Total = Rs {total}\n")

while True: 
    print("\n--- Expense Tracker ---")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Today’s Expenses")
    print("4. View This Week’s Expenses")
    print("5. View This Month’s Expenses")
    print("6. Exit")

    choice = input("Choose an option (1-6): ")

    if choice == "1": 
        added_expense()
    elif choice == "2": 
        view_expenses("all")
    elif choice == "3":
        view_expenses("day")
    elif choice == "4": 
        view_expenses("week")
    elif choice == "5": 
        view_expenses("month")
    elif choice == "6": 
        print("Goodbye! Stay smart with your money 💵💖")
        break 
    else: 
        print("Invalid choice, try again!")
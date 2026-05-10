import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Files
USER_FILE = "users.csv"
EXPENSE_FILE = "expenses.csv"
DEBT_FILE = "debts.csv"
BUDGET_FILE = "budgets.csv"
SAVINGS_FILE = "savings.csv"

# CSV Handling
def read_csv(file):
    try:
        with open(file, newline='') as f:
            return list(csv.DictReader(f))
    except:
        return []

def write_csv(file, fields, data):
    with open(file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

# Category Menu
CATEGORIES = ["food", "housing", "entertainment", "shopping", "health", "other"]

def select_category():
    print("\nCategories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}.{cat.capitalize()}")
    while True:
        ch = input("Select category: ")
        if ch.isdigit() and 1 <= int(ch) <= len(CATEGORIES):
            return CATEGORIES[int(ch) - 1]
        print("Invalid choice! Try again.")

# USER
def register_user(username, password):
    users = read_csv(USER_FILE)
    if len(username.strip()) == 0:
        print("Username cannot be empty!")
        return False
    for u in users:
        if u['username'] == username:
            print("User already registered! Please login.")
            return False
    if len(password) <= 0:
        print("Password cannot be empty!")
        return False
    user_id = len(users) + 1
    users.append({"id": user_id, "username": username, "password": password})
    write_csv(USER_FILE, ["id", "username", "password"], users)
    savings = read_csv(SAVINGS_FILE)
    savings.append({"user_id": user_id, "goal": 0, "current": 0})
    write_csv(SAVINGS_FILE, ["user_id", "goal", "current"], savings)
    print("Registered!")
    return True

def login_user(username, password):
    if len(username.strip()) == 0:
        print("Username cannot be empty!")
        return None
    users = read_csv(USER_FILE)
    for u in users:
        if u['username'] == username and u['password'] == password:
            print("Login success!")
            return u
    print("Invalid!")
    return None

# Expenses, Debts, Budgets, Savings
def add_expense(user_id, amount, category):
    try:
        amount = float(amount)
    except:
        print("Invalid amount!")
        return
    date = datetime.now().strftime("%Y-%m-%d")
    data = read_csv(EXPENSE_FILE)
    data.append({
        "id": len(data) + 1,
        "user_id": user_id,
        "amount": amount,
        "category": category,
        "date": date
    })
    write_csv(EXPENSE_FILE, ["id", "user_id", "amount", "category", "date"], data)
    print(f"Expense added on {date}!")

def view_expenses(user_id):
    for e in read_csv(EXPENSE_FILE):
        if e['user_id'] == str(user_id):
            print(e)

def add_debt(user_id, name, amount):
    try:
        amount = float(amount)
    except:
        print("Invalid amount!")
        return
    data = read_csv(DEBT_FILE)
    data.append({
        "id": len(data) + 1,
        "user_id": user_id,
        "name": name,
        "total": amount,
        "remaining": amount
    })
    write_csv(DEBT_FILE, ["id", "user_id", "name", "total", "remaining"], data)
    print("Debt added!")

def view_debts(user_id):
    for d in read_csv(DEBT_FILE):
        if d['user_id'] == str(user_id):
            print(d)

def repay_debt(user_id, debt_id, amount):
    data = read_csv(DEBT_FILE)
    found = False
    repaid_amount = 0
    for d in data:
        if d['id'] == str(debt_id):
            found = True
            remaining = float(d['remaining'])
            if amount > remaining:
                print(f"Amount exceeds remaining debt!")
                print(f"Remaining amount: {remaining}")
                return
            d['remaining'] = str(max(0, remaining - amount))
            repaid_amount = amount
            print(f"Payment successful!")
            print(f"Remaining amount: {d['remaining']}")
    if not found:
        print("Wrong Debt ID!")
        return
    write_csv(DEBT_FILE, ["id", "user_id", "name", "total", "remaining"], data)
    
    add_expense(user_id, repaid_amount, "debt_repay")

def set_budget(user_id, category, limit):
    data = read_csv(BUDGET_FILE)
    for b in data:
        if b['user_id'] == str(user_id) and b['category'] == category:
            print("Budget for this category already exists!")
            return
    data.append({
        "id": len(data) + 1,
        "user_id": user_id,
        "category": category.lower(),
        "limit": limit
    })
    write_csv(BUDGET_FILE, ["id", "user_id", "category", "limit"], data)
    print("Budget set!")

def view_budgets(user_id):
    for b in read_csv(BUDGET_FILE):
        if b['user_id'] == str(user_id):
            print(b)

def set_goal(user_id, goal):
    data = read_csv(SAVINGS_FILE)
    for s in data:
        if s['user_id'] == str(user_id):
            s['goal'] = str(goal)
    write_csv(SAVINGS_FILE, ["user_id", "goal", "current"], data)
    print("Goal set!")

def add_savings(user_id, amount):
    data = read_csv(SAVINGS_FILE)
    for s in data:
        if s['user_id'] == str(user_id):
            s['current'] = str(float(s['current']) + amount)
    write_csv(SAVINGS_FILE, ["user_id", "goal", "current"], data)
    print("Savings updated!")

def view_savings(user_id):
    for s in read_csv(SAVINGS_FILE):
        if s['user_id'] == str(user_id):
            print(s)

def category_graph(user_id):
    data = read_csv(EXPENSE_FILE)
    totals = {}
    for e in data:
        if e['user_id'] == str(user_id):
            totals[e['category']] = totals.get(e['category'], 0) + float(e['amount'])
    if totals:
        plt.pie(totals.values(), labels=totals.keys(), autopct='%1.1f%%')
        plt.title("Category-wise Expenses")
        plt.show()
    else:
        print("No data to display.")

def monthly_graph(user_id):
    data = read_csv(EXPENSE_FILE)
    totals = {}
    for e in data:
        if e['user_id'] == str(user_id):
            month = e['date'][:7]
            totals[month] = totals.get(month, 0) + float(e['amount'])
    if totals:
        plt.bar(totals.keys(), totals.values())
        plt.title("Monthly Expenses")
        plt.show()
    else:
        print("No data to display.")

def savings_graph(user_id):
    for s in read_csv(SAVINGS_FILE):
        if s['user_id'] == str(user_id):
            values = [float(s['goal']), float(s['current'])]
            if sum(values) > 0:
                plt.pie(values, labels=["Goal", "Current"], autopct='%1.1f%%')
                plt.title("Savings Progress")
                plt.show()
            else:
                print("No data to display.")

def debt_graph(user_id):
    names, values = [], []
    for d in read_csv(DEBT_FILE):
        if d['user_id'] == str(user_id):
            names.append(d['name'])
            values.append(float(d['remaining']))
    if values:
        plt.pie(values, labels=names, autopct='%1.1f%%')
        plt.title("Debt Remaining")
        plt.show()
    else:
        print("No data to display.")

def budget_warning_graph(user_id):
    expenses = read_csv(EXPENSE_FILE)
    budgets = read_csv(BUDGET_FILE)
    totals = {}
    for e in expenses:
        if e['user_id'] == str(user_id):
            totals[e['category']] = totals.get(e['category'], 0) + float(e['amount'])
    labels = []
    values = []
    for b in budgets:
        if b['user_id'] == str(user_id):
            cat = b['category']
            use = totals.get(cat, 0)
            labels.append(cat)
            values.append(use)
            if use > float(b['limit']):
                print(f"WARNING: {cat} exceeded budget!")
    if values:
        plt.bar(labels, values)
        plt.title("Budget Usage")
        plt.show()
    else:
        print("No data to display.")

# Menus
def graph_menu(user):
    while True:
        print("\n1.Category\n2.Monthly\n3.Savings\n4.Debt\n5.Warning\n6.Back")
        ch = input("Choice: ")
        if ch == '1':
            category_graph(user['id'])
        elif ch == '2':
            monthly_graph(user['id'])
        elif ch == '3':
            savings_graph(user['id'])
        elif ch == '4':
            debt_graph(user['id'])
        elif ch == '5':
            budget_warning_graph(user['id'])
        elif ch == '6':
            break

def expense_menu(user_id):
    while True:
        print("\n1.Add\n2.View\n3.Back")
        ch = input("Choice: ")
        if ch == '1':
            amount = input("Amount: ")
            category = select_category()
            add_expense(user_id, amount, category)
        elif ch == '2':
            view_expenses(user_id)
        elif ch == '3':
            break

def debt_menu(user_id):
    while True:
        print("\n1.Add\n2.View\n3.Repay\n4.Back")
        ch = input("Choice: ")
        if ch == '1':
            add_debt(user_id, input("Name: "), input("Amount: "))
        elif ch == '2':
            view_debts(user_id)
        elif ch == '3':
            repay_debt(user_id, input("Debt ID: "), float(input("Amount: ")))
        elif ch == '4':
            break

def budget_menu(user_id):
    while True:
        print("\n1.Set\n2.View\n3.Back")
        ch = input("Choice: ")
        if ch == '1':
            category = select_category()
            set_budget(user_id, category, float(input("Limit: ")))
        elif ch == '2':
            view_budgets(user_id)
        elif ch == '3':
            break

def savings_menu(user_id):
    while True:
        print("\n1.View\n2.Set Goal\n3.Add\n4.Back")
        ch = input("Choice: ")
        if ch == '1':
            view_savings(user_id)
        elif ch == '2':
            set_goal(user_id, float(input("Goal: ")))
        elif ch == '3':
            add_savings(user_id, float(input("Amount: ")))
        elif ch == '4':
            break

def user_menu(user):
    while True:
        print("""
1.Expense
2.Debt
3.Budget
4.Savings
5.Graphs
6.Logout
""")
        ch = input("Choice: ")
        if ch == '1':
            expense_menu(user['id'])
        elif ch == '2':
            debt_menu(user['id'])
        elif ch == '3':
            budget_menu(user['id'])
        elif ch == '4':
            savings_menu(user['id'])
        elif ch == '5':
            graph_menu(user)
        elif ch == '6':
            break

def main():
    while True:
        print("\n1.Register\n2.Login\n3.Exit")
        ch = input("Choice: ")
        if ch == '1':
            register_user(input("User: "), input("Pass: "))
        elif ch == '2':
            user = login_user(input("User: "), input("Pass: "))
            if user:
                user_menu(user)
        elif ch == '3':
            break

if __name__ == "__main__":
    main()
import json
import argparse
from datetime import datetime


EXPENSES_FILE = "expenses.json"


###########################################
# Helper functions                        #
###########################################

def load_expenses():
    # Load expenses from a JSON file, if it exists. If the file doesn't exist, return an empty list.
    try:
        with open(EXPENSES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    # Saves the list of expenses to a JSON file.
    with open(EXPENSES_FILE, "w") as file:
        json.dump(expenses, file)

############################################
# Core functionality                       #
############################################

def add_expense(description, amount):
    # Create a new expense dictionary and add it to the list of expenses, then save it.
    expenses = load_expenses()
    new_expense = {
        "id": len(expenses) + 1,
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    expenses.append(new_expense)
    save_expenses(expenses)

def list_expenses():
    # List all expenses.
    expenses = load_expenses()
    print("ID   Description   Amount   Date")
    for expense in expenses:
        print(f"{expense['id']}   {expense['description']}   {expense['amount']}   {expense['date']}")

def delete_expense(expense_id):
    # Delete an expense by its ID.
    expenses = load_expenses()
    expenses = [expense for expense in expenses if expense["id"] != expense_id]
    save_expenses(expenses)

def summarize_expenses(month=None):
    # Summarize expenses, optionally filtering by month.
    expenses = load_expenses()
    if month:
        expenses = [expense for expense in expenses if expense["date"].startswith(month)]
    total = sum(expense["amount"] for expense in expenses)
    print(f"Total expenses for {month if month else 'all time'}: {total}")

#############################################
# Command-line interface setup              #
#############################################

def setup_cli():
    parser = argparse.ArgumentParser(description="A simple expense tracker.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # The 'add' command setup
    parser_add = subparsers.add_parser("add", help="Add a new expense")
    parser_add.add_argument("--description", type=str, required=True, help="Description of expense")
    parser_add.add_argument("--amount", type=int, required=True, help="Amount of expense")

    # The 'list' command setup
    parser_list = subparsers.add_parser("list", help="List all expenses")

    # The 'delete' command setup
    parser_delete = subparsers.add_parser("delete", help="Delete an expense")
    parser_delete.add_argument("--id", type=int, required=True, help="ID of the expense to delete")

    # The 'summary' command setup
    parser_summary = subparsers.add_parser("summary", help="Show summary of expenses")
    parser_summary.add_argument("--month", type=int, help="Month to summarize (1-12)")

    return parser.parse_args()

# Starts the program
if __name__ == "__main__":
    args = setup_cli()
    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "list":
        list_expenses()
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "summary":
        summarize_expenses(month=args.month)
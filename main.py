#!/usr/bin/env python3

import json
import argparse
from datetime import datetime

EXPENSES_FILE = "expenses.json"

###########################################
# Helper functions                        #
###########################################

def load_expenses():
    # Load expenses from a JSON file, if it exists. If not, return an empty list.
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
    
    # BUG FIX 1: Safely generate a unique ID based on the highest existing ID
    new_id = max([expense["id"] for expense in expenses], default=0) + 1
    
    new_expense = {
        "id": new_id,
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")

def list_expenses():
    # List all expenses with clean, aligned columns.
    expenses = load_expenses()
    print(f"{'ID':<4} {'Date':<12} {'Description':<15} {'Amount'}")
    for expense in expenses:
        print(f"{expense['id']:<4} {expense['date']:<12} {expense['description']:<15} ${expense['amount']}")

def delete_expense(expense_id):
    # Delete an expense by its ID.
    expenses = load_expenses()
    initial_count = len(expenses)
    
    # Filter out the expense with the matching ID
    expenses = [expense for expense in expenses if expense["id"] != expense_id]
    
    # Check if anything was actually deleted before saving
    if len(expenses) < initial_count:
        save_expenses(expenses)
        print("Expense deleted successfully")
    else:
        print(f"No expense found with ID {expense_id}")

def summarize_expenses(month=None):
    # Summarize expenses, optionally filtering by month.
    expenses = load_expenses()
    
    if month:
        # BUG FIX 2: Format month integer to a 2-digit string (e.g., 8 becomes "08")
        target_month = f"{month:02d}"
        # Split the "YYYY-MM-DD" string and check the middle element (the month)
        expenses = [expense for expense in expenses if expense["date"].split("-")[1] == target_month]
        
    total = sum(expense["amount"] for expense in expenses)
    
    if month:
        print(f"Total expenses for month {month}: ${total}")
    else:
        print(f"Total expenses: ${total}")

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
import requests
from config import API_KEY

# Sample Input Data
expenses = [
    "$50 on groceries",
    "$100 on dining out",
    "$20 on movies",
    "$40 on public transport",
    "$75 on groceries",
    "$25 on coffee",
]


# Function to parse expenses
def parse_expenses(expense_list):
    parsed_expenses = []
    for entry in expense_list:
        try:
            amount, description = entry.split(" ", 1)
            amount = float(amount.replace("$", ""))
            parsed_expenses.append({"amount": amount, "description": description})
        except ValueError:
            print(f"Error parsing entry: {entry}")
    return parsed_expenses


# Get Cerebras's response
def cerebras_response(description):
    url = "https://api.openai.com/v1/engines/davinci/completions"  # Replace with Cerebras API endpoint
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # Replace YOUR_API_KEY with your actual API key
        "Content-Type": "application/json"
    }
    data = {
        "text": description
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        category = response.json().get("category", "Other")
        return category
    else:
        print("Error:", response.status_code, response.text)
        return "Other"


# Categorize and analyze spending
parsed_expenses = parse_expenses(expenses)
category_totals = {}

for expense in parsed_expenses:
    category = cerebras_response(expense["description"])
    expense["category"] = category
    category_totals[category] = category_totals.get(category, 0) + expense["amount"]

# Output results
print("Categorized Expenses:")
for expense in parsed_expenses:
    print(" - $" + str(round(expense["amount"], 2)) + " on " + expense["description"] + " (Category: " + expense[
        "category"] + ")")

print("\nCategory Totals:")
for category, total in category_totals.items():
    print(" - " + category + ": $" + str(round(total, 2)))

highest_spending_category = max(category_totals, key=category_totals.get)
print("\nHighest Spending Category:", highest_spending_category)

from .filter import filter_by_purchase

def sum_data(data: list, has_header=False):
    """
    Sums the values in the second column of data.
    [date, amount, note, total_amount]
    """
    total = 0.0
    try:
        for row in data:
            if has_header:
                has_header = False # skips the header row
                continue
            amount_str = row[1]
            amount = float(amount_str.replace(",", "").replace("₱", ""))
            total += amount
    except Exception as e:
        print(f"Error summing data: {e}")

    return total

def summarize_items(data: list):
    income_items = filter_by_purchase(data, positive=True)
    expense_items = filter_by_purchase(data, positive=False)
    income_total = sum_data(income_items)
    expense_total = sum_data(expense_items)
    net_total = sum_data(data, has_header=True)
    
    return {
        "count": len(data),
        "income_total": round(income_total, 2),
        "expense_total": round(expense_total, 2),
        "net_total": round(net_total, 2),         
    }
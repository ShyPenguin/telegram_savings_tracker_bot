from datetime import date, datetime

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

def filter_by_date(data: list, start_date: datetime, end_date: datetime):
    """
    Filters the data by a specific date.
    """
    filtered_data = []
    
    try:
        for idx, row in enumerate(data):
            if idx == 0: 
                filtered_data.append(row)
                continue # skips header
            date_str = row[0]
            date = datetime.strptime(date_str, "%m/%d/%Y")
            if date < start_date:
                continue
            if date > end_date:
                continue
            filtered_data.append(row)
    except Exception as e:
        print(f"Error filtering by date: {e}")

    return filtered_data

def filter_items(
    data,
    start_date: datetime,
    end_date: datetime,
    purchase_type=None,
):
    filtered = filter_by_date(data, start_date, end_date)

    if purchase_type == "income":
        return filter_by_purchase(filtered, positive=True)
    if purchase_type == "expense":
        return filter_by_purchase(filtered, positive=False)
    return filtered


def filter_by_purchase(data: list, positive=True):
    """
    Filters the data by purchase (positive or negative values).
    """
    filtered_data = []
    try:
        for idx, row in enumerate(data):
            if idx == 0: continue # skips header
            amount_str = row[1]
            amount = float(amount_str.replace(",", "").replace("₱", ""))
            if positive and amount > 0:
                filtered_data.append(row)
            elif not positive and amount < 0:
                filtered_data.append(row)
    except Exception as e:
        print(f"Error filtering by purchase: {e}")

    return filtered_data
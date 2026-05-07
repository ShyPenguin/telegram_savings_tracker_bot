from datetime import datetime

from gs_savings_tracker.models import Savings

def filter_by_date(data: list[Savings], start_date: datetime, end_date: datetime) -> list[Savings]:
    """
    Filters the data by a specific date.
    """
    filtered_data = []
    
    try:
        for idx, row in enumerate(data):
            if idx == 0: 
                filtered_data.append(row)
                continue # skips header
            date_str = row.date
            date = datetime.strptime(date_str, "%m/%d/%Y")
            if date < start_date:
                continue
            if date > end_date:
                continue
            filtered_data.append(row)
    except Exception as e:
        print(f"Error filtering by date: {e}")

    return filtered_data

def list_head(data: list[Savings], num: int) -> list[Savings]:
    return data[-num:]
    
def list_tail(data: list[Savings], num: int) -> list[Savings]:
    return data[:num]

def filter_items(
    data: list[Savings],
    start_date: datetime,
    end_date: datetime,
    purchase_type=None,
) -> list[Savings]:
    filtered = filter_by_date(data, start_date, end_date)

    if purchase_type == "income":
        return filter_by_purchase(filtered, positive=True)
    if purchase_type == "expense":
        return filter_by_purchase(filtered, positive=False)
    return filtered


def filter_by_purchase(data: list[Savings], positive=True) -> list[Savings]:
    """
    Filters the data by purchase (positive or negative values).
    """
    filtered_data = []
    try:
        for row in data:
            amount_str = row.amount
            amount = float(amount_str.replace(",", "").replace("₱", ""))
            if positive and amount > 0:
                filtered_data.append(row)
            elif not positive and amount < 0:
                filtered_data.append(row)
    except Exception as e:
        print(f"Error filtering by purchase: {e}")

    return filtered_data
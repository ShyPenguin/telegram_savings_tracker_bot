from datetime import datetime

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

def filter_by_date(data: list, day=None, month=None, year=None):
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
            if date and day and date.day != int(day):
                continue
            if date and month and date.month != int(month):
                continue
            if date and year and date.year != int(year):
                continue
            filtered_data.append(row)
    except Exception as e:
        print(f"Error filtering by date: {e}")

    return filtered_data

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
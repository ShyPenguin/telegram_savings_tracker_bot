from datetime import datetime
from typing import Optional

def parse_filter_args(
    args: list[str],
) -> tuple[datetime, datetime]:
    start_day = None
    start_month = None
    start_year = None
    
    end_day = None
    end_month = None
    end_year = None
    
    for arg in args:
        if arg.startswith("start_day="):
            start_day = arg.split("=", 1)[1]
        elif arg.startswith("start_month="):
            start_month = arg.split("=", 1)[1]
        elif arg.startswith("start_year="):
            start_year = arg.split("=", 1)[1]
        elif arg.startswith("end_day="):
            end_day = arg.split("=", 1)[1]
        elif arg.startswith("end_month="):
            end_month = arg.split("=", 1)[1]
        elif arg.startswith("end_year="):
            end_year = arg.split("=", 1)[1]

    start_date = datetime.strptime(start_month + "/"  + start_day + "/" + start_year, "%m/%d/%Y")
    end_date = datetime.strptime(end_month + "/"  + end_day + "/" + end_year, "%m/%d/%Y") 
        
    return start_date, end_date

def parse_items_get_args(args: list[str]) -> tuple[Optional[int], Optional[int]]:
    head = None
    tail = None
    
    for arg in args:
        match arg.split("=", 1):
            case ["head", value]:
                head = int(value)
            case ["tail", value]:
                tail = int(value)
            case _:
                pass 
    
    return head, tail
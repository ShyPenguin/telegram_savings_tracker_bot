from datetime import datetime

from .helpers import filter_items, summarize_items

from .sheet_manager import SheetManager

class SpreadSheetService(SheetManager):
    def __init__(self):
        super().__init__()
        
    def append_item(self, values):
        body = {
            "values": values
        }
        result = self.spreadsheets_api.values().append(
            spreadsheetId=self.spreadsheet_id,
            range=self.get_active_worksheet(),
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",  # ensures new rows are added
            body=body
        ).execute()

        print(f"{result.get('updates').get('updatedCells')} cells appended.")
    
    def read_items(self):
        data = self.read_worksheet()
        message = f"{self.get_active_worksheet()}'s items:\n"
        
        message += f"{data[0][0]}\t\t {data[0][1]}\t\t {data[0][2]}\n"
        for i in range(1, len(data)):
            message += f"{i}: {data[i][0]}\t {data[i][1]}\t {data[i][2]}\n"
            
        return message
    
    
    def filter_items_by_date(self, start_date: datetime, end_date: datetime) -> str:
        data = self.read_worksheet()
        filtered_items = filter_items(data, start_date, end_date)
        filtered_summary = summarize_items(filtered_items)
        
        message = (
            f"Filtered ({self.get_active_worksheet()})\n"
            f"- Items: {filtered_summary['count']}\n"
            f"- Income: ₱{filtered_summary['income_total']:,.2f}\n"
            f"- Expense: ₱{filtered_summary['expense_total']*-1:,.2f}\n"
            f"- Net: ₱{filtered_summary['net_total']:,.2f}\n\n"
            f"Filter format: /filter start_day={start_date.day} start_month={start_date.month} start_year={start_date.year} " 
            f"end_day={end_date.day} end_month={end_date.month} end_year={end_date.year}"
        )
        
        return message
    
    def delete_item(self, row_index: int):
        worksheet = self._get_worksheet_by_title(self.get_active_worksheet())
        request = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": worksheet["sheetId"],
                            "dimension": "ROWS",
                            "startIndex": row_index,
                            "endIndex": row_index + 1
                        }
                    }
                }
            ]
        }

        self.spreadsheets_api.batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=request
        ).execute()
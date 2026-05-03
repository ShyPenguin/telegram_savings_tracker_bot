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
            range=self._worksheet_title,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",  # ensures new rows are added
            body=body
        ).execute()

        print(f"{result.get('updates').get('updatedCells')} cells appended.")
        
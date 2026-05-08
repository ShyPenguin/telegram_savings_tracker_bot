import os
from abc import ABC
from dotenv import load_dotenv
from utils.index import extract_google_doc_id
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from .helpers import summarize_items
from gs_savings_tracker.models import Savings

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

class SheetManager(ABC):
    def __init__(self):
        self.auth_path = os.path.join(os.getcwd(), "auth")
        self.credentials_path = os.path.join(self.auth_path, "service_credentials.json")
        self.creds = self._get_credentials()
        self.spreadsheet_id = extract_google_doc_id(os.getenv("SPREADSHEET_URL"))
        self.spreadsheets_api = build("sheets", "v4", credentials=self.creds).spreadsheets()
        self._active_worksheet_title = "Sheet1";

    def _get_credentials(self):
        creds = Credentials.from_service_account_file(
            filename=self.credentials_path,
            scopes=SCOPES
        )
        return creds
    
    def get_active_worksheet(self):
        return self._active_worksheet_title

    def set_active_worksheet(self, title):
        self._ensure_target_worksheet_exists(title)
        print(f"Setting active worksheet to {title}...")
        self._active_worksheet_title = title
    
    def get_worksheets_title(self):
        worksheets = self._get_worksheets()
        
        worksheets_titles = []
        for worksheet in worksheets:
            if worksheet["title"] == self._active_worksheet_title:
                worksheets_titles.append(f"{self._active_worksheet_title} (active)")
                continue
            
            worksheets_titles.append(worksheet["title"])
            
        return worksheets_titles
    
    def read_worksheet(self) -> list[Savings]:
        self._ensure_target_worksheet_exists(self._active_worksheet_title)
        result = self.spreadsheets_api.values().get(
            spreadsheetId=self.spreadsheet_id, range=self._active_worksheet_title
        ).execute()
        values = result.get("values", [])
        new_values = []  # Create a new list to store filtered rows
        
        for i in range(1, len(values)):
            row = values[i]
            has_content = False
            
            for cell in row:
            # ignores empty cells
                if cell.strip():
                    has_content = True
                    break
            
            if has_content:
                item = Savings(i, row[0], row[1], row[2])
                new_values.append(item)
                
        return new_values
        
    def add_worksheet(self, title: str):
        request = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title
                        }
                    }
                }
            ]
        }
        
        response = self.spreadsheets_api.batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=request
        ).execute()
                
        worksheet_properties = response["replies"][0]["addSheet"]["properties"]
        self._initialize_worksheet(worksheet_properties["sheetId"])
        worksheet_title = worksheet_properties["title"]
        return worksheet_title
    
    
    def _initialize_worksheet(self, sheet_id):
        request = {
            "requests": [
                {
                    "updateCells": {
                        "start": {
                        "sheetId": sheet_id,  # tricky part!
                        "rowIndex": 0,
                        "columnIndex": 0
                        },
                        "rows": [
                        {
                            "values": [
                            {"userEnteredValue": {"stringValue": "Date"}},
                            {"userEnteredValue": {"stringValue": "Amount"}},
                            {"userEnteredValue": {"stringValue": "Notes"}}
                            ]
                        }
                        ],
                        "fields": "userEnteredValue"
                    }                           
                },{
                    
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startColumnIndex": 1,  # Column B (0-based index)
                            "endColumnIndex": 2
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "numberFormat": {
                                    "type": "CURRENCY",
                                    "pattern": "₱#,##0.00"
                                }
                            }
                        },
                        "fields": "userEnteredFormat.numberFormat"
                    }                                                
                }
            ]
        }
        self.spreadsheets_api.batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=request
        ).execute()

# Depreciated we use initialize worksheet
    def _set_header_row(self, worksheet_title):
        values = [
            ["Date", "Amount", "Notes", "Total"]
        ]

        self.spreadsheets_api.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f"{worksheet_title}!A1",
            valueInputOption="RAW",
            body={"values": values}
        ).execute()

# Depreciated we use initialize worksheet
    def _format_column_as_peso(self, sheet_id):
        request = {
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startColumnIndex": 1,  # Column B (0-based index)
                            "endColumnIndex": 2
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "numberFormat": {
                                    "type": "CURRENCY",
                                    "pattern": "₱#,##0.00"
                                }
                            }
                        },
                        "fields": "userEnteredFormat.numberFormat"
                    }
                }
            ]
        }

        self.spreadsheets_api.batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=request
        ).execute()
       
    def delete_worksheet(self, title: str) -> None:
        worksheet = self._get_worksheet_by_title(title)
        
        request = {
            "requests": [
                {
                    "deleteSheet": {
                        "sheetId": worksheet["sheetId"]
                    }
                }
            ]
        }

        self.spreadsheets_api.batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=request
        ).execute()
        print(f"Sheet: {title} is successfully deleted.")
    
    def summarize_worksheet(self)-> str:
        data = self.read_worksheet()
        
        summary_data = summarize_items(data)
        
        message = (
            f"Summary ({self._active_worksheet_title})\n"
            f"- Count: {summary_data['count']}\n"
            f"- Income: ₱{summary_data['income_total']:,.2f}\n"
            f"- Expense: ₱{summary_data['expense_total']*-1:,.2f}\n"
            f"- Net: ₱{summary_data['net_total']:,.2f}"
        )
            
        return message
        
    def _get_worksheet_by_title(self, title: str) -> list[str]:
        worksheets = self._get_worksheets()
        filtered_worksheets = list(filter(lambda worksheet: worksheet["title"] == title, worksheets))
        if len(filtered_worksheets) < 1:
            raise ValueError(f"Target sheet `{title}` does not exist.")
        return filtered_worksheets[0]

    def _get_worksheets(self):
        spreadsheet = (
            self.spreadsheets_api
            .get(spreadsheetId=self.spreadsheet_id)
            .execute()
        )
        return [sheet['properties'] for sheet in spreadsheet["sheets"]]
      
    def _ensure_target_worksheet_exists(self, target_worksheet: str):
        worksheets = self._get_worksheets()
        worksheet_titles = list(map(lambda worksheet: worksheet["title"], worksheets))
        if target_worksheet not in worksheet_titles:
            raise ValueError(f"Target sheet '{target_worksheet}' does not exist.")
        
    
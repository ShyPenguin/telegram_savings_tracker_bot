from abc import ABC
from dotenv import load_dotenv
import os
from utils.index import extract_google_doc_id
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from .helpers import summarize_items


env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

class SheetManager(ABC):
    def __init__(self):
        self.auth_path = os.path.join(os.getcwd(), "auth")
        self.credentials_path = os.path.join(self.auth_path, "service_credentials.json")
        self.creds = self._get_credentials()
        self.spreadsheet_id = extract_google_doc_id(os.getenv("TEST_URL"))
        self.spreadsheets_api = build("sheets", "v4", credentials=self.creds).spreadsheets()
        self._worksheet_title = "Sheet1";

    def _get_credentials(self):
        creds = Credentials.from_service_account_file(
            filename=self.credentials_path,
            scopes=SCOPES
        )
        return creds
    
    def get_current_worksheet(self):
        return self._worksheet_title

    def set_current_worksheet(self, title):
        self._ensure_target_worksheet_exists(self, title)
        print(f"Setting worksheet to {self, title}...")
        self._worksheet_title = title
    
    def get_worksheets(self):
        worksheets = self._get_worksheets()
        
        return list(map(lambda worksheet: worksheet["title"], worksheets))
    
    def read_worksheet(self):
        self._ensure_target_worksheet_exists(self._worksheet_title)
        result = self.spreadsheets_api.values().get(
            spreadsheetId=self.spreadsheet_id, range=self._worksheet_title
        ).execute()
        values = result.get("values", [])
        # ignores empty cells
        values = [row for row in values if any(cell.strip() for cell in row)]
        return values
        
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
        self._set_header_row(title)
        worksheet_title = worksheet_properties["title"]
        return worksheet_title
    
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
            f"Summary ({self._worksheet_title})\n"
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
      
    def _ensure_target_worksheet_exists(self, target_sheet: str):
        worksheets = self._get_worksheets()
        worksheet_titles = list(map(lambda worksheet: worksheet["title"], worksheets))
        if target_sheet not in worksheet_titles:
            raise ValueError(f"Target sheet '{target_sheet}' does not exist.")
        
    
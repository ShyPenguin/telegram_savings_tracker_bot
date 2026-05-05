from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from .helper import parse_filter_args

from gs_savings_tracker import SpreadSheetService


class SpreadSheetController:
    def __init__(self):
        self.spreadsheet_service = SpreadSheetService()
        
    async def hello(_, update:Update, _c: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hello world!")  # type: ignore
        
    async def help(_, update:Update, _c: ContextTypes.DEFAULT_TYPE) -> None:
        message = (
            "Available commands:\n"
            "/add_item <amount> <note> - Append a new savings entry\n"
            "/add_worksheet <title> - Add a new worksheet\n"
            "/delete_worksheet <title> - Delete a worksheet\n"
            "/get_worksheets - Lists all worksheet\n"
            "/filter start_day=<d> start_month=<m> start_year=<y>"
            "end_day=<d> end_month=<m> end_year=<y> - Filter and summarize\n"
            "/help - Show this message"
        )
        
        await update.message.reply_text(message)
        
#Arg: amount=str note=str
    async def add_item(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(  # type: ignore
                "Usage: /add <amount> <note>\nExample: /add 250 groceries"
            )
            return

        try:
            amount = float(context.args[0])
        except ValueError:
            await update.message.reply_text("Amount must be a number.")  # type: ignore
            return

        note = " ".join(context.args[1:])
        values = [
            [
                datetime.now().strftime("%m/%d/%Y"),
                f"{amount:.2f}",
                note,
            ]
        ]
        
        print(f"note: {note} \namount: {amount:.2f}")
        self.spreadsheet_service.append_item(
            values=values
        )
        await update.message.reply_text("Item appended successfully.")  # type: ignore
        
# Arg: title=str
    async def add_worksheet(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args or len(context.args) < 1:
            await update.message.reply_text(  # type: ignore
                "Usage: /add_worksheet <worksheet_title> \nExample: /add_worksheet Sheet2"
            )
        title = context.args[0]
        self.spreadsheet_service.add_worksheet(title=title)
        await update.message.reply_text(f"Sheet: {title} added successfully")

    async def delete_worksheet(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args or len(context.args) < 1:
            await update.message.reply_text(  # type: ignore
                "Usage: /delete_worksheet <worksheet_title> \nExample: /delete_worksheet Sheet2"
            )
        title = context.args[0]
        self.spreadsheet_service.delete_worksheet(title=title)
        await update.message.reply_text(f"Sheet: {title} deleted successfully")
    
    async def get_worksheets(self, update:Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        worksheets = self.spreadsheet_service.get_worksheets()
        message = "Sheets:\n"
        for name in worksheets:
            message += f"{name}\n"
            
        await update.message.reply_text(message)

    async def summary(self, update:Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        message = self.spreadsheet_service.summarize_worksheet()
        
        await update.message.reply_text(message)
        
# Arg: start_day=int start_month=int start_year=int end_day=int end_month=int end_year=int
    async def filter(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        start_date, end_date = parse_filter_args(context.args)
        
        message = self.spreadsheet_service.filter_items_by_date(start_date, end_date)
        
        print(message)
        await update.message.reply_text(message)

from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from .service import SpreadSheetService

class SpreadSheetController:
    def __init__(self):
        self.spreadsheet_service = SpreadSheetService()
        
    def hello(self):
        async def hello(update:Update, _: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text("Hello world!")  # type: ignore
        return hello
    
    def add_item(self):
        async def add(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        return add
    
    def add_worksheet(self):
        async def add(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            if not context.args or len(context.args) < 1:
                await update.message.reply_text(  # type: ignore
                    "Usage: /add_worksheet <worksheet_title> \nExample: /add_worksheet Sheet2"
                )
            title = context.args[0]
            self.spreadsheet_service.add_worksheet(title=title)
            await update.message.reply_text(f"Sheet: {title} added successfully")
        return add

    def delete_worksheet(self):
        async def add(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            if not context.args or len(context.args) < 1:
                await update.message.reply_text(  # type: ignore
                    "Usage: /delete_worksheet <worksheet_title> \nExample: /delete_worksheet Sheet2"
                )
            title = context.args[0]
            self.spreadsheet_service.delete_worksheet(title=title)
            await update.message.reply_text(f"Sheet: {title} deleted successfully")
        return add
    
    
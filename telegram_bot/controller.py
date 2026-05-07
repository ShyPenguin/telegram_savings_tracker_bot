from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from .helper import parse_filter_args, parse_items_get_args

from gs_savings_tracker import SpreadSheetService

class SpreadSheetController:
    def __init__(self):
        self.spreadsheet_service = SpreadSheetService()
        
    async def hello(_, update:Update, _c: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hello world!")  # type: ignore
        
    async def help(_, update:Update, _c: ContextTypes.DEFAULT_TYPE) -> None:
        message = (
            "Available commands:\n"
            "/item_add <amount> <note> - Append a new savings entry\n"
            "/worksheet_add <title> - Add a new worksheet\n"
            "/worksheet_delete <title> - Delete a worksheet\n"
            "/worksheets_get - Lists all worksheet\n"
            "/active_worksheet - Show active worksheet\n"
            "/active_worksheet <title> - Change active worksheet\n"
            "/filter start_day=<d> start_month=<m> start_year=<y>"
            "end_day=<d> end_month=<m> end_year=<y> - Filter and summarize\n"
            "/help - Show this message"
        )
        
        await update.message.reply_text(message)
        
#Arg: amount=str note=str
    async def item_add(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    async def worksheet_add(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args:
            await update.message.reply_text(  # type: ignore
                "Usage: /worksheet_add <worksheet_title> \nExample: /worksheet_add Sheet2"
            )
            return
        title = context.args[0]
        
        try:
            self.spreadsheet_service.add_worksheet(title=title)
        except Exception as e:
            print(e)
            message = "Something went wrong"
            if "already exists. Please enter another name." in str(e):
                message = f'"{title}" already exists. Please enter another name'
            return await update.message.reply_text(f"{message}")
        
        await update.message.reply_text(f"Sheet: {title} added successfully")

    async def worksheet_delete(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args:
            await update.message.reply_text(  # type: ignore
                "Usage: /worksheet_delete <worksheet_title> \nExample: /worksheet_delete Sheet2"
            )
            return
        
        title = context.args[0]
        if title == self.spreadsheet_service.get_active_worksheet():
            await update.message.reply_text("Cannot delete active worksheet")
            return
        
        try:
            self.spreadsheet_service.delete_worksheet(title=title)
        except ValueError as e:
            await update.message.reply_text(f"{e}")
            return
        
        await update.message.reply_text(f"Sheet: {title} deleted successfully")
    
    async def worksheets_get(self, update:Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        worksheets = self.spreadsheet_service.get_worksheets_title()
        message = "Sheets:\n"
        for name in worksheets:
            message += f"{name}\n"
            
        await update.message.reply_text(message)

    async def summary(self, update:Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        message = self.spreadsheet_service.summarize_worksheet()
        await update.message.reply_text(message)
        
# Arg: start_day=int start_month=int start_year=int end_day=int end_month=int end_year=int
    async def filter(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            start_date, end_date = parse_filter_args(context.args)
        except Exception:
            await update.message.reply_text("Usage:\n/filter start_day=<d> start_month=<m> start_year=<y> end_day=<d> end_month=<m> end_year=<y> - Filter and summarize")
            return    
        message = self.spreadsheet_service.filter_items_by_date(start_date, end_date)
        
        await update.message.reply_text(message)
    
    async def active_worksheet(self, update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
        
        if not context.args:
            await update.message.reply_text(  # type: ignore
                f"Active worksheet: {self.spreadsheet_service.get_active_worksheet()}"
            )
            return
    
        if len(context.args) > 1:
            await update.message.reply_text(  # type: ignore
                "Usage: /active_worksheet <worksheet_title> \nExample: /active_worksheet Sheet2"
            )
            return 
            
            
        title = context.args[0]
        
        try:
            self.spreadsheet_service.set_active_worksheet(title)
        except ValueError:
            available_sheet_names = self.spreadsheet_service.get_worksheets_title()
            await update.message.reply_text(  # type: ignore
                f'Worksheet "{title}" does not exist.\n'
                f"Available worksheets:\n{'\n'.join(available_sheet_names)}"
            )
            return
        
        await update.message.reply_text(f"Active worksheet changed to: {self.spreadsheet_service.get_active_worksheet()}")
        
    async def items_get(self, update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
        head, tail = parse_items_get_args(context.args)
        if head is not None and tail is not None:
            await update.message.reply_text(f"Usage /items_get head=<head> OR /items_get tail=<tail>")
        message = self.spreadsheet_service.read_items(head=head, tail=tail)
        
        await update.message.reply_text(message) 
        
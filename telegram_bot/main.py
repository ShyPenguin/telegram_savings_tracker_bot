from telegram.ext import ApplicationBuilder, CommandHandler
from gs_expenses_tracker import SpreadSheetController, SpreadSheetService
import dotenv
import os

dotenv.load_dotenv()


def build_application():
    token = os.getenv("TELEGRAM_API_KEY")
    if not token:
        raise ValueError("TELEGRAM_API_KEY not found in environment variables.")
    app = ApplicationBuilder().token(token).build()
    
    spread_controller = SpreadSheetController()
    app.add_handler(CommandHandler("add_item", spread_controller.add()))
    app.add_handler(CommandHandler("hello", spread_controller.hello()))
    return app


def main(): 
    print("Savings tracker bot is running...")
    # app = build_application()
    # app.run_polling()
    spread_service = SpreadSheetService()
    spread_service.delete_worksheet("Sheet2")
    spread_service.add_worksheet("Sheet2")
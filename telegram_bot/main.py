from telegram.ext import ApplicationBuilder, CommandHandler
from telegram_bot.controller import SpreadSheetController
import dotenv
import os


dotenv.load_dotenv()


def build_application():
    token = os.getenv("TELEGRAM_API_KEY")
    if not token:
        raise ValueError("TELEGRAM_API_KEY not found in environment variables.")
    app = ApplicationBuilder().token(token).build()
    
    spread_controller = SpreadSheetController()
    app.add_handler(CommandHandler("add_item", spread_controller.add_item))
    app.add_handler(CommandHandler("add_worksheet", spread_controller.add_worksheet))
    app.add_handler(CommandHandler("delete_worksheet", spread_controller.delete_worksheet))
    app.add_handler(CommandHandler("get_worksheets", spread_controller.get_worksheets))
    app.add_handler(CommandHandler("filter", spread_controller.filter))
    app.add_handler(CommandHandler("summary", spread_controller.summary))
    app.add_handler(CommandHandler("help", spread_controller.help))
    app.add_handler(CommandHandler("hello", spread_controller.hello))
    return app


def main(): 
    print("Savings tracker bot is running...")
    app = build_application()
    app.run_polling()
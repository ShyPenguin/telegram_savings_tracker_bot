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
    # Item related
    app.add_handler(CommandHandler("items_add", spread_controller.items_add))
    app.add_handler(CommandHandler("items_delete", spread_controller.items_delete))
    app.add_handler(CommandHandler("items_get", spread_controller.items_get))
    # Worksheet related
    app.add_handler(CommandHandler("worksheets_add", spread_controller.worksheets_add))
    app.add_handler(CommandHandler("worksheets_delete", spread_controller.worksheets_delete))
    app.add_handler(CommandHandler("worksheets_get", spread_controller.worksheets_get))
    app.add_handler(CommandHandler("active_worksheet", spread_controller.active_worksheet))
    # Summary
    app.add_handler(CommandHandler("filter", spread_controller.filter))
    app.add_handler(CommandHandler("summary", spread_controller.summary))
    
    app.add_handler(CommandHandler("help", spread_controller.help))
    app.add_handler(CommandHandler("hello", spread_controller.hello))
    return app


def main(): 
    app = build_application()
    print("Savings tracker bot is running...")
    app.run_polling()
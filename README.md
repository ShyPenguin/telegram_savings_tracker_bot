# Savings Tracker Telegram Bot

A telegram bot for tracking savings and expenses using Google Sheets

The bot allows you to:

- Add savings/expense entries
- Delete entries
- View entries
- Create and manage worksheets
- Switch active worksheets
- Generate summaries
- Filter entries by date

Built with:

- Python
- python-telegram-bot
- Google Sheets API

## Features

### Item Management

- Add Items
- Delete Items
- View Items

### Worksheet management

- Create worksheets
- Delete worksheets
- List worksheets
- Change active worksheet

### Reports

- Worksheet summaries
- Data filtering

## Projects Structure

`telegram_bot/main.py`
Responsible for:

- Building the Telegram application
- Registering command handlers
- Starting polling

`telegram_bot/controller.py`
Contains:

- Telegram command handlers
- Input validation
- User responses
- Communication with `SpreadSheetService`

`gs_savings_tracker`
Responsible for:

- Google Sheets API integration
- Worksheet management
- Item CRUD operations
- Filtering and summaries
  Contains:
- `gs_savings_tracker/sheet_manager.py` - contains SheetManager Class (an abstract class that initialize google spreadsheet api and worksheet commands)
- `gs_savings_tracker/service.py` - contains SpreadSheetService Class (a class that extends to SheetManager Class and item commands)
- `gs_savings_tracker/models/savings.py` - contains Savings Class (reflects the table and columns inside the sheet)

## Requirements

- Python 3.10+
- Telegram Bot Token
- Google Cloud Service Account
- Google Sheets API enabled

## Installation

### 1. Install uv

Official installation guide:
[uv Documentation](https://docs.astral.sh/uv/getting-started/installation)

#### Linux/macOS

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows(PowerShell)

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the repository

```
git clone https://github.com/ShyPenguin/telegram_savings_tracker_bot
cd telegram_savings_tracker_bot
```

### 3. Install dependencies

```
uv sync
```

### 4. Activate virtual environment

#### Linux / macOS

```
source .venv/bin/activate
```

#### Windows(PowerShell)

```
.venv\Scripts\activate
```

## Telegram Bot Setup

### 1. Create a Telegram bot

Use Telegram's BotFather:
[BotFather](https://t.me/BotFather)
Create a bot and copy the bot token.

### 2. Create `.env`

```
TELEGRAM_API_KEY=your_telegram_bot_token
```

## Google Sheets Setup

### 1. Create a Google Cloud Project

Go to:
[Google Cloud Console](https://console.cloud.google.com/welcome)

### 2. Enable Google Sheets API

Enable:

- Google Sheets API

### 3. Create a Servuce Account

1. Create a Service Account
2. Download the JSON credentials file
3. Store it securely

### 4. Share your SpreadSheet

Share your Google Spreadsheet with the service account email.
Example

```
my-service-account@project-id.iam.gserviceaccount.com
```

Give it Editor permission.

## Running the Bot

```
uv run main.py
```

or after activating the virtual envrionment:

```
python main.py
```

Expected output:

```
Savings tracker bot is running...
```

## Telegram Commands

### Help

- `/help` - Displays all available commands

### Item Commands

- `/items_add <amount> <note>` - adds a transaction (item) i.e. `/items_add -250 groceries`
- `/items_delete <id>` - deletes a transaction (item) i.e. `/items_delete 2`
- `/items_get` lists items i.e. `/items_get`
- `/items_get head=<head>` lists the latest items i.e. `/latest_items head=5` lists the latest 5 items
- `/items_get tail=tail` lists the first items i.e. `/latests_items tail=5` lists the fist 5 items that inserted in the worksheet

### Worksheet Commands

- `/worksheets_add <title>` - adds a worksheet i.e. `/worksheet_add GCash2`
- `/worksheets_delete <title>` - deletes an existing worksheet (can't delete an active worksheet) i.e. `/worksheets_delete Paypal2`
- `/worksheets_get` - lists all worksheets

### Active Worksheet Commands

- `/active_worksheet` - displays the name of the active worksheet
- `/active_worksheet <title>` - change active worksheet i.e. `/active_worksheet Gcash2`
- `/summary` - summarizes the active worksheet
- `/filter start_day=<d> start_month=<m> start_year=<y> end_day=<d> end_month=<m> end_year=<y>` - summarizes the worksheet filtered on the starting date and end month
  i.e. `/filter start_day=1 start_month=5 start_year=2026 end_day=30 end_month=5 end_year=2026`

## Environment Variables

```
TELEGRAM_API_KEY=your_telegram_bot_token
SPREADSHEET_URL=your_spreadsheet_url
```

## Credentials

Place your Google Service Account at:

- `auth/service_credentials.json`

## Notes

- Item refer to transaction
- Item with negative amount is an expense
- Worksheet refers to the sheet inside the spreadsheet file
- summary and filter only works on the active worksheet

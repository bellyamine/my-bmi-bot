# My BMI Bot

A small Telegram bot that calculates BMI from a weight and height message. This is a learning and entertainment project, not a medical tool.

## Requirements

- Python 3
- A Telegram bot token from [BotFather](https://t.me/BotFather)

Install the dependency:

```bash
python3 -m pip install -r requirements.txt
```

## Run locally on Linux

Set your token as an environment variable in the same terminal session. Replace the example text locally; do not paste your token into source code or commit it to GitHub.

```bash
export TELEGRAM_BOT_TOKEN='paste-your-token-here'
python3 bmi_bot.py
```

If the terminal reports that `TELEGRAM_BOT_TOKEN` is missing, set the variable in that terminal before running the script.

## Use

Send `/start` to the bot, then send your weight in kilograms and height in metres separated by a space, for example:

```text
70 1.75
```

The bot checks that both values are positive numbers. The BMI categories and messages are playful project behavior and should not be treated as medical advice.

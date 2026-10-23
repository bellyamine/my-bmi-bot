import math
import os

import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise SystemExit(
        "Error: TELEGRAM_BOT_TOKEN is missing. Set it in your terminal before running the bot."
    )

bot = telebot.TeleBot(TOKEN)


# Welcome message when the user sends /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "مرحباً! أرسل وزنك وطولك هكذا (الوزن ثم الطول مفصولين بمسافة، مثلا: 70 1.75)",
    )


# Receive weight and height, then calculate BMI
@bot.message_handler(func=lambda message: True)
def calculate_bmi(message):
    if not message.text:
        bot.reply_to(message, "يرجى إرسال الوزن والطول كأرقام، مثال: 70 1.75")
        return

    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "يرجى إرسال رقمين فقط: الوزن ثم الطول، مثال: 70 1.75")
        return

    try:
        weight = float(parts[0])
        height = float(parts[1])
    except ValueError:
        bot.reply_to(message, "خطأ! يرجى إرسال أرقام صحيحة، مثال: 70 1.75")
        return

    if not math.isfinite(weight) or not math.isfinite(height) or weight <= 0 or height <= 0:
        bot.reply_to(message, "يجب أن يكون الوزن والطول رقمين موجبين وصالحين.")
        return

    name = message.from_user.first_name or "User"
    bmi = weight / height**2

    bot.reply_to(message, f"Your BMI is: {round(bmi, 2)}")

    # Keep the project's original playful response categories.
    if bmi < 18.5:
        bot.send_message(message.chat.id, f"{name} you are Underweight")
    elif 22 <= bmi <= 23:
        bot.send_message(message.chat.id, f"{name} You are absolutly perfect")
    elif 18.5 <= bmi <= 24.9:
        bot.send_message(message.chat.id, f"{name} you are Normal")
    elif 25 <= bmi <= 29.9:
        bot.send_message(message.chat.id, f"{name} you are Overweight, do some sport bro")
    elif 30 <= bmi <= 35:
        bot.send_message(
            message.chat.id,
            f"{name} you are obese, you need a Medical consultation",
        )
    else:
        bot.send_message(message.chat.id, f"{name} Fuck you")


print("Bot is running...")
bot.infinity_polling()

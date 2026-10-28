import os
import telebot

# Reading the token from the device (server)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError(" Bot token not found! Make sure to set the environment variable. BOT_TOKEN.")

# bot Token
bot = telebot.TeleBot(TOKEN)

# When the user sends /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Body Mass Index (BMI) bot!\n Please send your details in the following format:\n Weight (kg) Height (in meters)\n Example: 70 1.75")

# Receiving messages and calculating BMI
@bot.message_handler(func=lambda message: True)
def calculate_bmi(message):
    try:
        parts = message.text.split()
        w = float(parts[0])
        h = float(parts[1])
        name = message.from_user.first_name
        
        bmi = w / (h ** 2)
        bmi_rounded = round(bmi, 2)
        
        if bmi < 18.5:
            reply = f"{name}, Your BMI result is: {bmi_rounded}.\n You are Underweight"
        elif 22 <= bmi <= 23:            
            reply = f"{name}, Your BMI result is: {bmi_rounded}.\n You are absolutely perfect! 🔥"
        elif 18.5 <= bmi <= 24.9:
            reply = f"{name}, Your BMI result is: {bmi_rounded}.\n You are Normal"
        elif 25 <= bmi <= 29.9:
            reply = f"{name}, Your BMI result is: {bmi_rounded}.\n You are Overweight, do some sport bro"
        elif 30 <= bmi <= 35:
            reply = f"{name}, Your BMI result is: {bmi_rounded}.\n You are obese, you need a Medical consultation"
        else:
            reply = f"{name}, Your BMI result is: {bmi_rounded}.\n You need medical consultation quickly."
            
        bot.reply_to(message, reply)
        
    except Exception as e:
        bot.reply_to(message, "Incorrect input format! Please enter your weight followed by your height, separated by a space—for example: 70 1.75")

# Run the bot
print("Bot is running...")
bot.polling()

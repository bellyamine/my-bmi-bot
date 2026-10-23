import os
import telebot

# ضع التوكن الذي أعطاك إياه BotFather هنا بين القوسين
TOKEN = ""
bot = telebot.TeleBot(TOKEN)

# عندما يرسل المستخدم /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في بوت حساب كتلة الجسم (BMI)! أرسل بياناتك بهذا الشكل:\nالوزن (كغ) الطول (بالمتر)\nمثال: 70 1.75")

# استقبال الرسائل وحساب الـ BMI
@bot.message_handler(func=lambda message: True)
def calculate_bmi(message):
    try:
        parts = message.text.split()
        w = float(parts[0])
        h = float(parts[1])
        name = message.from_user.first_name
        
        bmi = w / (h ** 2)
        bmi_rounded = round(bmi, 2)
        
        # الشروط التي برمجناها سابقاً
        if bmi < 18.5:
            reply = f"{name}, النتيجة {bmi_rounded}: you are Underweight"
        elif 22 <= bmi <= 23:
            reply = f"{name}, النتيجة {bmi_rounded}: You are absolutely perfect! 🔥"
        elif 18.5 <= bmi <= 24.9:
            reply = f"{name}, النتيجة {bmi_rounded}: you are Normal"
        elif 25 <= bmi <= 29.9:
            reply = f"{name}, النتيجة {bmi_rounded}: you are Overweight, do some sport bro"
        elif 30 <= bmi <= 35:
            reply = f"{name}, النتيجة {bmi_rounded}: you are obese, you need a Medical consultation"
        else:
            reply = f"{name}, النتيجة {bmi_rounded}: Fuck you 😂"
            
        bot.reply_to(message, reply)
        
    except Exception as e:
        bot.reply_to(message, "خطأ في طريقة الإدخال! يرجى إرسال الوزن ثم الطول مفصولين بمسافة، مثل: 70 1.75")

# تشغيل البوت
print("Bot is running...")
bot.polling()

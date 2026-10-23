import telebot
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
# رسالة الترحيب عند الضغط على /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أرسل وزنك وطولك هكذا (الوزن ثم الطول مفصولين بمسافة، مثلا: 70 1.75)")

# استقبال الوزن والطول وتطبيق كودك
@bot.message_handler(func=lambda message: True)
def calculate_bmi(message):
    try:
        # قراءة الوزن والطول من رسالة المستخدم في تيليجرام
        parts = message.text.split()
        w = float(parts[0])
        h = float(parts[1])
        n = message.from_user.first_name # اسم المستخدم على تيليجرام
        
        # كودك الأصلي تماماً:
        bmi = w / h**2
        
        # نرسل النتيجة للمستخدم كرسالة أولى
        bot.reply_to(message, f"Your BMI is: {round(bmi, 2)}")
        
        # شروطك أنت:
        if bmi < 18.5:
            bot.send_message(message.chat.id, f"{n} you are Underweight")
        elif bmi >= 22 and bmi <= 23:
            bot.send_message(message.chat.id, f"{n} You are absolutly perfect")
        elif bmi >= 18.5 and bmi <= 24.9:
            bot.send_message(message.chat.id, f"{n} you are Normal")
        elif bmi >= 25 and bmi <= 29.9:
            bot.send_message(message.chat.id, f"{n} you are Overweight, do some sport bro")
        elif bmi >= 30 and bmi <= 35:
            bot.send_message(message.chat.id, f"{n} you are obese, you need a Medical consultation")
        else:
            bot.send_message(message.chat.id, f"{n} Fuck you")
            
    except Exception as e:
        bot.reply_to(message, "خطأ! يرجى إرسال الأرقام بشكل صحيح، مثال: 70 1.75")

# تشغيل البوت
print("Bot is running...")
bot.polling()

import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz

# === НАСТРОЙКИ ===
BOT_TOKEN = "8434839569:AAGIhlPUxklWMiUwdDbVVCyMw3cMSscgttM"  # ← замени на свой!
TIMEZONE = "Europe/Moscow"       # ← замени на свою зону

# 🖼️ Картинка для напоминания (публичный URL)
CHILL_IMAGE_URL = "https://i.imgur.com/mD9Uk1L.jpg"  # котик отдыхает 😺

bot = telebot.TeleBot(BOT_TOKEN)
scheduler = BackgroundScheduler(timezone=pytz.timezone(TIMEZONE))
active_users = set()

def get_done_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("✅ Отдохнул(а)", callback_data="done")
    markup.add(button)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    active_users.add(message.chat.id)
    bot.send_message(
        message.chat.id,
        "Привет, дружище! 🌼\n\n"
        "Я твой личный chill-бот. 💭\n"
        "Каждый час с 10:00 до 18:00 я буду мягко напоминать тебе:\n"
        "«Эй, пора немного отключиться и подышать».\n\n"
        "Просто нажми кнопку, когда сделаешь перерыв — и я обниму тебя мысленно 🤗"
    )

@bot.callback_query_handler(func=lambda call: call.data == "done")
def handle_done(call):
    bot.answer_callback_query(call.id, "Ты молодец! 🌈")
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption="✨ Отдых засчитан! Ты — суперзвезда.\nПродолжай в том же духе, но не забывай про себя 💛",
        reply_markup=None
    )

def send_chill_reminder():
    now = datetime.now(pytz.timezone(TIMEZONE))
    for user_id in list(active_users):
        try:
            bot.send_photo(
                chat_id=user_id,
                photo=CHILL_IMAGE_URL,
                caption=(
                    f"🌤️ {now.strftime('%H:%M')} — Время немного отпустить всё.\n\n"
                    "Встань, потянись, посмотри в окно, выпей воды или просто помолчи 2 минуты.\n\n"
                    "Ты работаешь — но не забывай, что *ты важнее задач*.\n\n"
                    "Когда отдохнёшь — нажми кнопку ниже 👇"
                ),
                reply_markup=get_done_markup()
            )
        except Exception as e:
            print(f"Ошибка отправки {user_id}: {e}")
            active_users.discard(user_id)

# ⏰ Напоминания каждый час с 10:00 до 18:00
scheduler.add_job(
    send_chill_reminder,
    CronTrigger(hour='10-18', minute=0, timezone=TIMEZONE)
)

if __name__ == '__main__':
    scheduler.start()
    print("✅ Chill-бот запущен. Напоминания с 10:00 до 18:00.")
    bot.infinity_polling()
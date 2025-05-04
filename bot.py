import logging
import random
from datetime import datetime, time, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

# Конфигурация
TOKEN = "7910570129:AAFR8UvGLoVcdr0CjTUrTNCq-U2HkBwhN2c"
ALLOWED_USERNAME = "normalnaya63"
DEMOBEL_DATE = datetime(2025, 6, 24).date()
MOSCOW_TZ = timezone(timedelta(hours=3))

SWEET_MESSAGES = [
    {
        "text": "Привет Валентина! 👋 Короче, если ты это читаешь, значит я таки поставил ёбаного бота на хостинг! 💻 Люблю тебя! ❤️🔥",
        "photo": None
    },
    {
        "text": "До дембеля халява осталась, а я уже не знаю чем заняться... 🥱 Держи мой тост на свадьбе! 🥂",
        "photo": "https://cs20.pikabu.ru/s/2025/05/05/00/6nk2xrtx.webp"
    },
    {
        "text": "Привет Валентинка, безумно люблю тебя! 💘",
        "photo": None
    },
    {
        "text": "Дарова Любимыч-Валентиныч, сегодня ты прекрасна как и всегда! 👑",
        "photo": None
    },
    {
        "text": "Валентина, тебе очень идёт твой новый цвет волос! 💇♀️✨",
        "photo": None
    },
    {
        "text": "Моя любовь, вот тебе смешная картинка: Пасини Кактусини 🌵",
        "photo": "https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_67feb37de1caa514ea249051_67feb767e350361bd67ebcb3/scale_720"
    },
    {
        "text": "А вот тебе Я в будущем: Саламоне Тренболон 🐟💪",
        "photo": "https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_67feb37de1caa514ea249051_67feb5aac05ff97f14cf0cf8/scale_720"
    },
    {
        "text": "Валентина, сегодня ты просто бомба! 💣🔥",
        "photo": None
    },
    {
        "text": "Валентина Ильинична, вы обвиняетесь по статье 12.5.1. Изменение в конструкции и впоследствии доведение до состояния безумной любви! ⚖️💞",
        "photo": None
    },
    {
        "text": "Валентина, а ты ниче такая кстати 😏",
        "photo": None
    },
    {
        "text": "Любимка, ты самая лучшая! Осталось совсем чуть чуть ⏳💖",
        "photo": None
    },
    {
        "text": "Со временем у меня закончились фразы, но вот тебе очередное итальянское животное: Корво Песконессо 🐦",
        "photo": "https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_67feb37de1caa514ea249051_67feb90a4eceef3c6dd6d6f2/scale_720"
    },
    {
        "text": "Сейчас я снова не смог придумать фразу, но вот тебе ещё одно животное: Тиграттор Радиаттор 🐯⚡",
        "photo": "https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_67feb37de1caa514ea249051_67feb8727c0c2872e1fcac9c/scale_720"
    },
    {
        "text": "Просто очень сильно тебя люблю 💌",
        "photo": None
    },
    {
        "text": "Ты как всегда самая лучшая! 🏆",
        "photo": None
    },
    {
        "text": "Не устаю до сих пор писать эти сценарии для бота, всё ради тебя, Валентинка! 👩💻❤️",
        "photo": None
    },
    {
        "text": "Надеюсь тебе нравится эта тема с ботом, идея как никак твоя. Вот тебе в награду: Канелонни Драгони 🐉",
        "photo": "https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_67feb37de1caa514ea249051_67feb47720c968560e05e901/scale_1200"
    },
    {
        "text": "Шел 539 день как я пишу эти фразы... Вот тебе Дельфинатор Культиватор 🐬🔧",
        "photo": "https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_67feb37de1caa514ea249051_67feeb6ee350361bd6b237bc/scale_720"
    },
    {
        "text": "Валентинка, ты — мой личный антистресс! 💆‍♂️❤️ Без тебя дембель казался бы вечностью! ⏳",
        "photo": None
    },
    {
        "text": "Любимка, сегодня твои глаза ярче всех эмодзи в этом списке! 👀✨",
        "photo": None
    },
    {
        "text": "Валентина Ильинична! 🧐 Вы нарушаете статью 228.15 — чрезмерная милота! 🚔💘",
        "photo": None
    },
    {
        "text": "Валентина, ты как кофе ☕️ — бодришь даже в 6 утра на построении! 💂‍♀️",
        "photo": None
    },
    {
        "text": "Любимка, представляешь? 🤯 Когда ты рядом, даже «отжимания до упора» кажутся приколом! 💪😂",
        "photo": None
    },
    {
        "text": "Валентинка, ты единственная, кто может заставить меня чистить картошку с улыбкой! 🥔😁",
        "photo": None
    },
    {
        "text": "Валентина Ильинична! 🎖️ Вам присвоено звание «Главнокомандующий моего сердца»! 💞",
        "photo": None
    },
    {
        "text": "Валентинка, ты как дембельский альбом 📖 — такая же яркая и долгожданная! 🎉",
        "photo": None
    },
    {
        "text": "Валентина Ильинична! 🔍 Обнаружена угроза: ваша улыбка вызывает ЧП в моем сердце! 💥",
        "photo": None
    },
    {
        "text": "Валентина, ты — мой личный «устав», который хочется соблюдать! 📜❤️",
        "photo": None
    },
    {
        "text": "Любимка, с тобой даже солдатская каша 🥣 кажется десертом! 🍮",
        "photo": None
    },
    {
        "text": "Валентинка, если бы ты была ротой, то точно «ротой моей мечты»! 💂‍♂️💭",
        "photo": None
    },
    {
        "text": "Валентина Ильинична! ⚖️ Суд признал: вы виновны в краже моего спокойствия! 👮♂️💘",
        "photo": None
    },
    {
        "text": "Любимка, ты как дембельский отсчет ⏳ — с тобой время летит незаметно! ✈️",
        "photo": None
    },
    {
        "text": "Валентина, ты — мой единственный «неуставной» интерес! 😉🔍",
        "photo": None
    },
    {
        "text": "Валентинка, ты как армейский паёк — идеальна по составу! 🥫💯",
        "photo": None
    },
    {
        "text": "Любимка, если бы ты была нарядом 🦺, я бы ходил в него добровольно! 😄",
        "photo": None
    }
]

FORBIDDEN_MESSAGES = [
    "🚫 Ты не Валентинка! Уходи!",
    "🚫 Это не для тебя, уходи",
    "🚫 Сорян бро, это было написано не для тебя"
]

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def is_allowed_user(user) -> bool:
    return user.username.lower() == ALLOWED_USERNAME.lower() if user else False

def days_until_demebel() -> int:
    now = datetime.now(MOSCOW_TZ).date()
    return (DEMOBEL_DATE - now).days if DEMOBEL_DATE > now else 0

def get_day_suffix(days: int) -> str:
    if 11 <= days % 100 <= 14:
        return "дней"
    return {1: "день", 2: "дня", 3: "дня", 4: "дня"}.get(days % 10, "дней")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        if not is_allowed_user(user):
            await update.message.reply_text(random.choice(FORBIDDEN_MESSAGES))
            return

        keyboard = [[InlineKeyboardButton("💌 Получить сообщение сейчас", callback_data='extra_msg')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if 'job' not in context.user_data:
            target_time = time(20, 0, tzinfo=MOSCOW_TZ)
            
            context.job_queue.run_daily(
                send_sweet_message,
                time=target_time,
                days=tuple(range(7)),
                chat_id=user.id,
                name=f"daily_{user.id}"
            )
            
            await update.message.reply_text(
                "Привет, Валентинка! Буду радовать тебя каждый день в 20:00! 💌",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "Ты уже подписана на ежедневные сообщения! 😊",
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Ошибка в /start: {e}")

async def send_message_with_photo(context, chat_id, message_data):
    try:
        text = message_data["text"]
        photo_url = message_data["photo"]
        
        days_left = days_until_demebel()
        countdown = ("\n\n🎉 Дембель сегодня! 🎉" if days_left == 0 
                    else f"\n\n⏳ До дембеля: {days_left} {get_day_suffix(days_left)}!")
        
        full_text = text + countdown
        
        if photo_url:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo_url,
                caption=full_text
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=full_text
            )
    except Exception as e:
        logger.error(f"Ошибка отправки: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Не удалось отправить картинку 😢\n{full_text}"
        )

async def send_sweet_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    message_data = random.choice(SWEET_MESSAGES)
    await send_message_with_photo(context, job.chat_id, message_data)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        
        if not is_allowed_user(query.from_user):
            await query.edit_message_text("🚫 Эта кнопка не для тебя!")
            return
        
        message_data = random.choice(SWEET_MESSAGES)
        await send_message_with_photo(context, query.from_user.id, message_data)
    except Exception as e:
        logger.error(f"Ошибка обработки кнопки: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        if not is_allowed_user(user):
            await update.message.reply_text(random.choice(FORBIDDEN_MESSAGES))
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка: {context.error}", exc_info=True)

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()

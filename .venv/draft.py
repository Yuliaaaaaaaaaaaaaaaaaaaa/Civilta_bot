import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
import datetime
import random

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Токен вашего бота (замените на свой)
BOT_TOKEN = '7606085998:AAFy_zhmnPpx2YXG_2SWO8UaXs3G9zA8be0'

# Данные для бота
his_dat = ['Когда родился Данте Алигьери?', 'Когда родился Рафаэлло Санцио?', 'Когда Италия вступила в ВОВ?']

# Клавиатура
keyboard = [
    ['/culture', '/geography'],
    ['/with_picture', '/history'],
    ['/help']
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение и клавиатуру."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот по изучению лингвострановедения Италии! Выбери, что хочешь изучить:",
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение со списком команд."""
    await update.message.reply_text(
        "Выбери интересующую тебя тему на клавиатуре.\n"
        "/culture: задание по культуре Италии\n"
        "/geography: задание по географии Италии\n"
        "/with_picture: задание с картинкой про Италию\n"
        "/history: задание по истории Италии\n"
        "/time: текущее время",
        reply_markup=reply_markup, #Обновляем клавиатуру
    )


async def with_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение (пока ничего нет)."""
    await update.message.reply_text('сори тут ниче нет', reply_markup=reply_markup) #Обновляем клавиатуру


async def culture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение (пока ничего нет)."""
    await update.message.reply_text('сори тут ниче нет', reply_markup=reply_markup) #Обновляем клавиатуру


async def geography(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение (пока ничего нет)."""
    await update.message.reply_text('сори тут ниче нет', reply_markup=reply_markup) #Обновляем клавиатуру


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет случайный вопрос по истории Италии."""
    i = random.randint(0, len(his_dat) - 1)
    await update.message.reply_text(his_dat[i], reply_markup=reply_markup) #Обновляем клавиатуру


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Эхо-ответ на любое текстовое сообщение, кроме команд."""
    await update.message.reply_text('да, правильно', reply_markup=reply_markup) #Обновляем клавиатуру


# Главная функция
def main() -> None:
    """Запускает бота."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("culture", culture))
    application.add_handler(CommandHandler("geography", geography))
    application.add_handler(CommandHandler("with_picture", with_picture))
    application.add_handler(CommandHandler("history", history))

    # Обработчик текста (эхо)
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(text_handler)

    # Запуск бота
    application.run_polling()


# Запуск main()
if __name__ == '__main__':
    main()
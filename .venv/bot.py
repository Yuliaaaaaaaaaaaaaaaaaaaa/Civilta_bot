import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
import datetime
import random


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
BOT_TOKEN = '7606085998:AAFy_zhmnPpx2YXG_2SWO8UaXs3G9zA8be0'
com = {
    'culture': 'отправляю задание по культуре Италии',
    'geograhpy': 'отправляю задание по географии Италии',
    'with_picture': 'отправляю задание с картинкой',
    'history': 'отправляю задание по истории Италии',

}

his_dat = ['Когда родился Данте Алигьери?', 'Когда родился Рафаэлло Санцио?', 'Когда Италия вступила в ВОВ?']
async def echo(update, context):
    await update.message.reply_text('да, правильно')


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот по изучению лингвострановедения Италии! Выбери, что хочешь изучить, с помощью кнопки 'help'",
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    global com
    await update.message.reply_text(
    "/culture: отправляю задание по культуре Италии, /geograhpy: отправляю задание по географии Италии, /with_picture: отправляю задание с картинкой про Италию, /history: отправляю задание по истории Италии")


async def time(update, context):
    await update.message.reply_text(datetime.datetime.now().strftime('%H:%M:%S'))


async def with_picture(update, context):
    await update.message.reply_text('сори тут ниче нет')


async def culture(update, context):
    await update.message.reply_text('сори тут ниче нет')


async def geography(update, context):
    await update.message.reply_text('сори тут ниче нет')


async def history(update, context):
    global his_dat
    i = random.randint(0, len(his_dat) - 1)
    await update.message.reply_text(his_dat[i])


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("culture", culture))
    application.add_handler(CommandHandler("geography", geography))
    application.add_handler(CommandHandler("with_picture", with_picture))
    application.add_handler(CommandHandler("history", history))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
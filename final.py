import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
import datetime
import random
import sqlite3
from telegram.helpers import escape_markdown
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Токен вашего бота (замените на свой)
BOT_TOKEN = '7606085998:AAFy_zhmnPpx2YXG_2SWO8UaXs3G9zA8be0'
IMAGE_DIRECTORY = "data"
# Данные для бота
global answer_q
global ques_q
global wrong_answers
answer_q = ''
answer_q1 = ''
ques_q = ''
wrong_answers = []
# Клавиатура
keyboard = [
    ['/culture', '/geography'],
    ['/with_picture', '/history'],
    ['/help', '/mistakes']
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
    user_id = update.effective_user.id
    username = update.effective_user.username

    conn = sqlite3.connect('Game.db')
    cursor = conn.cursor()

    # Check if the user already exists
    cursor.execute("SELECT 1 FROM Users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        logger.info(f"Пользователь {username} ({user_id}) уже зарегистрирован.")

    else:
        # Add the user to the database
        cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
        logger.info(f"Пользователь {username} ({user_id}) успешно зарегистрирован.")
    conn.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение со списком команд."""
    await update.message.reply_text(
        "Выбери интересующую тебя тему на клавиатуре.\n"
        "/culture: задание по культуре Италии\n"
        "/geography: задание по географии Италии\n"
        "/with_picture: задание с картинкой про Италию\n"
        "/mistakes: можно посмотреть свои ошибки\n"
        "/history: задание по истории Италии",
        reply_markup=reply_markup, #Обновляем клавиатуру
    )


async def with_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends an image from the 'data' directory with a caption."""
    try:
        i = random.randint(0, len(Pictures) - 1)
        IMAGE_NAME = Pictures[i][3]
        CAPTION = Pictures[i][0]
        global answer_q
        global ques_q
        global answer_q1
        answer_q1 = Pictures[i][1]
        answer_q = Pictures[i][2]
        ques_q = Pictures[i][0]
        image_path = os.path.join(IMAGE_DIRECTORY, IMAGE_NAME)
        with open(image_path, "rb") as f:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=f, caption=CAPTION)
            logger.info(f"Картинка с подписью успешно отправлена пользователю {update.effective_user.username}")

    except FileNotFoundError:
        await update.message.reply_text("Ошибка: Картинка не найдена.")
        logger.error(f"Ошибка: Картинка '{image_path}' не найдена.")
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при отправке картинки.")
        logger.error(f"Ошибка при отправке картинки: {e}")


async def culture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    i = random.randint(0, len(Culture) - 1)
    global answer_q
    global ques_q
    answer_q = Culture[i][1]
    ques_q = Culture[i][0]
    await update.message.reply_text(Culture[i][0], reply_markup=reply_markup)  # Обновляем клавиатуру

async def geography(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение (пока ничего нет)."""
    i = random.randint(0, len(Geography) - 1)
    global answer_q
    global ques_q
    answer_q = Geography[i][1]
    ques_q = Geography[i][0]
    await update.message.reply_text(Geography[i][0], reply_markup=reply_markup)  # Обновляем клавиатуру


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет случайный вопрос по истории Италии."""
    i = random.randint(0, len(History) - 1)
    global answer_q
    global ques_q
    answer_q = History[i][1]
    ques_q = History[i][0]
    await update.message.reply_text(History[i][0], reply_markup=reply_markup)  # Обновляем клавиатуру


async def mistakes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    s = ""  # Инициализируем как пустую строку
    k = 0

    for question, correct, user_answer in wrong_answers:
        k += 1
        # Экранируем все компоненты
        safe_question = escape_markdown(str(question), version=2)
        safe_correct = escape_markdown(str(correct), version=2)
        safe_user = escape_markdown(str(user_answer), version=2)

        # Форматируем строку с ошибкой (экранируем спецсимволы)
        error_str = (
            f"{k}\\. {safe_question}\n"
            f"*Правильный ответ*\: {safe_correct}\n"
            f"~Ваш ответ~\: {safe_user}\n\n"
        )

        s += error_str  # Добавляем к основной строке

    if s:
        await update.message.reply_text(
            f"🚫 Ошибки:\n\n{s}",
            parse_mode='MarkdownV2',
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("🎉 Имба, ошибок нет!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Эхо-ответ на любое текстовое сообщение, кроме команд."""
    global answer_q
    global ques_q
    global answer_q1
    if answer_q1 == '':
        ans = answer_q
        if ans.lower() != update.message.text.lower():
            if (ques_q, answer_q, update.message.text) not in wrong_answers:
                wrong_answers.append((ques_q, answer_q, update.message.text))
        safe_ans = escape_markdown(str(answer_q), version=2)
    else:
        ans = answer_q1
        if ans.lower() != update.message.text.lower():
            if (ques_q, answer_q, update.message.text) not in wrong_answers:
                s = f"{ans} Доп инфа: {answer_q}"
                wrong_answers.append((ques_q, s, update.message.text))
        safe_ans = escape_markdown(str(answer_q1), version=2)
        answer_q1 = ''
    message = f"_Молодец\!_\n*Правильный ответ*\: {safe_ans}"

    await update.message.reply_text(
        message,
        parse_mode='MarkdownV2',
        reply_markup=reply_markup
    )

# Главная функция
def main() -> None:
    """Запускает бота."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mistakes", mistakes))
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
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('Game.db')
    cursor = connection.cursor()

    # Создаем таблицу
    # ПЕРВАЯ ТАБЛИЦА (культура)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Culture (
            question TEXT,
            answer TEXT
            )
            ''')

    cursor.execute('''
        INSERT INTO Culture (question, answer) VALUES
        ('Il motto di Caio Giuglio Cesare', 'Aut Caesar, aut nullus'),
        ('Che cosa Caio Giuglio Cesare portava sempre', 'la corona d’alloro'),
        ('Il libro più famoso di Caio Giuglio Cesare che parla della sua impresa più importante si chiama...', 'De bello gallico'),
        ('Il famoso detto che nasce quando Cesare torna dalla Gallia', 'passare il Rubicone'),
        ('Il motto di Caio Giuglio Cesare relativo a Bruto', 'ANCHE TU, BRUTO, FIGLIO MIO'),
        ('l’abbigliamento tipico dell’epoca fatto di lino e lana è...', 'tunica'),
        ('la giacca e cravatta dell’epoca romana, poteva essere indossata solo dai cittadini romani è...', 'toga'),
        ('(I romani) signori del mondo, popolo...', 'togato'),
        ('Qual è il nome di un luogo in un monastero dove si preparano le cure a base di erbe?', 'L’erboristeria'),
        ('Qual è il nome di un luogo in un monastero dove i monaci si lavano?', 'Il lavatorium'),
        ('Qual è il nome di un luogo in un monastero dove i monaci mangiano in silenzio?', 'Il refettorio'),
        ('Qual è il nome di un luogo in un monastero dove i monaci possono camminare e pregare?', 'Il chiostro'),
        ('La campana della cattedrale serviva per indicare le ore, e per comunicare le cose più importanti (la guerra, la pace, la festa, ecc.). È vero?', 'Sì'),
        ('Di che cosa vetrate, mosaici, affreschi sono gli elementi principali?', 'Cattedrale medievale')
        
        
        
        
        ''')

    # ВТОРАЯ ТАБЛИЦА (History)
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS History (
                question TEXT,
                answer TEXT
                )
                ''')

    cursor.execute('''
            INSERT INTO History (question, answer) VALUES ('Quando con la deposizione dell’ultimo imperatore Romolo Augustolo cadde l’Impero Romano dell’Occidente?', '476 d.C'),
            ('Quale periodo di tempo è chiamato Alto Medioevo (ossia Primo Medioevo)?', '476 d.C - 1000'),
            ('Quale periodo di tempo è chiamato Basso Medioevo (ossia Secondo Medioevo)?', '1000 - 1492'),
            ('L’universita di Bologna fu fondata nel...', '1088'),
            ('Quando i vandali saccheggiano Roma?', '410 d.C'),
            ('La chiesa e signori feudali sono due elementi fondamentali del mondo...', 'Medievale'),
            ('Fondazione di Roma?', '753 a.C'),
            ('Conquista della Gallia?', '52 a.C'),
            ('Incendio di Roma?', '64 d.C'),
            ('Anni della costruzione del Colosseo?', '72 d.C - 80 d.C'),
            ('Eruzione del Vesuvio?', '79 d.C'),
            ('Massima espansione dell’impero?', '117 d.C'),
            ('Sotto quale imperatore, nel 117, Roma raggiunge la sua massima espansione?', 'Traiano'),
            ('Caracalla, Diocleziano... nome della dinastia?', 'Dinastia dei Severi'),
            ('Costantino I il Grande, Teodosio I il Grande... nome della dinastia?', 'Dinastia dei Flavi'),
            ('Sotto quale imperatore si sono verificati questi eventi: (inaugurazione del Colosseo, eruzione del Vesuvio il 79 d.C', 'Tito'),
            ('Caduta dell’impero romano d’Occidente?', '476 d.C'),
            ('Anni della vita di Caio Giuglio Cesare?', '100 a.C - 44 a.C'),
            ('Le quattro lettere che in latino definivano il Senato e il Popolo Romano', 'SPQR'),
            ('Dopo le quattro vittorie sui galli, sull’Egitto, in Asia e in Spagna, Caio Giulio Cesare riceve il titolo', 'dittatore a vita'),
            ('Il primo imperatore?', 'Ottaviano Augusto'),
            ('Quanti anni regnò Ottaviano Augusto', '45'),
            ('Ottaviano Augusto fu "princeps pari"?', 'Sì'),
            ('Tiberio, Caligola, Nerone... nome della dinastia?', 'Giulio-Claudio'),
            ('Vespasiano, Tito... nome della dinastia?', 'Dinastia dei Flavi (1)'),
            ('Traiano, Adriano... nome della dinastia?', 'Dinastia degli Antonini'),
            ('Sotto quale imperatore, nel 117, Roma raggiunge la sua massima espansione?', 'Traiano'),
            ('Caracalla, Diocleziano... nome della dinastia?', 'Dinastia dei Severi'),
            ('Costantino I il Grande, Teodosio I il Grande... nome della dinastia?', 'Dinastia dei Flavi (2)'),
            ('Sotto quale imperatore si sono verificati questi eventi: (inaugurazione del Colosseo, eruzione del Vesuvio il 79 d.C', 'Tito'),
            ('Chi è noto per la sua crudeltà e ordinò l’arresto e la condanna a morte di Pilato?', 'Tiberio'),
            ('Chi fece nominare senatore il proprio cavallo?', 'Caligola'),
            ('La chiesa e signori feudali sono due elementi fondamentali del mondo...', 'Medievale'),
            ('L’Università più antica d’Europa è', 'L’Università di Bologna')
            ''')

    # ТРЕТЬЯ ТАБЛИЦА (Geography)
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Geography (
                    question TEXT,
                    answer TEXT
                    )
                    ''')

    cursor.execute('''
                INSERT INTO Geography (question, answer) VALUES ('Quando con la deposizione dell’ultimo imperatore Romolo Augustolo cadde l’Impero Romano dell’Occidente?', '476 d.C'),
                ('Quale periodo di tempo è chiamato Alto Medioevo (ossia Primo Medioevo)?', '476 d.C - 1000'),
                ('Quale periodo di tempo è chiamato Basso Medioevo (ossia Secondo Medioevo)?', '1000 - 1492'),
                ('L’universita di Bologna fu fondata nel...', '1088'),
                ('Quando i vandali saccheggiano Roma?', '410 d.C'),
                ('La chiesa e signori feudali sono due elementi fondamentali del mondo...', 'Medievale'),
                ('Il primo imperatore?', 'OTTAVIANO AUGUSTO'),
                ('Quanti anni regnò Ottaviano Augusto', '45'),
                ('Ottaviano Augusto fu "princeps pari"?', 'si'),
                ('Tiberio, Caligola, Nerone... nome della dinastia?', 'Giulio-Claudio'),
                ('Vespasiano, Tito... nome della dinastia?', 'Dinastia dei Flavi'),
                ('Traiano, Adriano... nome della dinastia?', 'Dinastia degli Antonini'),
                ('Sotto quale imperatore, nel 117, Roma raggiunge la sua massima espansione?', 'Traiano'),
                ('Caracalla, Diocleziano... nome della dinastia?', 'Dinastia dei Severi'),
                ('Costantino I il Grande, Teodosio I il Grande... nome della dinastia?', 'Dinastia dei Flavi'),
                ('Sotto quale imperatore si sono verificati questi eventi: (inaugurazione del Colosseo, eruzione del Vesuvio il 79 d.C', 'Tito'),
                
                
                ('Il famoso detto che nasce quando Cesare torna dalla Gallia', 'passare il Rubicone')
                ''')

    # ЧЕТВЁРТАЯ ТАБЛИЦА (Mistakes)
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Mistakes (
                        question TEXT,
                        answer_correct TEXT,
                        answer_user TEXT
                        )
                        ''')

    # ПЯТАЯ ТАБЛИЦА (With_pictures)
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Pictures (    
                        question TEXT,
                        answer_for_compare TEXT,
                        answer TEXT,
                        pict TEXT
                        )
                        ''')

    cursor.execute('''
                    INSERT INTO Pictures (question, answer_for_compare, answer, pict) VALUES
                    ('Qual è il nome dell’autore del dipinto?', 'LEONARDO DA VINCI', 'Autore è LEONARDO DA VINCI, nome è  Il Cenacolo (l’Ultima Cena), si trova a Chiesa di Santa Maria delle Grazie, Milano', 'Cenacolo.jpg'),
                    ('Come si chiama?', 'Galileo Galilei', 'Galileo Galilei', 'Galileo_Galilei.jpg'),
                    ('Qual è il nome dell’autore del dipinto?', 'LEONARDO DA VINCI', 'Autore è LEONARDO DA VINCI, nome è Gioconda (Monalisa), si trova a Museo del Louvre di Parigi', 'Gioconda.jpg'),
                    ('Qual è il nome dell’autore del dipinto?', 'RAFFAELLO SANZIO', 'Autore è RAFFAELLO SANZIO, nome è La Velata, si trova a Firenze, Palazzo Pitti', 'La_velata_Rafael.jpg'),
                    ('Come si chiama?', 'LEONARDO DA VINCI', 'LEONARDO DA VINCI', 'Leonardo_da_Vinci.jpg'),
                    ('Qual è il nome dell’autore del dipinto?', 'RAFFAELLO SANZIO', 'Autore è RAFFAELLO SANZIO, nome è  Madonna di casa Santi, si trova a Urbino', 'Madonna_di_Casa_Santi.jpg'),
                    ('Qual è il nome dell’autore del dipinto?', 'RAFFAELLO SANZIO', 'Autore è RAFFAELLO SANZIO, nome è Madonna Sistina, si trova Dresda', 'Madonna_Sistina.jpg'),
                    ('Di chi è questa invenzione?', 'LEONARDO DA VINCI', 'Inventore è LEONARDO DA VINCI, nome è "modello di elicottero"', 'modello_di_elicottero.jpg'),
                    ('Di chi è questa invenzione?', 'LEONARDO DA VINCI', 'Inventore è LEONARDO DA VINCI, nome è "ornitottero"', 'ornitottero.jpg'),
                    ('Come si chiama questo posto?', 'Palmanova', 'Palmanova', 'Palmanova.jpg'),
                    ('Come si chiama?', 'Raffaello Sanzio', 'Raffaello Sanzio', 'Raffaello_Sanzio.jpg'),
                    ('Come si chiama questo posto?', 'Terra del Sole', 'Terra del Sole', 'Terra_del_Sole.jpg')
                    ''')

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        user_id INTEGER,
                        username TEXT
                        )
                        ''')

    # создаём массив с данными из таблицы Culture
    cursor.execute("SELECT * FROM Culture")
    Culture = cursor.fetchall()
    print(Culture)
    # создаём массив с данными из таблицы History
    cursor.execute("SELECT * FROM History")
    History = cursor.fetchall()
    # создаём массив с данными из таблицы Geography
    cursor.execute("SELECT * FROM Geography")
    Geography = cursor.fetchall()
    # создаём массив с данными из таблицы Pictures
    cursor.execute("SELECT * FROM Pictures")
    Pictures = cursor.fetchall()

    cursor.execute("SELECT * FROM Users")
    User = cursor.fetchall()
    print(User)

    connection.commit()
    connection.close()
    main()
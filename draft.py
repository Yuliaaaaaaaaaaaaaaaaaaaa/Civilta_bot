import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
import datetime
import random
import sqlite3

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Токен вашего бота (замените на свой)
BOT_TOKEN = '7606085998:AAFy_zhmnPpx2YXG_2SWO8UaXs3G9zA8be0'

# Данные для бота
global answer_q
global ques_q
global wrong_answers
answer_q = ''
ques_q = ''
wrong_answers = []
# Клавиатура
keyboard = [
    ['culture', 'geography'],
    ['with_picture', 'history'],
    ['help']
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
        "/history: задание по истории Италии",
        reply_markup=reply_markup, #Обновляем клавиатуру
    )


async def with_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение (пока ничего нет)."""
    await update.message.reply_text('сори тут ниче нет', reply_markup=reply_markup) #Обновляем клавиатуру


async def culture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    i = random.randint(0, len(Culture) - 1)
    global answer_q
    global ques_q
    answer_q = Culture[i][1]
    ques_q = Culture[i][0]
    await update.message.reply_text(Culture[i][0], reply_markup=reply_markup)  # Обновляем клавиатуру

async def geography(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение (пока ничего нет)."""
    await update.message.reply_text('сори тут ниче нет', reply_markup=reply_markup) #Обновляем клавиатуру


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет случайный вопрос по истории Италии."""
    i = random.randint(0, len(History) - 1)
    global answer_q
    answer_q = History[i][1]
    await update.message.reply_text(History[i][0], reply_markup=reply_markup)  # Обновляем клавиатуру

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Эхо-ответ на любое текстовое сообщение, кроме команд."""
    global answer_q
    global ques_q
    ans = answer_q
    if ans.lower() != update.message.text.lower():
        wrong_answers.append((ques_q, answer_q))
    await update.message.reply_text(f"Молодец!\nПравильный ответ: {ans}", reply_markup=reply_markup) #Обновляем клавиатуру


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
        INSERT INTO Culture (question, answer) VALUES ('Le quattro lettere che in latino definivano il Senato e il Popolo Romano', 'SPQR'),
        ('Il motto di CAIO GIULIO CESARE', 'Aut Caesar, aut nullus'), ('Che cosa CAIO GIULIO CESARE portava sempre', 'la corona d’alloro'),
        ('Il libro più famoso di CAIO GIULIO CESARE che parla della sua impresa più importante si chiama...', 'De bello gallico'),
        ('Dopo le quattro vittorie sui galli, sull’Egitto, in Asia e in Spagna, Caio Giulio Cesare riceve il titolo', 'dittatore a vita'),
        ('Il famoso detto che nasce quando Cesare torna dalla Gallia', 'passare il Rubicone'),
        ('Il motto di CAIO GIULIO CESARE relativo a Bruto', 'ANCHE TU, BRUTO, FIGLIO MIO'),
        ('Il primo imperatore?', 'OTTAVIANO AUGUSTO'),
        ('Quanti anni regnò Ottaviano Augusto', '45'),
        ('Ottaviano Augusto fu "princeps pari"?', 'Sì'),
        ('Tiberio, Caligola, Nerone... nome della dinastia?', 'Giulio-Claudio'),
        ('Vespasiano, Tito... nome della dinastia?', 'Dinastia dei Flavi (1)'),
        ('Traiano, Adriano... nome della dinastia?', 'Dinastia degli Antonini'),
        ('Sotto quale imperatore, nel 117, Roma raggiunge la sua massima espansione?', 'Traiano'),
        ('Caracalla, Diocleziano... nome della dinastia?', 'Dinastia dei Severi'),
        ('Costantino I il Grande, Teodosio I il Grande... nome della dinastia?', 'Dinastia dei Flavi (2)'),
        ('Sotto quale imperatore si sono verificati questi eventi: (inaugurazione del Colosseo, eruzione del Vesuvio il 79 d.C', 'Tito'),
        ('l’abbigliamento tipico dell’epoca fatto di lino e lana è...', 'tunica'),
        ('la giacca e cravatta dell’epoca romana, poteva essere indossata solo dai cittadini romani è...', 'toga'),
        ('(I romani) signori del mondo, popolo...', 'togato'),
        ('La chiesa e signori feudali sono due elementi fondamentali del mondo...', 'Medievale'),
        ('L’Università più antica d’Europa è', 'L’Università di Bologna'),
        ('Qual è il nome di un luogo in un monastero dove si preparano le cure a base di erbe?', 'L’erboristeria'),
        ('Qual è il nome di un luogo in un monastero dove i monaci si lavano?', 'Il lavatorium'),
        ('Qual è il nome di un luogo in un monastero dove i monaci mangiano in silenzio?', 'Il refettorio'),
        ('Qual è il nome di un luogo in un monastero dove i monaci possono camminare e pregare?', 'Il chiostro'),
        ('La campana della cattedrale serviva per indicare le ore, e per comunicare le cose più importanti (la guerra, la pace, la festa, ecc.). È vero?', 'Sì'),
        ('Di che cosa vetrate, mosaici, affreschi sono gli elementi principali?', 'Cattedrale medievale'),
        ('Chi è noto per la sua crudeltà e ordinò l’arresto e la condanna a morte di Pilato?', 'Tiberio'),
        ('Chi fece nominare senatore il proprio cavallo?', 'Caligola'),
        ('Chi è accusato di aver causato il famoso incendio di Roma, si suicidò dopo l’incendio?', 'Nerone'),
        ('Sotto quale imperatore fu costruzione del Colosseo?', 'Vespasiano'),
        ('Chi proibì di uccidere gli schiavi e rafforzò i confini dell’Impero?', 'Adriano'),
        ('Chi concesse il diritto di cittadinanza romana a tutti gli abitanti liberi dell’Impero?', 'Caracalla'),
        ('Chi divise l’Impero nel 286 d.C?', 'Diocleziano'),
        ('Chi riunì l’Impero, contribuì alla diffusione del cristianesimo, il trasferimento della capitale a Bisanzio?', 'Costantino I il Grande'),
        ('Chi fece del Cristianesimo la religione unica e obbligatoria dell’Impero (dopo la sua morte l’Impero si divise di nuovo in due parti)?', 'Teodosio I il Grande')
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
            ('Il primo imperatore?', 'OTTAVIANO AUGUSTO'),
            ('Quanti anni regnò Ottaviano Augusto', '45'),
            ('Ottaviano Augusto fu "princeps pari"?', 'si'),
            ('Tiberio, Caligola, Nerone... nome della dinastia?', 'Giulio-Claudio'),
            ('Vespasiano, Tito... nome della dinastia?', 'Dinastia dei Flavi'),
            ('Traiano, Adriano... nome della dinastia?', 'Dinastia degli Antonini'),
            ('Sotto quale imperatore, nel 117, Roma raggiunge la sua massima espansione?', 'Traiano'),
            ('Caracalla, Diocleziano... nome della dinastia?', 'Dinastia dei Severi'),
            ('Costantino I il Grande, Teodosio I il Grande... nome della dinastia?', 'Dinastia dei Flavi'),
            ('Sotto quale imperatore si sono verificati questi eventi: (inaugurazione del Colosseo, eruzione del Vesuvio il 79 d.C', 'Tito')
            ''')

    # создаём массив с данными из таблицы Maze1
    cursor.execute("SELECT * FROM Culture")
    Culture = cursor.fetchall()
    print(Culture)
    # создаём массив с данными из таблицы Maze2
    cursor.execute("SELECT * FROM History")
    History = cursor.fetchall()

    connection.commit()
    connection.close()
    main()
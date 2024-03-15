import telebot
from telebot import types
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)
# Подключение к базе данных SQLite
conn = sqlite3.connect('terms.db')
cursor = conn.cursor()

# Создание таблицы для хранения терминов
cursor.execute('''CREATE TABLE IF NOT EXISTS terms
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT,
                definition TEXT)''')

conn.commit()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn = sqlite3.connect('terms.db')
    cursor = conn.cursor()
    markup = types.ReplyKeyboardMarkup(row_width=2)
    terms = get_all_terms(cursor)
    for term in terms:
        btn = types.KeyboardButton(term)
        markup.add(btn)
    bot.send_message(message.chat.id, "Выберите термин:", reply_markup=markup)
    conn.close()

# Обработчик нажатий на кнопки
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    conn = sqlite3.connect('terms.db')
    cursor = conn.cursor()
    term_definition = get_definition(cursor, message.text)
    bot.reply_to(message, term_definition)
    conn.close()

# Функция для получения всех терминов из базы данных
def get_all_terms(cursor):
    cursor.execute("SELECT term FROM terms")
    result = cursor.fetchall()
    return [row[0] for row in result]

# Функция для получения определения термина из базы данных
def get_definition(cursor, term):
    cursor.execute("SELECT definition FROM terms WHERE term=?", (term,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return "Определение для этого термина не найдено."

# Запуск бота
bot.polling()
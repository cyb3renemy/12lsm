import os
import pandas as pd
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# створюємо об'єкт бота та підключаємося до Telegram API
updater = Updater(token=os.environ['T5811427895:AAGqu0l6gOaX76KCXfWd0vQb6MrUU79g5qk'])
dispatcher = updater.dispatcher

# створюємо базу даних для зберігання унікальних строчок
db_path = 'db.csv'
if not os.path.exists(db_path):
    pd.DataFrame(columns=['string']).to_csv(db_path, index=False)

# функція для збереження унікальних строчок
def save_unique_strings(strings):
    db = pd.read_csv(db_path)
    new_strings = [s for s in strings if s not in db['string'].values]
    if new_strings:
        new_db = pd.concat([db, pd.DataFrame({'string': new_strings})], ignore_index=True)
        new_db.to_csv(db_path, index=False)

# функція для обробки команди /start
def start(update, context):
    # створюємо кнопку з посиланням на roblox.com
    button = KeyboardButton('roblox.com')
    # створюємо клавіатуру з цією кнопкою
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    # надсилаємо повідомлення з клавіатурою
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Натисніть кнопку, щоб отримати посилання на roblox.com",
                             reply_markup=keyboard)

# функція для обробки файлів, які надіслав користувач
def handle_document(update, context):
    # отримуємо файл
    file = context.bot.get_file(update.message.document.file_id)
    # читаємо файл
    content = file.download_as_bytearray()
    strings = content.decode().split('\n')
    # зберігаємо унікальні строчки в базу даних та надсилаємо їх користувачеві
    save_unique_strings(strings)
    unique_strings = pd.read_csv(db_path)['string'].tolist()
    unique_content = '\n'.join(unique_strings)
    context.bot.send_document(chat_id=update.effective_chat.id,
                              document=unique_content.encode(),
                              filename='unique_strings.txt')
# реєструємо обробники повідомлень та запускаємо бота
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

# додаємо обробник для кнопки "roblox.com"
def handle_button(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="https://www.roblox.com/")
dispatcher.add_handler(CallbackQueryHandler(handle_button, pattern='roblox.com'))

# запускаємо бота
updater.start_polling()
# функція для обробки команди /start
def start(update, context):
    # створюємо кнопку з посиланням на roblox.com
    button = KeyboardButton('roblox.com', callback_data='roblox.com')
    # створюємо клавіатуру з цією кнопкою
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    # надсилаємо повідомлення з клавіатурою
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Натисніть кнопку, щоб отримати посилання на roblox.com",
                             reply_markup=keyboard)

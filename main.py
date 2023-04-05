import os
import pandas as pd
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# читаємо файл бази даних
if os.path.exists("database.txt"):
    df = pd.read_csv("database.txt", header=None, names=["text"])
    existing_texts = set(df.text)
else:
    existing_texts = set()

# обробник команди /start
def start_handler(update, context):
    # створюємо клавіатуру з однією кнопкою
    button = KeyboardButton("roblox.com")
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    
    # відправляємо повідомлення користувачу з клавіатурою
    update.message.reply_text("Натисніть кнопку, щоб почати", reply_markup=reply_markup)

# обробник повідомлень з файлами
def file_handler(update, context):
    file = update.message.document
    if file.mime_type != "text/plain":
        update.message.reply_text("Будь ласка, надішліть файл у форматі .txt")
        return
    
    # зчитуємо файли і порівнюємо з базою
    text = file.get_file().download_as_string().decode("utf-8")
    new_texts = set(text.strip().split("\n")) - existing_texts
    
    if not new_texts:
        update.message.reply_text("Всі стрічки з файлу вже є в базі даних")
        return
    
    # додаємо унікальні строчки в базу
    new_df = pd.DataFrame({"text": list(new_texts)})
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv("database.txt", index=False, header=False)
    
    # створюємо файл з унікальними строчками та відправляємо його користувачу
    unique_text = "\n".join(sorted(new_texts))
    file_bytes = unique_text.encode("utf-8")
    update.message.reply_document(document=file_bytes, filename="unique.txt")

# реєструємо обробники повідомлень та запускаємо бота
updater = Updater(token='5811427895:AAGqu0l6gOaX76KCXfWd0vQb6MrUU79g5qk')
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(MessageHandler(Filters.document, file_handler))
updater.start_polling()
updater.idle()

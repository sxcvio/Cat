import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import requests

    # Токен бота 
TOKEN = 'токен все дела'

    # API-ключ от The Cat API
CAT_API_KEY = 'сайт первый '
CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'

    # получения случайного  кота
def get_random_cat_image():
        headers = {'x-api-key': CAT_API_KEY}
        params = {'mime_types': 'jpg,png', 'limit': 1}
        try:
            response = requests.get(CAT_API_URL, headers=headers, params=params, timeout=5)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()
            return data[0]['url']  # Возвращаем URL изображения
        except (requests.RequestException, IndexError) as e:
            print(f"Ошибка при запросе к Cat API: {e}")
            return None

    
def start(update, context):
        keyboard = [[InlineKeyboardButton("Котик", callback_data='meme')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Нажми кнопку, чтобы получить картинку с котиком!', reply_markup=reply_markup)

    # обработки нажатия кнопки
def button(update, context):
        query = update.callback_query
        query.answer()

        if query.data == 'meme':
            # Получение  изображение кота
            cat_image_url = get_random_cat_image()
            if cat_image_url:
                # Создает кнопку  "Мем"
                keyboard = [[InlineKeyboardButton("Котик", callback_data='meme')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                # Отправляем изображение с кнопкой
                context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=cat_image_url,
                    caption="Вот тебе котик!",
                    reply_markup=reply_markup
                )
            else:
                # Если ошибка
                keyboard = [[InlineKeyboardButton("Картинка котика", callback_data='meme')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="Не удалось загрузить котика, попробуй ещё раз!",
                    reply_markup=reply_markup
                )

def main():
        # инниц-бот
    
        updater = Updater(TOKEN, use_context=True)

        # Регистрация обработчиков
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CallbackQueryHandler(button))

        # Запускается все 
    
        updater.start_polling()
        updater.idle()

if __name__ == '__main__':
        main()

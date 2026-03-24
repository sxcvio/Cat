import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = 'твой_токен'

# API-ключ от The Cat API
CAT_API_KEY = 'твой_ключ'
CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def get_random_cat_image() -> str | None:
    """Возвращает URL случайного изображения кота."""
    headers = {'x-api-key': CAT_API_KEY}
    params = {'mime_types': 'jpg,png', 'limit': 1}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(CAT_API_URL, headers=headers, params=params, timeout=aiohttp.ClientTimeout(total=5)) as response:
                response.raise_for_status()
                data = await response.json()
                return data[0]['url']
    except (aiohttp.ClientError, IndexError) as e:
        logger.error(f"Ошибка при запросе к Cat API: {e}")
        return None


def cat_keyboard() -> InlineKeyboardMarkup:
    """Создаёт inline-клавиатуру с кнопкой котика."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐱 Ещё котик", callback_data="cat")]
    ])


@dp.message(CommandStart())
async def start(message: Message):
    """Обработчик команды /start."""
    await message.answer(
        "Нажми кнопку, чтобы получить картинку с котиком!",
        reply_markup=cat_keyboard()
    )


@dp.callback_query(F.data == "cat")
async def send_cat(callback: CallbackQuery):
    """Обработчик нажатия на кнопку котика."""
    await callback.answer()

    cat_url = await get_random_cat_image()

    if cat_url:
        await callback.message.answer_photo(
            photo=cat_url,
            caption="Вот тебе котик! 🐾",
            reply_markup=cat_keyboard()
        )
    else:
        await callback.message.answer(
            "Не удалось загрузить котика, попробуй ещё раз!",
            reply_markup=cat_keyboard()
        )


async def main():
    """Запуск бота."""
    logger.info("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

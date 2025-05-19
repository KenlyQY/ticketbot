from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Инициализация бота
TOKEN = "7275576099:AAEJhsE-INV2flo4yHEJYh98nfT8-PvPEIs"  # Замените на реальный токен
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# URL вашего Web App (замените на реальный)
WEBAPP_URL = "https://test-bot.githun.io"

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(
            text="📨 Открыть поддержку",
            web_app=types.WebAppInfo(url=WEBAPP_URL)
    ))
    await message.answer(
        "🛠 <b>Техническая поддержка</b>\n\n"
        "Нажмите кнопку ниже, чтобы создать тикет:",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling(bot))

# Обработка данных из Web App
@dp.message_handler(content_types=['web_app_data'])
async def handle_web_app(message: types.Message):
    data = json.loads(message.web_app_data.data)
    if data['action'] == 'create_ticket':
        await message.answer(f"Новый тикет от пользователя {message.from_user.id}:\n{data['text']}")

@dp.message_handler(content_types=['web_app_data'])
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        ticket_text = data.get('text', 'Нет текста')
        
        # Здесь можно сохранить тикет в БД
        await message.answer(f"✅ Тикет создан!\nТекст: {ticket_text}")
        
        # Отправка админу (замените ID на ваш)
        admin_id = 937491209
        await bot.send_message(
            admin_id,
            f"🚨 Новый тикет от @{message.from_user.username}:\n{ticket_text}"
        )
    except Exception as e:
        logging.error(f"Ошибка: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
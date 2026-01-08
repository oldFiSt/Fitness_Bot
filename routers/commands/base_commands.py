from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

from DATA_BASE.connect import db
from keyboards.common_keyboards.start_kb import get_on_start_kb


dp = Dispatcher()
router = Router()

@router.message(CommandStart())
async def handle_start(message: types.Message):
    user_data = db.get_user(message.from_user.id)

    if user_data:
        welcome_text = markdown.text(
            markdown.text(markdown.bold((message.from_user.full_name)), f"\\,с возвращением😃\\!"),
            f"Рады видеть вас снова\\!",
            f"Ваши последние сохраненные данные\\:",
            markdown.text(f"• Рост\\: {user_data['height']} см"),
            markdown.text(f"• Вес\\: {user_data['weight']} кг"),
            markdown.text(f"• Возраст\\: {user_data['age']} лет"),
            markdown.text(f"• Пол\\: {user_data['gender']}"),
            f"Для новых расчетов нажмите на кнопку КБЖУ ниже⬇️",
            sep="\n"
        )

    else:
        welcome_text = markdown.text(
            markdown.text(markdown.bold((message.from_user.full_name)), f"\\, привет😃\\!"),
            f"Добро пожаловать в наш бот",
            f"Я помогу тебе составить тренировки и питание\\.\\.\\.",
            f"Для начала давай рассичтаем необходимое КБЖУ",
            f"для твоих данных\\.",
            f"Для этого нажми на соответсвующую кнопку ниже⬇️",
            sep="\n"
        )

    markup = get_on_start_kb()
    text = welcome_text
    await message.answer(text = text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=markup)
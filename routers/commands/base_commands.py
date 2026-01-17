from aiogram.enums import ParseMode
from aiogram import Router, types
from aiogram.filters import CommandStart
import html  # ✅ стандартная библиотека

from DATA_BASE.connect import db
from keyboards.common_keyboards.start_kb import get_on_start_kb


router = Router()


def bold(text: str) -> str:
    return f"<b>{text}</b>"


@router.message(CommandStart())
async def handle_start(message: types.Message):
    user = db.get_user(message.from_user.id)

    full_name = message.from_user.full_name or "Пользователь"
    full_name_safe = html.escape(full_name)  # ✅ защита от спецсимволов

    if user:
        height = user["height"] if user["height"] is not None else "—"
        weight = user["weight"] if user["weight"] is not None else "—"
        age = user["age"] if user["age"] is not None else "—"
        gender = user["gender"] if user["gender"] is not None else "—"

        text = (
            f"{bold(full_name_safe)}, с возвращением 😃!\n"
            f"Рады видеть вас снова!\n\n"
            f"Ваши последние сохранённые данные:\n"
            f"• Рост: {height} см\n"
            f"• Вес: {weight} кг\n"
            f"• Возраст: {age} лет\n"
            f"• Пол: {gender}\n\n"
            f"Для новых расчётов нажмите на кнопку {bold('Рассчитать КБЖУ 🧮')} ниже ⬇️"
        )
    else:
        text = (
            f"{bold(full_name_safe)}, привет 😃!\n"
            f"Добро пожаловать в наш бот.\n"
            f"Я помогу тебе составить тренировки и питание.\n\n"
            f"Для начала давай рассчитаем необходимое КБЖУ для твоих данных.\n"
            f"Нажми на кнопку {bold('Рассчитать КБЖУ 🧮')} ниже ⬇️"
        )

    await message.answer(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_on_start_kb()
    )

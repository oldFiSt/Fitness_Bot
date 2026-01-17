from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
import html

from DATA_BASE.connect import db
from keyboards.common_keyboards.main_menu_kb import kb_main

router = Router()

@router.message(F.text == "📈 Профиль")
async def profile(message: Message):
    # гарантируем, что пользователь записан
    db.upsert_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )

    row = db.get_user_full(message.from_user.id)
    if not row:
        await message.answer("Профиль пуст. Нажми /start 🙂", reply_markup=kb_main())
        return

    # DictCursor -> доступ как row["..."]
    full_name = row["full_name"] or (message.from_user.first_name or "Пользователь")
    full_name = html.escape(full_name)

    height = row["height"] if row["height"] is not None else "—"
    weight = row["weight"] if row["weight"] is not None else "—"
    age = row["age"] if row["age"] is not None else "—"
    gender = row["gender"] if row["gender"] is not None else "—"
    goal = row["goal"] if row["goal"] is not None else "—"
    points = row["points"] if row["points"] is not None else 0

    meals_plan = row["meals_plan"]
    workouts_plan = row["workouts_plan"]

    text = (
        f"<b>📈 Профиль</b>\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 <b>{full_name}</b>\n"
        f"⭐ Очки: <b>{points}</b>\n"
        f"🎯 Цель: <b>{html.escape(str(goal))}</b>\n\n"
        f"📌 Данные:\n"
        f"• Рост: {height} см\n"
        f"• Вес: {weight} кг\n"
        f"• Возраст: {age}\n"
        f"• Пол: {html.escape(str(gender))}\n\n"
    )

    if meals_plan:
        text += f"<b>🍽 Последний план питания</b>\n{meals_plan}\n\n"
    else:
        text += "<b>🍽 Последний план питания</b>\nПока не создан. Нажми «🍽 Питание»\n\n"

    if workouts_plan:
        text += f"<b>🏋️ Последний план тренировок</b>\n{workouts_plan}\n"
    else:
        text += "<b>🏋️ Последний план тренировок</b>\nПока не создан. Нажми «🏋️ Тренировки»\n"

    # ⚠️ Telegram ограничение ~4096 символов:
    if len(text) > 3800:
        # отправим 2 сообщениями
        await message.answer(text[:3800], parse_mode=ParseMode.HTML, reply_markup=kb_main())
        await message.answer(text[3800:], parse_mode=ParseMode.HTML, reply_markup=kb_main())
    else:
        await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=kb_main())

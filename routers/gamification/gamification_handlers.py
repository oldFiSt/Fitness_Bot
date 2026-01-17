from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
import html

from DATA_BASE.connect import db
from keyboards.common_keyboards.main_menu_kb import kb_main

router = Router()


def render_profile_html(user_id: int, name_fallback: str) -> str:
    row = db.get_user_full(user_id)
    if not row:
        return "<b>📈 Профиль</b>\n━━━━━━━━━━━━━━\nПока нет данных. Нажми /start 🙂"

    full_name = row["full_name"] or name_fallback
    full_name = html.escape(full_name)

    height = row["height"] if row["height"] is not None else "—"
    weight = row["weight"] if row["weight"] is not None else "—"
    age = row["age"] if row["age"] is not None else "—"
    gender = row["gender"] if row["gender"] is not None else "—"
    goal = row["goal"] if row["goal"] is not None else "—"
    points = row["points"] if row["points"] is not None else 0

    meals_plan = row.get("meals_plan")
    workouts_plan = row.get("workouts_plan")

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
        text += f"<b>🍽 Последний план питания</b>\n{html.escape(meals_plan)}\n\n"
    else:
        text += "<b>🍽 Последний план питания</b>\nПока не создан. Нажми «🍽 Питание»\n\n"

    if workouts_plan:
        text += f"<b>🏋️ Последний план тренировок</b>\n{html.escape(workouts_plan)}\n"
    else:
        text += "<b>🏋️ Последний план тренировок</b>\nПока не создан. Нажми «🏋️ Тренировки»\n"

    return text


def render_rating_md(user_id: int, limit: int = 10) -> str:
    rows = db.get_top(limit)
    if not rows:
        return "🏆 *Рейтинг*\n━━━━━━━━━━━━━━\nПока рейтинг пуст 😅"

    me = db.get_user(user_id)
    my_points = me["points"] if me and me["points"] is not None else 0
    my_rank = db.get_rank(user_id) if me else None

    header = "🏆 *Рейтинг участников*\n━━━━━━━━━━━━━━\n"
    if my_rank is not None:
        header += f"👤 Ты: *#{my_rank}* | ⭐ *{my_points}*\n\n"

    medals = ["🥇", "🥈", "🥉"]
    lines = []
    for i, r in enumerate(rows, start=1):
        uid = r["telegram_id"]
        name = r["full_name"] or "Пользователь"
        points = r["points"] or 0
        icon = medals[i - 1] if i <= 3 else f"{i}."
        me_mark = "➡️ " if uid == user_id else ""
        lines.append(f"{me_mark}{icon} *{name}* — {points} ⭐")

    return header + "\n".join(lines)


@router.message(F.text == "📈 Профиль")
async def profile(message: Message):
    db.upsert_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    text = render_profile_html(message.from_user.id, message.from_user.first_name or "Пользователь")
    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=kb_main())


@router.message(F.text == "🏆 Рейтинг")
async def rating(message: Message):
    db.upsert_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    text = render_rating_md(message.from_user.id, limit=10)
    await message.answer(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_main())

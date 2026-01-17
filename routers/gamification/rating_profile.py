from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
import html

from DATA_BASE.connect import db
from keyboards.common_keyboards.main_menu_kb import kb_main

router = Router()


def bold(t: str) -> str:
    return f"<b>{t}</b>"


def render_profile(user_id: int, name_fallback: str):
    row = db.get_user(user_id)
    if not row:
        return (
            f"📈 {bold('Профиль')}\n"
            "━━━━━━━━━━━━━━\n"
            "Пока нет данных. Нажми /start 🙂"
        )

    points = row["points"] or 0
    full_name = row["full_name"] or name_fallback
    rank = db.get_rank(user_id) or "—"

    name_safe = html.escape(full_name)

    return (
        f"📈 {bold('Профиль')}\n"
        "━━━━━━━━━━━━━━\n"
        f"👤 {bold(name_safe)}\n"
        f"⭐ Очки: {bold(str(points))}\n"
        f"🏅 Место: {bold('#' + str(rank))}\n"
    )


def render_rating(user_id: int, limit: int = 10):
    rows = db.get_top(limit)
    if not rows:
        return (
            f"🏆 {bold('Рейтинг')}\n"
            "━━━━━━━━━━━━━━\n"
            "Пока рейтинг пуст 😅"
        )

    me = db.get_user(user_id)
    my_points = (me["points"] or 0) if me else 0
    my_rank = db.get_rank(user_id) if me else None

    header = f"🏆 {bold('Рейтинг участников')}\n━━━━━━━━━━━━━━\n"
    if my_rank is not None:
        header += f"👤 Ты: {bold('#' + str(my_rank))}  |  ⭐ {bold(str(my_points))}\n\n"

    medals = ["🥇", "🥈", "🥉"]
    lines = []
    for i, r in enumerate(rows, start=1):
        uid = r["telegram_id"]
        name = r["full_name"] or "Пользователь"
        points = r["points"] or 0

        icon = medals[i - 1] if i <= 3 else f"{i}."
        me_mark = "➡️ " if uid == user_id else ""

        name_safe = html.escape(name)
        lines.append(f"{me_mark}{icon} {bold(name_safe)} — {points} ⭐")

    return header + "\n".join(lines)


@router.message(F.text == "✅ Тренировка (+10)")
async def done_workout(message: Message):
    db.upsert_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    db.add_points(message.from_user.id, 10)
    await message.answer("🔥 Засчитано! +10 очков.", reply_markup=kb_main())


@router.message(F.text == "✅ Питание (+5)")
async def done_meals(message: Message):
    db.upsert_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    db.add_points(message.from_user.id, 5)
    await message.answer("🍽 Отлично! +5 очков.", reply_markup=kb_main())


@router.message(F.text == "📈 Профиль")
async def profile(message: Message):
    db.upsert_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    text = render_profile(message.from_user.id, message.from_user.first_name or "Пользователь")
    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=kb_main())


@router.message(F.text == "🏆 Рейтинг")
async def rating(message: Message):
    db.upsert_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    text = render_rating(message.from_user.id)
    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=kb_main())

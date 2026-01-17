from aiogram import Router
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

from keyboards.common_keyboards.main_menu_kb import kb_back, kb_main
from utils.planner import calculate_all_goals
from DATA_BASE.connect import db

router = Router()

class KBY(StatesGroup):
    height = State()
    weight = State()
    age = State()
    sex = State()
    activity = State()
    goal = State()

ACTIVITY_FACTORS = {
    "Нет физической нагрузки": 1.2,
    "Лёгкие нагрузки (1–3 раза в неделю)": 1.375,
    "Физические нагрузки (3–5 раз в неделю)": 1.55,
    "Ежедневные интенсивные нагрузки": 1.725,
    "Спортсмен или похожие нагрузки": 1.9
}

# ✅ СТАРТ РАСЧЁТА ПО КНОПКЕ
@router.message(F.text == "Рассчитать КБЖУ 🧮")
async def start_kby(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите ваш рост (см):", reply_markup=kb_back())
    await state.set_state(KBY.height)

@router.message(KBY.height)
async def get_height(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer("Главное меню:", reply_markup=kb_main())
        return
    try:
        await state.update_data(height=float(message.text))
        await message.answer("Введите ваш вес (кг):", reply_markup=kb_back())
        await state.set_state(KBY.weight)
    except ValueError:
        await message.answer("Неверный формат. Введите число, например: 175", reply_markup=kb_back())

@router.message(KBY.weight)
async def get_weight(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer("Главное меню:", reply_markup=kb_main())
        return
    try:
        await state.update_data(weight=float(message.text))
        await message.answer("Введите ваш возраст (лет):", reply_markup=kb_back())
        await state.set_state(KBY.age)
    except ValueError:
        await message.answer("Неверный формат. Введите число, например: 70", reply_markup=kb_back())

@router.message(KBY.age)
async def get_age(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer("Главное меню:", reply_markup=kb_main())
        return
    try:
        await state.update_data(age=int(message.text))

        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")],
                [KeyboardButton(text="⬅️ Назад")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Выберите ваш пол:", reply_markup=kb)
        await state.set_state(KBY.sex)
    except ValueError:
        await message.answer("Неверный формат. Введите число, например: 25", reply_markup=kb_back())

@router.message(KBY.sex)
async def get_sex(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer("Главное меню:", reply_markup=kb_main())
        return

    t = message.text.strip().lower()
    if t == "мужской":
        sex = "м"
    elif t == "женский":
        sex = "ж"
    else:
        await message.answer("Выбери пол кнопкой 🙂")
        return

    await state.update_data(sex=sex)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Нет физической нагрузки")],
            [KeyboardButton(text="Лёгкие нагрузки (1–3 раза в неделю)")],
            [KeyboardButton(text="Физические нагрузки (3–5 раз в неделю)")],
            [KeyboardButton(text="Ежедневные интенсивные нагрузки")],
            [KeyboardButton(text="Спортсмен или похожие нагрузки")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выберите уровень активности:", reply_markup=kb)
    await state.set_state(KBY.activity)

@router.message(KBY.activity)
async def get_activity(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer("Главное меню:", reply_markup=kb_main())
        return

    factor = ACTIVITY_FACTORS.get(message.text.strip())
    if not factor:
        await message.answer("Выбери активность кнопкой 🙂")
        return

    await state.update_data(
        activity=factor,
        lifestyle=message.text.strip()
    )

    # ✅ КЛАВИАТУРА ВЫБОРА ЦЕЛИ — ВОТ ОНА
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Похудение")],
            [KeyboardButton(text="Поддержание")],
            [KeyboardButton(text="Набор массы")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Выберите цель:", reply_markup=kb)
    await state.set_state(KBY.goal)

@router.message(KBY.goal, F.text.in_(["Похудение", "Поддержание", "Набор массы"]))
async def show_goal_result(message: Message, state: FSMContext):
    goal = message.text.strip()

    goal_map = {"Похудение": "Похудение", "Поддержание": "Поддержание", "Набор массы": "Набор"}
    goal_key = goal_map[goal]

    data = await state.get_data()
    results = calculate_all_goals(data, data.get("lifestyle", ""))

    goal_data = results[goal_key]
    await state.update_data(goal=goal_key, results=results)

    db.add_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        height=int(data["height"]),
        weight=float(data["weight"]),
        age=int(data["age"]),
        gender=data["sex"],
        goal=goal_key
    )

    text = (
        f"🎯 *Цель:* {goal_key}\n"
        f"━━━━━━━━━━━━━━\n"
        f"🔥 *Суточно:* {goal_data['calories']:.0f} ккал\n"
        f"🥩 *Белки:* {goal_data['proteins']:.0f} г\n"
        f"🥑 *Жиры:* {goal_data['fats']:.0f} г\n"
        f"🍞 *Углеводы:* {goal_data['carbs']:.0f} г\n\n"
        "Открой *Питание* или *Тренировки* в меню ниже 👇"
    )
    await message.answer(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_main())


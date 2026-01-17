from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import ParseMode

from keyboards.common_keyboards.main_menu_kb import (
    kb_main, kb_meals_count, kb_workouts_count, kb_plans, kb_after_meals, kb_after_workouts
)
from utils.planner import generate_personal_meals, generate_personal_workouts

router = Router()

last_plans = {}  # user_id: {"meals": str, "workouts": str}


def has_calc(data: dict) -> bool:
    goal = data.get("goal")
    results = data.get("results", {})
    return bool(goal and results.get(goal))


# ✅ ЗАНОВО — работает в любом состоянии
@router.message(F.text == "🔄 Заново")
async def restart(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ок! Начнём заново 🙂\nНажми /start или кнопку КБЖУ.", reply_markup=kb_main())


# ✅ МОИ ПЛАНЫ — работает в любом состоянии
@router.message(F.text == "🔁 Мои планы")
async def plans_menu(message: Message, state: FSMContext):
    # можно не чистить, но лучше чистить чтобы FSM не мешал
    await state.clear()
    await message.answer("Выбери, что показать:", reply_markup=kb_plans())


@router.message(F.text == "🔁 Питание ещё раз")
async def show_last_meals(message: Message):
    plan = last_plans.get(message.from_user.id, {}).get("meals")
    if not plan:
        await message.answer("Пока нет плана питания. Сначала сформируй его 🙂", reply_markup=kb_main())
        return
    await message.answer(plan, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_after_meals())


@router.message(F.text == "🔁 Тренировки ещё раз")
async def show_last_workouts(message: Message):
    plan = last_plans.get(message.from_user.id, {}).get("workouts")
    if not plan:
        await message.answer("Пока нет плана тренировок. Сначала сформируй его 🙂", reply_markup=kb_main())
        return
    await message.answer(plan, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_after_workouts())


# ✅ ПИТАНИЕ
@router.message(F.text == "🍽 Питание")
async def meals_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    if not has_calc(data):
        # не чистим state, чтобы человек мог вернуться к выбору цели,
        # но можно и чистить — как тебе удобнее
        await message.answer("Сначала рассчитай КБЖУ кнопкой 🧮", reply_markup=kb_main())
        return

    await message.answer("Сколько приёмов пищи в день? (1–6)", reply_markup=kb_meals_count())


# ✅ выбор количества приёмов пищи (1–6)
@router.message(F.text.in_(["1", "2", "3", "4", "5", "6"]))
async def meals_count_selected(message: Message, state: FSMContext):
    data = await state.get_data()
    if not has_calc(data):
        return

    meals = int(message.text)
    goal = data["goal"]
    goal_data = data["results"][goal]

    plan = generate_personal_meals(data, goal_data, meals)
    last_plans.setdefault(message.from_user.id, {})["meals"] = plan

    await message.answer(plan, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_after_meals())


# ✅ ТРЕНИРОВКИ
@router.message(F.text == "🏋️ Тренировки")
async def workouts_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    if not has_calc(data):
        await message.answer("Сначала рассчитай КБЖУ кнопкой 🧮", reply_markup=kb_main())
        return

    await message.answer("Сколько тренировок в неделю? (1–7)", reply_markup=kb_workouts_count())


# ✅ выбор количества тренировок (1–7)
@router.message(F.text.in_(["1", "2", "3", "4", "5", "6", "7"]))
async def workouts_count_selected(message: Message, state: FSMContext):
    data = await state.get_data()
    if not has_calc(data):
        return

    days = int(message.text)
    goal = data["goal"]
    goal_data = data["results"][goal]
    activity = data.get("activity", 1.2)

    plan = generate_personal_workouts(goal_data, days, activity)
    last_plans.setdefault(message.from_user.id, {})["workouts"] = plan

    await message.answer(plan, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_after_workouts())

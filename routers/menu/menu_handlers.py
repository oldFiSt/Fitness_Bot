from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import ParseMode

from utils.plan_storage import save_plan, load_plan
from utils.schedule import build_meals_schedule, build_workouts_schedule

from keyboards.common_keyboards.main_menu_kb import (
    kb_main, kb_meals_count, kb_workouts_count, kb_plans, kb_after_meals, kb_after_workouts
)
from utils.planner import generate_personal_meals, generate_personal_workouts

router = Router()


def has_calc(data: dict) -> bool:
    goal = data.get("goal")
    results = data.get("results", {})
    return bool(goal and results.get(goal))


@router.message(F.text == "🔄 Заново")
async def restart(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ок! Начнём заново 🙂\nНажми /start или кнопку КБЖУ.", reply_markup=kb_main())


@router.message(F.text == "🔁 Мои планы")
async def plans_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выбери, что показать:", reply_markup=kb_plans())


@router.message(F.text == "🔁 Питание ещё раз")
async def show_last_meals(message: Message):
    data = load_plan(message.from_user.id)
    plan = data.get("meals")
    if not plan:
        await message.answer("Пока нет плана питания. Сначала сформируй его 🙂", reply_markup=kb_main())
        return
    await message.answer(plan, parse_mode=ParseMode.HTML, reply_markup=kb_after_meals())


@router.message(F.text == "🔁 Тренировки ещё раз")
async def show_last_workouts(message: Message):
    data = load_plan(message.from_user.id)
    plan = data.get("workouts")
    if not plan:
        await message.answer("Пока нет плана тренировок. Сначала сформируй его 🙂", reply_markup=kb_main())
        return
    await message.answer(plan, parse_mode=ParseMode.HTML, reply_markup=kb_after_workouts())


@router.message(F.text == "🍽 Питание")
async def meals_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    if not has_calc(data):
        await message.answer("Сначала рассчитай КБЖУ кнопкой 🧮", reply_markup=kb_main())
        return

    await message.answer("Сколько приёмов пищи в день? (1–6)", reply_markup=kb_meals_count())


@router.message(F.text.in_(["1", "2", "3", "4", "5", "6"]))
async def meals_count_selected(message: Message, state: FSMContext):
    data = await state.get_data()
    if not has_calc(data):
        return

    meals = int(message.text)
    goal = data["goal"]
    goal_data = data["results"][goal]

    plan = generate_personal_meals(data, goal_data, meals)

    times = build_meals_schedule(meals)
    times_text = "\n".join([f"• {t.strftime('%H:%M')}" for t in times])

    plan_with_schedule = (
        "<b>🗓 График питания</b>\n"
        f"{times_text}\n\n"
        + plan
    )

    save_plan(message.from_user.id, meals_text=plan_with_schedule)
    await message.answer(plan_with_schedule, parse_mode=ParseMode.HTML, reply_markup=kb_after_meals())


@router.message(F.text == "🏋️ Тренировки")
async def workouts_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    if not has_calc(data):
        await message.answer("Сначала рассчитай КБЖУ кнопкой 🧮", reply_markup=kb_main())
        return

    await message.answer("Сколько тренировок в неделю? (1–7)", reply_markup=kb_workouts_count())


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

    days_list = build_workouts_schedule(days)
    days_text = "\n".join([f"• {d}" for d in days_list])

    plan_with_schedule = (
        "<b>🗓 График тренировок</b>\n"
        f"{days_text}\n\n"
        + plan
    )

    save_plan(message.from_user.id, workouts_text=plan_with_schedule)
    await message.answer(plan_with_schedule, parse_mode=ParseMode.HTML, reply_markup=kb_after_workouts())

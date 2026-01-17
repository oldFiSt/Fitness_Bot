from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def kb_main():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍽 Питание"), KeyboardButton(text="🏋️ Тренировки")],
            [KeyboardButton(text="🔁 Мои планы"), KeyboardButton(text="🔄 Заново")],
            [KeyboardButton(text="🏆 Рейтинг"), KeyboardButton(text="📈 Профиль")],
        ],
        resize_keyboard=True
    )

def kb_back(one_time: bool = True):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Назад")]],
        resize_keyboard=True,
        one_time_keyboard=one_time
    )

def kb_meals_count():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3")],
            [KeyboardButton(text="4"), KeyboardButton(text="5"), KeyboardButton(text="6")],
            [KeyboardButton(text="⬅️ Назад")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def kb_workouts_count():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3"), KeyboardButton(text="4")],
            [KeyboardButton(text="5"), KeyboardButton(text="6"), KeyboardButton(text="7")],
            [KeyboardButton(text="⬅️ Назад")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def kb_plans():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Питание ещё раз"), KeyboardButton(text="🔁 Тренировки ещё раз")],
            [KeyboardButton(text="⬅️ Назад")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def kb_after_meals():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Питание (+5)"), KeyboardButton(text="🔁 Мои планы")],
            [KeyboardButton(text="🍽 Питание"), KeyboardButton(text="🏋️ Тренировки")],
            [KeyboardButton(text="🏆 Рейтинг"), KeyboardButton(text="📈 Профиль")],
        ],
        resize_keyboard=True
    )

def kb_after_workouts():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Тренировка (+10)"), KeyboardButton(text="🔁 Мои планы")],
            [KeyboardButton(text="🍽 Питание"), KeyboardButton(text="🏋️ Тренировки")],
            [KeyboardButton(text="🏆 Рейтинг"), KeyboardButton(text="📈 Профиль")],
        ],
        resize_keyboard=True
    )

from datetime import time

DAYS_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

def build_meals_schedule(meals_per_day: int):
    # базовые "времена" под 1–6 приёмов
    presets = {
        1: [time(13, 0)],
        2: [time(10, 0), time(18, 0)],
        3: [time(9, 0), time(14, 0), time(19, 0)],
        4: [time(9, 0), time(12, 0), time(15, 0), time(19, 0)],
        5: [time(8, 30), time(11, 0), time(13, 30), time(16, 30), time(19, 30)],
        6: [time(8, 0), time(10, 30), time(13, 0), time(15, 30), time(18, 0), time(20, 30)],
    }
    return presets.get(meals_per_day, presets[3])

def build_workouts_schedule(days_per_week: int):
    # простая расстановка по неделе: первые N дней
    days_per_week = max(1, min(7, days_per_week))
    return DAYS_RU[:days_per_week]

def calculate_all_goals(data, lifestyle_text):
    weight = data['weight']
    height = data['height']
    age = data['age']
    sex = data['sex']
    activity = data['activity']

    if sex == 'м':
        tdee_base = (10 * weight + 6.25 * height - 5 * age + 5)
    else:
        tdee_base = (10 * weight + 6.25 * height - 5 * age - 161)

    tdee = tdee_base * activity

    goals = {
        "Похудение": tdee - 400,
        "Поддержание": tdee,
        "Набор": tdee + 400
    }

    results = {}
    for g, cal in goals.items():
        proteins = (cal * 0.30) / 4
        fats = (cal * 0.25) / 9
        carbs = (cal * 0.45) / 4
        results[g] = {"calories": cal, "proteins": proteins, "fats": fats, "carbs": carbs}

    return results

def generate_personal_meals(user_profile, daily_data, meals: int) -> str:
    # временная версия, чтобы бот не падал (заменишь на твою большую)
    return (
        "🥗 *План питания*\n"
        "━━━━━━━━━━━━━━\n"
        f"Приёмов пищи: *{meals}*\n"
        f"Цель: *{daily_data['calories']:.0f} ккал*\n"
        f"Б: {daily_data['proteins']:.0f} г | Ж: {daily_data['fats']:.0f} г | У: {daily_data['carbs']:.0f} г\n\n"
        "⚠️ Генератор блюд пока не подключён."
    )

def generate_personal_workouts(daily_data, days_per_week: int, activity: float) -> str:
    # временная версия, чтобы бот не падал (заменишь на твою большую)
    return (
        "🏋️ *План тренировок*\n"
        "━━━━━━━━━━━━━━\n"
        f"Тренировок в неделю: *{days_per_week}*\n"
        f"Коэф. активности: *{activity}*\n\n"
        "⚠️ Генератор тренировок пока не подключён."
    )

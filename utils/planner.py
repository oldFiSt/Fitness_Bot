import random

# ─────────────────────────────
# ПРОДУКТЫ (на 100 г)
# ─────────────────────────────
PRODUCTS = {
    "куриная грудка": {"kcal": 165, "protein": 31, "fat": 3.6, "carbs": 0},
    "куриное филе": {"kcal": 165, "protein": 31, "fat": 3.6, "carbs": 0},
    "говядина": {"kcal": 250, "protein": 26, "fat": 15, "carbs": 0},
    "лосось": {"kcal": 208, "protein": 20, "fat": 13, "carbs": 0},
    "рыба белая": {"kcal": 105, "protein": 20, "fat": 1.5, "carbs": 0},

    "яйцо (целое)": {"kcal": 155, "protein": 13, "fat": 11, "carbs": 1.1},
    "овсянка": {"kcal": 379, "protein": 13.2, "fat": 6.5, "carbs": 67.7},
    "рис (варёный)": {"kcal": 130, "protein": 2.4, "fat": 0.3, "carbs": 28},
    "картофель": {"kcal": 87, "protein": 2, "fat": 0.1, "carbs": 20},
    "булгур": {"kcal": 342, "protein": 12.3, "fat": 1.3, "carbs": 76},

    "творог 5%": {"kcal": 121, "protein": 18, "fat": 5, "carbs": 2.7},
    "йогурт": {"kcal": 59, "protein": 10, "fat": 0.4, "carbs": 3.6},

    "банан": {"kcal": 89, "protein": 1.1, "fat": 0.3, "carbs": 23},
    "яблоко": {"kcal": 52, "protein": 0.3, "fat": 0.2, "carbs": 14},
    "овощи": {"kcal": 35, "protein": 2, "fat": 0.3, "carbs": 7},

    "оливковое масло": {"kcal": 884, "protein": 0, "fat": 100, "carbs": 0},
    "орехи": {"kcal": 607, "protein": 20, "fat": 54, "carbs": 21},
}

# ─────────────────────────────
# БАЗОВЫЕ ГРАММОВКИ
# ─────────────────────────────
BASE_GRAMS = {
    "куриная грудка": 150,
    "куриное филе": 150,
    "говядина": 150,
    "лосось": 140,
    "рыба белая": 170,
    "яйцо (целое)": 120,
    "овсянка": 80,
    "рис (варёный)": 200,
    "картофель": 250,
    "булгур": 80,
    "творог 5%": 200,
    "йогурт": 250,
    "банан": 140,
    "яблоко": 180,
    "овощи": 250,
    "оливковое масло": 10,
    "орехи": 30,
}

# ─────────────────────────────
# ШАБЛОНЫ ПИТАНИЯ
# ─────────────────────────────
MEAL_TEMPLATES = {
    "breakfast": [
        ["овсянка", "яйцо (целое)", "банан"],
        ["творог 5%", "яблоко", "орехи"],
    ],
    "lunch": [
        ["куриная грудка", "рис (варёный)", "овощи"],
        ["говядина", "картофель", "овощи"],
    ],
    "dinner": [
        ["рыба белая", "овощи", "оливковое масло"],
        ["куриное филе", "овощи", "картофель"],
    ],
    "snack": [
        ["йогурт", "банан"],
        ["творог 5%", "яблоко"],
    ],
}

TYP_RU = {
    "breakfast": "🍳 Завтрак",
    "lunch": "🍽 Обед",
    "dinner": "🌙 Ужин",
    "snack": "🍏 Перекус",
    "full": "🍽 Приём пищи",
}

# ─────────────────────────────
# КБЖУ РАСЧЁТ
# ─────────────────────────────
def calculate_all_goals(data, _):
    weight = data["weight"]
    height = data["height"]
    age = data["age"]
    sex = data["sex"]
    activity = data["activity"]

    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if sex == "м" else -161)
    tdee = bmr * activity

    goals = {
        "Похудение": tdee - 400,
        "Поддержание": tdee,
        "Набор": tdee + 400,
    }

    results = {}
    for g, cal in goals.items():
        results[g] = {
            "calories": cal,
            "proteins": (cal * 0.30) / 4,
            "fats": (cal * 0.25) / 9,
            "carbs": (cal * 0.45) / 4,
        }
    return results

# ─────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ
# ─────────────────────────────
def meal_nutrition_from_portions(portions):
    kcal = p = f = c = 0
    for name, g in portions.items():
        info = PRODUCTS[name]
        k = g / 100
        kcal += info["kcal"] * k
        p += info["protein"] * k
        f += info["fat"] * k
        c += info["carbs"] * k
    return round(kcal), round(p), round(f), round(c)

def choose_template_for_meal(i, meals):
    if meals == 1:
        return "full"
    if meals == 2:
        return ["breakfast", "dinner"][i]
    if meals == 3:
        return ["breakfast", "lunch", "dinner"][i]
    if meals == 4:
        return ["breakfast", "snack", "lunch", "dinner"][i]
    return "breakfast"

def split_day_targets(daily, meals):
    weights = [1 / meals] * meals
    return [{
        "cal": daily["calories"] * w,
        "p": daily["proteins"] * w,
        "f": daily["fats"] * w,
        "c": daily["carbs"] * w,
    } for w in weights]

def scale_portions(products, target_cal):
    portions = {p: BASE_GRAMS[p] for p in products}
    total = sum(PRODUCTS[p]["kcal"] * g / 100 for p, g in portions.items())
    scale = target_cal / max(total, 1)
    return {p: int(g * scale) for p, g in portions.items()}

# ─────────────────────────────
# ГЕНЕРАЦИЯ ПИТАНИЯ
# ─────────────────────────────
def generate_personal_meals(_, daily_data, meals):
    targets = split_day_targets(daily_data, meals)
    result = []

    for i in range(meals):
        typ = choose_template_for_meal(i, meals)
        template = random.choice(
            MEAL_TEMPLATES["breakfast"] if typ == "full" else MEAL_TEMPLATES[typ]
        )
        portions = scale_portions(template, targets[i]["cal"])
        kcal, p, f, c = meal_nutrition_from_portions(portions)

        block = [f"{TYP_RU[typ]} — приём {i+1}", "━━━━━━━━━━━━━━"]
        for n, g in portions.items():
            block.append(f"{n} — {g} г")
        block.append(f"⚡ {kcal} ккал | Б {p} | Ж {f} | У {c}")

        result.append("\n".join(block))

    return "\n\n".join(result)

# ─────────────────────────────
# ТРЕНИРОВКИ (заглушка)
# ─────────────────────────────
def generate_personal_workouts(_, days, __):
    return f"🏋️ Тренировок в неделю: {days}"

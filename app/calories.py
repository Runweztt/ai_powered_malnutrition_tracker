ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "moderate":  1.55,
    "active":    1.725
}

CLASSIFICATION_ADJUSTMENTS = {
    "Underweight": +500,
    "Normal":        0,
    "Overweight":  -300,
    "Obese":       -500
}


def get_daily_calorie_target(
    classification: str,
    age: int,
    gender: str,
    activity_level: str
) -> int:
    bmr = (1600 - (5 * age)) if gender == "male" else (1400 - (5 * age))
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    tdee       = bmr * multiplier
    adjustment = CLASSIFICATION_ADJUSTMENTS.get(classification, 0)
    return max(1200, round(tdee + adjustment))

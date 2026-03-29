def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("Height and weight must be positive values.")
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


def classify_bmi(bmi_value: float) -> str:
    if bmi_value < 18.5:
        return "Underweight"
    elif bmi_value < 25.0:
        return "Normal"
    elif bmi_value < 30.0:
        return "Overweight"
    else:
        return "Obese"

VALID_GENDERS   = ("male", "female")
VALID_ACTIVITY  = ("sedentary", "moderate", "active")


def welcome_user():
    print("=" * 60)
    print("   Welcome to the AI-Powered Malnutrition Tracker!")
    print("=" * 60)
    print("  This tool will:")
    print("  - Calculate your BMI")
    print("  - Classify your nutritional status")
    print("  - Generate a personalised AI diet plan")
    print("  - Track your progress over time")
    print("\n  Type 'exit' at any prompt to quit.\n")


def _prompt(label, cast=str, options=None):
    while True:
        raw = input(f"  {label}: ").strip()
        if raw.lower() in ("exit", "quit"):
            return None
        if options and raw.lower() not in options:
            print(f"    [!] Please enter one of: {', '.join(options)}")
            continue
        try:
            value = cast(raw.lower()) if options else cast(raw)
            if cast in (int, float) and value <= 0:
                raise ValueError
            return value
        except (ValueError, TypeError):
            print("    [!] Invalid input. Please try again.")


def get_user_inputs():
    print("\n--- Enter your details ---")

    username = _prompt("Name")
    if username is None:
        return None

    age = _prompt("Age (years)", cast=int)
    if age is None:
        return None

    gender = _prompt(f"Gender ({'/'.join(VALID_GENDERS)})", options=VALID_GENDERS)
    if gender is None:
        return None

    height = _prompt("Height (cm)", cast=float)
    if height is None:
        return None

    weight = _prompt("Weight (kg)", cast=float)
    if weight is None:
        return None

    activity = _prompt(
        f"Activity level ({'/'.join(VALID_ACTIVITY)})",
        options=VALID_ACTIVITY
    )
    if activity is None:
        return None

    return {
        "username":       username,
        "age":            age,
        "gender":         gender,
        "height_cm":      height,
        "weight_kg":      weight,
        "activity_level": activity
    }

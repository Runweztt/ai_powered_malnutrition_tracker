import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.inputs import welcome_user, get_user_inputs
from app.bmi import calculate_bmi, classify_bmi
from app.calories import get_daily_calorie_target
from app.ai_diet import generate_diet_plan
from app.display import display_diet_plan
from app.reports import display_progress_report, ask_export
from database.queries import save_user_data, load_user_history


def main():
    welcome_user()

    while True:
        user_profile = get_user_inputs()
        if user_profile is None:
            print("\nGoodbye! Stay healthy.")
            break

        bmi_value      = calculate_bmi(user_profile["weight_kg"], user_profile["height_cm"])
        classification = classify_bmi(bmi_value)
        calorie_target = get_daily_calorie_target(
            classification,
            user_profile["age"],
            user_profile["gender"],
            user_profile["activity_level"]
        )

        bmi_data = {
            "bmi_value":      bmi_value,
            "classification": classification,
            "calorie_target": calorie_target
        }

        print(f"\n  BMI: {bmi_value}  |  Status: {classification}  |  Daily target: {calorie_target} kcal\n")

        diet_plan = generate_diet_plan(user_profile, bmi_data)
        display_diet_plan(diet_plan)

        save_user_data(user_profile, bmi_data, diet_plan)

        history = load_user_history(user_profile["username"])
        if history:
            display_progress_report(history)

        ask_export(user_profile, bmi_data, diet_plan)

        again = input("\n  Run a new session? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\nGoodbye! Stay healthy.")
            break


if __name__ == "__main__":
    main()

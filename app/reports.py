
"""Porpose of report in app section
- Loads BMI history for a user from the database
- Display a BMI trend table in the terminal
- Generat and save a full session summary as a .txt 
"""
import os
from datetime import datetime

EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")


def display_progress_report(history: list) -> None:
    if not history:
        print("\n  No previous sessions found.")
        return

    print("\n" + "=" * 60)
    print("            YOUR BMI PROGRESS HISTORY")
    print("=" * 60)
    print(f"  {'Date':<20} {'BMI':>6}  {'Status':<14} {'Calories':>8}")
    print("  " + "-" * 54)

    for r in history:
        date_str = (
            r["recorded_at"].strftime("%Y-%m-%d %H:%M")
            if isinstance(r["recorded_at"], datetime)
            else str(r["recorded_at"])[:16]
        )
        print(
            f"  {date_str:<20} "
            f"{r['bmi_value']:>6.2f}  "
            f"{r['classification']:<14} "
            f"{r['calorie_target']:>6} kcal"
        )

    print("=" * 60)

    if len(history) >= 2:
        diff = round(history[-1]["bmi_value"] - history[0]["bmi_value"], 2)
        if diff < 0:
            print(f"\n  Trend: BMI decreased by {abs(diff)} since first session. Never give up!")
        elif diff > 0:
            print(f"\n  Trend: BMI increased by {diff} since first session.")
        else:
            print("\n  Trend: BMI unchanged since first session.")


def ask_export(user_profile: dict, bmi_data: dict, diet_plan: str) -> None:
    choice = input("\n  Export session report to a text file? (yes/no): ").strip().lower()
    if choice in ("yes", "y"):
        _export_session(user_profile, bmi_data, diet_plan)


def _export_session(user_profile: dict, bmi_data: dict, diet_plan: str) -> None:
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath  = os.path.join(EXPORTS_DIR, f"{user_profile['username']}_{timestamp}.txt")

    lines = [
        "=" * 60,
        "  MALNUTRITION TRACKER SESSION REPORT",
        "=" * 60,
        f"  Name           : {user_profile['username']}",
        f"  Age            : {user_profile['age']}",
        f"  Gender         : {user_profile['gender']}",
        f"  Activity level : {user_profile['activity_level']}",
        f"  Height         : {user_profile['height_cm']} cm",
        f"  Weight         : {user_profile['weight_kg']} kg",
        "",
        f"  BMI            : {bmi_data['bmi_value']}",
        f"  Classification : {bmi_data['classification']}",
        f"  Calorie target : {bmi_data['calorie_target']} kcal/day",
        "",
        "=" * 60,
        "  DIET PLAN",
        "=" * 60,
        diet_plan,
        "",
        f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
    ]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n Report saved to: exports/{os.path.basename(filepath)}")



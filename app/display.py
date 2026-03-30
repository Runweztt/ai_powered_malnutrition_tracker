def display_diet_plan(plan: str) -> None:
    print("\n" + "=" * 60)
    print("         YOUR PERSONALISED DIET PLAN")
    print("=" * 60)
    print(plan)
    print("=" * 60 + "\n")


def display_summary(name: str, bmi: float, calories: int) -> None:
    print("\n" + "-" * 60)
    print(f"Patient: {name}")
    print(f"BMI: {bmi:.2f}")
    print(f"Recommended Daily Calories: {calories}")
    print("-" * 60 + "\n")


def display_error(message: str) -> None:
    print("\n[ERROR]")
    print(message)
    print()

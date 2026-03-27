
# Member 3 — Terminal Display



_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_GREEN  = "\033[92m"
_CYAN   = "\033[96m"
_YELLOW = "\033[93m"
_RED    = "\033[91m"
_BLUE   = "\033[94m"

# Width of the display panel
_WIDTH = 65


# ──────────────────────────────────────────────────────────────────────────────
# Public functions
# ──────────────────────────────────────────────────────────────────────────────

def display_bmi_result(bmi: float, classification: str, calorie_target: int) -> None:
    """
    Print the BMI value, WHO classification, and daily calorie target.

    Args:
        bmi (float): Calculated BMI value.
        classification (str): e.g. 'Normal', 'Overweight'.
        calorie_target (int): Recommended daily calories.
    """
    colour = _classification_colour(classification)

    _print_divider("═")
    _print_centred("BMI RESULTS", bold=True)
    _print_divider("═")

    print(f"  {'BMI Value':<30} {_BOLD}{bmi:.2f}{_RESET}")
    print(f"  {'Classification':<30} {colour}{_BOLD}{classification}{_RESET}")
    print(f"  {'Daily Calorie Target':<30} {_BOLD}{calorie_target} kcal{_RESET}")

    _print_divider("─")


def display_diet_plan(plan: dict, user_name: str) -> None:
    """
    Format and print the full diet plan in the terminal.

    Args:
        plan (dict): Diet plan dict returned by generate_diet_plan()
                     or get_fallback_diet_plan().
        user_name (str): Used to personalise the header.
    """
    source_tag = f"[{plan.get('source', 'AI')}]"

    _print_divider("═")
    _print_centred(f"PERSONALISED DIET PLAN  {source_tag}", bold=True)
    _print_centred(f"Prepared for {user_name}")
    _print_divider("═")

    # ── Calorie & Macros ──────────────────────────────────────────────────────
    _section_header("DAILY CALORIE TARGET")
    print(f"  {_BOLD}{plan['calories']} kcal / day{_RESET}\n")

    _section_header("MACRONUTRIENT SPLIT")
    macros = plan.get("macros", {})
    print(f"  {'Carbohydrates':<20} {macros.get('carbohydrates', 'N/A')}")
    print(f"  {'Protein':<20} {macros.get('protein', 'N/A')}")
    print(f"  {'Fats':<20} {macros.get('fats', 'N/A')}")

    # ── Meal Plan ─────────────────────────────────────────────────────────────
    _section_header("SAMPLE DAILY MEAL PLAN")
    meals = plan.get("meals", {})
    meal_order = ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner"]
    meal_icons = ["🌅", "🍎", "☀️ ", "🫐", "🌙"]

    for icon, meal_name in zip(meal_icons, meal_order):
        description = meals.get(meal_name, "N/A")
        print(f"\n  {icon}  {_CYAN}{_BOLD}{meal_name}{_RESET}")
        print(f"     {_wrap_text(description, indent=5)}")

    # ── Foods to Prioritise ───────────────────────────────────────────────────
    _section_header("FOODS TO PRIORITISE")
    for item in plan.get("prioritise", []):
        print(f"  {_GREEN}✔{_RESET}  {item}")

    # ── Foods to Avoid ────────────────────────────────────────────────────────
    _section_header("FOODS TO AVOID / LIMIT")
    for item in plan.get("avoid", []):
        print(f"  {_RED}✘{_RESET}  {item}")

    # ── Hydration ─────────────────────────────────────────────────────────────
    _section_header("HYDRATION GUIDELINE")
    print(f"  💧  {_wrap_text(plan.get('hydration', 'N/A'), indent=6)}")

    # ── Lifestyle Tip ─────────────────────────────────────────────────────────
    _section_header("LIFESTYLE TIP")
    print(f"  💡  {_wrap_text(plan.get('lifestyle_tip', 'N/A'), indent=6)}")

    _print_divider("═")
    print()


def display_welcome() -> None:
    """Print the welcome screen shown at application launch."""
    _print_divider("═")
    _print_centred("AI-POWERED MALNUTRITION TRACKER", bold=True)
    _print_centred("Personalised BMI & Diet Recommendation Tool")
    _print_divider("─")
    print()
    print("  This tool will:")
    print("    • Calculate your Body Mass Index (BMI)")
    print("    • Classify your nutritional status (WHO standards)")
    print("    • Generate a personalised daily diet plan via AI")
    print("    • Track your progress across sessions")
    print()
    print("  Type  exit  or  quit  at any prompt to leave the app.")
    print()
    _print_divider("═")
    print()


def display_progress_header() -> None:
    """Print a divider before the progress/history section."""
    _print_divider("─")
    _print_centred("SESSION HISTORY", bold=True)
    _print_divider("─")


def display_error(message: str) -> None:
    """Print a formatted error message."""
    print(f"\n  {_RED}[ERROR]{_RESET} {message}\n")


def display_info(message: str) -> None:
    """Print a formatted informational message."""
    print(f"\n  {_YELLOW}[INFO]{_RESET} {message}\n")


def display_success(message: str) -> None:
    """Print a formatted success message."""
    print(f"\n  {_GREEN}[OK]{_RESET} {message}\n")


# ──────────────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────────────

def _print_divider(char: str = "─") -> None:
    print(f"  {char * _WIDTH}")


def _print_centred(text: str, bold: bool = False) -> None:
    padding = (_WIDTH - len(text)) // 2
    line = " " * padding + text
    if bold:
        print(f"  {_BOLD}{line}{_RESET}")
    else:
        print(f"  {line}")


def _section_header(title: str) -> None:
    print(f"\n  {_BLUE}{_BOLD}{title}{_RESET}")
    print(f"  {'─' * len(title)}")


def _classification_colour(classification: str) -> str:
    return {
        "Underweight": _YELLOW,
        "Normal":      _GREEN,
        "Overweight":  _YELLOW,
        "Obese":       _RED,
    }.get(classification, _RESET)


def _wrap_text(text: str, indent: int = 0, width: int = 60) -> str:
    """Wrap long text lines to fit the terminal panel width."""
    words = text.split()
    lines = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = current + " " + word if current else word
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    joiner = "\n" + " " * indent
    return joiner.join(lines)

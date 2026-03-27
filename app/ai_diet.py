import anthropic
from config.settings import ANTHROPIC_API_KEY
from app.fallback_diet import get_fallback_diet_plan


def generate_diet_plan(user_profile: dict) -> dict:
   
    prompt = _build_prompt(user_profile)

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        raw_text = message.content[0].text
        return _parse_diet_response(raw_text, user_profile["daily_calorie_target"])

    except anthropic.APIConnectionError:
        print("\n[!] Could not reach the Claude API. Using offline diet plan.\n")
        return get_fallback_diet_plan(user_profile["bmi_classification"])

    except anthropic.AuthenticationError:
        print("\n[!] Invalid API key. Check your .env file. Using offline diet plan.\n")
        return get_fallback_diet_plan(user_profile["bmi_classification"])

    except anthropic.APIStatusError as e:
        print(f"\n[!] API error ({e.status_code}). Using offline diet plan.\n")
        return get_fallback_diet_plan(user_profile["bmi_classification"])


# ──────────────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────────────

def _build_prompt(p: dict) -> str:
    """Build the structured prompt sent to the Claude API."""
    return f"""You are a certified nutritionist. Generate a personalised, evidence-based
diet plan for the following individual.

User profile:
  Name            : {p['name']}
  Age             : {p['age']} years
  Gender          : {p['gender']}
  Height          : {p['height_cm']} cm
  Weight          : {p['weight_kg']} kg
  Activity level  : {p['activity_level']}
  BMI             : {p['bmi']:.2f}
  Classification  : {p['bmi_classification']}
  Daily calories  : {p['daily_calorie_target']} kcal

Return your answer in EXACTLY this format — do not add extra sections:

MACROS:
Carbohydrates: <percentage>%
Protein: <percentage>%
Fats: <percentage>%

MEALS:
Breakfast: <description>
Morning Snack: <description>
Lunch: <description>
Afternoon Snack: <description>
Dinner: <description>

PRIORITISE:
- <food item>
- <food item>
- <food item>
- <food item>
- <food item>

AVOID:
- <food item>
- <food item>
- <food item>
- <food item>

HYDRATION:
<one sentence guideline>

LIFESTYLE TIP:
<one sentence tip tailored to the BMI category>
"""


def _parse_diet_response(raw: str, calorie_target: int) -> dict:
   
    plan = {
        "source": "Claude AI",
        "calories": calorie_target,
        "macros": {"carbohydrates": "N/A", "protein": "N/A", "fats": "N/A"},
        "meals": {
            "Breakfast": "N/A",
            "Morning Snack": "N/A",
            "Lunch": "N/A",
            "Afternoon Snack": "N/A",
            "Dinner": "N/A",
        },
        "prioritise": [],
        "avoid": [],
        "hydration": "N/A",
        "lifestyle_tip": "N/A",
    }

    section = None

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        upper = line.upper()

        # Detect section headers
        if upper.startswith("MACROS:"):
            section = "macros"
            continue
        elif upper.startswith("MEALS:"):
            section = "meals"
            continue
        elif upper.startswith("PRIORITISE:"):
            section = "prioritise"
            continue
        elif upper.startswith("AVOID:"):
            section = "avoid"
            continue
        elif upper.startswith("HYDRATION:"):
            section = "hydration"
            rest = line[len("HYDRATION:"):].strip()
            if rest:
                plan["hydration"] = rest
            continue
        elif upper.startswith("LIFESTYLE TIP:"):
            section = "lifestyle_tip"
            rest = line[len("LIFESTYLE TIP:"):].strip()
            if rest:
                plan["lifestyle_tip"] = rest
            continue

        # Parse content by section
        if section == "macros":
            if ":" in line:
                key, _, val = line.partition(":")
                key = key.strip().lower()
                val = val.strip().rstrip("%")
                if key in plan["macros"]:
                    plan["macros"][key] = val + "%"

        elif section == "meals":
            if ":" in line:
                meal_name, _, description = line.partition(":")
                meal_name = meal_name.strip()
                if meal_name in plan["meals"]:
                    plan["meals"][meal_name] = description.strip()

        elif section == "prioritise":
            item = line.lstrip("-•* ").strip()
            if item:
                plan["prioritise"].append(item)

        elif section == "avoid":
            item = line.lstrip("-•* ").strip()
            if item:
                plan["avoid"].append(item)

        elif section == "hydration":
            plan["hydration"] += " " + line

        elif section == "lifestyle_tip":
            plan["lifestyle_tip"] += " " + line

    return plan
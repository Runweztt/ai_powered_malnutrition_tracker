import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.settings import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
from app.fallback_diet import get_fallback_plan

try:
    import anthropic
    _CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
except ImportError:
    _CLIENT = None


def generate_diet_plan(user_profile: dict, bmi_data: dict) -> str:
    if _CLIENT is None:
        return get_fallback_plan(bmi_data["classification"], bmi_data["calorie_target"])

    prompt = f"""
You are a registered nutritionist. Create a personalised diet plan for:

Name           : {user_profile['username']}
Age            : {user_profile['age']}
Gender         : {user_profile['gender']}
Activity level : {user_profile['activity_level']}
BMI            : {bmi_data['bmi_value']} ({bmi_data['classification']})
Daily target   : {bmi_data['calorie_target']} kcal

Provide a structured plan with:
1. Macronutrient split (carbs / protein / fats as percentages)
2. Sample daily meal plan (breakfast, lunch, dinner, 2 snacks)
3. Top 5 foods to prioritise
4. Top 3 foods to avoid
5. Daily hydration guideline
6. One lifestyle tip tailored to the BMI category

Be concise and practical. Use clear headings.
"""

    try:
        message = _CLIENT.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    except Exception as e:
        print(f"\n  [API WARNING] {e}")
        print("  Using offline fallback plan instead.\n")
        return get_fallback_plan(bmi_data["classification"], bmi_data["calorie_target"])

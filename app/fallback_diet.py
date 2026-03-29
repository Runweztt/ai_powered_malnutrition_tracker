PLANS = {
    "Underweight": """
GOAL: Healthy weight gain through a calorie surplus and nutrient-dense foods.

Macronutrient split:  Carbs 50%  |  Protein 25%  |  Fats 25%

Sample meal plan:
  Breakfast : Oatmeal with banana, peanut butter, and full-fat milk
  Snack 1   : Greek yoghurt with mixed nuts and honey
  Lunch     : Brown rice, grilled chicken, avocado, steamed vegetables
  Snack 2   : Whole grain bread with nut butter and a glass of milk
  Dinner    : Salmon, sweet potato, and stir-fried vegetables in olive oil

Prioritise : Nuts, whole grains, legumes, avocado, lean proteins
Avoid      : Junk food, excessive caffeine, diet/low-fat products
Hydration  : 2.0–2.5 litres of water daily
Tip        : Aim for 3 meals and 2–3 snacks daily. Add light strength
             training 2–3 times per week to convert calories into muscle.
""",
    "Normal": """
GOAL: Maintain current weight with a balanced, nutritious diet.

Macronutrient split:  Carbs 50%  |  Protein 20%  |  Fats 30%

Sample meal plan:
  Breakfast : Scrambled eggs, whole grain toast, and fresh fruit
  Snack 1   : Apple with a small handful of almonds
  Lunch     : Mixed salad with grilled chicken, olive oil, and quinoa
  Snack 2   : Low-fat yoghurt with berries
  Dinner    : Grilled fish, roasted vegetables, and brown rice

Prioritise : Colourful vegetables, whole grains, lean proteins, healthy fats
Avoid      : Sugary beverages, highly processed snacks, excessive alcohol
Hydration  : 2.0–2.5 litres of water daily
Tip        : Aim for 150 minutes of moderate exercise per week.
""",
    "Overweight": """
GOAL: Gradual weight loss through a moderate calorie deficit.

Macronutrient split:  Carbs 40%  |  Protein 30%  |  Fats 30%

Sample meal plan:
  Breakfast : Vegetable omelette with 2 eggs and whole grain toast
  Snack 1   : Carrot sticks with hummus
  Lunch     : Large salad with grilled turkey, chickpeas, lemon dressing
  Snack 2   : Small apple and 10 almonds
  Dinner    : Baked chicken breast, steamed broccoli, small portion quinoa

Prioritise : High-fibre vegetables, lean proteins, whole grains, legumes
Avoid      : Refined carbohydrates, fried food, sugary snacks
Hydration  : 2.5–3.0 litres of water daily — drink a glass before meals
Tip        : Target a deficit of 300–500 kcal per day combined with
             30 minutes of brisk walking most days.
""",
    "Obese": """
GOAL: Sustained weight loss through structured calorie deficit.
      Consult a healthcare provider before making major dietary changes.

Macronutrient split:  Carbs 35%  |  Protein 35%  |  Fats 30%

Sample meal plan:
  Breakfast : Boiled eggs with cucumber slices and unsweetened herbal tea
  Snack 1   : Small handful of walnuts
  Lunch     : Grilled fish with a large portion of steamed vegetables
  Snack 2   : Low-fat cottage cheese with sliced tomatoes
  Dinner    : Baked chicken or tofu, roasted cauliflower, small salad

Prioritise : Non-starchy vegetables, high-protein low-fat foods, fibre
Avoid      : All sugary beverages, processed and packaged foods, high-fat dairy
Hydration  : 3.0 litres of water daily — replace all sugary drinks immediately
Tip        : Start with low-impact activity such as walking or swimming
             for 20–30 minutes daily. Consider a dietitian for a supervised plan.
"""
}


def get_fallback_plan(classification: str, calorie_target: int) -> str:
    plan = PLANS.get(classification, PLANS["Normal"])
    return f"\n  [Offline plan]  Daily target: {calorie_target} kcal\n" + plan

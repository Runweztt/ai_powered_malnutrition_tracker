
# ──────────────────────────────────────────────────────────────────────────────
# Static plan templates
# ──────────────────────────────────────────────────────────────────────────────

_PLANS = {
    "Underweight": {
        "source": "Offline Fallback",
        "macros": {
            "carbohydrates": "50%",
            "protein": "25%",
            "fats": "25%",
        },
        "meals": {
            "Breakfast": "Oatmeal with whole milk, banana, and peanut butter",
            "Morning Snack": "Greek yoghurt with honey and mixed nuts",
            "Lunch": "Chicken and rice bowl with avocado and olive oil dressing",
            "Afternoon Snack": "Whole-grain bread with almond butter and a glass of milk",
            "Dinner": "Grilled salmon, sweet potato mash, and steamed broccoli",
        },
        "prioritise": [
            "Whole grains (oats, brown rice, whole wheat bread)",
            "Lean proteins (chicken, fish, eggs, legumes)",
            "Healthy fats (avocado, nuts, olive oil)",
            "Dairy or fortified plant-based alternatives",
            "Calorie-dense fruits (bananas, mangoes, dates)",
        ],
        "avoid": [
            "Skipping meals or eating irregularly",
            "Low-calorie diet foods or diet drinks",
            "Excessive caffeine (suppresses appetite)",
            "High-fibre foods in very large quantities (fills up quickly)",
        ],
        "hydration": "Drink at least 2 litres of water per day; include calorie-containing "
                     "drinks such as milk or 100% fruit juice to support weight gain.",
        "lifestyle_tip": "Aim to eat 5–6 small, calorie-dense meals throughout the day "
                         "and include light resistance training to build muscle mass.",
    },

    "Normal": {
        "source": "Offline Fallback",
        "macros": {
            "carbohydrates": "45%",
            "protein": "30%",
            "fats": "25%",
        },
        "meals": {
            "Breakfast": "Scrambled eggs with wholegrain toast and fresh orange juice",
            "Morning Snack": "Apple slices with a handful of mixed nuts",
            "Lunch": "Grilled chicken salad with quinoa, vegetables, and lemon dressing",
            "Afternoon Snack": "Low-fat yoghurt with fresh berries",
            "Dinner": "Baked fish with roasted vegetables and brown rice",
        },
        "prioritise": [
            "Vegetables and leafy greens (spinach, kale, broccoli)",
            "Lean proteins (chicken, turkey, fish, legumes)",
            "Whole grains (quinoa, oats, whole wheat)",
            "Fresh fruits (berries, apples, citrus)",
            "Healthy fats (olive oil, nuts, seeds)",
        ],
        "avoid": [
            "Processed and ultra-processed snack foods",
            "Sugary beverages (sodas, energy drinks)",
            "Excessive saturated and trans fats",
            "High-sodium ready meals",
        ],
        "hydration": "Drink 2–2.5 litres of water daily to support metabolism and "
                     "maintain energy levels throughout the day.",
        "lifestyle_tip": "Maintain your healthy weight by combining a balanced diet with "
                         "at least 150 minutes of moderate aerobic activity per week.",
    },

    "Overweight": {
        "source": "Offline Fallback",
        "macros": {
            "carbohydrates": "40%",
            "protein": "35%",
            "fats": "25%",
        },
        "meals": {
            "Breakfast": "Vegetable omelette (2 eggs) with wholegrain toast and green tea",
            "Morning Snack": "A small handful of unsalted nuts and a piece of fruit",
            "Lunch": "Large mixed salad with grilled chicken, chickpeas, and vinaigrette",
            "Afternoon Snack": "Carrot and cucumber sticks with hummus",
            "Dinner": "Baked skinless chicken breast with steamed vegetables and a small "
                      "portion of brown rice",
        },
        "prioritise": [
            "High-fibre vegetables (broccoli, cauliflower, zucchini)",
            "Lean proteins (chicken breast, turkey, tofu, legumes)",
            "Low-glycaemic fruits (berries, pears, apples)",
            "Whole grains in moderate portions",
            "Water-rich foods (cucumber, celery, lettuce)",
        ],
        "avoid": [
            "White bread, white rice, and refined pasta",
            "Sugary snacks, pastries, and desserts",
            "Fried and fast food",
            "Alcohol and sugary drinks",
            "Large portion sizes — use a smaller plate",
        ],
        "hydration": "Drink at least 2.5 litres of water per day; drink a glass of water "
                     "before each meal to help reduce portion sizes naturally.",
        "lifestyle_tip": "Combine a moderate calorie deficit with 30 minutes of brisk "
                         "walking or cycling daily to steadily reduce body weight.",
    },

    "Obese": {
        "source": "Offline Fallback",
        "macros": {
            "carbohydrates": "35%",
            "protein": "40%",
            "fats": "25%",
        },
        "meals": {
            "Breakfast": "Boiled eggs with sautéed spinach and half a wholegrain wrap",
            "Morning Snack": "A small apple or pear",
            "Lunch": "Lentil soup with a side of steamed vegetables (no added butter)",
            "Afternoon Snack": "Low-fat cottage cheese with sliced cucumber",
            "Dinner": "Grilled fish or tofu with a large portion of non-starchy vegetables "
                      "and a tablespoon of olive oil",
        },
        "prioritise": [
            "Non-starchy vegetables (leafy greens, peppers, mushrooms)",
            "High-protein foods (eggs, fish, chicken, legumes)",
            "Legumes and lentils (high fibre, high satiety)",
            "Low-sugar fruits (berries, watermelon)",
            "Healthy cooking methods: grilling, steaming, baking",
        ],
        "avoid": [
            "All sugary and sweetened beverages",
            "Processed meats (sausages, bacon, hot dogs)",
            "Deep-fried food of any kind",
            "High-calorie sauces and dressings",
            "Late-night eating and oversized portions",
        ],
        "hydration": "Aim for 3 litres of water daily; replace all sugary drinks with "
                     "plain water, herbal teas, or sparkling water with lemon.",
        "lifestyle_tip": "Consult a healthcare professional before starting any diet "
                         "programme; begin with low-impact exercise such as swimming or "
                         "walking, gradually increasing duration each week.",
    },
}


# ──────────────────────────────────────────────────────────────────────────────
# Public interface
# ──────────────────────────────────────────────────────────────────────────────

def get_fallback_diet_plan(bmi_classification: str) -> dict:
   
    plan = _PLANS.get(bmi_classification)

    if plan is None:
        # Defensive fallback — should never happen with validated BMI input
        plan = _PLANS["Normal"].copy()
        plan["lifestyle_tip"] = (
            "An unrecognised BMI classification was supplied; "
            "a general balanced diet plan has been applied."
        )

    return plan
# AI-Powered Malnutrition Tracker

A command-line Python application that helps users assess their nutritional
status and receive personalised diet recommendations powered by the Anthropic
Claude AI. All session data is stored in a MySQL database for progress tracking
over time.

---

## How the program works

When you run the program, it walks you through five stages:

**1. Onboarding**
You are welcomed and asked to enter your personal details: name, age, gender,
height (cm), weight (kg), and activity level (sedentary / moderate / active).
All inputs are validated before the program continues.

**2. BMI calculation**
Your Body Mass Index is calculated using the standard WHO formula:

    BMI = weight (kg) ÷ height (m)²

Your result is then classified into one of four categories:

| Classification | BMI Range     |
|----------------|---------------|
| Underweight    | Below 18.5    |
| Normal         | 18.5 – 24.9   |
| Overweight     | 25.0 – 29.9   |
| Obese          | 30.0 and above|

**3. Calorie target**
Based on your BMI classification, age, gender, and activity level, the program
calculates a personalised daily calorie target to help you reach or maintain a
healthy weight.

**4. AI diet plan**
Your full profile is sent to the Anthropic Claude API, which generates a
structured, evidence-based diet plan including:
- Recommended macronutrient split (carbohydrates, protein, fats)
- A sample daily meal plan (breakfast, lunch, dinner, two snacks)
- Foods to prioritise and foods to avoid
- Daily hydration guideline
- A lifestyle tip tailored to your BMI category

If the API is unavailable, the program automatically falls back to a built-in
offline diet plan based on your BMI classification.

**5. Progress tracking**
Your session (profile, BMI, and diet plan) is saved to the MySQL database.
Each time you run the program again under the same name, your BMI history is
loaded and displayed as a trend table so you can monitor your progress over
multiple sessions. You can also export your session summary to a `.txt` file.

---

## Project structure
```
malnutrition_tracker/
├── main.py                 ← entry point, runs the app
├── config/settings.py      ← loads environment variables
├── app/
│   ├── inputs.py           ← user input collection and validation
│   ├── bmi.py              ← BMI calculation and classification
│   ├── calories.py         ← daily calorie target calculation
│   ├── ai_diet.py          ← Claude API diet plan generation
│   ├── fallback_diet.py    ← offline static diet plan
│   ├── display.py          ← terminal output formatting
│   └── reports.py          ← progress report and .txt export
├── database/
│   ├── db_connect.py       ← MySQL connection
│   ├── queries.py          ← save and load session data
│   ├── schema.sql          ← database table definitions
│   └── seed.sql            ← sample data for testing
└── tests/                  ← unit tests for all modules
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Runweztt/malnutrition_tracker.git
cd malnutrition_tracker
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your values:
```
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASS=your_mysql_password
DB_NAME=malnutrition_tracker
ANTHROPIC_API_KEY=your_api_key_here
```

### 5. Set up the database
```bash
mysql -u your_user -p < database/schema.sql
```

### 6. Run the app
```bash
python main.py
```

---

## Git branches

| Member | Branch     | Responsibility                        |
|--------|------------|---------------------------------------|
| M1     | feature/m1 | Entry point, inputs, config           |
| M2     | feature/m2 | BMI calculation and calorie targets   |
| M3     | feature/m3 | AI diet generation and display        |
| M4     | feature/m4 | Database layer and schema             |
| M5     | feature/m5 | Progress reporting and export         |

---

## References
- WHO Malnutrition: https://www.who.int/news-room/fact-sheets/detail/malnutrition
- CDC BMI: https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html
- Anthropic Claude API: https://docs.anthropic.com
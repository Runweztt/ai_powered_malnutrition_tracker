# AI-Powered Malnutrition Tracker

A Python CLI application that calculates BMI, classifies nutritional status,
and generates personalised diet plans using the Anthropic Claude API.
User data is stored in a MySQL database.

---

## Project structure

```
malnutrition_tracker/
├── shared/          ← config, DB connection, schema — everyone imports from here
├── member_1/        ← entry point, CLI onboarding, input validation
├── member_2/        ← BMI calculation and calorie targets
├── member_3/        ← AI diet generation and terminal display
├── member_4/        ← MySQL database queries and migrations
├── member_5/        ← progress reports and session export
```

---

## Setup instructions

### 1. Clone the repo
```bash
git clone https://github.com/Runweztt/malnutrition_tracker.git
cd malnutrition_tracker
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r shared/requirements.txt
```

### 4. Create your .env file
Copy the example and fill in your own values:
```bash
cp member_1/.env.example .env
```

Edit `.env`:
```
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASS=your_mysql_password
DB_NAME=malnutrition_tracker
ANTHROPIC_API_KEY=your_api_key_here
```

### 5. Set up the MySQL database
```bash
mysql -u your_user -p < shared/schema.sql
```

### 6. (Optional) Load sample data
```bash
mysql -u your_user -p malnutrition_tracker < member_4/seed.sql
```

### 7. Run the app
```bash
python member_1/main.py
```

---

## Git workflow — one branch per member

| Member | Branch name       | Responsibility              |
|--------|-------------------|-----------------------------|
| M1     | feature/member-1  | Foundation & entry point    |
| M2     | feature/member-2  | BMI engine                  |
| M3     | feature/member-3  | AI API & diet display       |
| M4     | feature/member-4  | MySQL database layer        |
| M5     | feature/member-5  | Reporting & export          |

Each member works only on their own branch and opens a Pull Request to `main`.

---

## Running tests
```bash
python -m pytest member_1/tests/
python -m pytest member_2/tests/
python -m pytest member_4/tests/
python -m pytest member_5/tests/
```

---

## References
- WHO Malnutrition: https://www.who.int/news-room/fact-sheets/detail/malnutrition
- CDC BMI: https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html
- Anthropic Claude API: https://docs.anthropic.com

from database.db_connect import get_connection

def get_or_create_user(username, email, age, gender, activity_level):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM users WHERE user_email = %s", (email,))
    user = cursor.fetchone()
    if user:
        cursor.close()
        conn.close()
        return user["user_id"]
    cursor.execute(
        "INSERT INTO users (user_name, user_email, age, gender, activity_level) VALUES (%s, %s, %s, %s, %s)",
        (username, email, age, gender, activity_level)
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return user_id

def save_user_data(user_id, weight, height, bmi_value, classification, calorie_target, diet_plan_text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bmi_records (user_id, weight, height, bmi_value, classification, calorie_target) VALUES (%s, %s, %s, %s, %s, %s)",
        (user_id, weight, height, bmi_value, classification, calorie_target)
    )
    record_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO diet_plans (record_id, plan_text) VALUES (%s, %s)",
        (record_id, diet_plan_text)
    )
    conn.commit()
    cursor.close()
    conn.close()

def load_user_history(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM users WHERE user_email = %s", (email,))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        conn.close()
        return []
    cursor.execute(
        "SELECT recorded_at, bmi_value, classification, calorie_target FROM bmi_records WHERE user_id = %s ORDER BY recorded_at ASC",
        (user["user_id"],)
    )
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history
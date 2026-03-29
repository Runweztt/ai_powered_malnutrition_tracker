import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_connect import get_client


def _get_or_create_user(client, user_profile: dict) -> int:
    res = (client.table("users")
                 .select("id")
                 .eq("username", user_profile["username"])
                 .execute())

    if res.data:
        return res.data[0]["id"]

    insert = (client.table("users")
                    .insert({
                        "username":       user_profile["username"],
                        "age":            user_profile["age"],
                        "gender":         user_profile["gender"],
                        "activity_level": user_profile["activity_level"]
                    })
                    .execute())
    return insert.data[0]["id"]


def save_user_data(user_profile: dict, bmi_data: dict, diet_plan: str) -> None:
    try:
        client = get_client()

        user_id = _get_or_create_user(client, user_profile)

        bmi_res = (client.table("bmi_records")
                         .insert({
                             "user_id":        user_id,
                             "height_cm":      user_profile["height_cm"],
                             "weight_kg":      user_profile["weight_kg"],
                             "bmi_value":      bmi_data["bmi_value"],
                             "classification": bmi_data["classification"],
                             "calorie_target": bmi_data["calorie_target"]
                         })
                         .execute())

        bmi_record_id = bmi_res.data[0]["id"]
        source = "fallback" if "[Offline plan]" in diet_plan else "ai"

        (client.table("diet_plans")
               .insert({
                   "bmi_record_id": bmi_record_id,
                   "plan_text":     diet_plan,
                   "source":        source
               })
               .execute())

        print("\n  [✓] Session saved to Supabase.")

    except Exception as e:
        print(f"\n  [DB ERROR] Could not save session: {e}")


def load_user_history(username: str) -> list:
    try:
        client = get_client()

        user_res = (client.table("users")
                          .select("id")
                          .eq("username", username)
                          .execute())

        if not user_res.data:
            return []

        user_id = user_res.data[0]["id"]

        history = (client.table("bmi_records")
                         .select("recorded_at, bmi_value, classification, calorie_target")
                         .eq("user_id", user_id)
                         .order("recorded_at")
                         .execute())

        return history.data

    except Exception as e:
        print(f"\n  [DB ERROR] Could not load history: {e}")
        return []
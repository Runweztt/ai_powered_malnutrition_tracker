from database.queries import get_or_create_user, save_user_data, load_user_history

user_id = get_or_create_user("Didier", "d.abizera@alustudent.com", 22, "male", "moderate")
print(f"User ID: {user_id}")

save_user_data(user_id, 75, 1.75, 24.49, "Normal", 2200, "Eat balanced meals with vegetables and proteins.")
print("Data saved successfully!")

history = load_user_history("d.abizera@alustudent.com")
print("User history:", history)
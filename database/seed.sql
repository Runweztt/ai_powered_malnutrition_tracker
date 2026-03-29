

INSERT INTO users (username, age, gender, activity_level) VALUES
  ('alice', 28, 'female', 'moderate'),
  ('bob',   35, 'male',   'active'),
  ('carol', 22, 'female', 'sedentary');

INSERT INTO bmi_records (user_id, height_cm, weight_kg, bmi_value, classification, calorie_target) VALUES
  (1, 165, 58,  21.30, 'Normal',      1950),
  (1, 165, 61,  22.41, 'Normal',      1950),
  (2, 180, 95,  29.32, 'Overweight',  2200),
  (3, 160, 42,  16.41, 'Underweight', 2400);

INSERT INTO diet_plans (bmi_record_id, plan_text, source) VALUES
  (1, 'Sample plan — alice session 1', 'fallback'),
  (2, 'Sample plan — alice session 2', 'ai'),
  (3, 'Sample plan — bob',             'ai'),
  (4, 'Sample plan — carol',           'fallback');
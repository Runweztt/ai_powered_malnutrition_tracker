use malnutrition_tracker;
create table users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(100) UNIQUE NOT NULL,
    age INT,
    gender VARCHAR(20),
    activity_level VARCHAR(40),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    );



create table bmi_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    bmi_value FLOAT NOT NULL,
    classification VARCHAR(20) NOT NULL,
    calorie_target INT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


create table diet_plans (
    plan_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    record_id INT NOT NULL,
    plan_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (record_id) REFERENCES bmi_records(record_id)
 );



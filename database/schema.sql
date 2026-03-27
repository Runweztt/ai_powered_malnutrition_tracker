

CREATE TABLE IF NOT EXISTS users (
    id             SERIAL PRIMARY KEY,
    username       VARCHAR(100) NOT NULL UNIQUE,
    age            INT          NOT NULL,
    gender         VARCHAR(10)  NOT NULL,
    activity_level VARCHAR(20)  NOT NULL,
    created_at     TIMESTAMP    DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bmi_records (
    id             SERIAL PRIMARY KEY,
    user_id        INT          NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    height_cm      FLOAT        NOT NULL,
    weight_kg      FLOAT        NOT NULL,
    bmi_value      FLOAT        NOT NULL,
    classification VARCHAR(20)  NOT NULL,
    calorie_target INT          NOT NULL,
    recorded_at    TIMESTAMP    DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS diet_plans (
    id             SERIAL PRIMARY KEY,
    bmi_record_id  INT          NOT NULL REFERENCES bmi_records(id) ON DELETE CASCADE,
    plan_text      TEXT         NOT NULL,
    source         VARCHAR(20)  NOT NULL DEFAULT 'ai',
    generated_at   TIMESTAMP    DEFAULT NOW()
);
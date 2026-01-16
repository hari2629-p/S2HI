import mysql.connector

# ---------------- DB CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nandu",
    database="S2PHI"
)

cursor = db.cursor()

# ---------------- TABLE CREATION ----------------

# Users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    age_group VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Sessions
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Questions (AGE-SPECIFIC)
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    domain VARCHAR(10),
    difficulty VARCHAR(10),
    age_group VARCHAR(10),
    question_text TEXT,
    correct_option VARCHAR(255),
    options JSON
)
""")

# Responses
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_responses (
    response_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    user_id INT,
    question_id INT,
    domain VARCHAR(10),
    difficulty VARCHAR(10),
    correct BOOLEAN,
    response_time_ms INT,
    confidence VARCHAR(10),
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
)
""")

# Mistake Patterns
cursor.execute("""
CREATE TABLE IF NOT EXISTS mistake_patterns (
    mistake_id INT AUTO_INCREMENT PRIMARY KEY,
    response_id INT,
    mistake_type VARCHAR(50),
    severity VARCHAR(10),
    FOREIGN KEY (response_id) REFERENCES user_responses(response_id)
)
""")

# Final Predictions
cursor.execute("""
CREATE TABLE IF NOT EXISTS final_predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    user_id INT,
    dyslexia_risk FLOAT,
    dyscalculia_risk FLOAT,
    attention_risk FLOAT,
    final_label VARCHAR(25),
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

db.commit()

# ---------------- HELPER FUNCTIONS ----------------

def create_user(age_group):
    cursor.execute(
        "INSERT INTO users (age_group) VALUES (%s)",
        (age_group,)
    )
    db.commit()
    return cursor.lastrowid


def start_session(user_id):
    cursor.execute(
        "INSERT INTO sessions (user_id) VALUES (%s)",
        (user_id,)
    )
    db.commit()
    return cursor.lastrowid


def end_session(session_id):
    cursor.execute(
        "UPDATE sessions SET completed = TRUE WHERE session_id = %s",
        (session_id,)
    )
    db.commit()


def get_question(domain, difficulty, age_group):
    cursor.execute("""
        SELECT question_id, question_text, options
        FROM questions
        WHERE domain=%s AND difficulty=%s AND age_group=%s
        ORDER BY RAND()
        LIMIT 1
    """, (domain, difficulty, age_group))
    return cursor.fetchone()


def store_response(session_id, user_id, question_id,
                   domain, difficulty, correct,
                   response_time_ms, confidence):

    cursor.execute("""
        INSERT INTO user_responses
        (session_id, user_id, question_id,
         domain, difficulty, correct,
         response_time_ms, confidence)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (session_id, user_id, question_id,
          domain, difficulty, correct,
          response_time_ms, confidence))
    db.commit()
    return cursor.lastrowid


def store_mistake(response_id, mistake_type, severity):
    cursor.execute("""
        INSERT INTO mistake_patterns
        (response_id, mistake_type, severity)
        VALUES (%s,%s,%s)
    """, (response_id, mistake_type, severity))
    db.commit()


def store_prediction(session_id, user_id,
                     dyslexia, dyscalculia,
                     attention, label):
    cursor.execute("""
        INSERT INTO final_predictions
        (session_id, user_id,
         dyslexia_risk, dyscalculia_risk,
         attention_risk, final_label)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (session_id, user_id,
          dyslexia, dyscalculia,
          attention, label))
    db.commit()

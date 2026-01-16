import pandas as pd
import joblib
import os
import sys

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from question_generator_model import QuestionGeneratorModel
except ImportError as e:
    print("❌ ERROR: Could not find 'question_generator_model.py'")
    sys.exit(1)

def train_and_save():
    print(f"🚀 Starting 7-Feature Training in: {current_dir}")

    # 2. LOAD DATA
    csv_path = os.path.join(current_dir, "training_data_phase1.csv")
    
    if not os.path.exists(csv_path):
        print(f"❌ ERROR: 'training_data_phase1.csv' missing. Run make_data.py first!")
        return

    print("📊 Loading data...")
    df = pd.read_csv(csv_path)

    # 3. PREPARE 7 FEATURES (Updated list)
    features = [
        "last_correct", 
        "last_response_time", 
        "diff_easy", 
        "diff_medium", 
        "diff_hard", 
        "session_accuracy", 
        "current_domain" # <--- Feature #7 (Replaces d_read, d_math, etc.)
    ]
    
    # Check for missing columns
    missing = [col for col in features if col not in df.columns]
    if missing:
        print(f"❌ ERROR: CSV is missing columns: {missing}")
        return

    X = df[features].values
    y = df[["target_domain", "target_diff"]].values

    # 4. TRAIN
    print(f"🧠 Training on {len(df)} rows...")
    model = QuestionGeneratorModel()
    model.fit(X, y)

    # 5. TEST
    print("🔍 Testing Generator...")
    try:
        q = model.generate_question('math', 'medium')
        print(f"   ✅ Generated: \"{q['question_text']}\"")
    except Exception as e:
        print(f"   ❌ Test Failed: {e}")

    # 6. SAVE
    output_path = os.path.join(current_dir, "question_model.pkl")
    joblib.dump(model, output_path)
    print(f"\n✅ FINAL SUCCESS! Model saved to: {output_path}")

if __name__ == "__main__":
    train_and_save()
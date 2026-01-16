import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
import joblib

def train_adaptive_engine():
    # 1. Load the simulated text book
    df = pd.read_csv("training_data_phase1.csv")
    
    # 2. Separate Inputs (X) and Answers (y)
    X = df[["cur_domain", "cur_diff", "correct", "time_ms"]]
    y = df[["target_domain", "target_diff"]]

    # 3. Initialize the Brain (Random Forest)
    # MultiOutputClassifier allows predicting 2 things at once (Domain AND Difficulty)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    model = MultiOutputClassifier(rf)

    # 4. Train
    print("🧠 Training the Adaptive Model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model.fit(X_train, y_train)

    # 5. Check Score
    accuracy = model.score(X_test, y_test)
    print(f"🎯 Model Accuracy: {accuracy:.2%}")

    # 6. Save the Brain
    joblib.dump(model, "adaptive_engine_model.pkl")
    print("✅ Saved to 'adaptive_engine_model.pkl'")

if __name__ == "__main__":
    train_adaptive_engine()
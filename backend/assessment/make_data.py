import pandas as pd
import random

def generate_7_feature_data():
    data = []
    print("📊 Generating 7-feature data...")

    current_diff = 1
    current_domain = 0  # 0:Read, 1:Math, 2:Attn
    correct_streak = 0
    total_correct = 0

    for i in range(5000): # 5000 examples is enough
        # 1. Simulate Student
        if current_diff == 0: is_correct = 1 if random.random() > 0.2 else 0
        elif current_diff == 1: is_correct = 1 if random.random() > 0.4 else 0
        else: is_correct = 1 if random.random() > 0.6 else 0
        
        time_taken = random.randint(1000, 8000)

        # Update stats
        if is_correct: 
            correct_streak += 1
            total_correct += 1
        else: 
            correct_streak = 0
        
        accuracy = total_correct / (i + 1)

        # 2. Teacher Logic
        target_diff = current_diff
        target_domain = current_domain

        if correct_streak >= 3 and current_diff < 2: target_diff += 1
        elif not is_correct and current_diff > 0: target_diff -= 1
        
        if random.random() < 0.2: target_domain = (current_domain + 1) % 3

        # 3. Create Row (EXACTLY 7 FEATURES)
        row = {
            "last_correct": is_correct,
            "last_response_time": time_taken,
            "diff_easy": 1 if current_diff == 0 else 0,
            "diff_medium": 1 if current_diff == 1 else 0,
            "diff_hard": 1 if current_diff == 2 else 0,
            "session_accuracy": accuracy,
            "current_domain": current_domain, # <--- The 7th Feature
            
            "target_domain": target_domain,
            "target_diff": target_diff
        }
        data.append(row)
        current_diff = target_diff
        current_domain = target_domain

    df = pd.DataFrame(data)
    df.to_csv("training_data_phase1.csv", index=False)
    print("✅ Success! Created 'training_data_phase1.csv'")

if __name__ == "__main__":
    generate_7_feature_data()
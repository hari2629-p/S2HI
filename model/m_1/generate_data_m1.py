import pandas as pd
import random

# --- CONFIGURATION ---
SAMPLES = 10000
DOMAINS = [0, 1, 2] # 0: Reading, 1: Math, 2: Focus
DIFFICULTIES = [0, 1, 2] # 0: Easy, 1: Medium, 2: Hard

def get_teacher_decision(current_domain, current_diff, is_correct, time_taken):
    """
    This function acts as the 'Perfect Teacher' rulebook.
    The AI will learn to mimic this logic.
    """
    next_diff = current_diff
    next_domain = current_domain

    # Rule 1: Too Easy? (Correct + Fast) -> Level Up
    if is_correct == 1 and time_taken < 3000: # Less than 3 sec
        if current_diff < 2:
            next_diff += 1
    
    # Rule 2: Too Hard? (Wrong OR Too Slow) -> Level Down
    elif is_correct == 0 or time_taken > 10000: # More than 10 sec
        if current_diff > 0:
            next_diff -= 1
    
    # Rule 3: Random Domain Switch (To keep engagement)
    # Every ~5 turns, switch topic (simulated by random chance)
    if random.random() < 0.2: 
        possible_domains = [d for d in DOMAINS if d != current_domain]
        next_domain = random.choice(possible_domains)

    return next_domain, next_diff

def generate_dataset():
    data = []
    print("🤖 Simulating 10,000 student turns...")

    for _ in range(SAMPLES):
        # 1. Simulate a random state (What just happened?)
        current_domain = random.choice(DOMAINS)
        current_diff = random.choice(DIFFICULTIES)
        
        last_correct = random.choice([0, 1]) # 0=Wrong, 1=Right
        last_response_time = random.randint(500, 15000) # 0.5s to 15s
        
        # 2. Get the "Correct" decision based on rules
        target_domain, target_diff = get_teacher_decision(
            current_domain, current_diff, last_correct, last_response_time
        )

        # 3. Store the row
        data.append([
            current_domain, current_diff, last_correct, last_response_time, # INPUTS
            target_domain, target_diff # TARGETS (Answers)
        ])

    # Save to CSV
    columns = ["cur_domain", "cur_diff", "correct", "time_ms", "target_domain", "target_diff"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("training_data_phase1.csv", index=False)
    print("✅ 'training_data_phase1.csv' created successfully.")

if __name__ == "__main__":
    generate_dataset()
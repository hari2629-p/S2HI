"""
Question Generator Model Training Script

This script trains a model that can dynamically generate questions
for the LD screening assessment.
"""

import numpy as np
import random
from sklearn.model_selection import train_test_split
import joblib

# Import the model class from assessment module
from assessment.question_generator_model import QuestionGeneratorModel


def generate_training_data(n_samples=2000):
    """
    Generate synthetic training data for question generation.
    
    Returns:
        X: Features [cur_domain, cur_diff, correct, time_ms]
        y: Targets [target_domain, target_diff]
    """
    X = []
    y = []
    
    for _ in range(n_samples):
        # Current state
        cur_domain = random.randint(0, 2)  # 0=reading, 1=math, 2=attention
        cur_diff = random.randint(0, 2)    # 0=easy, 1=medium, 2=hard
        correct = random.randint(0, 1)
        time_ms = random.randint(500, 15000)
        
        # Adaptive logic for next question
        # If correct and fast, increase difficulty
        if correct and time_ms < 1000:
            target_diff = min(2, cur_diff + 1)
        # If wrong or slow, decrease difficulty
        elif not correct or time_ms > 5000:
            target_diff = max(0, cur_diff - 1)
        else:
            target_diff = cur_diff
        
        # Rotate domains to ensure coverage
        target_domain = (cur_domain + 1) % 3
        
        X.append([cur_domain, cur_diff, correct, time_ms])
        y.append([target_domain, target_diff])
    
    return np.array(X), np.array(y)


def train_model():
    """Train and save the question generator model."""
    print("=" * 60)
    print("Question Generator Model Training")
    print("=" * 60)
    
    # Generate training data
    print("\n📊 Generating Question Generation Training Data...")
    print("   Samples: 2000")
    X, y = generate_training_data(2000)
    print(f"   ✅ Generated {len(X)} samples")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    print("\n🤖 Training Question Generator Model...")
    model = QuestionGeneratorModel()
    
    print("   Training domain classifier...")
    print("   Training difficulty classifier...")
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    domain_accuracy = np.mean(y_pred[:, 0] == y_test[:, 0])
    difficulty_accuracy = np.mean(y_pred[:, 1] == y_test[:, 1])
    
    print(f"   ✅ Domain Accuracy: {domain_accuracy*100:.2f}%")
    print(f"   ✅ Difficulty Accuracy: {difficulty_accuracy*100:.2f}%")
    
    # Save model
    model_path = 'question_generator.pkl'
    joblib.dump(model, model_path)
    print(f"\n   💾 Saved to: {model_path}")
    
    # Test question generation
    print("\n" + "=" * 60)
    print("Testing Question Generation")
    print("=" * 60)
    
    for domain in ['reading', 'math', 'attention']:
        for difficulty in ['easy', 'medium', 'hard']:
            q = model.generate_question(domain, difficulty)
            print(f"\n{domain.upper()} - {difficulty.upper()}:")
            print(f"  Q: {q['question_text']}")
            print(f"  Options: {q['options']}")
            print(f"  Answer: {q['correct_option']}")
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE")
    print("=" * 60)
    print(f"Model saved to: {model_path}")
    print("\nThis model can generate questions dynamically!")


if __name__ == '__main__':
    train_model()

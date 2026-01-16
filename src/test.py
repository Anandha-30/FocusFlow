import os
import glob
import numpy as np
import matplotlib.pyplot as plt

from stable_baselines3 import PPO
from env import FocusEnv


# ---------------------------------------
# AUTO-DETECT MODEL IN ../models FOLDER
# ---------------------------------------

def load_latest_model():
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    print(f"🔍 Looking for models in: {model_dir}")

    # find ALL .zip files
    model_files = glob.glob(os.path.join(model_dir, "*.zip"))

    if not model_files:
        raise FileNotFoundError("❌ No model found in models/ folder. Train a model first!")

    # pick newest .zip file
    latest_model = max(model_files, key=os.path.getctime)
    print(f"📦 Loading model: {latest_model}")

    return PPO.load(latest_model)


# ---------------------------------------
# TEST THE TRAINED MODEL
# ---------------------------------------

def test_model(episodes=20):
    print("\n🚀 Starting model test...\n")

    model = load_latest_model()
    env = FocusEnv()

    rewards = []

    for ep in range(episodes):
        obs = env.reset()
        total_reward = 0
        done = False

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _, = env.step(action)
            total_reward += reward

        rewards.append(total_reward)
        print(f"🎯 Episode {ep + 1}: Total Reward = {round(total_reward, 2)}")

    avg_reward = sum(rewards) / len(rewards)
    print("\n====================================")
    print(f"✅ Average Reward over {episodes} episodes: {round(avg_reward, 2)}")
    print("====================================\n")

    # Plotting rewards
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, episodes + 1), rewards, marker='o')
    plt.title("FocusFlow AI - Model Performance")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.grid(True)
    plt.show()


# ---------------------------------------
# MAIN EXECUTION
# ---------------------------------------

if __name__ == "__main__":
    test_model(episodes=20)

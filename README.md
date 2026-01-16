# FocusFlow 

FocusFlow is a PPO-based reinforcement learning system that provides
real-time productivity suggestions based on user activity.

## Features
- PPO (Stable-Baselines3)
- Offline RL training
- Live inference (suggestion-only mode)
- Streamlit dashboard
- Modular system architecture

## Project Structure
- src/env.py — RL environment
- src/train_agent.py — PPO training
- src/main.py — live inference
- src/activity_monitor.py — activity logging
- src/dashboard.py — visualization

## Run Order
1. Activity Monitor
2. Suggestion Engine
3. Dashboard

## Tech Stack
- Python
- Gymnasium
- Stable-Baselines3
- Streamlit


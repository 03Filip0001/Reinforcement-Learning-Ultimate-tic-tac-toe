# Reinforcement Learning Ultimate Tic-Tac-Toe

This repository contains a Reinforcement Learning agent trained to master **Ultimate Tic-Tac-Toe**. The project features a cross-platform environment setup and automated training/running scripts.

## 🚀 Getting Started

You can manage the entire project using `make`. The system automatically detects your OS (Windows or Linux) and handles the virtual environment accordingly.

### 🛠 Installation & Usage

1. **Run the game** (automatically creates `.venv` and installs requirements):
```bash
   make
```
   This is the default command, equivalent to `make run`.

2. **Clean build** (wipes the environment and starts fresh):
```bash
   make environment delete
```

3. **Remove Python cache** (deletes `__pycache__` and `*.pyc` files):
```bash
   make clean
```

## 📂 Project Structure

- `src/` - Core logic, game engine, and RL agents
- `scripts/` - Maintenance scripts for environment setup and cleaning
- `.venv/` - Local virtual environment (created on first run)
- `requirements.txt` - Project dependencies

## 🧠 The Game: Ultimate Tic-Tac-Toe

Ultimate Tic-Tac-Toe is a strategic board game composed of nine Tic-Tac-Toe boards arranged in a 3-by-3 grid.

**Rules in Brief:**
- Winning a small board places your mark (X or O) in that large square
- Your move determines which small board the opponent must play in next
- Win three small boards in a row to win the entire game
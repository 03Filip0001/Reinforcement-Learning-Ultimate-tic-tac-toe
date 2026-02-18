import sys
from pathlib import Path
import argparse

from src.game import Game
from src.agent import agentTrain
from src.training.train import train

MODEL_PATH = "checkpoints/model_1.pt"

def main():
    print("\n=== Ultimate Tic-Tac-Toe ===")
    choice = input("Enter command (train/play/exit): ").strip().lower()
    
    if choice == 'train':
        # train()
        ### TRAIN AGENT
        parser = argparse.ArgumentParser()
        parser.add_argument("--iterations", type=int, default=10)
        parser.add_argument("--self_play_games", type=int, default=10)
        parser.add_argument("--mcts_simulations", type=int, default=100)
        parser.add_argument("--temperature_moves", type=int, default=10)
        parser.add_argument("--train_steps", type=int, default=50)
        parser.add_argument("--batch_size", type=int, default=64)
        parser.add_argument("--buffer_size", type=int, default=5000)
        parser.add_argument("--lr", type=float, default=1e-3)
        parser.add_argument("--checkpoint_dir", type=str, default="checkpoints")
        parser.add_argument("--cpu", action="store_true")
        train(parser.parse_args())
    elif choice == 'play':
        ### PLAY GAME
        print("\n--- Play Menu ---")
        print("1. Against another Player")
        print("2. Against an Agent")
        print("3. Back to Main Menu")

        sub_choice = input("Select an option (1-3): ").strip()
        agentCount = 0
        
        if sub_choice == '1':
            print("🎮 Local PvP started...")
            # start_pvp()
            agentCount = 0
        elif sub_choice == '2':
            print("🤖 Agent match started...")
            # start_agent_match()
            # playAgent()
            agentCount = 1
        else:
            print("❌ Invalid selection.")
            sys.exit(-1)
            
        game = Game(MODEL_PATH, agentCount=agentCount, window_size=1500)
        game.run()
            
    elif choice == 'exit':
        ### EXIT GAME
        print("Goodbye!")
        sys.exit()
    else:
        print("❌ Use 'train', 'play', or 'exit'.")

if __name__ == "__main__":
    temp_dir = Path("temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    main()
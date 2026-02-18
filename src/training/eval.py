import argparse

import numpy as np
import torch

from src.XO.cell import CellValues
# from src.training.env import UltimateTTTEnv
from src.gameEnvironment import GameEnvironment
from src.training.mcts import MCTS
from src.training.model import AlphaZeroNet


def play_game(model_a, model_b, mcts_simulations, device):
    env = GameEnvironment()
    env.reset()

    mcts_a = MCTS(model_a, n_simulations=mcts_simulations, device=device, dirichlet_epsilon=0.0)
    mcts_b = MCTS(model_b, n_simulations=mcts_simulations, device=device, dirichlet_epsilon=0.0)

    while not env.is_terminal():
        if env.getCurrentPlayer() == CellValues.X:
            policy = mcts_a.run(env, add_dirichlet=False)
        else:
            policy = mcts_b.run(env, add_dirichlet=False)

        action = int(np.argmax(policy))
        env.step(action)

    return env.getWinner()


def evaluate(args):
    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")

    model_a = AlphaZeroNet().to(device)
    model_b = AlphaZeroNet().to(device)

    model_a.load_state_dict(torch.load(args.model_a, map_location=device))
    model_b.load_state_dict(torch.load(args.model_b, map_location=device))

    model_a.eval()
    model_b.eval()

    wins_a = 0
    wins_b = 0
    draws = 0

    for _ in range(args.games):
        winner = play_game(model_a, model_b, args.mcts_simulations, device)
        if winner == CellValues.X:
            wins_a += 1
        elif winner == CellValues.O:
            wins_b += 1
        else:
            draws += 1

    print(f"A wins: {wins_a}, B wins: {wins_b}, Draws: {draws}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_a", type=str, required=True)
    parser.add_argument("--model_b", type=str, required=True)
    parser.add_argument("--games", type=int, default=20)
    parser.add_argument("--mcts_simulations", type=int, default=100)
    parser.add_argument("--cpu", action="store_true")
    evaluate(parser.parse_args())

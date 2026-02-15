import argparse
import copy
import os
import random
from collections import deque

import numpy as np
import torch
import torch.nn.functional as F

from cell import CellValues
from env import UltimateTTTEnv
from mcts import MCTS
from model import AlphaZeroNet


def self_play_game(model, mcts_simulations, device, temperature_moves=10):
    env = UltimateTTTEnv()
    env.reset()
    mcts = MCTS(model, n_simulations=mcts_simulations, device=device)

    history = []
    move_count = 0

    while not env.is_terminal():
        state = copy.deepcopy(env.board)
        current_player = env.current_player
        next_board_pos = copy.deepcopy(env.next_board_pos)

        policy = mcts.run(env, add_dirichlet=True)

        if move_count < temperature_moves:
            action = int(np.random.choice(len(policy), p=policy))
        else:
            action = int(np.argmax(policy))

        history.append((state, current_player, next_board_pos, policy))
        env.step(action)
        move_count += 1

    winner = env.winner
    examples = []
    for board, player, nb_pos, policy in history:
        if winner == CellValues.DRAW:
            z = 0.0
        elif winner == player:
            z = 1.0
        else:
            z = -1.0
        examples.append((board, player, nb_pos, policy, z))

    return examples


def encode_examples(examples, device):
    from encoding import encode_state

    states = []
    policies = []
    values = []
    for board, player, nb_pos, policy, z in examples:
        states.append(encode_state(board, player, nb_pos))
        policies.append(policy)
        values.append(z)

    states = torch.from_numpy(np.stack(states, axis=0)).to(device)
    policies = torch.from_numpy(np.stack(policies, axis=0)).to(device)
    values = torch.tensor(values, dtype=torch.float32).to(device)
    return states, policies, values


def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    model = AlphaZeroNet().to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-4)
    replay_buffer = deque(maxlen=args.buffer_size)

    os.makedirs(args.checkpoint_dir, exist_ok=True)

    for iteration in range(args.iterations):
        model.eval()
        for _ in range(args.self_play_games):
            examples = self_play_game(model, args.mcts_simulations, device, args.temperature_moves)
            replay_buffer.extend(examples)

        if len(replay_buffer) < args.batch_size:
            continue

        model.train()
        for _ in range(args.train_steps):
            batch = random.sample(replay_buffer, args.batch_size)
            states, target_policies, target_values = encode_examples(batch, device)

            logits, values = model(states)
            policy_loss = -torch.mean(torch.sum(target_policies * F.log_softmax(logits, dim=1), dim=1))
            value_loss = F.mse_loss(values, target_values)
            loss = policy_loss + value_loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        checkpoint_path = os.path.join(args.checkpoint_dir, f"model_{iteration}.pt")
        torch.save(model.state_dict(), checkpoint_path)
        print(f"Saved: {checkpoint_path}")


if __name__ == "__main__":
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

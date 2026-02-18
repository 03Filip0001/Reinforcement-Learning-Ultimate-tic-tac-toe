import argparse
import copy
import os
import random
from collections import deque

import numpy as np
import torch
import torch.nn.functional as F
from torch.cuda.amp import autocast, GradScaler

from src.XO.cell import CellValues
# from src.training.env import UltimateTTTEnv
from src.gameEnvironment import GameEnvironment
from src.training.mcts import MCTS
from src.training.model import AlphaZeroNet
from src.training.encoding import encode_state


def self_play_game(model, mcts_simulations, device, temperature_moves=10):
    env = GameEnvironment()
    env.reset()
    mcts = MCTS(model, n_simulations=mcts_simulations, device=device)

    history = []
    move_count = 0

    while not env.is_terminal():
        state = copy.deepcopy(env.board)
        current_player = env.getCurrentPlayer()
        next_board_pos = copy.deepcopy(env.getNextBoardPos())

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
    states = []
    policies = []
    values = []
    for board, player, nb_pos, policy, z in examples:
        states.append(encode_state(board, player, nb_pos))
        policies.append(policy)
        values.append(z)

    # Direktno pravi torch tensore na device-u, ne numpy
    states = torch.stack([torch.from_numpy(s) for s in states]).float().to(device)
    policies = torch.stack([torch.from_numpy(p) for p in policies]).float().to(device)
    values = torch.tensor(values, dtype=torch.float32, device=device)
    return states, policies, values


def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    print(f"Training on device: {device}")
    
    # GPU memory info
    if device.type == "cuda":
        torch.cuda.empty_cache()
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f}GB")
    
    model = AlphaZeroNet().to(device)
    
    # Optimizer sa lower_precision_grads za CUDA
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scaler = GradScaler()  # Za mixed precision training
    replay_buffer = deque(maxlen=args.buffer_size)

    os.makedirs(args.checkpoint_dir, exist_ok=True)

    for iteration in range(args.iterations):
        print(f"\n=== Iteration {iteration + 1}/{args.iterations} ===")
        
        model.eval()
        print(f"Self-play: Running {args.self_play_games} games...")
        for game_idx in range(args.self_play_games):
            examples = self_play_game(model, args.mcts_simulations, device, args.temperature_moves)
            replay_buffer.extend(examples)
            print(f"  Game {game_idx + 1}/{args.self_play_games}: Generated {len(examples)} examples")

        if len(replay_buffer) < args.batch_size:
            print(f"Buffer size ({len(replay_buffer)}) < batch size ({args.batch_size}). Skipping training.")
            continue

        print(f"Training: {args.train_steps} steps with buffer size {len(replay_buffer)}")
        model.train()
        total_loss = 0
        
        for step in range(args.train_steps):
            batch = random.sample(replay_buffer, args.batch_size)
            states, target_policies, target_values = encode_examples(batch, device)

            # Mixed precision training za brže treniranje na CUDA
            with autocast(device_type=device.type):
                logits, values = model(states)
                
                # Policy loss
                policy_loss = -torch.mean(torch.sum(target_policies * F.log_softmax(logits, dim=1), dim=1))
                
                # Value loss
                value_loss = F.mse_loss(values, target_values)
                
                loss = policy_loss + value_loss

            total_loss += loss.item()

            optimizer.zero_grad()
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            
            if (step + 1) % max(1, args.train_steps // 5) == 0:
                print(f"  Step {step + 1}/{args.train_steps}: Loss = {loss.item():.4f}")

        avg_loss = total_loss / args.train_steps
        print(f"Average loss: {avg_loss:.4f}")

        checkpoint_path = os.path.join(args.checkpoint_dir, f"model_{iteration}.pt")
        torch.save(model.state_dict(), checkpoint_path)
        print(f"✓ Saved: {checkpoint_path}")
        
        # Očisti GPU cache
        if device.type == "cuda":
            torch.cuda.empty_cache()


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
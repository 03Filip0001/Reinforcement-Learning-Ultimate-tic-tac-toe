import math
import numpy as np
import torch
import torch.nn.functional as F

from src.XO.cell import CellValues
from src.agent.encoding import encode_state, legal_action_mask


class MCTSNode:
    def __init__(self, prior):
        self.prior = prior
        self.visit_count = 0
        self.value_sum = 0.0
        self.children = {}

    @property
    def value(self):
        if self.visit_count == 0:
            return 0.0
        return self.value_sum / self.visit_count


class MCTS:
    def __init__(self, model, n_simulations=200, c_puct=1.5, dirichlet_alpha=0.3, dirichlet_epsilon=0.25, device="cpu"):
        self.model = model
        self.n_simulations = n_simulations
        self.c_puct = c_puct
        self.dirichlet_alpha = dirichlet_alpha
        self.dirichlet_epsilon = dirichlet_epsilon
        self.device = device

    def _policy_value(self, env):
        state = encode_state(env.board, env.current_player, env.next_board_pos)
        state_t = torch.from_numpy(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            policy_logits, value = self.model(state_t)
        policy_logits = policy_logits.squeeze(0)
        value = float(value.item())

        mask = legal_action_mask(env.board, env.next_board_pos)
        mask_t = torch.from_numpy(mask).to(self.device)
        policy_logits = torch.where(mask_t > 0, policy_logits, torch.tensor(-1e9, device=self.device))
        policy = F.softmax(policy_logits, dim=0).cpu().numpy()
        return policy, value

    def _select_child(self, node):
        best_score = -1e9
        best_action = None
        best_child = None
        total_visits = max(1, node.visit_count)

        for action, child in node.children.items():
            q_value = child.value
            u_value = self.c_puct * child.prior * math.sqrt(total_visits) / (1 + child.visit_count)
            score = q_value + u_value
            if score > best_score:
                best_score = score
                best_action = action
                best_child = child

        return best_action, best_child

    def _expand(self, node, policy, legal_mask):
        for action, p in enumerate(policy):
            if legal_mask[action] > 0:
                node.children[action] = MCTSNode(prior=float(p))

    def run(self, env, add_dirichlet=True):
        root = MCTSNode(prior=1.0)
        policy, _ = self._policy_value(env)
        legal_mask = legal_action_mask(env.board, env.next_board_pos)
        self._expand(root, policy, legal_mask)

        if add_dirichlet and root.children:
            legal_actions = list(root.children.keys())
            noise = np.random.dirichlet([self.dirichlet_alpha] * len(legal_actions))
            for a, n in zip(legal_actions, noise):
                root.children[a].prior = (1 - self.dirichlet_epsilon) * root.children[a].prior + self.dirichlet_epsilon * float(n)

        for _ in range(self.n_simulations):
            node = root
            search_env = env.clone()
            path = [node]

            while node.children:
                action, next_node = self._select_child(node)
                if next_node is None:
                    break
                search_env.step(action)
                node = next_node
                path.append(node)

            if search_env.is_terminal():
                winner = search_env.winner
                if winner == CellValues.DRAW:
                    value = 0.0
                elif winner == search_env.current_player:
                    value = 1.0
                else:
                    value = -1.0
            else:
                policy, value = self._policy_value(search_env)
                legal_mask = legal_action_mask(search_env.board, search_env.next_board_pos)
                self._expand(node, policy, legal_mask)

            for node in reversed(path):
                node.value_sum += value
                node.visit_count += 1
                value = -value

        visit_counts = np.zeros(81, dtype=np.float32)
        for action, child in root.children.items():
            visit_counts[action] = child.visit_count

        if visit_counts.sum() > 0:
            visit_counts /= visit_counts.sum()

        return visit_counts

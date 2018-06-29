"""
Title:  Learn how to sail with SARSA
Author: Sven Fritz (sfritz@stud.fra-uas.de)
        Martin Zakarian Khengi (khengi@stud.fra-uas.de)
"""
import numpy as np
import pandas as pd


class RL(object):
    def __init__(self, action_space, alpha=0.1, gamma=0.9, epsilon=0.3):
        self.actions = action_space  # list of actions
        self.alpha = alpha  # learn rate
        self.gamma = gamma  # discount
        self.epsilon = epsilon  # e-greedy policy

        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def choose_action(self, observation):
        self.check_state_exist(observation)
        # action selection
        if np.random.rand() > self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            state_action = state_action.reindex(
                np.random.permutation(state_action.index))  # some actions have same value
            action = state_action.idxmax()
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, *args):
        pass

    def get_list(self):
        return self.q_table

    def get_value(self, s, a):
        return self.q_table.loc[s, a]


class Sarsa(RL):

    def __init__(self, actions, alpha=0.1, gamma=1, epsilon=0.1):
        super(Sarsa, self).__init__(actions, alpha, gamma, epsilon)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'goal':
            q_target = r + self.gamma * self.q_table.loc[s_, a_]  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.alpha * (q_target - q_predict)  # update

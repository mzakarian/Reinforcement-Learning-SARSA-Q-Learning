"""
Sarsa is a online updating method for Reinforcement learning.

Unlike Q learning which is a offline updating method, Sarsa is updating while in the current trajectory.

You will see the sarsa is more coward when punishment is close because it cares about all behaviours,
while q learning is more brave because it only cares about maximum behaviour.
"""
from maze_env import Maze
from RL_brain import SarsaTable
import pandas as pd
import pickle
import numpy as np
import time


def get_row(dataframe, location):
    return dataframe.loc[location]


def scout(dataframe):
    row = get_row(dataframe, '[5.0, 269.0]')
    path = [row.name]
    softWinds, strongWinds = env.get_winds()
    unit = env.get_unit()
    width = env.get_width()
    height = env.get_height()

    while True:
        state_action = dataframe.loc[row.name, :]
        state_action = state_action.reindex(np.random.permutation(state_action.index))  # some actions have same value
        action = state_action.idxmax()

        s = row.name.replace("[", "").replace("]", "")
        s = [float(x) for x in s.split(", ")]
        base_action = np.array([0, 0])
        if s in strongWinds:
            if action == 0:  # up
                if s[1] > unit:
                    base_action[1] -= unit
            elif action == 1:  # down
                if s[1] < (height - 1) * unit:
                    base_action[1] += unit
            elif action == 2:  # right
                if s[0] < (width - 1) * unit:
                    base_action[0] += unit
            elif action == 3:  # left
                if s[0] > unit:
                    base_action[0] -= unit

            if s[1] + base_action[1] > unit * 2:
                base_action[1] -= unit * 2
            elif s[1] + base_action[1] > unit:
                base_action[1] -= unit

        elif s in softWinds:
            if action == 0:  # up
                if s[1] > unit:
                    base_action[1] -= unit
            elif action == 1:  # down
                if s[1] < (height - 1) * unit:
                    base_action[1] += unit
            elif action == 2:  # right
                if s[0] < (width - 1) * unit:
                    base_action[0] += unit
            elif action == 3:  # left
                if s[0] > unit:
                    base_action[0] -= unit

            if s[1] + base_action[1] > unit:
                base_action[1] -= unit

        else:
            if action == 0:  # up
                if s[1] > unit:
                    base_action[1] -= unit
            elif action == 1:  # down
                if s[1] < (height - 1) * unit:
                    base_action[1] += unit
            elif action == 2:  # right
                if s[0] < (width - 1) * unit:
                    base_action[0] += unit
            elif action == 3:  # left
                if s[0] > unit:
                    base_action[0] -= unit

        np.set_printoptions(formatter={'float': lambda x: "{0:0.1f}".format(x)})
        new = np.array([(base_action[0] + float(s[0])), (base_action[1] + float(s[1]))])
        new = np.array2string(new, separator=', ')

        print('From ' + row.name + ' to ' + new + ' moving ' + str(action) + " with " + str(base_action))

        if new == '[621.0, 269.0]':
            path.append(new)
            print('PATH COMPLETED')
            break

        row = get_row(dataframe, new)
        path.append(row.name)

    # print(path)
    return path


def update():
    for episode in range(100):
        # initial observation
        s1 = env.reset()

        # RL choose action based on observation
        a1 = RL.choose_action(str(s1))

        while True:
            # fresh env
            env.render()

            # RL take action and get next observation and reward
            s2, r, done = env.step(a1)

            # RL choose action based on next observation
            a2 = RL.choose_action(str(s2))

            # RL learn from this transition (s, a, r, s, a) ==> Sarsa
            RL.learn(str(s1), a1, r, str(s2), a2)

            # swap observation and action
            s1 = s2
            a1 = a2

            # break while loop when end of this episode
            if done:
                break

    # end of game
    result = RL.get_list()
    path = scout(result)
    print(path)
    env.draw(path)
    env.render()

    # with open('sarsa.pickle', 'wb') as handle:
    #     pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #
    # result.columns = ['Up', 'Down', 'Right', 'Left']
    #
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(result)
    # result.to_csv('sarsa.csv', sep='\t', encoding='utf-8')

    input("Press any key to close...")
    env.destroy()


if __name__ == "__main__":
    env = Maze()
    RL = SarsaTable(actions=list(range(env.n_actions)))

    env.after(100, update)
    env.mainloop()

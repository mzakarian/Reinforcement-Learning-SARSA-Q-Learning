"""
Title:  Learn how to sail with SARSA
Author: Sven Fritz (sfritz@stud.fra-uas.de)
        Martin Zakarian Khengi (khengi@stud.fra-uas.de)
"""
import matplotlib.pyplot as plt
from environment import Sea
from sarsa import Sarsa
import pandas as pd
import numpy as np
import pickle
import time


def get_row(df, location):
    return df.loc[location]


def plot(df):
    df.plot(style='.-', marker='o', markevery=10, markerfacecolor='black')
    plt.show()


def scout(df):
    # set start coordinates and environment conditions
    row = get_row(df, '[5.0, 269.0]')
    optimal_path = [row.name]
    softWinds, strongWinds = session.get_winds()
    unit = session.get_unit()
    width = session.get_width()
    height = session.get_height()

    # follow the optimal path by tracking the best action by highest QValue
    while True:
        # select best action
        state_action = df.loc[row.name, :]
        state_action = state_action.reindex(np.random.permutation(state_action.index))
        action = state_action.idxmax()

        # take action
        s = row.name.replace("[", "").replace("]", "")
        s = [float(x) for x in s.split(", ")]
        base_action = np.array([0, 0])
        if action == 0 or action == 4 or action == 5:  # u, ur, ul
            if s[1] > unit:
                base_action[1] -= unit
        if action == 1 or action == 6 or action == 7:  # d, dr, dl
            if s[1] < (height - 1) * unit:
                base_action[1] += unit
        if action == 2 or action == 4 or action == 6:  # r, ur, dr
            if s[0] < (width - 1) * unit:
                base_action[0] += unit
        if action == 3 or action == 5 or action == 7:  # l, ul, ul
            if s[0] > unit:
                base_action[0] -= unit
        if action == 'stay':
            pass

        if s in strongWinds:
            if s[1] + base_action[1] > unit * 2:
                base_action[1] -= unit * 2
            elif s[1] + base_action[1] > unit:
                base_action[1] -= unit

        elif s in softWinds:
            if s[1] + base_action[1] > unit:
                base_action[1] -= unit

        # formatting the coordinates
        np.set_printoptions(formatter={'float': lambda x: "{0:0.1f}".format(x)})
        new = np.array([(base_action[0] + float(s[0])), (base_action[1] + float(s[1]))])
        new = np.array2string(new, separator=', ')
        print('From ' + row.name + ' to ' + new + ' moving ' + str(action) + " with " + str(base_action))

        # break loop when goal is reached
        if new == '[621.0, 269.0]':
            optimal_path.append(new)
            print('PATH COMPLETED')
            break

        # add coordinates to optimal path
        row = get_row(df, new)
        optimal_path.append(row.name)

    return optimal_path


def update(interim=True):
    for episode in range(5000):
        # reset environment
        s1 = session.reset()

        if interim:
            session.draw_paths(agent.get_list())

        # choose action
        a1 = agent.choose_action(str(s1))

        while True:
            # refresh canvas
            session.render()

            # do action and get new state and its reward
            s2, r, done = session.step(a1)

            # choose next action based on policy
            a2 = agent.choose_action(str(s2))

            # start learning SARSA algorithm
            agent.learn(str(s1), a1, r, str(s2), a2)

            # set new state as root for next iteration
            s1 = s2
            a1 = a2

            # break loop when terminal state is reached
            if done:
                break

        if episode < 10:
            time.sleep(2)

    # get current QValue list, evaluate it and draw the optimal path
    result = agent.get_list()
    path = scout(result)
    print(path)
    session.draw_paths(result)
    session.render()
    input("Press Enter to show paths...")
    session.draw_optimal_path(path)
    session.render()
    input("Press Enter to show heatmap...")
    session.draw_heatmap()
    session.render()
    plot(session.get_telemetry())

    # EXPORT TO FILE
    with open('sarsa.pickle', 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(result)

    result.to_csv('sarsa.csv', sep=';', encoding='utf-8')
    session.get_telemetry().to_csv('telemetry.csv', sep=';', encoding='utf-8')


if __name__ == "__main__":
    session = Sea(action_set='advanced', is_stoachstic=False)
    agent = Sarsa(actions=list(range(session.n_actions)))

    session.after(100, update(interim=False))
    session.mainloop()

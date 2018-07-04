"""
Title:  Learn how to sail with SARSA
Author: Sven Fritz (sfritz@stud.fra-uas.de)
        Martin Zakarian Khengi (khengi@stud.fra-uas.de)
"""
import matplotlib.pyplot as plt
from environment import Sea
from reinforcement_learning import Sarsa
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
        # print('From ' + row.name + ' to ' + new + ' moving ' + str(action) + " with " + str(base_action))

        # break loop when goal is reached
        if new == '[621.0, 269.0]':
            optimal_path.append(new)
            print('Optimal Path closed!')
            break

        # add coordinates to optimal path
        row = get_row(df, new)
        optimal_path.append(row.name)

    return optimal_path


def update(episodes=100, show_steps=True, train=True, save=True):
    if train:
        rewards = pd.DataFrame(columns=['Rewards'])
        for episode in range(episodes):
            reward_counter = 0

            if show_steps and 1 <= episode < episodes * 0.1:
                # draw QValue updates
                session.draw_paths(agent.get_list())
                time.sleep(1)

            # reset environment
            s1 = session.reset()

            # choose action based on policy
            a1 = agent.choose_action(str(s1))

            while True:
                # refresh canvas
                session.render()

                # do action and get new state and its reward
                s2, r, done = session.step(a1)

                # choose action based on policy
                a2 = agent.choose_action(str(s2))

                # start learning SARSA algorithm
                agent.learn(str(s1), a1, r, str(s2), a2)
                reward_counter += agent.get_value(str(s1), a1)

                # set new state as root for next iteration
                s1 = s2
                a1 = a2

                # break loop when terminal state is reached
                if done:
                    break

            rewards.loc[episode] = [reward_counter]

        # get current data
        result = agent.get_list()
        heatmap = session.get_heatmap()
        telemetry = session.get_telemetry()
    else:
        # load saved data
        with open('data/sarsa.pickle', 'rb') as handle:
            result = pickle.load(handle)
        with open('data/heatmap.pickle', 'rb') as handle:
            heatmap = pickle.load(handle)
        with open('data/telemetry.pickle', 'rb') as handle:
            telemetry = pickle.load(handle)
        with open('data/rewards.pickle', 'rb') as handle:
            rewards = pickle.load(handle)

    # evaluate data and do some cool stuff
    # scout the optimal path
    print('Showing best action for each state')
    session.draw_paths(result)
    session.render()

    # show best actions for every state
    input("Press Enter to show optimal path...")
    session.reset()
    path = scout(result)
    session.draw_optimal_path(path)
    session.animate_path(path)
    session.render()

    # show heat map
    input("Press Enter to show heatmap...")
    session.draw_heatmap(df=heatmap)
    session.render()

    # plot rewards/episode and steps/episode
    plot(rewards)
    plot(telemetry)

    # export data to files
    if train and save:
        with open('data/sarsa.pickle', 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('data/heatmap.pickle', 'wb') as handle:
            pickle.dump(heatmap, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('data/telemetry.pickle', 'wb') as handle:
            pickle.dump(telemetry, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('data/rewards.pickle', 'wb') as handle:
            pickle.dump(rewards, handle, protocol=pickle.HIGHEST_PROTOCOL)

        result.to_csv('data/sarsa.csv', sep=';', encoding='utf-8')
        telemetry.to_csv('data/telemetry.csv', sep=';', encoding='utf-8')
        rewards.to_csv('data/rewards.csv', sep=';', encoding='utf-8')


if __name__ == "__main__":
    session = Sea(action_set='normal', is_stoachstic=False)
    agent = Sarsa(actions=list(range(session.n_actions)))

    session.after(100, update(episodes=100, show_steps=True, train=True, save=False))
    session.mainloop()

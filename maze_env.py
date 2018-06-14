"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
from builtins import print

import numpy as np
import time
import tkinter as tk

UNIT = 88  # pixels
MAZE_H = 7  # grid height
MAZE_W = 10  # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('SARSA: Segeln lernen')
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, height=MAZE_H * UNIT, width=MAZE_W * UNIT, bg="#5CB0C2")

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([20, 20])

        # create goal
        goal_center = origin + np.array([UNIT * 7, UNIT * 3])
        self.img1 = tk.PhotoImage(file=r"island.gif")
        self.goal = self.canvas.create_image((goal_center[0] - 15, goal_center[1] - 15), anchor=tk.NW, image=self.img1)

        # create boat
        boat_center = origin + np.array([0, UNIT * 3])
        self.img2 = tk.PhotoImage(file=r"boat.gif")
        self.boat = self.canvas.create_image((boat_center[0] - 15, boat_center[1] - 15), anchor=tk.NW, image=self.img2)

        # create wind
        self.softWinds = []
        self.strongWinds = []
        self.img = []
        counter = 0
        for i in range(7):
            for j in range(6):
                if i == 3 and (j + 4) == 8:
                    counter -= 1
                elif 7 <= (j + 4) <= 8:
                    wind_center = origin + np.array([UNIT * (j + 3), UNIT * i])
                    self.img.append(tk.PhotoImage(file=r"windStrong.gif"))
                    self.wind = self.canvas.create_image((wind_center[0] - 15, wind_center[1] - 15), anchor=tk.NW,
                                                         image=self.img[counter])
                    self.strongWinds.append(self.canvas.coords(self.wind))
                else:
                    wind_center = origin + np.array([UNIT * (j + 3), UNIT * i])
                    self.img.append(tk.PhotoImage(file=r"windWeak.gif"))
                    self.wind = self.canvas.create_image((wind_center[0] - 15, wind_center[1] - 15), anchor=tk.NW,
                                                         image=self.img[counter])
                    self.softWinds.append(self.canvas.coords(self.wind))
                counter += 1

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.boat)
        origin = np.array([20, 20])
        boat_center = origin + np.array([0, UNIT * 3])
        self.img2 = tk.PhotoImage(file=r"boat.gif")
        self.boat = self.canvas.create_image((boat_center[0] - 15, boat_center[1] - 15), anchor=tk.NW, image=self.img2)

        # return observation
        return self.canvas.coords(self.boat)

    def step(self, action):
        s = self.canvas.coords(self.boat)
        base_action = np.array([0, 0])
        if action == 0:  # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:  # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:  # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:  # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.boat, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.boat)  # next state

        # reward function
        if s_ == self.canvas.coords(self.goal):
            reward = 1
            done = True
            print('FOUND!')
            s_ = 'terminal'
            time.sleep(1.5)
        elif s_ in self.strongWinds:
            print('STRONG')
            reward = -1
            done = False
        elif s_ in self.softWinds:
            print("SOFT")
            reward = -1
            done = False
        else:
            reward = -1
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()

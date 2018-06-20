
"""
Title:  Learn how to sail with SARSA
Author: Sven Fritz (sfritz@stud.fra-uas.de)
        Martin Zakarian Khengi (khengi@stud.fra-uas.de)
"""
import tkinter as tk
import numpy as np
import time

UNIT = 88  # sprite size
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
        self.steps_taken = 0
        self.generation = 0

    def get_unit(self):
        return UNIT

    def get_width(self):
        return MAZE_W

    def get_height(self):
        return MAZE_H

    def get_winds(self):
        return self.softWinds, self.strongWinds

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

        # create wind
        self.softWinds = []
        self.strongWinds = []
        self.img = []
        counter = 0
        for i in range(7):
            for j in range(6):
                if 7 <= (j + 4) <= 8:
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

        # create goal
        goal_center = origin + np.array([UNIT * 7, UNIT * 3])
        self.img1 = tk.PhotoImage(file=r"goal.gif")
        self.goal = self.canvas.create_image((goal_center[0] - 15, goal_center[1] - 15), anchor=tk.NW,
                                             image=self.img1)

        # create agent
        boat_center = origin + np.array([0, UNIT * 3])
        self.img2 = tk.PhotoImage(file=r"boat.gif")
        self.boat = self.canvas.create_image((boat_center[0] - 15, boat_center[1] - 15), anchor=tk.NW,
                                             image=self.img2)

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        self.steps_taken = 0
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
        if s in self.strongWinds:
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

            if s[1] + base_action[1] > UNIT * 2:
                base_action[1] -= UNIT * 2
            elif s[1] + base_action[1] > UNIT:
                base_action[1] -= UNIT

        elif s in self.softWinds:
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

            if s[1] + base_action[1] > UNIT:
                base_action[1] -= UNIT

        else:
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
        self.steps_taken += 1

        # reward function
        if s_ == self.canvas.coords(self.goal):
            reward = 1000
            done = True
            self.generation += 1
            print('END! Episode: ' + str(self.generation) + ' Steps taken --> ' + str(self.steps_taken))
            s_ = 'terminal'
            # time.sleep(5)
        else:
            reward = -1
            done = False

        return s_, reward, done

    def render(self):
        # time.sleep(0.66)
        self.update()

    def draw(self, path):
        time.sleep(3)
        self.canvas.delete(self.boat)

        for point in path:
            s = point.replace("[", "").replace("]", "")
            s = [float(x) for x in s.split(", ")]
            self.canvas.create_rectangle(s[0] - 5, s[1] - 5, s[0] + 88 - 5, s[1] + 88 - 5, fill='green')

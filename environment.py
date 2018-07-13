"""
Title:  Learn how to sail with SARSA
Author: Sven Fritz (sfritz@stud.fra-uas.de)
        Martin Zakarian Khengi (khengi@stud.fra-uas.de)
"""
import tkinter as tk
import pandas as pd
import numpy as np
import time

UNIT = 88  # sprite size
SEA_H = 7  # grid height
SEA_W = 10  # grid width


class Sea(tk.Tk, object):
    def __init__(self, action_set='normal', is_stoachstic=False):
        super(Sea, self).__init__()
        if action_set == 'normal':
            self.action_space = ['u', 'd', 'l', 'r']
        elif action_set == 'advanced':
            self.action_space = ['u', 'd', 'l', 'r', 'ur', 'ul', 'dr', 'dl']
        elif action_set == 'advanced_plus':
            self.action_space = ['u', 'd', 'l', 'r', 'ur', 'ul', 'dr', 'dl', 'stay']
        self.n_actions = len(self.action_space)
        self.title('Learn how to sail with SARSA')
        self.geometry('{0}x{1}'.format(SEA_W * UNIT, SEA_H * UNIT))
        self._build_sea()
        self.steps_taken = 0
        self.generation = 0
        self.lines = []
        self.telemetrics = pd.DataFrame(columns=['Steps'])
        self.stochastic = is_stoachstic
        self.heat_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def get_unit(self):
        return UNIT

    def get_width(self):
        return SEA_W

    def get_height(self):
        return SEA_H

    def get_winds(self):
        return self.softWinds, self.strongWinds

    def get_telemetry(self):
        return self.telemetrics

    def get_heatmap(self):
        return self.heat_map

    def _build_sea(self):
        self.canvas = tk.Canvas(self, height=SEA_H * UNIT, width=SEA_W * UNIT, bg="#5CB0C2")

        # create grids
        for c in range(0, SEA_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, SEA_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, SEA_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, SEA_W * UNIT, r
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

        self.heat_map[int((s[1] - 5) / 88)][int((s[0] - 5) / 88)] += 1

        # Basic Movement
        if action == 0 or action == 4 or action == 5:  # u, ur, ul
            if s[1] > UNIT:
                base_action[1] -= UNIT
        if action == 1 or action == 6 or action == 7:  # d, dr, dl
            if s[1] < (SEA_H - 1) * UNIT:
                base_action[1] += UNIT
        if action == 2 or action == 4 or action == 6:  # r, ur, dr
            if s[0] < (SEA_W - 1) * UNIT:
                base_action[0] += UNIT
        if action == 3 or action == 5 or action == 7:  # l, ul, ul
            if s[0] > UNIT:
                base_action[0] -= UNIT
        if action == 'stay':
            pass

        # Movement due Winds
        if s in self.strongWinds:
            if self.stochastic:
                temp = np.random.choice(np.arange(1, 4), p=[(1 / 3), (1 / 3), (1 / 3)])
                if temp == 1:
                    if s[1] + base_action[1] > UNIT * 3:
                        base_action[1] -= UNIT * 3
                    elif s[1] + base_action[1] > UNIT * 2:
                        base_action[1] -= UNIT * 2
                    elif s[1] + base_action[1] > UNIT:
                        base_action[1] -= UNIT
                elif temp == 2:
                    if s[1] + base_action[1] > UNIT * 2:
                        base_action[1] -= UNIT * 2
                    elif s[1] + base_action[1] > UNIT:
                        base_action[1] -= UNIT
                elif temp == 3:
                    if s[1] + base_action[1] > UNIT:
                        base_action[1] -= UNIT
            else:
                if s[1] + base_action[1] > UNIT * 2:
                    base_action[1] -= UNIT * 2
                elif s[1] + base_action[1] > UNIT:
                    base_action[1] -= UNIT

        elif s in self.softWinds:
            if self.stochastic:
                temp = np.random.choice(np.arange(1, 4), p=[(1 / 3), (1 / 3), (1 / 3)])
                if temp == 1:
                    if s[1] + base_action[1] > UNIT:
                        base_action[1] -= UNIT
                elif temp == 2:
                    if s[1] + base_action[1] > UNIT * 2:
                        base_action[1] -= UNIT * 2
                    elif s[1] + base_action[1] > UNIT:
                        base_action[1] -= UNIT
                elif temp == 3:
                    pass
            else:
                if s[1] + base_action[1] > UNIT:
                    base_action[1] -= UNIT
        else:
            if self.stochastic:
                temp = np.random.choice(np.arange(1, 3), p=[(1 / 3), (2 / 3)])
                if temp == 1:
                    if s[1] + base_action[1] > UNIT:
                        base_action[1] -= UNIT
                elif temp == 2:
                    pass

        # actual moving
        self.canvas.move(self.boat, base_action[0], base_action[1])
        s_ = self.canvas.coords(self.boat)
        self.steps_taken += 1

        # rewards
        if s_ == self.canvas.coords(self.goal):
            reward = 100
            done = True
            self.telemetrics.loc[self.generation] = [self.steps_taken]
            self.generation += 1
            print('Episode: ' + str(self.generation) + ' Steps taken --> ' + str(self.steps_taken))
            self.heat_map[int((s_[1] - 5) / 88)][int((s_[0] - 5) / 88)] += 1
            s_ = 'goal'
            # time.sleep(5)
        else:
            reward = -1
            done = False

        return s_, reward, done

    def render(self):
        # time.sleep(0.66)
        self.update()

    def draw_optimal_path(self, path):
        time.sleep(3)
        self.canvas.delete(self.boat)

        for line in self.lines:
            self.canvas.delete(line)

        for point in path:
            s = point.replace("[", "").replace("]", "")
            s = [float(x) for x in s.split(", ")]
            self.canvas.create_rectangle(s[0] - 5, s[1] - 5, s[0] + 88 - 5, s[1] + 88 - 5, fill='green')

    def animate_path(self, path):
        for point in path:
            self.canvas.delete(self.boat)
            s = point.replace("[", "").replace("]", "")
            s = [float(x) for x in s.split(", ")]
            self.img2 = tk.PhotoImage(file=r"boat.gif")
            self.boat = self.canvas.create_image(s[0], s[1], anchor=tk.NW, image=self.img2)
            self.render()
            time.sleep(0.33)

    def pseudocolor(self, value, minval, maxval, palette):
        """ Maps given value to a linearly interpolated palette color. """
        max_index = len(palette) - 1
        # Convert value in range minval...maxval to the range 0..max_index.
        v = (float(value - minval) / (maxval - minval)) * max_index
        i = int(v)
        f = v - i  # Split into integer and fractional portions.
        c0r, c0g, c0b = palette[i]
        c1r, c1g, c1b = palette[min(i + 1, max_index)]
        dr, dg, db = c1r - c0r, c1g - c0g, c1b - c0b
        return c0r + (f * dr), c0g + (f * dg), c0b + (f * db)  # Linear interpolation.

    def colorize(self, value, minval, maxval, palette):
        """ Convert value to heatmap color and convert it to tkinter color. """
        color = (int(c * 255) for c in self.pseudocolor(value, minval, maxval, palette))
        return '#{:02x}{:02x}{:02x}'.format(*color)  # Convert to hex string.

    def draw_heatmap(self, df):
        # print(df)

        heat_min = min(min(row) for row in df)
        heat_max = max(max(row) for row in df)

        # Heatmap rgb colors in mapping order (ascending).
        palette = (0, 0, 1), (0, .5, 0), (0, 1, 0), (1, .5, 0), (1, 0, 0)

        for y, row in enumerate(df):
            for x, temp in enumerate(row):
                x0, y0 = x * UNIT, y * UNIT
                x1, y1 = x0 + UNIT, y0 + UNIT
                color = self.colorize(temp, heat_min, heat_max, palette)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)

        origin = np.array([20, 20])
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

    def draw_paths(self, df):
        self.reset()
        center = UNIT / 2

        for line in self.lines:
            self.canvas.delete(line)

        for index, row in df.iterrows():
            state_action = df.loc[row.name, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()

            if not row.name == 'goal':
                s = row.name.replace("[", "").replace("]", "")
                s = [float(x) for x in s.split(", ")]
            else:
                continue

            if action == 0:  # up
                self.lines.append(
                    self.canvas.create_line(center + s[0], center + s[1], center + s[0], 0 + s[1], tags=("line",),
                                            arrow="last", width=5))
            elif action == 1:  # down
                self.lines.append(
                    self.canvas.create_line(center + s[0], center + s[1], center + s[0], UNIT + s[1], tags=("line",),
                                            arrow="last", width=5))
            elif action == 2:  # right
                self.lines.append(
                    self.canvas.create_line(center + s[0], center + s[1], UNIT + s[0], center + s[1], tags=("line",),
                                            arrow="last", width=5))
            elif action == 3:  # left
                self.lines.append(
                    self.canvas.create_line(center + s[0], center + s[1], 0 + s[0], center + s[1], tags=("line",),
                                            arrow="last", width=5))
            elif action == 4:  # up right
                self.lines.append(
                    self.canvas.create_line(center + s[0], center + s[1], UNIT + s[0], 0 + s[1], tags=("line",),
                                            arrow="last", width=5))
            elif action == 5:  # up left
                self.lines.append(
                    self.canvas.create_line(center + s[0], center + s[1], 0 + s[0], 0 + s[1], tags=("line",),
                                            arrow="last", width=5))
            elif action == 6:  # down right
                self.lines.append(
                    self.canvas.create_line(center + s[0], center + s[1], UNIT + s[0], UNIT + s[1], tags=("line",),
                                            arrow="last", width=5))
            elif action == 7:  # down left
                self.lines.append(
                    self.canvas.create_line(center + s[0], center + s[1], 0 + s[0], UNIT + s[1], tags=("line",),
                                            arrow="last", width=5))
            elif action == 8:  # nothing
                self.lines.append(self.canvas.create_oval(center - 10 + s[0], center - 10 + s[1], center + 10 + s[0],
                                                          center + 10 + s[1], fill="black"))

# import pandas as pd
# import numpy as np
# import pickle
# import tkinter as tk
#
# UNIT = 88  # pixels
# MAZE_H = 7  # grid height
# MAZE_W = 10  # grid width
#
#
# def get_row(dataframe, location):
#     return dataframe.loc[location]
#
#
# with open('sarsa.pickle', 'rb') as handle:
#     df = pickle.load(handle)
#
# with open('softWinds.pickle', 'rb') as handle:
#     softWinds = pickle.load(handle)
#
# with open('strongWinds.pickle', 'rb') as handle:
#     strongWinds = pickle.load(handle)
#
# # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# #     print(df)
#
# row = get_row(df, '[5.0, 269.0]')
# path = [row.name]
# while True:
#     best = row[0]
#     action = 0
#     if best < row[1]:
#         best = row[1]
#         action = 1
#     if best < row[2]:
#         best = row[2]
#         action = 2
#     if best < row[3]:
#         action = 3
#         best = row[3]
#
#     s = row.name.replace("[", "").replace("]", "")
#     s = [float(x) for x in s.split(", ")]
#     base_action = np.array([0, 0])
#     if s in strongWinds:
#         if action == 0:  # up
#             if s[1] > UNIT:
#                 base_action[1] -= UNIT
#         elif action == 1:  # down
#             if s[1] < (MAZE_H - 1) * UNIT:
#                 base_action[1] += UNIT
#         elif action == 2:  # right
#             if s[0] < (MAZE_W - 1) * UNIT:
#                 base_action[0] += UNIT
#         elif action == 3:  # left
#             if s[0] > UNIT:
#                 base_action[0] -= UNIT
#
#         if s[1] + base_action[1] > UNIT * 2:
#             base_action[1] -= UNIT * 2
#         elif s[1] + base_action[1] > UNIT:
#             base_action[1] -= UNIT
#
#     elif s in softWinds:
#         if action == 0:  # up
#             if s[1] > UNIT:
#                 base_action[1] -= UNIT
#         elif action == 1:  # down
#             if s[1] < (MAZE_H - 1) * UNIT:
#                 base_action[1] += UNIT
#         elif action == 2:  # right
#             if s[0] < (MAZE_W - 1) * UNIT:
#                 base_action[0] += UNIT
#         elif action == 3:  # left
#             if s[0] > UNIT:
#                 base_action[0] -= UNIT
#
#         if s[1] + base_action[1] > UNIT:
#             base_action[1] -= UNIT
#
#     else:
#         if action == 0:  # up
#             if s[1] > UNIT:
#                 base_action[1] -= UNIT
#         elif action == 1:  # down
#             if s[1] < (MAZE_H - 1) * UNIT:
#                 base_action[1] += UNIT
#         elif action == 2:  # right
#             if s[0] < (MAZE_W - 1) * UNIT:
#                 base_action[0] += UNIT
#         elif action == 3:  # left
#             if s[0] > UNIT:
#                 base_action[0] -= UNIT
#
#     np.set_printoptions(formatter={'float': lambda x: "{0:0.1f}".format(x)})
#     new = np.array([(base_action[0] + float(s[0])), (base_action[1] + float(s[1]))])
#     new = np.array2string(new, separator=', ')
#
#     if new == '[621.0, 269.0]':
#         path.append(new)
#         break
#
#     print('From ' + row.name + ' to ' + new + ' moving ' + str(action) + " with " + str(base_action))
#
#     row = get_row(df, new)
#     path.append(row.name)
#
# print(path)
#
# canvas = tk.Canvas(height=MAZE_H * UNIT, width=MAZE_W * UNIT)
#
# for c in range(0, MAZE_W * UNIT, UNIT):
#     x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
#     canvas.create_line(x0, y0, x1, y1)
# for r in range(0, MAZE_H * UNIT, UNIT):
#     x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
#     canvas.create_line(x0, y0, x1, y1)
#
# for point in path:
#     s = point.replace("[", "").replace("]", "")
#     s = [float(x) for x in s.split(", ")]
#
#     rect = canvas.create_rectangle(s[0] - 5, s[1] - 5, s[0] + 88 - 5, s[1] + 88 - 5, fill='red')
#
# canvas.pack()
#
# tk.mainloop()
#
#
# import pandas as pd
# import matplotlib.pyplot as plt
#
# df1 = pd.read_csv("telemetry.csv", sep='\t')
# df1.plot(style='.-', marker='o', markevery=10, markerfacecolor='black')
#
# plt.show()
#
# import random
#
# print(random.randint(1, 3))
#
# import numpy
# test = numpy.random.choice(numpy.arange(1, 4), p=[(1/3), (1/3), (1/3)])
# print(test)

from tkinter import *  # Python 3

heat_map = [[0, 1, 2, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

heat_min = min(min(row) for row in heat_map)
heat_max = max(max(row) for row in heat_map)

# Heatmap rgb colors in mapping order (ascending).
palette = (0, 0, 1), (0, .5, 0), (0, 1, 0), (1, .5, 0), (1, 0, 0)


def pseudocolor(value, minval, maxval, palette):
    """ Maps given value to a linearly interpolated palette color. """
    max_index = len(palette) - 1
    # Convert value in range minval...maxval to the range 0..max_index.
    v = (float(value - minval) / (maxval - minval)) * max_index
    i = int(v);
    f = v - i  # Split into integer and fractional portions.
    c0r, c0g, c0b = palette[i]
    c1r, c1g, c1b = palette[min(i + 1, max_index)]
    dr, dg, db = c1r - c0r, c1g - c0g, c1b - c0b
    return c0r + (f * dr), c0g + (f * dg), c0b + (f * db)  # Linear interpolation.


def colorize(value, minval, maxval, palette):
    """ Convert value to heatmap color and convert it to tkinter color. """
    color = (int(c * 255) for c in pseudocolor(value, minval, maxval, palette))
    return '#{:02x}{:02x}{:02x}'.format(*color)  # Convert to hex string.


root = Tk()
root.title('Heatmap')

# Create and fill canvas with rectangular cells.
width, height = 400, 400  # Canvas size.
rows, cols = len(heat_map), len(heat_map[0])
rect_width, rect_height = width // rows, height // cols
border = 1  # Pixel width of border around each.

print(heat_map[0][2])

canvas = Canvas(root, width=width, height=height)
canvas.pack()
for y, row in enumerate(heat_map):
    for x, temp in enumerate(row):
        x0, y0 = x * rect_width, y * rect_height
        x1, y1 = x0 + rect_width - border, y0 + rect_height - border
        color = colorize(temp, heat_min, heat_max, palette)
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)

root.mainloop()

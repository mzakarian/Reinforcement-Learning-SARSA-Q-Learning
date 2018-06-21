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

import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv("telemetry.csv", sep='\t')
df1.plot(style='.-', marker='o', markevery=10, markerfacecolor='black')

plt.show()

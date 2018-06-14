import tkinter as tk
import numpy as np

UNIT = 40  # pixels
MAZE_H = 7  # grid height
MAZE_W = 10  # grid width

# canvas_width = 300
# canvas_height =300
# 
# master = tk.Tk()
#
# canvas = tk.Canvas(master,
#            width=canvas_width,
#            height=canvas_height)
# canvas.pack()
#
# img = tk.PhotoImage(file="viking.gif")
# canvas.create_image(20,20, anchor=tk.NW, image=img)



canvas = tk.Canvas(height=MAZE_H * UNIT, width=MAZE_W * UNIT)

# create grids
for c in range(0, MAZE_W * UNIT, UNIT):
    x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
    canvas.create_line(x0, y0, x1, y1)
for r in range(0, MAZE_H * UNIT, UNIT):
    x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
    canvas.create_line(x0, y0, x1, y1)

# create origin
origin = np.array([20, 20])

# create oval
oval_center = origin + np.array([UNIT * 7, UNIT * 3])
oval = canvas.create_oval(
    oval_center[0] - 15, oval_center[1] - 15,
    oval_center[0] + 15, oval_center[1] + 15,
    fill='green')

# create boat
rectangle_center = origin + np.array([0, UNIT * 3])
rect = canvas.create_rectangle(
    rectangle_center[0] - 15, rectangle_center[1] - 15,
    rectangle_center[0] + 15, rectangle_center[1] + 15,
    fill='red')

img = tk.PhotoImage(file=r"viking.gif")
canvas.create_image((20, 20), anchor=tk.NW, image=img)

# pack all
canvas.pack()

tk.mainloop()
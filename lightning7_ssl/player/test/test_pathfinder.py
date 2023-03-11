from typing import List
import unittest
import math
from lightning7_ssl.player.pathfinder import find_path
from unittest.mock import MagicMock, patch
import tkinter as tk

from lightning7_ssl.vecMath.vec_math import Vec2

root = tk.Tk()
root.title("Path-Finding Visualization")
canvas = tk.Canvas(root, width=900, height=600, bg="white")
BALL_RADIUS = 5
ROBOT_RADIUS = 9
canvas.pack()
team = [(200, 200), (100, 100), (100, 200), (100, 300), (100, 400), (100, 500)]
opp = [(800, 50), (800, 150), (800, 250), (800, 350), (800, 450), (800, 550)]
BASE_FACTOR = 4
SPEED_FACTOR = 1


class MovableCircle:
    def __init__(self, canvas, x, y, radius, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.r = radius * BASE_FACTOR
        self.circle = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, fill=color
        )
        # make another circle to show the influence radius
        self.influence_circle = self.canvas.create_oval(
            x - radius * BASE_FACTOR,
            y - radius * BASE_FACTOR,
            x + radius * BASE_FACTOR,
            y + radius * BASE_FACTOR,
            outline="black",
        )
        self.canvas.tag_bind(self.circle, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.circle, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.circle, "<ButtonRelease-1>", self.on_release)
        # bind the influence circle to the drag event
        self.canvas.tag_bind(self.influence_circle, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.influence_circle, "<B1-Motion>", self.shrink)
        self.canvas.tag_bind(
            self.influence_circle, "<ButtonRelease-1>", self.on_release
        )
        self.is_dragging = False

    def on_click(self, event):
        for item in canvas.find_all():
            if canvas.type(item) == "line":
                canvas.delete(item)
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    # user can drag the boundary of the influence circle to change its radius
    def shrink(self, event):
        if self.is_dragging:
            self.r = math.sqrt((event.x - self.x) ** 2 + (event.y - self.y) ** 2)
            if self.r > BASE_FACTOR * ROBOT_RADIUS:
                self.canvas.coords(
                    self.influence_circle,
                    self.x - self.r,
                    self.y - self.r,
                    self.x + self.r,
                    self.y + self.r,
                )

    def on_drag(self, event):
        if self.is_dragging:
            delta_x = event.x - self.drag_start_x
            delta_y = event.y - self.drag_start_y
            self.canvas.move(self.circle, delta_x, delta_y)
            # move the influence circle
            self.canvas.move(self.influence_circle, delta_x, delta_y)
            self.x += delta_x
            self.y += delta_y
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def on_release(self, event):
        self.is_dragging = False


team = [(200, 200), (100, 100), (100, 200), (100, 300), (100, 400), (100, 500)]
opp = [(800, 50), (800, 150), (800, 250), (800, 350), (800, 450), (800, 550)]
goal = Vec2(450, 300)
items = []
items.append(MovableCircle(canvas, goal[0], goal[1], BALL_RADIUS, "red"))
# delete the influence circle of the goal
canvas.delete(items[0].influence_circle)
for i in range(6):
    items.append(MovableCircle(canvas, team[i][0], team[i][1], ROBOT_RADIUS, "blue"))
    items.append(MovableCircle(canvas, opp[i][0], opp[i][1], ROBOT_RADIUS, "green"))
canvas.delete(items[1].influence_circle)


def update():
    # delete previous path
    for item in canvas.find_all():
        if canvas.type(item) == "line":
            canvas.delete(item)
    team_position: List[Vec2] = []
    opp_position: List[Vec2] = []
    team_vel: List[Vec2] = []
    opp_vel: List[Vec2] = []
    for i in range(1, 13, 2):
        team_position.append(Vec2(items[i].x, items[i].y))
        # calculate unit vector between item[i] and item[0]
        dv = (items[0].x - items[i].x, items[0].y - items[i].y)
        dv = (
            dv[0] / math.sqrt(dv[0] ** 2 + dv[1] ** 2),
            dv[1] / math.sqrt(dv[0] ** 2 + dv[1] ** 2),
        )
        speed = (items[i].r - BASE_FACTOR * ROBOT_RADIUS) / SPEED_FACTOR
        team_vel.append(Vec2(dv[0] * speed, dv[1] * speed))
        opp_position.append(Vec2(items[i + 1].x, items[i + 1].y))
        # calculate unit vector between item[i+1] and item[0]
        dv = (items[0].x - items[i + 1].x, items[0].y - items[i + 1].y)
        dv = (
            dv[0] / math.sqrt(dv[0] ** 2 + dv[1] ** 2),
            dv[1] / math.sqrt(dv[0] ** 2 + dv[1] ** 2),
        )
        speed = (items[i + 1].r - BASE_FACTOR * ROBOT_RADIUS) / SPEED_FACTOR
        opp_vel.append(Vec2(dv[0] * speed, dv[1] * speed))
    goal = Vec2(items[0].x, items[0].y)
    path = test_pathfinder(team_position, opp_position, team_vel, opp_vel, goal)
    canvas.create_line(
        team_position[0][0],
        team_position[0][1],
        team_position[0][0] + path[0] * 40,
        team_position[0][1] + path[1] * 40,
        fill="black",
    )


def test_pathfinder(
    team_position: List[Vec2],
    opp_position: List[Vec2],
    team_vel: List[Vec2],
    opp_speed: List[Vec2],
    goal: Vec2,
):
    # start_pos -> team_position[0], end_pos -> goal
    mock_world = MagicMock()
    mock_world.get_team_position.return_value = [pos * 10 for pos in team_position]
    mock_world.get_opp_position.return_value = [pos * 10 for pos in opp_position]
    mock_world.get_team_vel.return_value = [pos * 10 for pos in team_vel]
    mock_world.get_opp_vel.return_value = [pos * 10 for pos in opp_speed]
    return find_path(mock_world, 0, goal * 10)


button = tk.Button(root, text="Update", command=update)
button.pack()
# root.mainloop()

import matplotlib.pyplot as plt
import numpy as np
import random
# from ..vecMath.vec_math import Vec2

"""
    Calculates the potential field of the obstacles and goal, and draw the path towards goal. Make all parameters tunable.

    Input: Ball and player positions
           Player of interest
    
    Output: Vector or equation of path 
"""

"""
    Pseudocode:

    Initialize goal
        - Position
        - Field strength
    
    Initialize obstacles
        - Positions
        - Field strength
        - Raiud of influence
    
    Draw path to goal
        - Select robot of interest
        - Ignore its own potential field
        - Calculate gradient from it to the goal
    
    Display goal, obstacles, and path
"""

# Set globals

ROBOT_R = 0.2
BALL_R = 0.2
NUM_PLAYERS = 11
POT_RES = 0.3 # Potential field 'resolution'
FIELD_LEN = 9
FIELD_WIDTH = 9
s = 2
x = np.arange(0, FIELD_LEN, POT_RES)
y = np.arange(0, FIELD_LEN, POT_RES)
X, Y = np.meshgrid(x, y)
goal = [random.uniform(0, FIELD_LEN), random.uniform(0, FIELD_LEN)]

def add_goal(X, Y, s, loc):
    delx = np.zeros_like(X)
    dely = np.zeros_like(Y)
    s = 2
    for i in range(len(x)):
        for j in range(len(y)):
            d = np.sqrt((loc[0]-X[i][j])**2 + (loc[1]-Y[i][j])**2)
            theta = np.arctan2(loc[1]-Y[i][j], loc[0] - X[i][j])

            if d < BALL_R:
                delx[i][j] = 0
                dely[i][j] = 0
            elif d > BALL_R + s:
                delx[i][j] = 9 * s *np.cos(theta)
                dely[i][j] = 9 * s *np.sin(theta)
            else:
                delx[i][j] = 9 * (d - BALL_R) * np.cos(theta)
                dely[i][j] = 9 * (d - BALL_R) * np.sin(theta)
    return delx, dely

def add_obstacles(X, Y, s, delx, dely, goal):
    obstacle = [random.uniform(0, FIELD_LEN), random.uniform(0, FIELD_LEN)]
    s = 2
    a = 1
    for i in range(len(x)):
        for j in range(len(y)):
            d_goal = np.sqrt((goal[0]-X[i][j])**2 + (goal[1]-Y[i][j])**2)
            d_obstacle = np.sqrt((obstacle[0]-X[i][j])**2 + (obstacle[1]-Y[i][j])**2)

            theta_goal = np.arctan2(goal[1]-Y[i][j], goal[0] - X[i][j])
            theta_obstacle = np.arctan2(obstacle[1]-Y[i][j], obstacle[0] - X[i][j])

            if d_obstacle < ROBOT_R:
                delx[i][j] = -np.sign(np.cos(theta_obstacle))
                dely[i][j] = -np.sign(np.sin(theta_obstacle))
            elif d_obstacle > ROBOT_R + s:
                delx[i][j] += -a*s *np.cos(theta_goal)
                dely[i][j] += -a*s *np.sin(theta_goal)
                # print(delx[i][j], dely[i][j])
            elif d_obstacle < ROBOT_R + s:
                delx[i][j] += -27 * (s + ROBOT_R - d_obstacle) * np.cos(theta_obstacle)
                dely[i][j] += -27 * (s + ROBOT_R - d_obstacle) * np.sin(theta_obstacle)

            if d_goal <= ROBOT_R + s:
                # print(delx[i][j], dely[i][j])
                if delx[i][j] != 0:
                    delx[i][j] += (9 * (d_goal - ROBOT_R) * np.cos(theta_goal))
                    dely[i][j] += (9 * (d_goal - ROBOT_R) * np.sin(theta_goal))
                else:
                    delx[i][j] = 9 * (d_goal - ROBOT_R) * np.cos(theta_goal)
                    dely[i][j] = 9 * (d_goal - ROBOT_R) * np.sin(theta_goal)
            
            if d_goal > ROBOT_R + s:
                if delx[i][j] != 0:
                    delx[i][j] += 9 * s * np.cos(theta_goal)
                    dely[i][j] += 9 * s * np.sin(theta_goal)
                else:
                    delx[i][j] = 9 * s * np.cos(theta_goal)
                    dely[i][j] = 9 * s * np.sin(theta_goal)
            
            if d_goal < BALL_R:
                delx[i][j] = 0
                dely[i][j] = 0

    return delx, dely, obstacle
    
def plot_graph(X, Y, delx, dely, fig, ax, loc, r, color):
    # ax.quiver(X, Y, delx, dely)
    ax.add_patch(plt.Circle(loc, r, color=color))
    ax.set_title('Potential Field')
    
    return ax

fig, ax = plt.subplots(figsize = (9, 9))
delx, dely = add_goal(X, Y, s, goal)
plot_graph(X, Y, delx, dely, fig, ax, goal, BALL_R, 'green')
# delx = np.zeros_like(X)
# dely = np.zeros_like(Y)
# ax.quiver(X, Y, delx, dely)
# plt.show()

for i in range(22):
    delx, dely, loc = add_obstacles(X, Y, s, delx, dely, goal)
    plot_graph(X, Y, delx, dely, fig, ax, loc, ROBOT_R, 'red')

# delx, dely = add_goal(X, Y, s, goal)
# plot_graph(X, Y, delx, dely, fig, ax, goal, BALL_R, 'green')
ax.quiver(X, Y, delx, dely)
    # print(delx, dely)
# loc = [loc[1], loc[0]]
# print(loc)
ax.streamplot(X, Y, delx, dely, start_points=[loc], linewidth = 1, cmap = 'autu')

plt.show()
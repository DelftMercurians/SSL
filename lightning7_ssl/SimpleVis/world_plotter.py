import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pickle
import numpy as np
from ..control_client import VisionData

class WorldPlotter():
    def __init__(self, log_path: str) -> None:
        """
            Class to plot positions of robots and ball, and create animation of the play.
        """
        self.logPath = log_path
        self.fig, self.ax = plt.subplots(figsize=(12, 9))
        
        with open(self.logPath, 'rb') as f:
            self.data = pickle.load(f)
    
    def plot(self) -> None:
        """
            Plot the last positions of the robots and ball.
        """
        # Render data from the last 5 frames
        for dat in self.data[-5:-1]:
            ball = dat.ball
            blues = dat.blue_robots
            yellows = dat.yellow_robots

            # Only plot when data is not None
            # TODO:
                # Check if robot positions are correct
                # Check if field size is correct
            if ball is not None:
                self.ax.scatter(ball.x/1000, ball.y/1000, s = 10, c = 'red')

            if blues is not None:
                for pointB in blues:
                    self.ax.scatter(pointB.x/1000, pointB.y/1000, s = 10, c = 'blue')
            
            if yellows is not None:
                for pointY in yellows:
                    self.ax.scatter(pointY.x/1000, pointY.y/1000, s = 10, c = 'yellow')
        self.ax.set_xlim([-6, 6])
        self.ax.set_ylim([-10, 10])
        self.ax.set_facecolor('black')
        plt.show()
    
    def play(self) -> None:
        # TODO
            # Implement replay of simulation
            # Maybe try using Pygame for simulation
        colors = ['red', 'blue', 'green', 'purple', 'yellow']
        def replay_frmaes(i):
            ball = self.data[i]["Ball"]

            self.ax.scatter(ball[0], ball[1], s = 10, c = colors[i])
        
        animation = FuncAnimation(self.fig, func=replay_frmaes, frames = np.arange(0, len(self.data)), interval=10)
        plt.show()
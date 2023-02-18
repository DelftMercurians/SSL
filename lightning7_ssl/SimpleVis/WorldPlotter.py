import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pickle
import numpy as np

class WorldPlotter():
    def __init__(self, log_path: str) -> None:
        self.logPath = log_path
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        
        with open(self.logPath, 'rb') as f:
            self.data = pickle.load(f)
    
    def plot(self) -> None:
        for dat in self.data:
            ball = dat["Ball"]
            blues = dat["BlueTeam"]
            yellows = dat["YellowTeam"]

            self.ax.scatter(ball[0], ball[1], s = 10, c = 'red')
            for pointB, pointY in zip(blues, yellows):
                self.ax.scatter(pointB[0], pointB[1], s = 10, c = 'blue')
                self.ax.scatter(pointY[0], pointY[1], s = 10, c = 'yellow')
        
        plt.show()
    
    def play(self) -> None:
        colors = ['red', 'blue', 'green', 'purple', 'yellow']
        def replay_frmaes(i):
            ball = self.data[i]["Ball"]

            self.ax.scatter(ball[0], ball[1], s = 10, c = colors[i])
        
        animation = FuncAnimation(self.fig, func=replay_frmaes, frames = np.arange(0, len(self.data)), interval=10)
        plt.show()
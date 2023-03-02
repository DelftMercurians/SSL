from typing import List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pickle
import numpy as np
from ..World.maintainer import filteredDataWrapper


class WorldPlotter:
    data: List[filteredDataWrapper]

    def __init__(self, log_path: str) -> None:
        """
        Class to plot positions of robots and ball, and create animation of the play.
        """
        self.logPath = log_path
        self.fig, self.ax = plt.subplots(figsize=(12, 9))

        with open(self.logPath, "rb") as f:
            self.data = pickle.load(f)

    def plot(self) -> None:
        """
        Plot the last positions of the robots and ball.
        """
        # Render data from the last 5 frames
        for dat in self.data[-5:-1]:
            ball = dat.ball_status
            blues = dat.own_robots_status
            yellows = dat.opp_robots_status

            # Only plot when data is not None
            # TODO:
            # Check if robot positions are correct
            # Check if field size is correct
            if ball is not None:
                self.ax.scatter(
                    ball.position[0] / 1000, ball.position[1] / 1000, s=10, c="red"
                )

            if blues is not None:
                for pointB in blues:
                    self.ax.scatter(
                        pointB.position[0] / 1000,
                        pointB.position[1] / 1000,
                        s=10,
                        c="blue",
                    )

            if yellows is not None:
                for pointY in yellows:
                    self.ax.scatter(
                        pointY.position[0] / 1000,
                        pointY.position[1] / 1000,
                        s=10,
                        c="yellow",
                    )
        self.ax.set_xlim([-6, 6])
        self.ax.set_ylim([-10, 10])
        self.ax.set_facecolor("black")
        plt.show()

    def play(self) -> None:
        # TODO
        # Implement replay of simulation
        # Maybe try using Pygame for simulation
        colors = ["red", "blue", "green", "purple", "yellow"]

        def replay_frmaes(i):
            ball = self.data[i].ball_status

            self.ax.scatter(ball.position[0], ball.position[1], s=10, c=colors[i])

        animation = FuncAnimation(
            self.fig,
            func=replay_frmaes,
            frames=np.arange(0, len(self.data)),
            interval=10,
        )
        plt.show()

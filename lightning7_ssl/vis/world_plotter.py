import pickle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from lightning7_ssl.playground.potential_pathfinder import descent_step


class WorldPlotter:
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
            ball = dat["ball"]
            blues = dat["friends"]
            yellows = dat["opps"]

            # Only plot when data is not None
            # TODO:
            # Check if robot positions are correct
            # Check if field size is correct
            if ball is not None:
                self.ax.scatter(ball.position[0] / 1000, ball.position[1] / 1000, s=10, c="red")

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
                    if pointY is not None:
                        self.ax.scatter(
                            pointY.position[0] / 1000,
                            pointY.position[1] / 1000,
                            s=10,
                            c="yellow",
                        )
        self.ax.set_xlim([-6, 6])  # type: ignore
        self.ax.set_ylim([-10, 10])  # type: ignore
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

        FuncAnimation(
            self.fig,
            func=replay_frmaes,
            frames=np.arange(0, len(self.data)),
            interval=10,
        )
        plt.show()


class PotentialWorldPlotter:
    def __init__(
        self, agp: float, rpg: float, field_len: int, field_width: int, pmap: list[list[float]]
    ) -> None:
        """
        Class to plot potential field.
        """
        self.apg = agp
        self.rpg = rpg
        self.field_len = field_len
        self.field_width = field_width
        self.pmap = pmap

    def darw_heatmap(self, starting_point, goal) -> None:
        """
        Draw heatmap of the potential field.
        """
        _, self.ax_heat = plt.subplots()
        self.ax_heat.pcolor(self.pmap, vmax=100.0, cmap=plt.cm.Blues)  # type: ignore
        self.ax_heat.scatter(starting_point[1], starting_point[0], s=100, c="red")  # type: ignore
        self.ax_heat.scatter(goal[0], goal[1], s=10, c="green")  # type: ignore

    def plot_path(self, path: list[descent_step]) -> None:
        """
        Plot the path taken by the robot.
        """
        for segment in path:
            self.ax_heat.scatter(segment.y_index, segment.x_index, s=10, c="red")

    def draw_3d(self) -> None:
        """
        Draw 3D plot of the potential field.
        """
        X, Y = np.meshgrid(range(self.field_len), range(self.field_width))

        plt.figure()
        self.ax_3d = plt.axes(projection="3d")
        # self.ax_3d.plot_wireframe(X, Y, np.clip(self.pmap, min(self.pmap), 100), color="blue")  # type: ignore
        self.ax_3d.plot_surface(
            X,
            Y,
            np.clip(self.pmap, min(self.pmap), 100),
            rstride=10,
            cstride=1,
            cmap="viridis",
            edgecolor="none",
        )  # type: ignore

    def plot_path_3d(self, path: list[descent_step]) -> None:
        for seg in path:
            self.ax_3d.scatter(seg.y_index, seg.x_index, self.pmap[seg.x_index][seg.y_index], s=10, c="red")  # type: ignore


# self.axrpg = self.fig_heat.add_axes([0.25, 0.01, 0.65, 0.03])
# self.rpg_slider = Slider(
#     ax=self.axrpg,
#     label="RPG",
#     valmin=0.0,
#     valmax=500.0,
#     valinit=self.rpg,
# )

# self.axapg = self.fig_heat.add_axes([0.25, 0.05, 0.65, 0.03])
# self.apg_slider = Slider(
#     ax=self.axapg,
#     label="APG",
#     valmin=0.0,
#     valmax=10.0,
#     valinit=self.apg,
# )

# self.rpg_slider.on_changed(self.update_heatmap)
# self.apg_slider.on_changed(self.update_heatmap)

# def pot_update(val):
#         global RPG
#         global APG
#         RPG = rpg_slider_3D.val
#         APG = apg_slider_3D.val
#         ax.clear()
#         pmap = calc_potential_field(goal[1], goal[0], ox, oy, POT_RES, robot_radius, FIELD_LEN, FIELD_WIDTH, s)
#         ax.plot_wireframe(Y, X, np.clip(pmap, min(pmap), 100), color='blue')  # type: ignore
#         fig.canvas.draw_idle()

#     axrpg_3D = fig.add_axes([0.25, 0.01, 0.65, 0.03])
#     rpg_slider_3D = Slider(
#         ax=axrpg_3D,
#         label='RPG',
#         valmin=0.0,
#         valmax=500.0,
#         valinit=100,
#     )

#     axapg_3D = fig.add_axes([0.25, 0.05, 0.65, 0.03])
#     apg_slider_3D = Slider(
#         ax=axapg_3D,
#         label='APG',
#         valmin=0.0,
#         valmax=10.0,
#         valinit=APG,
#     )

#     rpg_slider_3D.on_changed(pot_update)
#     apg_slider_3D.on_changed(pot_update)

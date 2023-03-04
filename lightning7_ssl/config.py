from lightning7_ssl.SimpleVis.world_plotter import WorldPlotter
from lightning7_ssl.SimpleVis.generate_log import LogGenerator
from lightning7_ssl.world.maintainer import World
import matplotlib
matplotlib.use("TkAgg")
class GlobalConfig:
    TICK_INTERVAL_SEC = 0.1
    OWN_TEAM = "blue"
    NUM_PLAYERS = 6
    # Field info
    DIV = "B"
    LENGTH = 9
    WIDTH = 6
    #A robot must fit inside a 0.18 meters wide and 0.15 meters high cylinder at any point in time.
    RADIUS_ROBOT = 0.09
    RADIUS_BALL = 0.0215
    world = World(NUM_PLAYERS, OWN_TEAM == "blue")
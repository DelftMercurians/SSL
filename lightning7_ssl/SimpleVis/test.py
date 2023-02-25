from lightning7_ssl.SimpleVis.generate_log import LogGenerator
import pickle
from lightning7_ssl.SimpleVis.world_plotter import WorldPlotter

logger = LogGenerator("test.pickle")
logger.step(
    {
        "Ball": (7, 7),
        "BlueTeam": [(1, 1), (2, 2), (3, 3)],
        "YellowTeam": [(4, 4), (5, 5), (6, 6)],
    }
)
logger.step(
    {
        "Ball": (7, 8),
        "BlueTeam": [(1, 1), (2, 2), (3, 3)],
        "YellowTeam": [(4, 4), (5, 5), (6, 6)],
    }
)
logger.step(
    {
        "Ball": (7, 9),
        "BlueTeam": [(1, 1), (2, 2), (3, 3)],
        "YellowTeam": [(4, 4), (5, 5), (6, 6)],
    }
)
logger.step(
    {
        "Ball": (7, 10),
        "BlueTeam": [(1, 1), (2, 2), (3, 3)],
        "YellowTeam": [(4, 4), (5, 5), (6, 6)],
    }
)
logger.step(
    {
        "Ball": (7, 11),
        "BlueTeam": [(1, 1), (2, 2), (3, 3)],
        "YellowTeam": [(4, 4), (5, 5), (6, 6)],
    }
)
logger.generate()

# with open(logger.outFile, 'rb') as f:
#     obj = pickle.load(f)
#     for row in obj:
#         print(row)

plotter = WorldPlotter("test.pickle")
plotter.plot()
plotter.play()

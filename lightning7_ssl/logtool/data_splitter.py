import argparse

from Gamelog import Gamelog

parser = argparse.ArgumentParser(description="split a gamelog into multiple parts")
parser.add_argument("path", type=str, help="the path to the gamelog")
parser.add_argument("type", type=str, choices=["goal", "foul"], help="the type of scene to split on")
parser.add_argument("--output", type=str, help="The output folder")
parser.set_defaults(output=".")
args = parser.parse_args()
g = Gamelog.from_binary(args.path)
filename = args.path.split("/")[-1].split(".")[0]
if args.type == "goal":
    scenes = g.getGoalScenes()
    for i, scene in enumerate(scenes):
        g.to_binary(f"{args.output}/{filename}_goal_{i}.log", scene)
if args.type == "foul":
    scenes = g.getFoulScenes()
    for i, scene in enumerate(scenes):
        reasons, segments = scene
        g.to_binary(f"{args.output}/{filename}_foul_{i}_{reasons}.log", segments)

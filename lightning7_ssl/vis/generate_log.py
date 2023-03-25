import pickle
from typing import Dict, List

from ..vis.data_store import DataStore


class LogGenerator:
    """Class that stores robot and ball informations and saves them to a csv file."""

    data: List[Dict]

    def __init__(self, dest_path: str) -> None:
        """
        Create csv file with heading.
        """
        self.outFile = dest_path
        self.data = []

    def step(self, update: Dict, _: DataStore) -> None:
        """
        Stores data of current timestamp.
        """
        self.data.append(update)

    def generate(self) -> None:
        """
        Generate log file.
        """
        with open(self.outFile, "wb") as f:
            pickle.dump(self.data, f)

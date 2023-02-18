import numpy as np
import pickle

class LogGenerator():
    """
        Class that stores robot and ball informations and saves them to a csv file.
    """
    def __init__(self, dest_path: str) -> None:
        """
            Create csv file with heading.
        """
        self.outFile = dest_path
        self.data = []
    
    def step(self, data:dict) -> None:
        """
            Stores data of current timestamp.
        """
        self.data.append(data)

    def generate(self) -> None:
        """
            Generate log file.
        """
        with open(self.outFile, 'wb') as f:
            pickle.dump(self.data, f)
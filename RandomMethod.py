import numpy as np

class RandomMethod():
    def __init__(self): #the method will determine the choice of the agent
        self.choice = 'none'

    def choose(self, QtableCoord): #the QtableCoord parameter is useless here
        self.choice = np.random.choice(['up', 'down', 'left', 'right'])

    def display(self):
        print("Random choice")

    def method(self):
        return "Random"
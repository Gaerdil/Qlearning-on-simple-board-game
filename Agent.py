import numpy as np
import RandomMethod as RM

class Agent():
    def __init__(self, method): #the method will determine the choice of the agent
        self.brain = method
        self.choice = 'none'

    def choose(self,QtableCoord):
        self.brain.choose(QtableCoord)
        self.choice = self.brain.choice

    def display(self):
        self.brain.display()


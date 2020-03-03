import numpy as np
import math
import random

#Here, one state = one spot in the Board.
#this is why this method will only work with one ice cream
#Because we would have to implement 1 state = 1 spot in one type of board (number of ice creams displayed)

class Qlearning():
    def __init__(self): #the method will determine the choice of the agent.
        self.choice = 'none'
        self.alpha = 0.5
        self.gama = 0.7
        # we have 4 states : start, glaces, maxi glaces, clown
        #init Q table :
        self.types = ['start','glace','multiglaces','clown','empty_spot']
        self.rewards = {"glace": 10 , "multiglaces":30 ,"clown":-math.inf,'empty_spot': -1 }
        self.actions = ['up','down','left','right']
        self.rows = 0
        self.cols = 0
        self.initBoard = []
        self.Board = [] #will help keep track of disappearing ice creams
        self.Qtable = []

    def initBoard_Qtable(self, InitBoard):  # we will do the learning without calling all of  the time a new instance of the game
        self.rows = len(InitBoard)
        self.cols = len(InitBoard[0])
        self.initBoard = np.array(InitBoard).flatten()
        self.Board = [x[:] for x in self.initBoard]
        self.Qtable =  np.zeros((self.rows*self.cols,4))  # each spot of the board is a state. And we have 4 actions for each case.
        self.setUnavailableActions() # we have to remove impossible moves


    def setUnavailableActions(self):
        for state in range(len(self.Qtable)):
            if state < self.cols:
                self.Qtable[state][0] = -math.inf #will never be updated, or chosen
            if state >= (self.rows - 1 )*self.cols :
                self.Qtable[state][1] = -math.inf
            if state % self.cols == 0 :
                self.Qtable[state][2] = -math.inf
            if state % self.cols == self.cols-1:
                self.Qtable[state][3] = -math.inf

    def choose(self, QtableCoord): #the coordinate to fetch in the Q table for value
        #part for real game
        self.choice = self.actions[np.argmax(self.Qtable[QtableCoord])]


    def findNewState(self, state, action): #action is an int , state the coordinate in the Qtable

        newState = -1

        if action == 0 :
            newState = state - self.cols
        elif action == 1 :
            newState = state + self.cols
        elif action == 2:
            newState = state - 1
        elif action == 3:
            newState = state + 1
        return newState

    def updateQtable(self, state, action):
        if self.Qtable[state][action] > -math.inf :
            newState = self.findNewState(state, action)
            self.Qtable[state][action] = (1- self.alpha)*self.Qtable[state][action] + self.alpha*(self.reward(state, action) + self.gama*self.maxQ(state, newState))


    def reward(self, state, action): #returns reward of taking this action (int) when in this states
        newState = self.findNewState(state,action)
        return self.rewards[self.Board[newState]] #reward of the action - in current board.

    def maxQ(self, state, newState):  #Maximum expected update at new state, coming from state state.
       return max(self.Qtable[newState]) #perfect if we did not had to take in account the removal of the ice creams


    def updateBoard(self, state):  # keep track of the fact that the ice cream disappeared
        # part for training only
        current = self.Board[state]
        if current == 'glace' or current == 'multiglaces':
            self.Board[state] = 'empty_spot'

    def train(self, initPosition, etha): #One epoch of training : until the score is too low.
        #etha stands for exploration tradeoff
        limit = -20
        score = 0
        self.Board = [x[:] for x in self.initBoard] #be sure to begin a new session
        state = initPosition[0]*self.cols + initPosition[1]

        condiVar = (("glace" in self.Board) or ("multiglaces" in self.Board)) and (score > limit)
        while  condiVar:
            #new action
            coin = random.random()
            if etha >= coin :
                action = random.choice([0,1,2,3])
                while self.Qtable[state][action] <= -math.inf :
                    action = random.choice([0,1,2,3])
            else :
                action = np.argmax(self.Qtable[state])

            #updates
            self.updateQtable(state, action) #Qtable updated
            state = self.findNewState(state, action)
            score += self.rewards[self.Board[state]]
            self.updateBoard(state) #remove ice cream
            condiVar = (("glace" in self.Board) or ("multiglaces" in self.Board)) and (score > limit)
            # print(score, state)
            # print("---condiVar: "+str(condiVar))
            # print(score>limit)
            # print(("glace" in self.Board))
            # print("multiglaces" in self.Board)
            # print((("glace" in self.Board) or ("multiglaces" in self.Board)))




    def display(self):
        print("\n_______________Q learning____________________ \n")
        print("_______Initial Board__________")
        print(self.initBoard)

        print("\n_______Q table__________")
        for y in self.Qtable:
            print(y)
        print("\n")

    def method(self):
        return "Qlearning"

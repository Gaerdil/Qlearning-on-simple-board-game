import os
import GameWithIA as GIA
import RandomMethod as RM
import Qlearning as Q
import Agent as A


#___________Initialisation  step : Get the initBoard of the game__________________________
Outputs = []  # list of outputs
# Create a Random agent first to get the init board #method = RM.RandomMethod()
method = RM.RandomMethod()
playerAgent = A.Agent(method)

initGame = GIA.LaunchGame(playerAgent, Outputs, True)

InitBoard, initPosition = initGame.simpleBoard, initGame.initialPosition


#_____________Board initialized : we can make the real IA play____________________________
Outputs = []
method = Q.Qlearning()
playerAgent = A.Agent(method)    # we will be able to update the parameters of our agent easily
playerAgent.brain.initBoard_Qtable(InitBoard)
playerAgent.display()

#GIA.LaunchGame(playerAgent,Outputs) #not trained yet : performs really badly

#_____________Training the agent, and making tests________________________
trainIterations = 3
i =0
epochs = 50

for j in range(trainIterations):
    while i % epochs != 0:
        etha = 5/(j+5)
        playerAgent.brain.train(initPosition, etha)
        i += 1
    playerAgent.display()
    GIA.LaunchGame(playerAgent, Outputs)
    i += 1

# for i in range(3):
#     print("Round "+str(i))
#     GIA.LaunchGame(playerAgent, Outputs, InitBoard)
#     if Outputs[i] :
#         print('WON')
#     else:
#         print('LOST')
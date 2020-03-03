# Pygame template -skeleton for a new project
import pygame as py
import random
import os
import math
import Agent as A
import RandomMethod as RM
#IA VERSION !



class LaunchGame():
    def __init__(self, agent, Outputs, initialiseBoard = False): #the method will determine the choice of the agent.
        random.seed(0)  # Very simple Q table to begin with

        self.output = False #not won yet
        self.simpleBoard = []
        self.initialPosition = [] #to get the initial position for training sessions

        playerAgent = agent

        largeur = 1500
        longueur = 1000
        FPS = 12
        spot_size = 150
        Spots_col = 8
        Spots_line = 5
        player_size = 150

        # define colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        VIOLET = (255, 0, 255)
        LightYELLOW = (255, 255, 100)
        LightBrown = (220, 220, 150)

        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, "img")
        sound_folder = os.path.join(game_folder, "sound")

        font_name = py.font.match_font('arial')  # pygame finds closest font in the computer

        def draw_text(surf, text, size, x, y, color=BLACK):  # pas si évident avec pygame
            font = py.font.Font(font_name, size)
            text_surface = font.render(text, True, color)  # white for color true for anti aliased
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
            surf.blit(text_surface, text_rect)  # le text surface est sur le text rectangle

        # ___________Sprites________________________

        class Child(py.sprite.Sprite):
            # sprite for the Player
            def __init__(self, player_size, agent):
                py.sprite.Sprite.__init__(self)
                self.image = child
                self.agent = agent
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (4 * player_size // 3, player_size))
                self.rect = self.image.get_rect()
                self.rect.center = (longueur // 2, largeur // 2)
                self.current_spot_neighbors = []
                self.score = 1
                self.line = -1
                self.col = -1 #has to be initialized


            def update(self):
                QtableCoord = (self.line)*(Spots_col) + self.col
                self.agent.choose(QtableCoord)
                choice = self.agent.choice
                if choice == 'up':
                    if self.current_spot_neighbors[0] != None:
                        self.Move_to(self.current_spot_neighbors[0])
                if choice == 'down':
                    if self.current_spot_neighbors[1] != None:
                        self.Move_to(self.current_spot_neighbors[1])
                if choice == 'left':
                    if self.current_spot_neighbors[2] != None:
                        self.Move_to(self.current_spot_neighbors[2])
                if choice == 'right':
                    if self.current_spot_neighbors[3] != None:
                        self.Move_to(self.current_spot_neighbors[3])

            def Initialize(self, objects):
                nested = False
                while not nested:
                    line = random.choice(objects)
                    obj = random.choice(line)
                    if obj.type == 'empty_spot':
                        if not obj.surrounded_by_clowns():
                            self.Move_to(obj)
                            nested = True

            def Move_to(self, spot):
                # if self.current_spot != None :
                #     self.current_spot.kill()
                self.rect.center = spot.rect.center
                self.current_spot_neighbors = spot.neighbors
                self.score += spot.reward
                self.line = spot.line
                self.col = spot.col
                if spot.type == 'glace' or spot.type == 'multiglaces':
                    spot.meet()

        # _______________________Types of spot_______________________________________________

        class Empty_spot(py.sprite.Sprite):
            def __init__(self, spot_size, spot_center,i,j): #i,j = coordinates in the Matrix
                py.sprite.Sprite.__init__(self)
                spot_size = 2 * spot_size // 3
                self.image = py.Surface((spot_size, spot_size))
                self.image.fill(LightYELLOW)
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (spot_size, spot_size))
                self.rect = self.image.get_rect()
                self.rect.center = spot_center
                self.type = 'empty_spot'
                self.reward = -1
                self.neighbors = []  # only up / down / right /left
                self.line = i
                self.col = j

            def surrounded_by_clowns(self):
                answer = True
                for x in self.neighbors:
                    if x != None:
                        if x.type != 'clown':
                            answer = False
                return answer

        class Glace(py.sprite.Sprite):
            def __init__(self, spot_size, spot_center,i,j):
                py.sprite.Sprite.__init__(self)
                self.height = spot_size  # générer des hauteurs différentes
                self.image = glace
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (3 * spot_size // 4, spot_size))
                self.rect = self.image.get_rect()
                self.rect.center = spot_center
                self.type = 'glace'
                self.reward = 10
                self.neighbors = []  # only up / down / right /left
                self.line = i
                self.col = j

            def meet(self):
                self.reward = -1
                self.kill()

        class Multiglaces(py.sprite.Sprite):
            def __init__(self, spot_size, spot_center,i,j):
                py.sprite.Sprite.__init__(self)
                self.height = spot_size  # générer des hauteurs différentes
                self.image = multiglaces
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (spot_size, spot_size))
                self.rect = self.image.get_rect()
                self.rect.center = spot_center
                self.type = 'multiglaces'
                self.reward = 30
                self.neighbors = []  # only up / down / right /left
                self.line = i
                self.col = j

            def meet(self):
                self.reward = -1
                self.kill()

        class Clown(py.sprite.Sprite):
            def __init__(self, spot_size, spot_center,i,j):
                py.sprite.Sprite.__init__(self)
                self.height = spot_size  # générer des hauteurs différentes
                self.image = clown
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (spot_size, spot_size))
                self.rect = self.image.get_rect()
                self.rect.center = spot_center
                self.type = 'clown'
                self.reward = -math.inf
                self.neighbors = []  # only up / down / right /left
                self.line = i
                self.col = j

        # ______________________________________________________________________________

        def Spot_Choice(i, j, ice):
            rand = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            if rand <= 3:
                spot = Clown(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)),i,j)
            # elif rand <= 3:
            #     spot = Glace(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)),i,j)
            elif rand <= 4 :
                if ice :
                    ice = False
                    spot = Multiglaces(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)),i,j)
                else :
                    spot = Empty_spot(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)), i, j)
            else:
                spot = Empty_spot(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)),i,j)

            return spot,ice

        def Construct_neighbors(objects):
            for i in range(len(objects)):
                for j in range(len(objects[0])):
                    obj = objects[i][j]
                    if i == 0:
                        obj.neighbors.append(None)
                    elif i != 0:
                        obj.neighbors.append(objects[i - 1][j])  # up
                    if i == Spots_line - 1:
                        obj.neighbors.append(None)
                    elif i != Spots_line - 1:
                        obj.neighbors.append(objects[i + 1][j])  # down

                    if j == 0:
                        obj.neighbors.append(None)
                    elif j != 0:
                        obj.neighbors.append(objects[i][j - 1])  # up
                    if j == Spots_col - 1:
                        obj.neighbors.append(None)
                    elif j != Spots_col - 1:
                        obj.neighbors.append(objects[i][j + 1])  # down

        def still_Ice_creams(obj_sprite):  # is the game resolved ?
            answer = False
            for obj in obj_sprites:
                if obj.type == 'glace' or obj.type == 'multiglaces':
                    answer = True
            return answer


        def simplifiedBoard(objects):  #For geting the initialized board, for Qlearning
            for obj_line in objects:
                line = []
                for obj in obj_line:
                    line.append(obj.type)
                self.simpleBoard.append(line)


        # initialize pygame and create window

        py.init()
        py.mixer.init()
        screen = py.display.set_mode((largeur, longueur))
        py.display.set_caption("Qlearning")
        clock = py.time.Clock()  # pour contrôler nos FPS

        background = py.image.load(os.path.join(img_folder, "officialbackground.jpg")).convert()
        background_rect = background.get_rect()  # pour le background

        multiglaces = py.image.load(os.path.join(img_folder, "multiglaces.png"))
        glace = py.image.load(os.path.join(img_folder, "glace.png"))
        clown = py.image.load(os.path.join(img_folder, "clown.png"))
        child = py.image.load(os.path.join(img_folder, "child.png"))

        obj_sprites = py.sprite.Group()  # objects like clowns and ices creams
        spots_sprites = py.sprite.Group()
        child_sprite = py.sprite.Group()
        all_sprites = py.sprite.Group()

        player = Child(player_size, playerAgent)
        child_sprite.add(player)
        all_sprites.add(player)

        Objects = []
        ice = True
        for i in range(Spots_line):
            Objects_row = []
            for j in range(Spots_col):
                obj,ice = Spot_Choice(i, j,ice)
                spot = Empty_spot(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)), i,j)
                Objects_row.append(obj)
                spots_sprites.add(spot)
                obj_sprites.add(obj)
                all_sprites.add(obj)
                all_sprites.add(spot)
            Objects.append(Objects_row)

        Construct_neighbors(Objects)
        player.Initialize(Objects)
        #Record initial position of the player
        self.initialPosition = [player.line, player.col]

        if initialiseBoard: # we initialise the board
            simplifiedBoard(Objects) # Will help in the Qlearning problem
        # __________SOUND LOAD__________________________________________________

        death_sound = py.mixer.Sound(os.path.join(sound_folder, "scream.ogg"))
        death_sound.set_volume(0.2)

        clown = py.mixer.Sound(os.path.join(sound_folder, "Evil-toy-laughing.ogg"))
        clown.set_volume(1.2)

        happy = py.mixer.Sound(os.path.join(sound_folder, "Mcdonald-melody-toy.ogg"))
        happy.set_volume(0.4)

        py.mixer.music.load(os.path.join(sound_folder, "Circus-music.ogg"))  # musique en continue
        py.mixer.music.set_volume(0.5)

        # ________________________________ Game loop_______________________________________________________________________

        py.mixer.music.play(loops=-1)  # ici la config de loop remet la musique au début lorsqu'elle est finie


        # Game loop

        running = True
        NotfirstLoop = False

        py.time.wait(300)
        while running:
            # keep loop running at the right speed
            clock.tick(FPS)
            py.time.wait(300)
            # Process input (events)
            for event in py.event.get():
                # Check for closing window
                if event.type == py.QUIT:
                    running = False

            # Update
            if NotfirstLoop :
                all_sprites.update()

            if player.score <= -20:  # met a clown / exhaustion
                py.mixer.music.stop()
                clown.play()
                death_sound.play()
                running = False

            if not still_Ice_creams(obj_sprites):
                self.output = True # we won !
                py.mixer.music.stop()
                happy.play()
                running = False

            # Draw/render
            screen.fill(LightBrown)
            screen.blit(background, background_rect)  # mettre la vraie image de fond
            spots_sprites.draw(screen)
            obj_sprites.draw(screen)
            child_sprite.draw(screen)
            draw_text(screen, "SCORE :" + str(player.score), 30, largeur // 2, longueur - 40,
                      RED)  # 30 est pour la taille
            draw_text(screen, "EAT ICE CREAM & AVOID CLOWNS!", 50, largeur // 2, 10, RED)  # 18 est pour la taille
            # *after* drawing everything, flip the display
            py.display.flip()  # permet de passer du background qu'on ne redraw pas à chaque fois au foreground
            NotfirstLoop = True

            if not running:
                py.time.wait(500) #2000 with sound

        Outputs.append(self.output)
        py.quit()




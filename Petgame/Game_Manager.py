import json
import pygame
import Events_System
from UI_Manager import UIManager
from Sunny import Sunny
"""
This is the main class responsible for initializing the game 
"""
class GameManager:
    instance = None #Track if GameManager object has already been created

    #Override new so this class stays a singleton
    def __new__(cls):
        #Make a GM object if it hasn't been created already
        if cls.instance is None:
            cls.instance = super().__new__(cls) #Record that the object was created
        #Return the new instance
        return cls.instance

    #Gets game save data and makes non-pygame objects
    def __init__(self):
        print("Initializing game...")

        #The current version (needed for telling how to read older/newer save files)
        self.version = 1.0
        self.targetFPS = 60
        saveData = self.readSave()
        self.pet = Sunny(saveData.get("Pet"))

        #Other variables that will be initialized when starting/running the game 
        self.screen = None
        self.uim = None
        self.isRunning = False

        #Subscribe to the global events
        Events_System.on_game_start.subscribe(self.startGame)
        Events_System.on_game_end.subscribe(self.endGame)

    def readSave(self):
        print("Checking save file...")
        try:
            inFile = open("save.json", 'r')
            return json.load(inFile)
        except FileNotFoundError:
            return {}

    #Saves Sunny's stats and gameplay information in a json file
    def saveGame(self):
        print("Saving game...")
        newSaveData = {
            "version": self.version,
            "target FPS": self.targetFPS,
            "Sunny": self.pet.getSave()
            }
        with open("save.json", "w") as newSaveFile:
            json.dump(newSaveData, newSaveFile)

    #Sets up the display before running the game loop
    def startGame(self):
       pygame.init()
       #Getting information about the screen
       monitorDimensions = pygame.display.Info()
       screenWidth = monitorDimensions.current_w
       screenHeight = monitorDimensions.current_h

       #Make the main game surface to draw stuff on
       self.screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
       pygame.display.set_caption("Sunny game")

       #Check if the display is being scaled to position UI correctly, like your laptop is at 125% vs PC at 100%
       scaleFactor = 1920/screenWidth

       #Create the wrapped UI manager to handle switching screens
       self.uim = UIManager(self.pet, screenWidth, screenHeight, scaleFactor)
       #Finally, run the main game loop
       self.run()
       #Game Manager=> UI manager = >current screen => ui component

    #Runs the gameplay loop
    def run(self):
        self.isRunning = True
        clock = pygame.time.Clock()
        while self.isRunning:
            #Delta time lets you make your game frame rate indpendent
            #Convert ms that have passed to seconds, then multiply by targetFPS to make up for any lost frames
            dt = clock.tick(60) * 0.001 * self.targetFPS
            clock.tick(60) #Cap the FPS at 60

            #Capture and process input/events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

                #Send events to the UI manager to interpret/respond to them
                self.uim.readEvents(event)

            self.uim.gui.update(dt)
            self.screen.fill((0,0,0))
            self.uim.draw(self.screen)
            pygame.display.flip()

    def endGame(self):
        self.saveGame()

gm = GameManager()
gm.startGame()
gm.run()
        
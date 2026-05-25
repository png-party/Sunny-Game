import json
import pygame
import pygame_gui
from UI_Manager import UIManager
from Event_System import GameEvent
from Sunny import Sunny
class GameManager:
    instance = None #Track if Game object has been created

    #Override new so this class stays a singleton
    def __new__(cls):
        #Make a GM object if it hasn't been created already
        if cls.instance is None:
            cls.instance = super().__new__(cls) #Record that the object was created
        #return the new instance
        return cls.instance
    #Gets game save data and makes non-pygame objects
    def __init__(self):
        print("Initialzing game")
        #The current version (needed for telling how to read older/newer save files)
        self.version = 1.0
        saveData = self.readSave()
        self.pet = Sunny(saveData.get("Pet"))
        #Other variables that will be initialized when starting/running the game 
        self.screen = None
        self.uim = None
        self.isRunning = False
       

    def readSave(self):
        print("Checking save file...")
        try:
            inFile = open("save.json", 'r')
            return json.load(inFile)
        except FileNotFoundError:
            return {}

    def saveGame(self):
        print("Saving game...")
        newSaveData = {
            "version": self.version,
            "Sunny": self.pet.getSave()
            }
        with open("save.json", "w") as newSaveFile:
            json.dump(newSaveData, newSaveFile)

    def startGame(self):
       pygame.init()
       #Make the main game surface to draw stuff on
       self.screen = pygame.display.set_mode((1920, 1080))
       pygame.display.set_caption("Sunny game")

       #Create the wrapped UI manager to handle switching screens
       self.uim = UIManager() #todo: add delegates
       #Start the main game loop
       self.run()
       #Game Manager=> UI manager = >current screen => ui component
       #create GUI
    def run(self):
        self.isRunning = True
        clock = pygame.time.Click()
        while self.isRunning:
            clock.tick(60) #Cap the FPS at 60

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
    def endGame(self):
        self.saveGame()
#todo: add main
gm = GameManager()
        
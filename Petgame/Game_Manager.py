import json
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
    def __init__(self):
        print("Initialzing game")
        #The current version (needed for telling how to read older/newer save files)
        self.version = 1.0
        saveData = self.readSave()
        self.pet = Sunny(saveData.get("Pet"))
        
        #create GUI

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

   
    def endGame(self):

        self.saveGame()

gm = GameManager()
gm.endGame()
        
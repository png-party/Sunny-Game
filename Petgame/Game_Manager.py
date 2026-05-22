import json
import Sunny
class GameManager:
    instance = None #Track if Game object has been created

    #Override new so this class stays a singleton
    def __new__(cls):
        #Make a GM object if it hasn't been created already
        if cls.instance is None:
            cls.instance = super().__new__(cls) #Record that the object was created
    def __init__(self):
        saveData = self.readSave()
        self.pet = Sunny(saveData.get("Pet"))
        #create GUI
    def readSave(self):
        try:
            inFile = open("save.json", 'r')
            return json.load(inFile)
        except FileNotFoundError:
            return {}
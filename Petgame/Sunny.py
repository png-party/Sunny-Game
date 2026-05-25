import json
from Event_System import GameEvent
class Sunny:
    def __init__(self, savedStats:dict=None):
        #if no saved stats exist, use an empty dict
        if not savedStats: savedStats = {}
        print("Making sunny object")
        #create sunny with saved or default stats
        self.health = savedStats.get("health", 50)
        self.energy = savedStats.get("energy", 50)
        self.happiness = savedStats.get("happiness", 20)

        #Create delegates to handle events pertaining to Sunny
        #stat-related events
        self.on_hpMax = GameEvent()
        self.on_hp_updated = GameEvent()
        self.on_hpMin = GameEvent()

        self.on_energyMin = GameEvent()
        self.on_energyUpdated = GameEvent()
        self.on_energyMax = GameEvent()
  
        self.on_happinessMax = GameEvent()
        self.on_happinessChanged = GameEvent()
        self.on_happinessMin = GameEvent()


        
    """
    Increments or decrements health by specified amount
    Max HP = 100, min HP = 10
    Game ends when HP <= 10
    """
    def updateHealth(self, hp:int):
        newHP = self.health + hp
        if 10 <= newHP:
            if newHP <= 100:
                self.health = newHP
                self.on_hpUpdated.invoke(self.health)
               
            else:
                self.on_hpMax.invoke(self.health, newHP)
                print("HP too high")
        else:
            self.on_hpMin.invoke(self.health, newHP)
            print("HP too low")

        return self.health

    def updateEnergy(self, e:int):
        newEnergy = self.energy + e
        if 0 <= newEnergy:
            if newEnergy <= 99:
                #Can successfully update energy
                self.energy = newEnergy
                self.on_energyUpdated.invoke(self.energy)
            else:
                #Lose condition when energy >= 100
                self.on_energyMax.invoke(self.energy, newEnergy)
        else:
            self.on_energyMin.invoke(self.energy, newEnergy)
            return self.energy

    def updateHappiness(self, h:int):
        newHappiness = self.happiness + h
        if 15 <= newHappiness:
            if newHappiness <= 100:
                self.happiness = newHappiness
                self.on_happinessChanged.invoke(self.happiness)
                #Check if pet has enough happiness to win (95)
                if 95 <= self.happiness:
                    self.on_happinessWin.invoke(self.happiness)
            else:
                self.on_happinessMax.invoke(self.happiness, newHappiness)
        else:
            self.on_happinessMin.invoke(self.happiness, newHappiness)
        return self.happiness

    #Sends the pet's stats as a dict to the GM class so it can be saved as a json
    def getSave(self):
        return {
            "health": self.health,
            "energy": self.energy,
            "happiness": self.happiness
            }

  



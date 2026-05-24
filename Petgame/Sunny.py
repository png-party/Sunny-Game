import json
from collections import deque
import Events_Sunny
class Sunny:
    def __init__(self, savedStats:dict=None):
        if not savedStats: savedStats = {}
        print("Making sunny object")
        self.health = savedStats.get("health", 50)
        self.energy = savedStats.get("energy", 50)
        self.happiness = savedStats.get("happiness", 20)
        
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
                Events_Sunny.on_hpUpdated.invoke(self.health)
               
            else:
                Events_Sunny.on_hpMax.invoke(self.health, newHP)
                print("HP too high")
        else:
            Events_Sunny.on_hpMin.invoke(self.health, newHP)
            print("HP too low")

        return self.health

    def updateEnergy(self, e:int):
        newEnergy = self.energy + e
        if 0 <= newEnergy:
            if newEnergy <= 99:
                #Can successfully update energy
                self.energy = newEnergy
                Events_Sunny.on_energyUpdated.invoke(self.energy)
                #Add a debuff if energy is too high
                if 85 <= newEnergy:
                    Events_Sunny.on_energyDebuff.invoke(self.energy)
            else:
                #Lose condition when energy >= 100
                Events_Sunny.on_energyMax.invoke(self.energy, newEnergy)
        else:
            Events_Sunny.on_energyMin.invoke(self.energy, newEnergy)
            return self.energy

    def updateHappiness(self, h:int):
        newHappiness = self.happiness + h
        if 15 <= newHappiness:
            if newHappiness <= 100:
                self.happiness = newHappiness
                Events_Sunny.on_happinessChanged.invoke(self.happiness)
                #Check if pet has enough happiness to win (95)
                if 95 <= self.happiness:
                    Events_Sunny.on_happinessWin.invoke(self.happiness)
            else:
                Events_Sunny.on_happinessMax.invoke(self.happiness, newHappiness)
        else:
            Events_Sunny.on_happinessMin.invoke(self.happiness, newHappiness)
        return self.happiness

    #Sends the pet's stats as a dict to the GM class so it can be saved as a json
    def getSave(self):
        return {
            "health": self.health,
            "energy": self.energy,
            "happiness": self.happiness
            }

  



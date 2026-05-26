import json
from Game_Event import GameEvent
from Food import Food
class Sunny:
    def __init__(self, savedStats:dict=None):
        #if no saved stats exist, use an empty dict
        if not savedStats: savedStats = {}
        print("Making sunny object")
        #create sunny with saved or default stats
        self.health = savedStats.get("health", 50)
        self.energy = savedStats.get("energy", 50)
        self.happiness = savedStats.get("happiness", 20)

        #Dict with the food name, the food object, and the quantity of that food
        self.foodInventory= {"Dry food": [Food("Dry food", 10, 15, -3), savedStats.get("Dry food", 3)],
                          "Catnip": [Food("Catnip", -6,-5,8), savedStats.get("Catnip", 3)],
                          "Wet food": [Food("Wet food", 6,9,3), savedStats.get("Wet food", 2)],
                          "Churu paste": [Food("Churu paste", 0,2,6), savedStats.get("Churu paste", 1)]}

        #Create delegates to handle events pertaining to Sunny
        #stat-related events
        self.on_hpMax = GameEvent()
        self.on_hpUpdated = GameEvent()
        self.on_hpMin = GameEvent()

        self.on_energyMin = GameEvent()
        self.on_energyUpdated = GameEvent()
        self.on_energyMax = GameEvent()
  
        self.on_happinessMax = GameEvent()
        self.on_happinessUpdated = GameEvent()
        self.on_happinessMin = GameEvent()

        self.on_happinessWin = GameEvent()

        
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
                self.health = 100
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
                self.on_happinessUpdated.invoke(self.happiness)
                #Check if pet has enough happiness to win (95)
                if 95 <= self.happiness:
                    self.on_happinessWin.invoke(self.happiness)
            else:
                self.happiness = 100
                self.on_happinessMax.invoke(self.happiness, newHappiness)
        else:
            self.on_happinessMin.invoke(self.happiness, newHappiness)
        return self.happiness

    def removeFood(self, itemName:str):
        if itemName in self.foodInventory:
            self.foodInventory[itemName][1] -= 1

            if self.foodInventory[itemName][1] <= 0:
                self.foodInventory[itemName][1] = 0 #avoid getting negative food
    def addFood(self, itemName:str):
        if itemName in self.foodInventory:
            self.foodInventory[itemName][1] += 1

    def Feed(self, itemName:str): #todo: only make it show/process relevant stats
        if itemName in self.foodInventory and self.foodInventory.get(itemName)[1] > 0:
            food = self.foodInventory.get(itemName)[0]
            
            print("Feeding sunny", food.name)
            self.updateHealth(food.hp)
            self.updateEnergy(food.energy)
            self.updateHappiness(food.happiness)
            self.removeFood(itemName)

    #Sends Sunny's stats as a dict to the GM class so it can be saved as a json
    def getSave(self):
        return {
            "health": self.health,
            "energy": self.energy,
            "happiness": self.happiness,
            "Dry food": self.foodInventory.get("Dry food")[1],
            "Catnip": self.foodInventory.get("Catnip")[1],
            "Wet food": self.foodInventory.get("Wet food")[1],
            "Churu paste": self.foodInventory.get("Churu paste")[1]
            }

  



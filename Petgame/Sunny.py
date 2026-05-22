from collections import deque
import Events_Sunny
class Sunny:
    def __init__(self, savedStats:dict, churuDebuffActive:bool=False, churuCount:int=0, highEnergyDebuffActive:bool=False, excessEnergy:int=1, lowHealthDebuff:bool=False):
        self.health = savedStats.get("health", 50)
        self.energy = savedStats.get("energy", 50)
        self.happiness = savedStats.get("happiness", 20)
        self.recentGames = deque(savedStats.get("recentGames", [0]), maxlen=10)
        self.activeDebuffs = savedStats.get("activeDebuffs", [])
        self.status = [["Churu debuff", churuDebuffActive, churuCount], ["High energy debuff", highEnergyDebuffActive, excessEnergy], ["Low HP debuff", lowHealthDebuff, 0.25]]
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
            if newEnergy <= 100:
                #Can successfully update energy
                self.energy = newEnergy
                Events_Sunny.on_energyUpdated.inoke(self.energy)
                #Add a debuff if energy is too high
                if 85 <= newEnergy:
                    Events_Sunny.on_energyDebuff.invoke(self.energy)
            else:
                Events_Sunny.on_energyMax.invoke(self.energy, newEnergy)
        else:
            Events_Sunny.on_energyMin.invoke(self.energy, newEnergy)
  
print("making sunny object")
s = Sunny()
s.updateHealth(10000)



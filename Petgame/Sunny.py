from collections import deque
class Sunny:
    def __init__(self, health:int=50, energyLevel:int=50, joy:int=20, recentGames:list=[0,0,0,0,0,0,0,0,0,0], churuDebuffActive:bool=False, churuCount:int=0, highEnergyDebuffActive:bool=False, excessEnergy:int=1, lowHealthDebuff:bool=False):
        self.hp = health
        self.energy = energyLevel
        self.happiness = joy
        self.gameLog = deque(recentGames, maxlen=10)
        self.status = [["Churu debuff", churuDebuffActive, churuCount], ["High energy debuff", highEnergyDebuffActive, excessEnergy], ["Low HP debuff", lowHealthDebuff, 0.25]]
    """
    Increments or decrements health by specified amount
    Max HP = 100, min HP = 10
    Game ends when HP <= 10
    """
    def updateHealth(self, hp:int):
        if self.health + hp <= 10:
            #TODO: add function to end the game
            print("game over")
        
print("test")




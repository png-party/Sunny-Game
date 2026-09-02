class Food:
    def __init__(self, foodName:str, hpGain:int, energyGain:int, happinessGain:int):
        self.name = foodName
        self.hp = hpGain
        self.energy = energyGain
        self.happiness = happinessGain
    def __str__(self):
        return f"{self.name}\nHP: {self.hp}\nEnergy: {self.energy}\nHappiness: {self.happiness}"
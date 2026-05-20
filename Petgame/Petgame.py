class Sunny:
    def __init__(self):
        self.health = 50
        self.hunger = 50
        self.skill = 0
        self.joy = 50
    """
    Increments or decrements health by specified amount
    Max HP = 100, min HP = 10
    Game ends when HP <= 10
    """
    def updateHealth(self, hp:int):
        if self.health + hp <= 10:
            #TODO: add function to end the game
            print("game over")
        self.health += hp if 10 < self.health + hp <= 100 else 




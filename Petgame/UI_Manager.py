import pygame
class UIManager:
    def __init__(self):
        #Store all of the different game screens in a dict
        self.screens = {
            "mainMenu": MainMenu(),
            "home": Home(),
            "ballGame": BallGame()
            }
        self.currentScreen = self.screens["home"]

    #Change the current active screen to something else
    def switchScreen(self, newScreen):
        self.currentScreen = self.screens[newScreen]
    #Only draw the current active screen selected by the ui manager onto the main game surface
    def draw(self, gameSurface:pygame.Surface):
        self.currentScreen.draw(gameSurface) #gameSurface is the one that comes from GM

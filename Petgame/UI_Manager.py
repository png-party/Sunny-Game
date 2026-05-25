import pygame
import pygame_gui
from UI_Screens import MainMenu, Home, BallGame
"""
Acts like a wrapper class for pygame_gui's UIManager object
This makes it easier to switch screens, work with delegates, etc
This also loads/creates all of the screens up front when booting up the game 
"""
class UIManager:
    def __init__(self):
        self.gui = pygame_gui.UIManager((1080, 1920))
        #Store all of the different game screens in a dict so we can swap to them
        
        self.screens = {
            "mainMenu": MainMenu(self.gui),
            "home": Home(self.gui),
            "ballGame": BallGame(self.gui)
            }
        #Start with the main menu
        self.currentScreen = self.screens["mainMenu"]

        #Hide the other screens that the player doesn't need yet
        self.screens["home"].hide()
        self.screens["ballGame"].hide()

    #Change the current active screen to something else
    def switchScreen(self, newScreen):
        self.currentScreen.hide() #hide old screen
        self.currentScreen = self.screens[newScreen] #todo: add input validation
        self.currentScreen.show() #show new screen

    #Only draw the current active screen selected by the ui manager onto the main game surface
    def draw(self, gameSurface:pygame.Surface):
        #draw the specific game mode graphics
        self.currentScreen.draw(gameSurface) #gameSurface is the one that comes from GM
        #draw the UI from the main game itself
        self.gui.draw_ui(gameSurface)

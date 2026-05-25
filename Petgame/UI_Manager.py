import pygame
import pygame_gui
import Events_System #get all of the global delegates
from UI_Screens import MainMenu, Home, BallGame
from Sunny import Sunny
"""
Acts like a wrapper class for pygame_gui's UIManager object
This makes it easier to switch screens, work with delegates, etc
This also loads/creates all of the screens up front when booting up the game 
"""
class UIManager:
    def __init__(self, pet:Sunny):
        print("Creating UI manager..")
        self.gui = pygame_gui.UIManager((1080, 1920))
        #Store all of the different game screens in a dict so we can swap to them
        
        self.screens = {
            "mainMenu": MainMenu(self.gui),
            "home": Home(self.gui, pet),
            "ballGame": BallGame(self.gui, pet)
            }
        #Start with the main menu
        self.currentScreen = self.screens["mainMenu"]

        #Hide the other screens that the player doesn't need yet
        self.screens["home"].hide()
        self.screens["ballGame"].hide()

        #subscribe to the screen-switching event
        Events_System.on_screen_switch.subscribe(self.switchScreen)
         
    #send the input events collected in the main loop to the correct UI elements
    def readEvents(self, event):
        self.gui.process_events(event)
        self.currentScreen.processEvents(event)

    #Change the current active screen to something else
    def switchScreen(self, newScreen):
        print("switching screen to", newScreen)
        self.currentScreen.hide() #hide old screen
        self.currentScreen = self.screens[newScreen] #todo: add input validation
        self.currentScreen.show() #show new screen

    #Only draw the current active screen selected by the ui manager onto the main game surface
    def draw(self, gameSurface:pygame.Surface):
        #draw the specific game mode graphics

      
        #self.currentScreen.render_background_graphics(gameSurface)#gameSurface is the one that comes from GM
        #draw the UI from the main game itself

        self.gui.draw_ui(gameSurface)
        
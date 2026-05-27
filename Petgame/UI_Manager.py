import pygame
import pygame_gui
import Events_System #get all of the global delegates
from UI_Screens import StatPanel, MainMenu, Home, BallGame, Kitchen
from Sunny import Sunny
"""
Acts like a wrapper class for pygame_gui's UIManager object
This makes it easier to switch screens, work with delegates, etc
-This also loads/creates all of the screens up front when booting up the game 
-This class owns/uses UI_Screens and UI_Component
-Game Manager creates an instance of this class
"""
class UIManager:
    def __init__(self, pet:Sunny, width:int=1920, height:int=1080):
        print("Creating UI manager..")
        self.width = width
        self.height = height
        self.gui = pygame_gui.UIManager((width, height), 'theme.json')
        
        self.screens = {
            "mainMenu": MainMenu(self.gui),
            "home": Home(self.gui, pet),
             "kitchen": Kitchen(self.gui, pet),
            "ballGame": BallGame(self.gui, pet)
            }
        #Start with the main menu
        self.currentScreen = self.screens["mainMenu"]

        #Hide the other screens that the player doesn't need yet
        self.screens["home"].hide()
        self.screens["kitchen"].hide()
        self.screens["ballGame"].hide()

        
        #Make the main sidebar that displays Sunny's stats
        self.sunnyStats = StatPanel(self.gui, pet)
        self.sunnyStats.show()
        self.sunnyStats.hide() #Hide the bar bc we're on the main menu

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
        print(self.currentScreen.name)
        #Only show Sunny's stats if the current screen needs it 
        if self.currentScreen.showStatbar:
            print("showing sunny stats")
            self.sunnyStats.show()
        else: self.sunnyStats.hide()

    #Only draw the current active screen selected by the ui manager onto the main game surface
    def draw(self, gameSurface:pygame.Surface):
        #draw the specific game mode graphics

      
        #self.currentScreen.render_background_graphics(gameSurface)#gameSurface is the one that comes from GM
        #draw the UI from the main game itself

        self.gui.draw_ui(gameSurface)
        
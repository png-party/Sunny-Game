import pygame
import pygame_gui
import pygame_gui.elements as graphics #I dont want to type the whole thing out
import Events_System
from Sunny import Sunny

#A basic parent screen that other types of screens can inherit from
class BasicScreen:
    def __init__(self, uiManager, name:str="Basic Screen", xPosition:float=0, yPosition:float=0, width:float=1080, height:float=1920):
        self.name = name
        #make a rectangle for the position and dimensions of the element
        self.rect = pygame.Rect(xPosition, yPosition, width, height)
        #The container that will group all of the elements
        self.container = pygame_gui.core.UIContainer(relative_rect=self.rect, manager=uiManager)

    def hide(self):
        self.container.hide()
    def show(self):
        self.container.show()

class MainMenu(BasicScreen): #inherit the container,hide, and show from basic screen
    def __init__(self, gui): #gui is the ui manager
        print("Creating main menu screen...")
        super().__init__(gui, "Main menu") #pass the ui manager into the parent constructor
     
        
        self.startButton = graphics.UIButton(relative_rect=pygame.Rect(20,30,400,300),
                                            text="start",
                                            container=self.container,
                                            manager=gui)
        self.sentence = graphics.UILabel(relative_rect=pygame.Rect(0,0, 200,300), 
                                         text="testtest", 
                                         container=self.container, 
                                         manager=gui)
  
                                           
    def processEvents(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.startButton:
                print("Start button clicked")
                Events_System.on_screen_switch.invoke("home")
    

class Home(BasicScreen):
    def __init__(self, gui, pet:Sunny):
        print("Creating home screen...")
        super().__init__(gui, "Home Screen")
        self.foodButton = graphics.UIButton(relative_rect=pygame.Rect(25, 25, 20, 50),
                                            text="Visit kitchen",
                                            container=self.container,
                                            manager=gui)
        self.gameButton = graphics.UIButton(relative_rect=pygame.Rect(75, 75, 20, 50),
                                            text="Play catch",
                                            container=self.container,
                                            manager=gui)
        self.mainMenuButton = graphics.UIButton(relative_rect=pygame.Rect(120, 120, 20, 50),
                                                text="Return to main menu",
                                                container=self.container,
                                                manager=gui)
        self.title = graphics.UITextBox("welcome", 
                                        relative_rect=pygame.Rect(20,30,300,400), 
                                        container=self.container,
                                        manager=gui)
    def processEvents(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.foodButton:
                Events_System.on_screen_switch.invoke("kitchen")
            if event.ui_element == self.gameButton:
                Events_System.on_screen_switch.invoke("ballGame")
            if event.ui_element == self.mainMenuButton:
                Events_System.on_screen_switch.invoke("mainMenu")


class Kitchen(BasicScreen):
    def __init__(self, gui, pet:Sunny):
        print("Creating kitchen...")
        super().__init__(gui, "Kitchen")
        self.title = graphics.UILabel(relative_rect=pygame.Rect(20,30,200,200), 
                                      text="Kitchen",
                                      container=self.container,
                                      manager=gui)
        def processEvents(self, event):
            return ""

class BallGame(BasicScreen):
    def __init__(self, gui, pet:Sunny):
        print("Creating ball game screen...")
        super().__init__(gui, "Ball Game")
        self.pet = pet
        self.title = graphics.UITextBox("ball game", 
                                        relative_rect=pygame.Rect(20,30,300,400), 
                                        manager=gui, 
                                        container=self.container)
    def processEvents(self, events):
        return ""
    def testFunction(self):
        print("ball game")

    def show(self):
        super.show()
        self.pet.on_energyUpdated.subscribe(self.testFunction)

    def hide(self):
        super().hide()
        self.pet.on_energyUpdated.unsubscribe(self.testFunction)



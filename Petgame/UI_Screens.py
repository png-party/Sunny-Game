import pygame
import pygame_gui
import pygame_gui.elements as graphics #I dont want to type the whole thing out
import Events_System
from Sunny import Sunny

#A basic parent screen that other types of screens can inherit from
class BasicScreen:
    def __init__(self, uiManager, 
                 name:str="Basic Screen", 
                 xPosition:float=0, yPosition:float=0, 
                 width:float=1920, height:float=1080,
                 showStatbar:bool=False):
        self.name = name
        
        #make a rectangle for the position and dimensions of the element
        self.rect = pygame.Rect(xPosition, yPosition, width, height)
        #The container that will group all of the elements
        self.container = pygame_gui.core.UIContainer(relative_rect=self.rect, manager=uiManager)
        #Not all screens will show Sunny's stats so you can toggle it off
        self.showStatbar = showStatbar

    def hide(self):
        self.container.hide()
    def show(self):
        self.container.show()

#The side bar that displays Sunny's stats
class StatPanel:
    def __init__(self,gui, pet:Sunny):
        self.pet = pet
        self.barPanel = graphics.UIPanel(relative_rect=pygame.Rect(1520,162,400,756),
                                         starting_height=1,
                                         object_id="statpanel",
                                         manager=gui)
        self.hpLabel = graphics.UILabel(relative_rect=pygame.Rect(10,50,200,50),
                                            text="Health: ",
                                            object_id="statlabel",
                                            container=self.barPanel,
                                            manager=gui)
        self.hpBar = graphics.UIProgressBar(relative_rect=pygame.Rect(10,95,180,40),
                                                  object_id="statbar",
                                                  container=self.barPanel,
                                                  manager=gui)
        self.energyLabel = graphics.UILabel(relative_rect=pygame.Rect(10,160,200,50), 
                                            text="Energy: ",
                                            object_id="statlabel",
                                            container=self.barPanel,
                                            manager=gui)
        self.energyBar = graphics.UIProgressBar(relative_rect=pygame.Rect(10,200,180,40),
                                                  object_id="statbar",
                                                  container=self.barPanel,
                                                  manager=gui)
        self.happinessLabel = graphics.UILabel(relative_rect=pygame.Rect(10,265,200,50),
                                            text="Happiness: ",
                                            object_id="statlabel",
                                            container=self.barPanel,
                                            manager=gui)
        self.happinessBar = graphics.UIProgressBar(relative_rect=pygame.Rect(10,305,180,40),
                                                  object_id="statbar",
                                                  container=self.barPanel,
                                                  manager=gui)
     
        #Get the initial stats
        self.hpBar.set_current_progress(self.pet.health)
        self.energyBar.set_current_progress(self.pet.energy)
        self.happinessBar.set_current_progress(self.pet.happiness)

    def hide(self):
        #unsubscribe when hidden
        print("hiding sunny's stats")
        self.pet.on_hpUpdated.unsubscribe(self.hpBar.set_current_progress)
        self.pet.on_energyUpdated.unsubscribe(self.energyBar.set_current_progress)
        self.pet.on_happinessUpdated.unsubscribe(self.happinessBar.set_current_progress)
        self.barPanel.hide()

    def show(self):
        #subscribe when shown
        print("showing sunny's stats")
        self.pet.on_hpUpdated.subscribe(self.hpBar.set_current_progress)
        self.pet.on_energyUpdated.subscribe(self.energyBar.set_current_progress)
        self.pet.on_happinessUpdated.subscribe(self.happinessBar.set_current_progress)
        self.barPanel.show()
                                   
    def processEvents(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.hpButton:
                print("hp button clicked")
                self.pet.on_hpUpdated.invoke(10)
    


class MainMenu(BasicScreen): #inherit the container,hide, and show from basic screen
    def __init__(self, gui): #gui is the ui manager
        print("Creating main menu screen...")
        super().__init__(gui, "Main menu", showStatbar=False) #pass the ui manager into the parent constructor
     
        
        self.startButton = graphics.UIButton(relative_rect=pygame.Rect(80,108,453,119),
                                            text="start",
                                            object_id="menubutton",
                                            container=self.container,
                                            manager=gui)
        self.sentence = graphics.UILabel(relative_rect=pygame.Rect(80,314, 453,119), 
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
        super().__init__(gui, "Home Screen", showStatbar=True)
        self.pet = pet

        self.foodButton = graphics.UIButton(relative_rect=pygame.Rect(220, 250, 317, 83),
                                            text="Visit kitchen",
                                            object_id="menubutton",
                                            container=self.container,
                                            manager=gui)

        self.gameButton = graphics.UIButton(relative_rect=pygame.Rect(220, 388, 317, 83),
                                            text="Play catch",
                                            object_id="menubutton",
                                            container=self.container,
                                            manager=gui)

        self.mainMenuButton = graphics.UIButton(relative_rect=pygame.Rect(220, 526, 317, 83),
                                            text="Return to main menu",
                                            object_id="menubutton",
                                            container=self.container,
                                            manager=gui)

        self.settingsButton = graphics.UIButton(relative_rect=pygame.Rect(220, 664, 317, 83),
                                            text="Settings",
                                            object_id="menubutton",
                                            container=self.container,
                                            manager=gui)
        self.hpButton = graphics.UIButton(relative_rect=pygame.Rect(10,400,453,119),
                                            text="start",
                                            object_id="menubutton",
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
            if event.ui_element == self.settingsButton:
                str = "todo: fill this in later"
            if event.ui_element == self.hpButton:
                print("hp button clicked")
                self.pet.updateHealth(10)
       

class Kitchen(BasicScreen):
    def __init__(self, gui, pet:Sunny):
        print("Creating kitchen...")
        super().__init__(gui, "Kitchen", showStatbar=True)
        self.title = graphics.UILabel(relative_rect=pygame.Rect(20,30,200,200), 
                                      text="Kitchen",
                                      container=self.container,
                                      manager=gui)
    def processEvents(self, event):
        return ""

class BallGame(BasicScreen):
    def __init__(self, gui, pet:Sunny):
        print("Creating ball game screen...")
        super().__init__(gui, "Ball Game", showStatbar=True)
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



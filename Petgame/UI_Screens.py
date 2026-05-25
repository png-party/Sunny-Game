import pygame
import pygame_gui
import pygame_gui.elements as graphics #I dont want to type the whole thing out

#A basic parent screen that other types of screens can inherit from
class BasicScreen:
    def __init__(self, uiManager, xPosition:float=0, yPosition:float=0, width:float=1080, height:float=1920):
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
        super().__init__(gui) #pass the ui manager into the parent constructor
        self.startButton = graphics.UIButton(relative_rect=pygame.Rect(20,30,400,300),
                                            text="start", 
                                            manager=gui, 
                                            container=self.container)

class Home(BasicScreen):
    def __init__(self, gui):
        super().__init__(gui)
        self.title = graphics.UITextBox("welcome", 
                                        relative_rect=pygame.Rect(20,30,300,400), 
                                        manager=gui, 
                                        container=self.container)

class BallGame(BasicScreen):
    def __init__(self, gui):
        super().__init__(gui)
        self.title = graphics.UITextBox("ball game", 
                                        relative_rect=pygame.Rect(20,30,300,400), 
                                        manager=gui, 
                                        container=self.container)
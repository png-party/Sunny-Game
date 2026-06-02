import pygame
import pygame_gui
import pygame_gui.elements as graphics #I don't want to type the whole thing out
import Events_System
from Sunny import Sunny

"""
A basic parent class that other types of screens can inherit from to create gameplay screens
"""
class BasicScreen:
    def __init__(self, uiManager, scaleFactor:float=1, name:str="Basic Screen", xPosition:float=0, yPosition:float=0, width:float=1920, height:float=1080, showStatbar:bool=False):
        self.name = name
        self.scale = scaleFactor
        #make a rectangle for the position and dimensions of the element
        self.rect = pygame.Rect(xPosition, yPosition, width, height)
        #The container that will group all of the elements
        self.container = pygame_gui.core.UIContainer(relative_rect=self.rect, manager=uiManager)
        #Not all screens will show Sunny's stats so you can toggle it off
        self.showStatbar = showStatbar

    def hide(self):
        print("hiding", self.name)
        self.container.hide()
    def show(self):
        print("showing", self.name)
        self.container.show()


"""
This class creates the UI component for displaying Sunny's stats
Depending on the current screen, it may or may not be shown
"""
class StatPanel:
    def __init__(self,gui, pet:Sunny, scaleFactor:float=1):
        self.gui = gui
        self.scale = scaleFactor
        self.pet = pet
        print("x:", self.gui.window_resolution[0], "y:", self.gui.window_resolution[1])
        self.barPanel = graphics.UIPanel(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.8626*self.scale, self.gui.window_resolution[1]*0.0810*self.scale, self.gui.window_resolution[0]*0.2604*self.scale, self.gui.window_resolution[1]*0.8750*self.scale),
                                         starting_height=1,
                                         object_id="statpanel",
                                         manager=gui)
        self.hpLabel = graphics.UILabel(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.0065*self.scale, self.gui.window_resolution[1]*0.0579*self.scale, self.gui.window_resolution[0]*0.1302*self.scale, self.gui.window_resolution[1]*0.0579*self.scale),
                                            text="Health: ",
                                            object_id="statlabel",
                                            container=self.barPanel,
                                            manager=gui)
        self.hpBar = graphics.UIProgressBar(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.0065*self.scale, self.gui.window_resolution[1]*0.1100*self.scale, self.gui.window_resolution[0]*0.1172*self.scale, self.gui.window_resolution[1]*0.0463*self.scale),
                                            object_id="hpbar",
                                            container=self.barPanel,
                                            manager=gui)
        self.energyLabel = graphics.UILabel(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.0065*self.scale, self.gui.window_resolution[1]*0.1852*self.scale, self.gui.window_resolution[0]*0.1302*self.scale, self.gui.window_resolution[1]*0.0579*self.scale),
                                            text="Energy: ",
                                            object_id="statlabel",
                                            container=self.barPanel,
                                            manager=gui)
        self.energyBar = graphics.UIProgressBar(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.0065*self.scale, self.gui.window_resolution[1]*0.2315*self.scale, self.gui.window_resolution[0]*0.1172*self.scale, self.gui.window_resolution[1]*0.0463*self.scale),
                                            object_id="energybar",
                                            container=self.barPanel,
                                            manager=gui)
        self.happinessLabel = graphics.UILabel(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.0065*self.scale, self.gui.window_resolution[1]*0.3067*self.scale, self.gui.window_resolution[0]*0.1302*self.scale, self.gui.window_resolution[1]*0.0579*self.scale),
                                            text="Happiness: ",
                                            object_id="statlabel",
                                            container=self.barPanel,
                                            manager=gui)
        self.happinessBar = graphics.UIProgressBar(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.0065*self.scale, self.gui.window_resolution[1]*0.3530*self.scale, self.gui.window_resolution[0]*0.1172*self.scale, self.gui.window_resolution[1]*0.0463*self.scale),
                                            object_id="happinessbar",
                                            container=self.barPanel,
                                            manager=gui)
     
        #Get the initial stats and update the bars to match
        self.hpBar.set_current_progress(self.pet.health)
        self.energyBar.set_current_progress(self.pet.energy)
        self.happinessBar.set_current_progress(self.pet.happiness)

    def hide(self):
        #Unsubscribe from stat delegates when hidden
        print("hiding sunny's stats")
        self.pet.on_hpUpdated.unsubscribe(self.hpBar.set_current_progress)
        self.pet.on_energyUpdated.unsubscribe(self.energyBar.set_current_progress)
        self.pet.on_happinessUpdated.unsubscribe(self.happinessBar.set_current_progress)

        self.barPanel.hide()

    def show(self):
        #Subscribe to stat delegates when shown
        self.pet.on_hpUpdated.subscribe(self.hpBar.set_current_progress)
        self.pet.on_energyUpdated.subscribe(self.energyBar.set_current_progress)
        self.pet.on_happinessUpdated.subscribe(self.happinessBar.set_current_progress)

        self.barPanel.show()

class MainMenu(BasicScreen): #inherit the container,hide, and show from basic screen
    def __init__(self, gui, scaleFactor:float=1): #gui is the ui manager
        self.gui = gui
        print("Creating main menu screen...")
        super().__init__(gui, scaleFactor,"Main menu", showStatbar=False) #pass the ui manager into the parent constructor

        #Getting the main menu background
        menuImage = pygame.image.load("Assets/Images/Sunny Game with logo.png")
        #Resizing it to fit the monitor
        backgroundImage = pygame.transform.smoothscale(menuImage, (self.gui.window_resolution[0], self.gui.window_resolution[1]))
        #Make a ui image element using it
        self.menuBG = graphics.UIImage(relative_rect=pygame.Rect(0,0,self.gui.window_resolution[0],self.gui.window_resolution[1]),
                                            image_surface=backgroundImage,
                                            container=self.container,
                                            manager=gui)       

        self.menuBG.change_layer(0) #make sure the background is behind all the other ui elements
        self.startButton = graphics.UIButton(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.4297*self.scale, self.gui.window_resolution[1]*0.6134*self.scale, self.gui.window_resolution[0]*0.1497*self.scale, self.gui.window_resolution[1]*0.1157*self.scale),
                                            text="Start Game",
                                            object_id="menubutton",
                                            container=self.container,
                                            manager=gui)

                                           
    def processEvents(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.startButton:
                print("Start button clicked")
                Events_System.on_screen_switch.invoke("kitchen")

"""
This class creates the kitchen screen with the game mode that lets you feed Sunny
"""
class Kitchen(BasicScreen):
    def __init__(self, gui, pet:Sunny, scaleFactor:float=1):
        print("Creating kitchen...")
        super().__init__(gui, scaleFactor, "Kitchen", showStatbar=True)
        self.gui = gui
        self.scale = scaleFactor
        self.pet = pet
        self.foodList= [] #List for all of the food items in the inventory,
        self.currentFood = 0 #index for the current food item being displayed
        self.currentFoodEaten = 1 #show the eaten or uneaten version of the food
    
        #Adding kitchen background
        backgroundImage = pygame.image.load("Assets/Images/kitchen.png")
        self.kitchenBG = graphics.UIImage(relative_rect=pygame.Rect(0,0,self.gui.window_resolution[0]*self.scale,self.gui.window_resolution[1]*self.scale),
                                            image_surface=backgroundImage,
                                            container=self.container,
                                            manager=gui)       
        self.kitchenBG.change_layer(0) #make sure the background is behind all the other ui elements
        
        self.menuBackButton = graphics.UIButton(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.0195*self.scale, self.gui.window_resolution[1]*0.0174*self.scale, self.gui.window_resolution[0]*0.1562*self.scale, self.gui.window_resolution[1]*0.0833*self.scale),
                                            text="Return home",
                                            object_id="menuarrowbutton",
                                            container=self.container,
                                            manager=gui)
        
        backIcon = pygame.image.load("Assets/Images/sunnybackbutton.png").convert_alpha()
        self.menuBackButtonIcon = graphics.UIImage(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.0293*self.scale, self.gui.window_resolution[1]*0.0347*self.scale, self.gui.window_resolution[0]*0.0260*self.scale, self.gui.window_resolution[1]*0.0463*self.scale),
                                           image_surface=backIcon,
                                           container=self.container,
                                           manager=gui)

        #Making a light blue rectangle to sit behind the UI
        feedMenuBG = pygame.Surface((self.gui.window_resolution[0]*0.2670*self.scale, self.gui.window_resolution[1]*0.4051*self.scale), pygame.SRCALPHA)
        feedMenuBG.fill((173, 216, 230, 150)) 
        self.menuBG = graphics.UIImage(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.1953*self.scale, self.gui.window_resolution[1]*0.6134*self.scale, self.gui.window_resolution[0]*0.2669*self.scale, self.gui.window_resolution[1]*0.4051*self.scale),
                                        image_surface = feedMenuBG,
                                        container=self.container,
                                        manager=gui)

        #Adding the buttons to click through the foods
        self.foodForwardButton = graphics.UIButton(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.4036*self.scale, self.gui.window_resolution[1]*0.9144*self.scale, self.gui.window_resolution[0]*0.0456*self.scale, self.gui.window_resolution[1]*0.0810*self.scale),
                                            text="",
                                            object_id="foodarrowbutton",
                                            container=self.container,
                                            manager=gui)
        foodForwardIcon = pygame.image.load("Assets/Images/feedforward.png").convert_alpha()
        self.foodForwardIcon = graphics.UIImage(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.4121*self.scale, self.gui.window_resolution[1]*0.9259*self.scale, self.gui.window_resolution[0]*0.0326*self.scale, self.gui.window_resolution[1]*0.0579*self.scale),
                                             image_surface=foodForwardIcon,
                                             container=self.container,  
                                             manager=gui)

        self.feedButton = graphics.UIButton(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.2734*self.scale, self.gui.window_resolution[1]*0.9144*self.scale, self.gui.window_resolution[0]*0.1107*self.scale, self.gui.window_resolution[1]*0.0810*self.scale),
                                            text="Feed",
                                            object_id="foodarrowbutton",
                                            container=self.container,
                                            manager=gui)

        self.foodBackButton = graphics.UIButton(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.2083*self.scale, self.gui.window_resolution[1]*0.9144*self.scale, self.gui.window_resolution[0]*0.0456*self.scale, self.gui.window_resolution[1]*0.0810*self.scale),
                                            text="",
                                            object_id="foodarrowbutton",
                                            container=self.container,
                                            manager=gui)

        foodBackIcon = pygame.image.load("Assets/Images/feedbackward.png").convert_alpha()
        self.foodBackwardIcon = graphics.UIImage(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.2148*self.scale, self.gui.window_resolution[1]*0.9259*self.scale, self.gui.window_resolution[0]*0.0326*self.scale, self.gui.window_resolution[1]*0.0579*self.scale),
                                            image_surface=foodBackIcon,
                                            container=self.container,  
                                            manager=gui)
        #Adding sunny graphic into the game
        sunnyPicture = pygame.image.load("Assets/Images/sunny sit.png").convert_alpha()
        self.sunnyIcon = graphics.UIImage(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.4883*self.scale, self.gui.window_resolution[1]*0.2662*self.scale, self.gui.window_resolution[0]*0.3906*self.scale, self.gui.window_resolution[1]*0.8102*self.scale),
                                           image_surface=sunnyPicture,
                                           container=self.container,
                                           manager=gui)
        self.updateFoodList(gui) #Get the list of food names from the food dictionary and make icons

    def show(self):
        self.container.show()
        self.showFood()
        #Avoid showing all of the other food assets when switching screens

        for item in self.foodList:
            item[1].hide()
            item[2].hide()
            item[3].hide()

        self.currentFood = 0 #Reset the index to 0 so it starts on the first food item
        self.currentFoodEaten = 1

        self.showFood()
    """
    This creates the UI images for all the food items
    """
    def updateFoodList(self, gui):
        for key in self.pet.foodInventory:
            #Customize the image path based on each key and create a graphic
            foodIcon = pygame.image.load(f"Assets/Images/{key}.png")
            foodIconEaten = pygame.image.load(f"Assets/Images/{key} fed.png").convert_alpha()
            foodIconGrey = pygame.transform.grayscale(foodIcon)
           
            foodIconUI = graphics.UIImage(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.2734*self.scale,self.gui.window_resolution[1]*0.6366*self.scale,self.gui.window_resolution[0]*0.130*self.scale,self.gui.window_resolution[1]*0.2314*self.scale),
                                          image_surface=foodIcon.convert_alpha(),
                                          container=self.container,
                                          manager=gui)

            foodIconEatenUI = graphics.UIImage(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.2734*self.scale,self.gui.window_resolution[1]*0.6366*self.scale,self.gui.window_resolution[0]*0.130*self.scale,self.gui.window_resolution[1]*0.2314*self.scale),
                                          image_surface=foodIconEaten,
                                          container=self.container,
                                          manager=gui)

            foodIconGreyUI = graphics.UIImage(relative_rect=pygame.Rect(self.gui.window_resolution[0]*0.2734*self.scale,self.gui.window_resolution[1]*0.6366*self.scale,self.gui.window_resolution[0]*0.130*self.scale,self.gui.window_resolution[1]*0.2314*self.scale),
                                          image_surface=foodIconGrey.convert_alpha(),
                                          container=self.container,
                                          manager=gui)

            #Hide the food graphics we just created
            foodIconUI.hide()
            foodIconEatenUI.hide()
            foodIconGreyUI.hide()
            self.foodList.append([key, foodIconUI, foodIconEatenUI, foodIconGreyUI])

    #Controls the back button for the food inventory UI
    def goBack(self):
        self.foodList[self.currentFood][self.currentFoodEaten].hide() #Hide the old graphic
        self.currentFoodEaten = 1 #todo: update this 
        self.currentFood = (self.currentFood - 1) % len(self.foodList)
   
        print("Backward:", self.currentFood,":",self.currentFoodEaten, ", ", self.foodList[self.currentFood][0])
        self.showFood()

    #Controls the forward button for the food inventory UI
    def goForward(self):
        self.foodList[self.currentFood][self.currentFoodEaten].hide() #hide the old graphic
        self.currentFoodEaten = 1 #todo: update this 
        self.currentFood = (self.currentFood + 1) % len(self.foodList)
        print("Forward:", self.currentFood,":",self.currentFoodEaten, ", ", self.foodList[self.currentFood][0])

        self.showFood()
    #This lets you feed Sunny, updating his stats and the graphic being displayed
    def eatFood(self):
        foodName = self.foodList[self.currentFood][0]
        foodItem = self.pet.foodInventory.get(foodName)
        foodAmount = foodItem[1]
        if foodAmount > 0 and self.currentFoodEaten != 3:
            self.pet.Feed(foodName)
            self.foodList[self.currentFood][self.currentFoodEaten].hide() #hide the old uneaten graphic
            self.currentFoodEaten = 2 #show the eaten version
            print("Eating:", self.currentFood,":",self.currentFoodEaten, ", ", self.foodList[self.currentFood][0])
        
        else:  
            print("Could not eat:", self.currentFood,":",self.currentFoodEaten, ", ", self.foodList[self.currentFood][0])
            self.currentFoodEaten = 3 #Make sure we're showing the grey version
        self.showFood()

    #Display the current food item and the correct version (normal, eaten, grey) on screen
    def showFood(self):
        foodItem = self.pet.foodInventory.get(self.foodList[self.currentFood][0])
        foodAmount = foodItem[1]
        if foodAmount <= 0: self.currentFoodEaten = 3 #Show the greyscale version of the food if we ran out
        #Hide all previous potential versions
        self.foodList[self.currentFood][1].hide() #normal
        self.foodList[self.currentFood][2].hide() #eaten/fed
        self.foodList[self.currentFood][3].hide() #greyed out

        print("Showing:", self.currentFood,":",self.currentFoodEaten, ", ", self.foodList[self.currentFood][0])

        self.foodList[self.currentFood][self.currentFoodEaten].show()

    def processEvents(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
           if event.ui_element == self.foodForwardButton:
                self.goForward()
           if event.ui_element == self.feedButton:
                self.eatFood()
           if event.ui_element == self.foodBackButton:
                self.goBack()
           if event.ui_element == self.menuBackButton:
                Events_System.on_screen_switch.invoke("mainMenu")


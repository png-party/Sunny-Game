import pygame
import pygame_gui
import pygame_gui.elements as graphics #I dont want to type the whole thing out
import Events_System
from Sunny import Sunny

#A basic parent screen that other types of screens can inherit from
class BasicScreen:
    def __init__(self, uiManager, name:str="Basic Screen", xPosition:float=0, yPosition:float=0, width:float=1920, height:float=1080, showStatbar:bool=False):
        self.name = name
        
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


#The side bar that displays Sunny's stats
class StatPanel:
    def __init__(self,gui, pet:Sunny):
        self.pet = pet
        self.barPanel = graphics.UIPanel(relative_rect=pygame.Rect(1325,70,400,756),
                                         starting_height=1,
                                         object_id="statpanel",
                                         manager=gui)
        self.hpLabel = graphics.UILabel(relative_rect=pygame.Rect(10,50,200,50),
                                            text="Health: ",
                                            object_id="statlabel",
                                            container=self.barPanel,
                                            manager=gui)
        self.hpBar = graphics.UIProgressBar(relative_rect=pygame.Rect(10,95,180,40),
                                            object_id="hpbar",
                                            container=self.barPanel,
                                            manager=gui)
        self.energyLabel = graphics.UILabel(relative_rect=pygame.Rect(10,160,200,50), 
                                            text="Energy: ",
                                            object_id="statlabel",
                                            container=self.barPanel,
                                            manager=gui)
        self.energyBar = graphics.UIProgressBar(relative_rect=pygame.Rect(10,200,180,40),
                                            object_id="energybar",
                                            container=self.barPanel,
                                            manager=gui)
        self.happinessLabel = graphics.UILabel(relative_rect=pygame.Rect(10,265,200,50),
                                            text="Happiness: ",
                                            object_id="statlabel",
                                            container=self.barPanel,
                                            manager=gui)
        self.happinessBar = graphics.UIProgressBar(relative_rect=pygame.Rect(10,305,180,40),
                                            object_id="happinessbar",
                                            container=self.barPanel,
                                            manager=gui)
     
        #Get the initial stats and update the bars to match
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
        return ""

class MainMenu(BasicScreen): #inherit the container,hide, and show from basic screen
    def __init__(self, gui): #gui is the ui manager
        self.gui = gui
        print("Creating main menu screen...")
        super().__init__(gui, "Main menu", showStatbar=False) #pass the ui manager into the parent constructor

        #Getting the main menu background
        menuImage = pygame.image.load("Assets/Images/Sunny Game with logo.png")
        #resizing it to fit the monitor
        backgroundImage = pygame.transform.smoothscale(menuImage, (self.gui.window_resolution[0], self.gui.window_resolution[1]))
        #make a ui image element using it 
        self.menuBG = graphics.UIImage(relative_rect=pygame.Rect(0,0,self.gui.window_resolution[0],self.gui.window_resolution[1]),
                                            image_surface=backgroundImage,
                                            container=self.container,
                                            manager=gui)       

        self.menuBG.change_layer(0) #make sure the background is behind all the other ui elements
        self.startButton = graphics.UIButton(relative_rect=pygame.Rect(660,530,230,100),
                                            text="Start Game",
                                            object_id="menubutton",
                                            container=self.container,
                                            manager=gui)
                                           
    def processEvents(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.startButton:
                print("Start button clicked")
                Events_System.on_screen_switch.invoke("kitchen")
    

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
                                            text="hp",
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
            if event.ui_element == self.hpButton: #todo: delete this later
                print("hp button clicked")
                self.pet.updateHealth(10)
       

class Kitchen(BasicScreen):
    def __init__(self, gui, pet:Sunny):
        print("Creating kitchen...")
        super().__init__(gui, "Kitchen", showStatbar=True)
        self.gui = gui #todo: remove this and switch to using a panel to display food
        self.pet = pet
        self.foodList= [] #List for all of the food items in the inventory, gets populated when the screen is shown
        self.currentFood = 0 #index for the current food item being displayed
        self.currentFoodEaten = 1 #show the eaten or uneaten version of the food
    
        #Adding kitchen background
        backgroundImage = pygame.image.load("Assets/Images/kitchen.png")
        self.kitchenBG = graphics.UIImage(relative_rect=pygame.Rect(0,0,self.gui.window_resolution[0],self.gui.window_resolution[1]),
                                            image_surface=backgroundImage,
                                            container=self.container,
                                            manager=gui)       
        self.kitchenBG.change_layer(0) #make sure the background is behind all the other ui elements
        
        self.menuBackButton = graphics.UIButton(relative_rect=pygame.Rect(30, 15, 240, 72),
                                            text="Return home",
                                            object_id="menuarrowbutton",
                                            container=self.container,
                                            manager=gui)
        
        backIcon = pygame.image.load("Assets/Images/sunnybackbutton.png").convert_alpha()
        self.menuBackButtonIcon = graphics.UIImage(relative_rect=pygame.Rect(45, 30, 40, 40),
                                           image_surface=backIcon,
                                           container=self.container,
                                           manager=gui)

        #Making a light blue rectangle to sit behind the UI
        feedMenuBG = pygame.Surface((410, 350), pygame.SRCALPHA)
        feedMenuBG.fill((173, 216, 230, 150)) 
        self.menuBG = graphics.UIImage(relative_rect=pygame.Rect(300,530,410,350),
                                        image_surface = feedMenuBG,
                                        container=self.container,
                                        manager=gui)
        #Adding the buttons to click through the foods

        self.foodForwardButton = graphics.UIButton(relative_rect=pygame.Rect(620, 790, 70, 70),
                                            text="",
                                            object_id="foodarrowbutton",
                                            container=self.container,
                                            manager=gui)
        foodForwardIcon = pygame.image.load("Assets/Images/feedforward.png").convert_alpha()
        self.foodForwardIcon = graphics.UIImage(relative_rect=pygame.Rect(633, 800, 50, 50),
                                             image_surface=foodForwardIcon,
                                             container=self.container,  
                                             manager=gui)

        self.feedButton = graphics.UIButton(relative_rect=pygame.Rect(420, 790, 170, 70),
                                            text="Feed",
                                            object_id="foodarrowbutton",
                                            container=self.container,
                                            manager=gui)

        self.foodBackButton = graphics.UIButton(relative_rect=pygame.Rect(320, 790, 70, 70),
                                            text="",
                                            object_id="foodarrowbutton",
                                            container=self.container,
                                            manager=gui)

        foodBackIcon = pygame.image.load("Assets/Images/feedbackward.png").convert_alpha()
        self.foodBackwardIcon = graphics.UIImage(relative_rect=pygame.Rect(330, 800, 50, 50),
                                            image_surface=foodBackIcon,
                                            container=self.container,  
                                            manager=gui) 
        #Adding sunny into the game
        sunnypicture = pygame.image.load("Assets/Images/sunny sit.png").convert_alpha()
        self.sunnyIcon = graphics.UIImage(relative_rect=pygame.Rect(750,230,600,700),
                                           image_surface=sunnypicture,
                                           container=self.container,
                                           manager=gui)
        self.updateFoodList(gui) #Get the list of food names from the food dictionary and make icons

        #foodStats, foodItem[0].name, amount + str(fooditem[1]) 1325
    
        self.foodStatsText = graphics.UITextBox(relative_rect=pygame.Rect(1345, 450,185,650), 
                                            html_text="Food Name",
                                            wrap_to_height=True,
                                            object_id="foodlabel",
                                            container=self.container)

   

    def show(self):
        self.container.show()
        self.showFood()
        
        for item in self.foodList:
            item[1].hide()
            item[2].hide()
            item[3].hide()

        self.currentFood = 0 #reset the index to 0 so it starts on the first food item
        self.currentFoodEaten = 1

        self.showFood()

    def updateFoodList(self, gui):
        for key in self.pet.foodInventory: #key is the food name
            #Customize the image path based on each key and create a graphic
            foodIcon = pygame.image.load(f"Assets/Images/{key}.png")
            foodIconEaten = pygame.image.load(f"Assets/Images/{key} fed.png").convert_alpha()
            foodIconGrey = pygame.transform.grayscale(foodIcon)
           
            foodIconUI = graphics.UIImage(relative_rect=pygame.Rect(420,550,200,200),
                                          image_surface=foodIcon.convert_alpha(),
                                          container=self.container,
                                          manager=gui)

            foodIconEatenUI = graphics.UIImage(relative_rect=pygame.Rect(420,550,200,200),
                                          image_surface=foodIconEaten,
                                          container=self.container,
                                          manager=gui)

            foodIconGreyUI = graphics.UIImage(relative_rect=pygame.Rect(420,550,200,200),
                                          image_surface=foodIconGrey.convert_alpha(),
                                          container=self.container,
                                          manager=gui)

            #Hide the food graphics we just created
            foodIconUI.hide()
            foodIconEatenUI.hide()
            foodIconGreyUI.hide()
            self.foodList.append([key, foodIconUI, foodIconEatenUI, foodIconGreyUI])
    
    def goBack(self):
        self.foodList[self.currentFood][self.currentFoodEaten].hide() #hide the old graphic
        self.currentFoodEaten = 1 #todo: update this 
        self.currentFood = (self.currentFood - 1) % len(self.foodList)
   
        print("Backward:", self.currentFood,":",self.currentFoodEaten, ", ", self.foodList[self.currentFood][0])
        self.showFood()
       
    def goForward(self):
        self.foodList[self.currentFood][self.currentFoodEaten].hide() #hide the old graphic
        self.currentFoodEaten = 1 #todo: update this 
        self.currentFood = (self.currentFood + 1) % len(self.foodList)
        print("Forward:", self.currentFood,":",self.currentFoodEaten, ", ", self.foodList[self.currentFood][0])

        self.showFood()

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

    def showFood(self):
        
        foodItem = self.pet.foodInventory.get(self.foodList[self.currentFood][0])
        foodStats = str(foodItem[0])
        foodAmount = foodItem[1]
     
        self.foodStatsText.set_text(foodStats)
        self.foodStatsText.append_html_text("\nAmount: " + str(foodAmount))
        if foodAmount <= 0: self.currentFoodEaten = 3 #show the greyscale version of the food if we ran out
        #hide all previous potential versions
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



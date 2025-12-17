import pygame, sys, os, time, ButtonManager
from ScreensManager import Screen as Display, ScreenManager
from Elements import Button, Label
import ScreenElements as ElementsManager

pygame.init()
Clock = pygame.time.Clock()
Screen = pygame.display.set_mode((1280, 720))

def CreateScreens():
    Manager = ScreenManager()
    MainMenu = ElementsManager.MainMenu()
    SimParameters = ElementsManager.SimParameters()
    SimViewPort = ElementsManager.SimViewPort()
    Manager.AddScreens(MainMenu, SimParameters, SimViewPort)
    return Manager

def MainLoop():
    global Screen
    Manager = CreateScreens()
    Manager.SetDisplay(Screen)
    Manager.SetScreen('MainMenu')
    Running = True 
    
    while Running:        

        Manager.GetMouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        FuncName, FuncCalled = Manager.UpdateScreen()
        if FuncCalled:
            print(f'Function Called - {FuncName}')
            getattr(ButtonManager, FuncName)(Manager)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # os.system('clear')
                print(Manager.GetAgentStats())
                print()
                print(Manager.GetSpatialData())
                print(Manager.CollectParameters())
                pygame.quit()
                sys.exit()  
        pygame.display.update()
        Clock.tick(60)
#variable to count no. of ticks passed. Inrement ticks, check variable amount for dayamount etc.
if __name__ == '__main__':
    MainLoop()
    

# matplotlib, random seeds add to top later
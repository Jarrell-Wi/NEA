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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.system('clear')
                pygame.quit()
                sys.exit()
            FuncName, FuncCalled = Manager.UpdateScreen()
            if FuncCalled:
                print(f'Function Called - {FuncName}')
                getattr(ButtonManager, FuncName)(Manager)
        Clock.tick(120)

if __name__ == '__main__':
    MainLoop()
    

# matplotlib, random seeds add to top later
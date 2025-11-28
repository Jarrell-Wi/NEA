import pygame, sys, os
from ScreensManager import ScreenManager as Manager

def Slide():
    return
def Start(Manager):
    Manager.SetScreen('SimParameters')
    Manager.UpdateScreen()

def GoBack(Manager):
    Manager.SetScreen(Manager.Previous)
    Manager.UpdateScreen()

def StartSim(Manager):
    Manager.CollectParameters()
    Manager.SetScreen('SimViewPort')
    Manager.UpdateScreen()
    Manager.PrepareSim()

def Quit(Manager):
    os.system('clear')
    pygame.quit()
    sys.exit()
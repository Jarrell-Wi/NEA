import pygame, sys, os
from ScreensManager import ScreenManager as Manager

def Start(Manager):
    Manager.SetScreen('SimParameters')
    Manager.UpdateScreen()

def GoBack(Manager):
    Manager.SetScreen(Manager.Previous)
    Manager.UpdateScreen()

def StartSim(Manager):
    Manager.CollectParameters()
    Manager.PrepareSim()
    Manager.SetScreen('SimViewPort')
    Manager.UpdateScreen()

def Quit(Manager):
    #os.system('clear')
    pygame.quit()
    sys.exit()
import pygame
from ScreensManager import Screen
from Elements import Label, Button, Slider, Tile
from Agents import AgentManager

AssetsPath = 'Main/Assets/'
SlideButtonImage = pygame.transform.scale(pygame.image.load(f'{AssetsPath}SlideButton.png'), (45,45))
SliderImage = pygame.transform.scale(pygame.image.load(f'{AssetsPath}SliderImage.png'), (200, 25))
ButtonImage =  pygame.transform.scale(pygame.image.load(f'{AssetsPath}ButtonImage.png'), (256, 144))
BackButtonImage = pygame.transform.scale(pygame.image.load(f'{AssetsPath}BackButton.png'), (120, 120))
ButtonImageWide = pygame.transform.scale(pygame.image.load(f'{AssetsPath}ButtonImage.png'), (272, 144))
ViewPortBg = pygame.transform.scale(pygame.image.load(f'{AssetsPath}ViewPortBg.png'), (880, 660))

def MainMenu():
    Menu = Screen('MainMenu', (48, 48, 48))
    Title = Label(640, 180, 'Hunters Vs Runners')
    Start = Button(ButtonImage, 640, 400, 'Start', 'Start')
    Quit = Button(ButtonImage, 640, 600, 'Quit', 'Quit')
    Menu.AddElements(Title, Start, Quit)
    return Menu

def SimParameters():
    SimParameters = Screen('SimParameters', (48, 48, 48))
    Title = Label(640, 180, 'Select Simulation Parameters')

    AgentCount = Slider(SliderImage, SlideButtonImage, 200, 200, '', 'Slide')
    

    Start = Button(ButtonImageWide, 640, 600, 'Start Simulation', 'StartSim')
    Back = Button(BackButtonImage, 120, 120, '<-', 'GoBack')

    Back.SetHoverColour('red')

    SimParameters.AddElements(Title, Start, Back, AgentCount)
    return SimParameters

def SimViewPort():
    SimViewPort = Screen('SimViewPort', (48, 48, 48))
    Viewport = Tile(ViewPortBg, 480, 360)
    SimViewPort.AddElements(Viewport)
    return SimViewPort
import pygame
from Agents import AgentManager

class Screen:
    def __init__(self, Name, Colour):
        self.Name = Name
        self.Colour = Colour
        self.Elements = []

    def DrawElements(self, MousePos, MouseInp, Screen):
        Pressed = None
        Called = False
        MouseLeft = MouseInp[0]
        Screen.fill(self.Colour)
        for Element in self.Elements:
            if Element.Type == 'Button':
                if Element.Hover(MousePos) and MouseLeft:
                    print(MousePos)
                    print(Element.Func)
                    Pressed = Element.Func
                    Called = True
            elif Element.Type == 'Slider':
                if Element.Hover(MousePos) and MouseLeft:
                    print('Pressed Slider')
                    Element.UpdateSlidePos(MousePos)
            Element.Update(Screen)
        return Pressed, Called
    
    def AddElements(self, *args):
        for i in args:
            self.Elements.append(i)

    def CollectParameters(self):
        Parameters = {}
        # have dict with {ParameterName: Val for each element in parameter set screen}
        for Element in self.Elements:
            if Element.Parameterised:
                Parameters = Element.GiveParameter(Parameters)
        return Parameters
class ScreenManager:
    def __init__(self):
# here += Viweport mangaer only render when screen set to sim
        self.ViewportManager = AgentManager()

        self.Screens = {}

        self.Current = None
        self.Previous = None
        
        self.MousePos = None
        self.MouseInp = None
        self.Display = None

    def GetSpatialData(self):
        return self.ViewportManager.GetSpatialData()
    
    def CollectParameters(self):
        self.Parameters = self.Screens[self.Current].CollectParameters()
        self.Parameters['Bounds'] = ((80, 880), (60, 660))
        self.Parameters['Screen'] = self.Display
    
    def GetAgentStats(self):
        return self.ViewportManager.GetAgentStats()
    def UpdateScreen(self):
        FuncName, Called = self.Screens[self.Current].DrawElements(self.MousePos, self.MouseInp, self.Display)
        if self.Current == 'SimViewPort':
            self.ViewportManager.Update(self.Display)
        return FuncName, Called

    def PrepareSim(self):
        print(self.Parameters)
        self.ViewportManager.PrepareSim(self.Parameters)
        return
    
    def SetScreen(self, ScreenName):
       if ScreenName in self.Screens:
            self.Previous = self.Current
            self.Current = ScreenName
    
    def AddScreens(self, *args):
        for i in args:
            self.Screens[i.Name] = i
        print(self.Screens)
    
    def GetMouse(self, Mousepos, MouseInp):
        self.MousePos = Mousepos
        self.MouseInp = MouseInp
    
    def SetDisplay(self, Screen):
        self.Display = Screen

    

        
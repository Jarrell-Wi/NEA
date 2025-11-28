import pygame
import sys
pygame.init()
Font = pygame.font.SysFont('comic sans ms', 50)

class Tile:
    def __init__(self, Image, XPos, YPos):
        self.Type = 'Tile'
        self.Parameterised = False
        self.XPos = XPos
        self.YPos = YPos
        self.Image = Image
        self.ImageRect = self.Image.get_rect(center = (self.XPos, self.YPos))
    
    def Update(self, Screen):
        Screen.blit(self.Image, self.ImageRect)

class Label:
    def __init__(self, XPos, YPos, TextInp):
        self.Type = 'Label'
        self.Parameterised = False
        self.XPos = XPos
        self.YPos = YPos
        self.TextInp = TextInp
        self.Text = Font.render(self.TextInp, True, 'white')
        self.TextRect = self.Text.get_rect(center = (self.XPos, self.YPos))

    def Update(self, Screen):
        Screen.blit(self.Text, self.TextRect)
        
class Button(Label):
    def __init__(self, Image, XPos, YPos, TextInp, Func):
        super().__init__(XPos, YPos, TextInp)
        self.Func = Func
        self.Type = 'Button'
        self.ButtonImage = Image
        self.ButtonRect = self.ButtonImage.get_rect(center = (self.XPos, self.YPos))
        self.HoverColour = 'green'
    
    def SetHoverColour(self, Colour):
        self.HoverColour = Colour

    def Update(self, Screen):
        Screen.blit(self.ButtonImage, self.ButtonRect)
        Screen.blit(self.Text, self.TextRect)
    
    def Hover(self, Pos):
        if Pos[0] in range(self.ButtonRect.left, self.ButtonRect.right) and Pos[1] in range(self.ButtonRect.top, self.ButtonRect.bottom):
            self.Text = Font.render(self.TextInp, True, self.HoverColour)
            return True
        self.Text = Font.render(self.TextInp, True, 'white')
        return False

class Slider(Button):
    def __init__(self, SlideImage, ButtonImage, XPos, YPos, TextInp, Func):
        super().__init__(ButtonImage, XPos, YPos, TextInp, Func)
        self.Type = 'Slider'
        self.Parameterised = True
        
        self.XRight = XPos - 100
        self.XLeft = XPos + 100
        self.SlideX = XPos
        self.SlideY = YPos
        self.SlideImage = SlideImage
        self.SlideRect = self.SlideImage.get_rect(center = (self.SlideX, self.SlideY))

        self.Min = 20
        self.ButtonIncrement = self.Min
        self.Increment = 20
        self.ButtonRect = self.ButtonImage.get_rect(center = (self.XRight, self.SlideY))
        self.Dragging = False
        self.PrevMouseLeft = 0

    
    def GetIncrement(self):
        return self.Increment()

    def SetMin(self, Min):
        self.Min = Min

    def SetIncrement(self, Increment):
        self.Increment = Increment

    def Update(self, Screen):
        self.Text = str(self.ButtonIncrement)
        self.Text = Font.render(self.Text, True, 'white')
        self.TextRect = self.Text.get_rect(center = (self.SlideX, self.SlideY + 40))
        Screen.blit(self.SlideImage, self.SlideRect)
        Screen.blit(self.ButtonImage, self.ButtonRect)        
        Screen.blit(self.Text, self.TextRect)

    def Hover(self, Pos):
        if Pos[0] in range(self.ButtonRect.left, self.ButtonRect.right) and Pos[1] in range(self.ButtonRect.top, self.ButtonRect.bottom):
            return True
        return False

    def UpdateSlidePos(self, MousePos):
        XPos = MousePos[0]
        while XPos % self.Increment != 0:
            if XPos > self.XLeft:
                XPos = self.XLeft
            elif XPos < self.XRight:
                XPos = self.XRight
            else:
                XPos -= 1
        self.ButtonIncrement = self.Min +((XPos - self.XRight) // self.Increment)
        
        self.XPos = XPos
        self.ButtonRect = self.ButtonImage.get_rect(center = (self.XPos, self.YPos))


                
    
    

import random, pygame

def StatCurve(self, Min, Max, Power = 2.2):
    Factor = random.random() ** Power
    return Min + (Max - Min) * Factor

class AgentManager:
    def __init__(self):
        self.Type = 'AgentManager'
        self.Runners = []
        self.Hunters = []
        self.SpawnCoords = None
        self.SpawnStyle = 'Random'
        self.XBounds = None
        self.YBounds = None
        
    def Update(self, Screen):
        self.UpdateAgents(Screen)

    def UpdateAgents(self, Screen):
        for Runner in self.Runners:
            Runner.Update(Screen)
        for Hunter in self.Hunters:
            Hunter.Update(Screen)
    
    def MoveAgents(self, Screen):
        for Runner in self.Runners:
            Runner.Move()
        for Hunter in self.Hunters:
            Hunter.Move()

    def GenerateSpawns(self):
        Coords = []
        for i in range(len(self.Hunters) + len(self.Runners)):
            Unique = False
            while not Unique:
                Coordinate = (random.randint(self.XBounds[0], self.XBounds[1]), random.randint(self.YBounds[0], self.YBounds[1]))
                if Coordinate not in Coords:
                    Unique = True
            Coords.append(Coordinate)
        self.SpawnCoords = Coords

    def SpawnAgents(self, Screen):
        for Index, Coordinate in enumerate(self.SpawnCoords):
            if Index < len(self.Hunters):
                self.Hunters[Index].SetPos(Coordinate[0], Coordinate[1])
            else:
                self.Runners[Index - len(self.Hunters)].SetPos(Coordinate[0], Coordinate[1])
            
    def SetBounds(self, XBounds, YBounds):
        self.XBounds = XBounds
        self.YBounds = YBounds

    def ApplyBounds(self):
        for Runner in self.Runners:
            Runner.SetBounds(self.XBounds, self.YBounds)

        for Hunter in self.Hunters:
            Hunter.SetBounds(self.XBounds, self.YBounds)

    def SetSpawnStyle(self, Style):
        self.SpawnStyle = Style

    def GenerateHunters(self, BatchSize):
        for i in range(BatchSize):
            TempHold = Hunter()
            self.Hunters.append(TempHold)

    def GenerateRunners(self, BatchSize):
        for i in range(BatchSize):
            TempHold = Runner()
            self.Runners.append(TempHold)

class Agent:
    def __init__(self):
        self.XBounds = None
        self.YBounds = None
        self.XPos = None
        self.YPos = None

        self.Speed = None
        self.MoveCost = None

        self.Sight = 20
        self.DetectRange = None

        self.AttackRange = None
        self.AttackCost = None

        self.StaminaMax = None
        self.StaminaRegen = None
        self.ExhaustPoint = None
        self.ExhaustSpeed = None

def GenerateAttributes(self):
    Speed = StatCurve(5, 15)
    self.Sight = StatCurve(10, 40)
    
    self.Speed = max(2, Speed -((self.Sight - 25) * 0.05))
    self.MoveCost = 1 + (self.Speed ** 2) * 0.01

    self.DetectRange = self.Sight * 2
    self.AttackRange = self.Sight * 0.4
    self.AttackCost = 3 + (self.Speed * 0.4)

    self.StaminaMax = max(30, 80 + (self.Sight * 1.5) - (self.Speed * 2))
    self.Stamina = self.StaminaMax
    self.StaminaRegen = 0.4 + (self.Sight / 100)
    self.ExhaustPoint = self.StaminaMax * 0.2
    self.ExhaustSpeed = max(1.5, self.Speed * 0.5)

    def SetPos(self, XPos, YPos):
        self.XPos = XPos
        self.YPos = YPos

    def Update(self, Screen):#
        pygame.draw.circle(Screen, pygame.color('gray'), (self.XPos, self.YPos), round(self.Sight))
        pygame.draw.circle(Screen, self.Colour, (self.XPos, self.YPos), 10)

    def Scan(self, Screen):
        pass

    def Move(self):
        XNotValid = True
        YNotValid = True
        while XNotValid or YNotValid:
            if XNotValid:
                NewXPos = self.XPos + random.randint(-self.Speed, self.Speed)
                if NewXPos >= self.XBounds[0] and NewXPos <= self.XBounds[1]:
                    XNotValid = False
                    self.XPos = NewXPos
            if YNotValid:
                NewYPos = self.YPos + random.randint(-self.Speed, self.Speed)
                if NewYPos >= self.YBounds[0] and NewYPos <= self.YBounds[1]:
                    YNotValid = False   
                    self.YPos = NewYPos    


    def SetBounds(self, XBounds, YBounds):
        self.XBounds = XBounds
        self.YBounds = YBounds

class Hunter(Agent):
    def __init__(self):
        super().__init__()
        self.Type = 'Hunter'
        self.Colour = (215, 0, 64)
        self.Damage = 0
        self.Kills = 0
        self.ChaseTime = 0
    
class Runner(Agent):
    def __init__(self):
        super().__init__()
        self.Type = 'Runner'
        self.Colour = (124, 252, 0)
        self.Health = 0
        self.SurvivalTime = 0
        self.RushSpeed = 0
        self.Panicked = False
    



 
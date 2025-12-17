import math, random, pygame
pygame.init()

class AgentManager:
    def __init__(self):
        self.Type = 'AgentManager'
        self.Runners = []
        self.Hunters = []
        self.SpawnCoords = None
        self.SpawnStyle = 'Random'
        self.XBounds = None
        self.YBounds = None
        self._CellSize = None
        self._Grid = None
    
    def GetSpatialData(self):
        return self._Grid
    def BuildSpatialIndex(self, CellSize=40):
        self._CellSize = CellSize
        self._Grid = {}

        def Key(X, Y):
            return (X // self._CellSize, Y // self._CellSize)
        
        for Agent in self.Hunters + self.Runners:
            XPos, YPos = Agent.GetPos()
            XCell, YCell = Key(XPos, YPos)
            self._Grid.setdefault((XCell, YCell), []).append(Agent)
        
    def QueryNearby(self, XPos, YPos, Radius):
        if not self._CellSize:
            self.BuildSpatialIndex()
        CellSize = self._CellSize
        MinCellX = (XPos - Radius) // CellSize
        MaxCellX = (XPos + Radius) // CellSize
        MinCellY = (YPos - Radius) // CellSize
        MaxCellY = (YPos + Radius) // CellSize
        Candidates = []
        for CellX in range(int(MinCellX), int(MaxCellX)+ 1):
            for CellY in range(int(MinCellY), int(MaxCellY) +  1):
                CellSet = self._Grid.get((CellX, CellY), [])
                for Agent in CellSet:
                    Candidates.append((Agent, getattr(Agent, 'Type', None)))
        return Candidates

    def PrepareSim(self, Parameters):
        Bounds = Parameters['Bounds']
        self.XBounds, self.YBounds = Bounds[0], Bounds[1]
        print('Bounded')
        self.GenerateHunters(Parameters['HunterCount'])
        print('HuntersGenerated')
        self.GenerateRunners(Parameters['RunnerCount'])
        print('RunnersGenerated')
        self.ApplyBounds()
        print('BoundsApplied')
        self.GenerateSpawns()
        print('Spawns Generated')
        self.SpawnAgents(Parameters['Screen'])
        print('Agents Spawned')

    def Update(self, Screen):
        self.MoveAgents(Screen)
        self.UpdateAgents(Screen)

    def UpdateAgents(self, Screen):
        for Runner in self.Runners:
            Runner.UpdateSight(self)
            Runner.RenderSight(Screen)
        for Hunter in self.Hunters:
            Hunter.UpdateSight(self)
            Hunter.RenderSight(Screen)
        for Hunter in self.Hunters:
            Hunter.RenderAgent(Screen)
        for Runner in self.Runners:
            Runner.RenderAgent(Screen)
    
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

    def SetSpawnStyle(self, Style):
        self.SpawnStyle = Style

    def ApplyBounds(self):
        for Runner in self.Runners:
            Runner.SetBounds(self.XBounds, self.YBounds)

        for Hunter in self.Hunters:
            Hunter.SetBounds(self.XBounds, self.YBounds)

    def GenerateHunters(self, BatchSize):
        for i in range(BatchSize):
            TempHold = Hunter()
            TempHold.GenerateAttributes()
            self.Hunters.append(TempHold)

    def GenerateRunners(self, BatchSize):
        for i in range(BatchSize):
            TempHold = Runner()
            TempHold.GenerateAttributes()
            self.Runners.append(TempHold)
    
    def GetAgentStats(self):
        HunterData = ['Hunters']
        for Hunter in self.Hunters:
            HunterData.append(Hunter.GiveStats())
        RunnerData = ['Runners']
        for Runner in self.Runners:
            RunnerData.append(Runner.GiveStats())
        return (HunterData, RunnerData)

class Agent:
    def __init__(self):
        self.Type = None
        self.XBounds = None
        self.YBounds = None
        self.XPos = None
        self.YPos = None

        self.Speed = None
        self.MoveCost = None

        self.Sight = None
        self.DetectRange = None

        self.AttackRange = None
        self.AttackCost = None

        self.StaminaMax = None
        self.StaminaRegen = None
        self.ExhaustPoint = None
        self.ExhaustSpeed = None

        self.VisibleHunters = []
        self.VisibleRunners = []
        self.DetectedNearby = False

    def DetectNearby(self, Manager, DetectRadius):
        Nearby = Manager.QueryNearby(self.XPos, self.YPos, DetectRadius)
        RadiusSquare = DetectRadius * DetectRadius
        for Agent, AgentType in Nearby:
            if Agent is self:
                continue
            DeltaX = Agent.XPos - self.XPos
            DeltaY = Agent.YPos - self.YPos
            if (DeltaX * DeltaX) + (DeltaY * DeltaY) <= RadiusSquare:
                self.DetectedNearby = True
                return True
        self.DetectedNearby = False
        return False
    
    def UpdateSight(self, Manager):
        self.VisibleHunters.clear()
        self.VisibleRunners.clear()
        SightRnd = int(round(self.Sight))
        SightSquare = SightRnd * SightRnd
        InSight = Manager.QueryNearby(self.XPos, self.YPos, SightRnd)
        for Agent, AgentType in InSight:
            if Agent is self:
                continue
            DeltaX = Agent.XPos - self. XPos
            DeltaY = Agent.YPos - self.YPos
            if (DeltaX * DeltaX) + (DeltaY * DeltaY) <= SightSquare:
                if AgentType == 'Hunter':
                    self.VisibleHunters.append(Agent)
                elif AgentType == 'Runner':
                    self.VisibleRunners.append(Agent)
                
    def GetType(self):
        return self.Type
    
    def StatCurve(self, Min, Max, Power = 2.2):
        Factor = random.random() ** Power
        return Min + (Max - Min) * Factor
    
    def GetPos(self):
        return self.XPos, self.YPos
    
    def SetPos(self, XPos, YPos):
        self.XPos, self.YPos = XPos, YPos


    def GiveStats(self):
        return [self.Speed, self.Sight]
    
    def GenerateAttributes(self):
        Speed = self.StatCurve(5, 15)
        self.Sight = self.StatCurve(10, 40)
        
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

    def RenderSight(self, Screen):
        pygame.draw.circle(Screen, (128, 128, 128), (self.XPos, self.YPos), int(round(self.Sight)))

    def RenderAgent(self, Screen):
        pygame.draw.circle(Screen, (self.Colour), (self.XPos, self.YPos), (int(round(self.Sight)) * 0.35) )

    def Scan(self, Screen):
        pass

    def Move(self):
        XNotValid = True
        YNotValid = True
        while XNotValid or YNotValid:
            if XNotValid:
                NewXPos = self.XPos + random.randint(-int(round(self.Speed)), int(round((self.Speed))))
                if NewXPos >= self.XBounds[0] and NewXPos <= self.XBounds[1]:
                    XNotValid = False
                    self.XPos = NewXPos
            if YNotValid:
                NewYPos = self.YPos + random.randint(-int(round(self.Speed)), int(round((self.Speed))))
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




 
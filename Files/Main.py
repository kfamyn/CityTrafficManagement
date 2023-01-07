from tkinter import *
from tkinter import ttk
from random import randint
import time
import colorsys
from base import *
import copy

class Car:
    def __init__(self, object, path, MoveVector):
        self.object = object
        self.path = path
        self.MoveVector = MoveVector
        
class Edge:
    def __init__(self, object, path, NodePath):
        self.object = object
        self.path = path
        self.NodePath = NodePath

class Node:
    def __init__(self, object, CarCount):
        self.object = object
        self.CarCount = CarCount

class TrafficLight:
    def __init__(self, object, path, mode, NodePath):
        self.object = object
        self.path = path
        self.mode = mode
        self.NodePath = NodePath

def CountToColor(Count):
    if Count > 20:
        NewColor = "#e60000"
    else:
        OldColor = colorsys.hsv_to_rgb((100 - Count * 5)/360, 1, 0.9)
        NewColor = [0] * 3
        for j in range(3):
            NewColor[j] = str(hex(round(OldColor[j] * 255)))[2:]
            if len(NewColor[j]) == 1:
                NewColor[j] = "0" + NewColor[j]
        NewColor = "#" + NewColor[0] + NewColor[1] + NewColor[2]
    return NewColor

def GraphToGraph(Graph):
    GraphCopy = []
    for i in range(len(Graph)):
        GraphCopy.append([])
        for j in range(len(Graph[i])):
            if Graph[i][j] > 0:
                GraphCopy[i].append(j)
    return GraphCopy

def CheckMatrix(Graph):
    Graph = GraphToGraph(Graph)
    visited = [False] * len(Graph)
    CheckNode(0, visited, Graph)
    if len(Graph) == visited.count(True):
        result = True
    else:
        result = False
    return result

def CheckNode(Node, visited, Graph):
    visited[Node] = True
    for Node2 in Graph[Node]:
        if not visited[Node2]:
            CheckNode(Node2, visited, Graph)

def CreatePath(path, CreatePathMode):
    global CityGraph
    global Nodes
    CopyCityGraph = copy.deepcopy(CityGraph)
    if CreatePathMode == 'Optimise':
        for i in range(len(CopyCityGraph)):
            for j in range(len(CopyCityGraph)):
                if CopyCityGraph[i][j] != 0:
                    CopyCityGraph[i][j] += int(canvas.itemconfig(Nodes[j].CarCount)["text"][4]) * 10
                    CopyCityGraph[i][j] += int(canvas.itemconfig(Nodes[i].CarCount)["text"][4]) * 10
    Size = len(CopyCityGraph)
    start = path[0]
    end = path[1]
    Distance = [10000] * Size
    VisitedNodes = [1] * Size
    Distance[start] = 0
    MinIndex = 0
    while MinIndex < 10000:
        MinIndex = 10000
        min = 10000
        for i in range(Size):
            if (VisitedNodes[i] == 1 and Distance[i] < min):
                min = Distance[i]
                MinIndex = i
        if MinIndex != 10000:
            for i in range(Size):
                if (CopyCityGraph[MinIndex][i] > 0):
                    temp = min + CopyCityGraph[MinIndex][i]
                    if temp < Distance[i]:
                        Distance[i] = temp
            VisitedNodes[MinIndex] = 0
    VisitedNodes[0] = end
    k = 1
    weight = Distance[end]
    while (end != start):
        for i in range(Size):
            if (CopyCityGraph[i][end] != 0):
                temp = weight - CopyCityGraph[i][end]
                if (temp == Distance[i]):
                    weight = temp
                    end = i
                    VisitedNodes[k] = i
                    k += 1
    i = k - 1
    path = [0] * k
    j = 0
    while i >= 0:
        path[j] = VisitedNodes[i]
        j += 1
        i -= 1
    return path

def CreateCar(CreateCarMode):
    global Cars
    NewCar = Car(0, [0, 0], [0, 0])
    while NewCar.path[0] == NewCar.path[1]:
        NewCar.path = [randint(0, len(Nodes) - 1), randint(0, len(Nodes) - 1)]
    NewCar.path = CreatePath(NewCar.path, CreateCarMode)
    coords = canvas.coords(Nodes[NewCar.path[0]].object)
    coords[0] += 5
    coords[1] += 5
    coords[2] -= 5
    coords[3] -= 5
    NewCar.object = canvas.create_oval(coords, fill="yellow")
    CarCount = int(canvas.itemconfig(Nodes[NewCar.path[0]].CarCount)["text"][4]) + 1
    canvas.itemconfig(Nodes[NewCar.path[0]].CarCount, text = CarCount)
    Cars.append(NewCar)

def OutInformation(FrameCount, AverageCarCount, AverageMaxCarCount):
    Count = 0
    MaxCount = 0
    for i in range(len(Nodes)):
        Count += int(canvas.itemconfig(Nodes[i].CarCount)['text'][4])
        MaxCount = max(MaxCount, int(canvas.itemconfig(Nodes[i].CarCount)['text'][4]))
    canvas.itemconfig(Information[0], text = str(Count))
    canvas.itemconfig(Information[1], text = str(MaxCount))
    if round(FrameCount) % 60 < 10:
        String = "0"
    else:
        String = ""
    canvas.itemconfig(Information[2], text = str(round(FrameCount) // 60) + ":" + String + str(round(FrameCount) % 60))
    FrameCount = round(FrameCount * 100 / 3) - 1
    if FrameCount > 0:
        AverageCarCount = (AverageCarCount * (FrameCount - 1) + Count) / FrameCount
        AverageMaxCarCount = (AverageMaxCarCount * (FrameCount - 1) + MaxCount) / FrameCount
    canvas.itemconfig(Information[3], text = str(round(AverageCarCount)))
    canvas.itemconfig(Information[4], text = str(round(AverageMaxCarCount)))
    return [AverageCarCount, AverageMaxCarCount]

def DrawPath(path, LineOptions):
    coords = canvas.coords(Nodes[path[0]].object)
    coords[0] += 20
    coords[1] += 20
    coords[2] -= 20
    coords[3] -= 20
    canvas.create_oval(coords, fill="green")
    coords = canvas.coords(Nodes[path[-1]].object)
    coords[0] += 20
    coords[1] += 20
    coords[2] -= 20
    coords[3] -= 20
    canvas.create_oval(coords, fill="green")
    while len(path) > 1:
        PathToDraw = [path[0], path[1]]
        DrawLine(PathToDraw, NodesCoords, canvas, LineOptions)
        path.pop(0)

def DrawTrafficLight(path, TrafficCoords, canvas):
    NewTrafficLight = [0, 0]
    LightTrafficOptions = {
        'fill': 'green',
        'width': 6
    }

    for i in range(4):
        TrafficCoords[i] += 10

    LineVector = [TrafficCoords[2] - TrafficCoords[0], TrafficCoords[3] - TrafficCoords[1]]
    LineLength = (LineVector[0]**2 + LineVector[1]**2)**(1/2)
    LineVector = [LineVector[0] / LineLength, LineVector[1] / LineLength]

    for i in range(2):
        TrafficCoords[i+2] = TrafficCoords[i] + LineVector[i] * 25
    NewTrafficLight[0] = canvas.create_line(TrafficCoords, LightTrafficOptions)

    for i in range(2):
        TrafficCoords[i+2] = TrafficCoords[i] + LineVector[i] * 30

    NewLineVector = [-LineVector[1], LineVector[0]]
    TriangleCoords = [
        TrafficCoords[2],
        TrafficCoords[3], 
        TrafficCoords[2] - LineVector[0] * 10 + NewLineVector[0] * 10, 
        TrafficCoords[3] - LineVector[1] * 10 + NewLineVector[1] * 10,
        TrafficCoords[2] - LineVector[0] * 10 - NewLineVector[0] * 10, 
        TrafficCoords[3] - LineVector[1] * 10 - NewLineVector[1] * 10,
    ]
    NewTrafficLight[1] = canvas.create_polygon(TriangleCoords, LightTrafficOptions)
    
    return NewTrafficLight

def Simulation():
    global Nodes
    global ModeKey
    global CreateCarMode
    global CarSpawnFrequency
    global Box
    i = 0
    FrameCount = 0
    AverageCarCount = 0
    AverageMaxCarCount = 0
    while True:
        FrameCount += 0.03
        if ModeKey == 0:
            Clean()
            break
        FunctionResult = OutInformation(FrameCount, AverageCarCount, AverageMaxCarCount)
        AverageCarCount = FunctionResult[0]
        AverageMaxCarCount = FunctionResult[1]
        if i % CarSpawnFrequency == 0 and len(Cars) < 400:
            CreateCar(CreateCarMode)

        if i % 300 == 0 and i != 0:
            for i in range(len(TrafficLights)):
                TrafficLights[i].mode =  (TrafficLights[i].mode + 1) % 2
                for j in range(2):
                        canvas.itemconfig(TrafficLights[i].object[j], fill = TrafficLightColors[TrafficLights[i].mode])
        for car in Cars:
            car.MoveVector = [canvas.coords(Nodes[car.path[1]].object)[0] - canvas.coords(Nodes[car.path[0]].object)[0], canvas.coords(Nodes[car.path[1]].object)[1] - canvas.coords(Nodes[car.path[0]].object)[1]]
            speed = 0
            if car.MoveVector != (0, 0):
                speed = 1 / (2 * (car.MoveVector[0]**2 + car.MoveVector[1]**2)**(1/2))
            CarCoords = canvas.coords(car.object)
            NodeCoords = canvas.coords(Nodes[car.path[0]].object)
            CarCoords[0] -= 5
            CarCoords[1] -= 5
            CarCoords[2] += 5
            CarCoords[3] += 5
            NodeDistanse = ((CarCoords[0] - NodeCoords[0])**2 + (CarCoords[1] - NodeCoords[1])**2)**(1/2)
            if CarCoords == NodeCoords:
                car.path = [car.path[0], car.path[-1]]
                car.path = CreatePath(car.path, CreateCarMode)
                for TrafficLight in TrafficLights:
                    if TrafficLight.path[0] == car.path[0] and TrafficLight.path[1] == car.path[1]:
                        if TrafficLight.mode == 0:
                            speed = 0
                for car2 in Cars:
                    if car2.path[0:2] == car.path[0:2]:
                        Car2Coords = canvas.coords(car2.object)
                        Car2Coords[0] -= 5
                        Car2Coords[1] -= 5
                        NodeDistanse = ((Car2Coords[0] - NodeCoords[0])**2 + (Car2Coords[1] - NodeCoords[1])**2)**(1/2)
                        if NodeDistanse < 10 and NodeDistanse > 0:
                            speed = 0
                if speed != 0:
                    CarCount = int(canvas.itemconfig(Nodes[car.path[0]].CarCount)["text"][4]) - 1
                    NodeColor = CountToColor(CarCount)
                    canvas.itemconfig(Nodes[car.path[0]].CarCount, fill = NodeColor)
                    canvas.itemconfig(Nodes[car.path[0]].CarCount, text = CarCount)
                    CarCount = int(canvas.itemconfig(Nodes[car.path[1]].CarCount)["text"][4]) + 1
                    NodeColor = CountToColor(CarCount)
                    canvas.itemconfig(Nodes[car.path[1]].CarCount, fill = NodeColor)
                    canvas.itemconfig(Nodes[car.path[1]].CarCount, text = CarCount)
            
            canvas.move(car.object, speed * car.MoveVector[0], speed * car.MoveVector[1])
            CarCoords = [0, 0]
            NodeCoords = [0, 0]
            CarCoords[0] = canvas.coords(car.object)[0] + 5
            CarCoords[1] = canvas.coords(car.object)[1] + 5
            NodeCoords[0] = canvas.coords(Nodes[car.path[1]].object)[0] + 10
            NodeCoords[1] = canvas.coords(Nodes[car.path[1]].object)[1] + 10
            if ((CarCoords[0] - NodeCoords[0])**2 + (CarCoords[1] - NodeCoords[1])**2) ** (1/2) < 1:
                car.path.pop(0)
                NewCoords = canvas.coords(Nodes[car.path[0]].object)
                NewCoords[0] += 5
                NewCoords[1] += 5
                NewCoords[2] -= 5
                NewCoords[3] -= 5
                canvas.coords(car.object, NewCoords)
            if len(car.path) < 2:
                CarCount = int(canvas.itemconfig(Nodes[car.path[0]].CarCount)["text"][4]) - 1
                NodeColor = CountToColor(CarCount)
                canvas.itemconfig(Nodes[car.path[0]].CarCount, text = CarCount)
                canvas.itemconfig(Nodes[car.path[0]].CarCount, fill = NodeColor)
                Cars.remove(car)
                canvas.delete(car.object)
            
        canvas.update()
        i += 1
        time.sleep(0.01)
    
def Clean():
    global Cars
    for car in Cars:
        canvas.delete(car.object)
    Cars = []
    for i in range(len(Nodes)):
        canvas.itemconfig(Nodes[i].CarCount, text = "0")
        canvas.itemconfig(Nodes[i].CarCount, fill = "#4de600")

    canvas.itemconfig(Information[0], text = "0")
    canvas.itemconfig(Information[1], text = "0")
    canvas.itemconfig(Information[2], text = "0:00")
    canvas.itemconfig(Information[3], text = "0")
    canvas.itemconfig(Information[4], text = "0")
    for i in range(len(Edges)):
        canvas.itemconfig(Edges[i].object, fill="black")
    CreateAllMatrix()

def Delete(event, ModeKey):
    global CityModeGraph
    global DefaultCityGraph
    global CityGraph
    EdgeColors = {
        'lightgray': "black",
        'black': "lightgray"
    }
    Edge = 0
    x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    y = canvas.winfo_pointery() - canvas.winfo_rooty()
    for i in range(len(Edges)):
        distance = 1000
        CurrentEdgeCoords = canvas.coords(Edges[i].object)
        A = (CurrentEdgeCoords[3] - CurrentEdgeCoords[1]) / (CurrentEdgeCoords[2] - CurrentEdgeCoords[0])
        B = CurrentEdgeCoords[1] - A * CurrentEdgeCoords[0]
        distance = abs((A * x - 1 * y + B) / (A**2 + 1)**(1/2))
        if i == 0:
            MinDistance = distance
        if distance <= MinDistance and Edges == 0:
            Edge = Edges[i]
            Number = i
            MinDistance = distance
        if ((x >= CurrentEdgeCoords[0]) == (x <= CurrentEdgeCoords[2])) and ((y >= CurrentEdgeCoords[1]) == (y <= CurrentEdgeCoords[3])):
            if distance <= MinDistance:
                Edge = Edges[i]
                Number = i
                MinDistance = distance
    if ModeKey == 0 and Edge != 0 and DeleteMode == 1:
        DeleteEdge(Number)
    if Edge != 0 and ModeKey == 1:
        CityModeGraph[Edge.path[0]][Edge.path[1]] = (CityModeGraph[Edge.path[0]][Edge.path[1]] + 1) % 2
        CityModeGraph[Edge.path[1]][Edge.path[0]] = (CityModeGraph[Edge.path[1]][Edge.path[0]] + 1) % 2
        CopyCityGraph = [[0] * len(Nodes) for i in range(len(Nodes))]
        for i in range(len(Nodes)):
            for j in range(len(Nodes)):
                CopyCityGraph[i][j] = DefaultCityGraph[i][j] * CityModeGraph[i][j]

        if CheckMatrix(CopyCityGraph):
            for i in range(len(Nodes)):
                for j in range(len(Nodes)):
                    CityGraph[i][j] = CopyCityGraph[i][j]
            canvas.itemconfig(Edge.object, fill=EdgeColors[canvas.itemconfig(Edge.object)["fill"][4]])
        else:
            CityModeGraph[Edge.path[0]][Edge.path[1]] = (CityModeGraph[Edge.path[0]][Edge.path[1]] + 1) % 2
            CityModeGraph[Edge.path[1]][Edge.path[0]] = (CityModeGraph[Edge.path[1]][Edge.path[0]] + 1) % 2
        

def ModeButtonClick():
    global ModeKey
    global CityGraph
    global CityModeGraph
    global DefaultCityGraph
    CreateAllMatrix()
    for i in range(len(Nodes)):
            for j in range(len(Nodes)):
                CityGraph[i][j] = DefaultCityGraph[i][j] * CityModeGraph[i][j]

    if ModeKey == 0 and CheckMatrix(CityGraph) and EditMode == 0 and len(Nodes) > 1:
        ModeKey = (ModeKey + 1) % 2
        ModeButton["text"] = "Стоп"
        EditButton.config(state = "disabled")
        
        Simulation()

    elif ModeKey == 1:
        ModeKey = (ModeKey + 1) % 2
        ModeButton["text"] = "Старт"
        EditButton.config(state = "normal")
        Clean()

def CurrentCreateCarMode(event):
    global CreateCarMode
    global Box
    CreateCarModes = {
        'Оптимизированный': 'Optimise',
        'Неоптимизированный': 'NonOptimise'
    }
    CreateCarMode = CreateCarModes[Box.get()]

def CurrentCarSpawnFrequency():
    global CarSpawnFrequency
    FrequenciesMode = {
        'Низкая': 15,
        'Средняя': 7,
        'Высокая': 5
    }
    CarSpawnFrequency = FrequenciesMode[Frequencies.get()]

def CurrentDeleteMode():
    global DeleteMode
    global AddMode
    global LightMode
    DeleteMode = 1
    AddMode = 0
    LightMode = 0

def CurrentAddMode():
    global DeleteMode
    global AddMode
    global LightMode
    global NewLine
    NewLine = [0, 0]
    DeleteMode = 0
    AddMode = 1
    LightMode = 0

def CurrentLightMode():
    global DeleteMode
    global AddMode
    global LightMode
    global NewLight
    NewLight = [0, 0]
    DeleteMode = 0
    AddMode = 0
    LightMode = 1

def CurrentEditMode():
    global EditMode
    global EditWindow1
    global EditWindow2
    global EditWindow3
    global DeleteMode
    global AddMode
    global LightMode
    EditMode = (EditMode + 1) % 2
    if EditMode == 1:
        EditButton.config(text = "Сохранить")
        Delete = "Удалить"
        Add = "Добавить"
        Light = "Светофоры"
        Edit = StringVar()
        FirstEditButton = Radiobutton(
            text = Delete,
            value = Delete, 
            variable = Edit, 
            font = TextFont,
            background = 'gray',
            indicatoron = 0,
            command = CurrentDeleteMode
        )
        FirstEditButton.pack()
        SecondEditButton = Radiobutton(
            text = Add, 
            value = Add, 
            variable = Edit, 
            background = 'gray',
            font = TextFont,
            indicatoron = 0,
            command = CurrentAddMode
        )
        SecondEditButton.pack()
        ThirdEditButton = Radiobutton(
            text = Light, 
            value = Light, 
            variable = Edit, 
            background = 'gray',
            font = TextFont,
            indicatoron = 0,
            command = CurrentLightMode
        )
        ThirdEditButton.pack()
        EditWindow1 = canvas.create_window((WindowX * (300 / 1500), WindowY * (40 / 950)), anchor = "center", window = FirstEditButton)
        EditWindow2 = canvas.create_window((WindowX * (450 / 1500), WindowY * (40 / 950)), anchor = "center", window = SecondEditButton)
        EditWindow3 = canvas.create_window((WindowX * (600 / 1500), WindowY * (40 / 950)), anchor = "center", window = ThirdEditButton)
    
    else:
        DeleteMode = 0
        AddMode = 0
        LightMode = 0
        EditButton.config(text = "Редактировать")
        canvas.delete(EditWindow1)  
        canvas.delete(EditWindow2) 
        canvas.delete(EditWindow3) 

def CreateAllMatrix():
    global DefaultCityGraph
    global CityModeGraph
    global CityGraph
    CityGraph = [[0] * len(Nodes) for i in range(len(Nodes))]
    CityModeGraph = [[0] * len(Nodes) for i in range(len(Nodes))]
    DefaultCityGraph = [[0] * len(Nodes) for i in range(len(Nodes))]
    for Edge in Edges:
        CityModeGraph[Edge.path[0]][Edge.path[1]] = 1
        CityModeGraph[Edge.path[1]][Edge.path[0]] = 1
    for i in range(len(Nodes)):
        for j in range(i + 1, len(Nodes)):
            if Nodes[i] != 0 and Nodes[j] != 0:
                FirstCoords = [
                    int(round(canvas.coords(Nodes[i].object)[0] + canvas.coords(Nodes[i].object)[2]) / 2),
                    int(round(canvas.coords(Nodes[i].object)[1] + canvas.coords(Nodes[i].object)[3]) / 2)
                ]
                SecondCoords = [
                    int(round(canvas.coords(Nodes[j].object)[0] + canvas.coords(Nodes[j].object)[2]) / 2),
                    int(round(canvas.coords(Nodes[j].object)[1] + canvas.coords(Nodes[j].object)[3]) / 2)
                ]
                distance = int(round(((SecondCoords[0] - FirstCoords[0])**2 + (SecondCoords[1] - FirstCoords[1])**2)**(1/2)))
                DefaultCityGraph[i][j] = distance * CityModeGraph[i][j]
                DefaultCityGraph[j][i] = distance * CityModeGraph[j][i]

def CreateNode(Coords):
    global Nodes
    global NewLine
    NewNode = Node(0, 0)
    NewNode.object = DrawPoint(Coords, canvas)
    NewNode.CarCount = DrawCarCount(NewNode, canvas)
    Nodes.append(NewNode)

def DeleteNode(Number):
    canvas.delete(Nodes[Number].object)
    canvas.delete(Nodes[Number].CarCount)
    NumbersToDelete = []
    for i in range(len(Edges)):
        if Edges[i].path[0] == Number or Edges[i].path[1] == Number:
            NumbersToDelete.append(i)
    for i in NumbersToDelete:
        DeleteEdge(i)
        for j in range(len(NumbersToDelete)):
            NumbersToDelete[j] -= 1
    Nodes.pop(Number)

def CreateEdge(path):
    NewEdge = Edge(0, 0, 0)
    NewEdge.path = path
    NewEdge.NodePath = (Nodes[path[0]], Nodes[path[1]])
    NewEdgeCoords = [
        canvas.coords(Nodes[path[0]].object)[0] + 10,
        canvas.coords(Nodes[path[0]].object)[1] + 10,
        canvas.coords(Nodes[path[1]].object)[0] + 10,
        canvas.coords(Nodes[path[1]].object)[1] + 10
    ]
    NewEdge.object = DrawLine(NewEdgeCoords, canvas)
    Edges.append(NewEdge)
    canvas.tag_bind(Edges[len(Edges) - 1].object, '<Button>', lambda event: Delete(event, ModeKey))

def DeleteEdge(Number):
    canvas.delete(Edges[Number].object)
    NumbersToDelete = []
    path = Edges[Number].path
    for i in range(len(TrafficLights)):
        if (path[0] == TrafficLights[i].path[0] and path[1] == TrafficLights[i].path[1]) or (path[0] == TrafficLights[i].path[1] and path[1] == TrafficLights[i].path[0]):
            NumbersToDelete.append(i)
    for i in NumbersToDelete:
        for j in range(len(NumbersToDelete)):
            NumbersToDelete[j] -= 1
        DeleteTrafficLight(i)
    Edges.pop(Number)

def CreateTrafficLight(path):
    NewTrafficLight = TrafficLight(0, 0, 0, 0)
    NewTrafficLight.path = path
    NewTrafficLight.NodePath = (Nodes[path[0]], Nodes[path[1]])
    NewTrafficLight.mode = 1
    TrafficCoords = canvas.coords(Nodes[path[0]].object)[0:2] + canvas.coords(Nodes[path[1]].object)[0:2]
    NewTrafficLight.object = DrawTrafficLight(path, TrafficCoords, canvas)
    for j in range(2):
        canvas.itemconfig(NewTrafficLight.object[j], fill = TrafficLightColors[NewTrafficLight.mode])
    TrafficLights.append(NewTrafficLight)

def DeleteTrafficLight(Number):
    canvas.delete(TrafficLights[Number].object[0])
    canvas.delete(TrafficLights[Number].object[1])
    TrafficLights.pop(Number)

def EditEvents(event):
    global NewLine
    global NewLight
    x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    y = canvas.winfo_pointery() - canvas.winfo_rooty()
    if (x >= 40 and x <= 1010 and y >= 90 and y <= 890):
        NewNodeCoords = [
            x - 10,
            y - 10,
            x + 10,
            y + 10
        ]
        if AddMode == 1:
            CreateNode(NewNodeCoords)
            if len(canvas.find_overlapping(NewNodeCoords[0] - 5, NewNodeCoords[1] - 5, NewNodeCoords[2] + 5, NewNodeCoords[3] + 5)) > 2:
                DeleteNode(len(Nodes) - 1)
            else:
                NewLine = [0, 0]
            for i in range(len(Nodes)):
                if Nodes[i] != 0:
                    NodeCoords = [
                        canvas.coords(Nodes[i].object)[0] + 10,
                        canvas.coords(Nodes[i].object)[1] + 10
                    ]
                    distance = ((NodeCoords[0] - x)**2 + (NodeCoords[1] - y)**2)**(1/2)
                    if distance <= 15:
                        if NewLine[0] == 0:
                            NewLine[0] = i
                        elif NewLine[1] == 0 and NewLine[0] != i:
                            NewLine[1] = i
                            flag = 1
                            for j in range(len(Edges)):
                                if Edges[j].path[0] == NewLine[0] and Edges[j].path[1] == NewLine[1] or Edges[j].path[0] == NewLine[1] and Edges[j].path[1] == NewLine[0]:
                                    flag = 0
                            if flag == 1:
                                CreateEdge(NewLine)
                                NewLine = [0, 0]     
                            else:
                                NewLine = [NewLine[1], 0] 
        if DeleteMode == 1:
            NumberToDelete = -1
            for i in range(len(Nodes)):
                if Nodes[i] != 0:
                    NodeCoords = [
                        canvas.coords(Nodes[i].object)[0] + 10,
                        canvas.coords(Nodes[i].object)[1] + 10
                    ]
                    distance = ((NodeCoords[0] - x)**2 + (NodeCoords[1] - y)**2)**(1/2)
                    if distance <= 15:
                        NumberToDelete = i
            if NumberToDelete != -1:
                DeleteNode(NumberToDelete)
            while i < len(TrafficLights):
                TriangleCoords = canvas.coords(TrafficLights[i].object[1])
                CenterCoords = [
                    (TriangleCoords[0] + TriangleCoords[2] + TriangleCoords[4]) / 3,
                    (TriangleCoords[1] + TriangleCoords[3] + TriangleCoords[5]) / 3
                ]
                FirstPoint = [TriangleCoords[0], TriangleCoords[1]]
                SecondPoint = [TriangleCoords[2], TriangleCoords[3]]
                ThirdPoint = [TriangleCoords[4], TriangleCoords[5]]
                FirstPoint = GoFromCenter(FirstPoint, CenterCoords)
                SecondPoint = GoFromCenter(SecondPoint, CenterCoords)
                ThirdPoint = GoFromCenter(ThirdPoint, CenterCoords)
                TriangleCoords = FirstPoint + SecondPoint + ThirdPoint
                if PointInTriangle(TriangleCoords, x, y):
                    DeleteTrafficLight(i)
                i += 1

        if LightMode == 1:
            for i in range(len(Nodes)):
                if Nodes[i] != 0:
                    NodeCoords = [
                        canvas.coords(Nodes[i].object)[0] + 10,
                        canvas.coords(Nodes[i].object)[1] + 10
                    ]
                    distance = ((NodeCoords[0] - x)**2 + (NodeCoords[1] - y)**2)**(1/2)
                    if distance <= 15:
                        if NewLight[0] == 0:
                            NewLight[0] = i
                        elif NewLight[1] == 0 and NewLight[0] != i:
                            NewLight[1] = i
                            flag = 0
                            Path1 = (NewLight[0], NewLight[1])
                            Path2 = (NewLight[1], NewLight[0])
                            for j in range(len(Edges)):
                                if Edges[j].path == Path1 or Edges[j].path == Path2:
                                    flag = 1
                            for j in range(len(TrafficLights)):
                                if TrafficLights[j].path == Path1:
                                    flag = 0
                            if flag == 1:
                                CreateTrafficLight(NewLight)
                                NewLight = [0, 0]
                            else:
                                NewLight = [NewLight[1], 0]

            for i in range(len(TrafficLights)):
                TriangleCoords = canvas.coords(TrafficLights[i].object[1])
                CenterCoords = [
                    (TriangleCoords[0] + TriangleCoords[2] + TriangleCoords[4]) / 3,
                    (TriangleCoords[1] + TriangleCoords[3] + TriangleCoords[5]) / 3
                ]
                FirstPoint = [TriangleCoords[0], TriangleCoords[1]]
                SecondPoint = [TriangleCoords[2], TriangleCoords[3]]
                ThirdPoint = [TriangleCoords[4], TriangleCoords[5]]
                FirstPoint = GoFromCenter(FirstPoint, CenterCoords)
                SecondPoint = GoFromCenter(SecondPoint, CenterCoords)
                ThirdPoint = GoFromCenter(ThirdPoint, CenterCoords)
                TriangleCoords = FirstPoint + SecondPoint + ThirdPoint
                if PointInTriangle(TriangleCoords, x, y):
                    TrafficLights[i].mode = (TrafficLights[i].mode + 1) % 2
                    for j in range(2):
                        canvas.itemconfig(TrafficLights[i].object[j], fill = TrafficLightColors[TrafficLights[i].mode])
        UpdatePath()
    
def UpdatePath():
    for i in range(len(Edges)):
        Edges[i].path = NodePathToPath(Edges[i].NodePath, Nodes, canvas)
    for i in range(len(TrafficLights)):
        TrafficLights[i].path = NodePathToPath(TrafficLights[i].NodePath, Nodes, canvas)

def GoFromCenter(Point, Center):
    NewPoint = [
        Center[0] + (Point[0] - Center[0]) * 2.5,
        Center[1] + (Point[1] - Center[1]) * 2.5
    ]
    return NewPoint

def PointInTriangle(TriangleCoords, x, y):
    a = [TriangleCoords[0], TriangleCoords[1]]
    b = [TriangleCoords[2], TriangleCoords[3]]
    c = [TriangleCoords[4], TriangleCoords[5]]
    p = [x, y]
    TriangleArea = GetTriangleArea(a, b, c)
    FirstArea = GetTriangleArea(a, b, p)
    SecondArea = GetTriangleArea(a, p, c)
    ThirdArea = GetTriangleArea(p, b, c)
    if TriangleArea == (FirstArea + SecondArea + ThirdArea):
        return True
    else: return False

def GetTriangleArea(a, b, c):
    return abs((a[0] - c[0]) * (b[1] - c[1]) + (b[0] - c[0]) * (c[1] - a[1]))

def OutputInformation():
    InfoWindow = Tk()
    InfoWindowX = round(InfoWindow.winfo_screenwidth() / 1.5)
    print(InfoWindowX)
    InfoWindowY = round(InfoWindow.winfo_screenheight() / 1.2)
    InfoWindow.geometry("{}x{}".format(InfoWindowX, InfoWindowY))
    InfoCanvas = Canvas(InfoWindow, width=InfoWindowX, height=InfoWindowY, bg='white')
    InfoCanvas.pack()
    InfoFont = ("Arial", round(16 / InfoWindowX * 1280), "bold")
    InformationOptions = {
        'font': InfoFont,
        'text': InfoText,
        'anchor': 'center',
        'fill': 'black'
    }
    """ label = Label(InfoWindow, text = InfoText, font = InfoFont, anchor = 'center', fg='black')
    label.pack() """
    InfoCanvas.create_text(InfoWindowX / 2, InfoWindowY / 2, InformationOptions)

    InfoWindow.mainloop()

if __name__ == "__main__":
    TrafficLightColors = {
        1: 'green',
        0: 'red'
    }
    CreateCarMode = 'Optimise'
    CarSpawnFrequency = 7
    Cars = []
    ModeKey = 0
    EditMode = 0
    DeleteMode = 0
    AddMode = 0
    LightMode = 0
    window = Tk()
    WindowX = round(window.winfo_screenwidth() / 1.28)
    WindowY = round(window.winfo_screenheight() / 1.137)
    TextX = round(WindowX * (1250 / 1500))
    window.title("Main")
    window.geometry("{}x{}".format(WindowX, WindowY))
    canvas = Canvas(window, width=WindowX, height=WindowY - 50, bg='white')
    canvas.pack()
    TextFont = ("Arial", 12, "bold")
    ModeButton = Button(window, text="Старт", font = TextFont, height = 2, width = 10, command=ModeButtonClick)   
    ModeButton.pack()
    TextFont = ("Arial", 16, "bold")
    Box = ttk.Combobox(
        values = ('Оптимизированный', 'Неоптимизированный'),
        state = "readonly",
        justify = "center",
        width = 25,
        font = TextFont
    )
    Box.current(0)
    Box.pack()
    Box.bind("<<ComboboxSelected>>", CurrentCreateCarMode)
    canvas.create_window((TextX, WindowY * (225 / 950)), anchor = "center", window = Box)
    Nodes = [Node(0, 0) for i in range(20)]
    Edges = [Edge(0, 0, 0) for i in range(28)]
    TrafficLights = [TrafficLight(0, 0, 0, 0) for i in range(56)]
    Information = [0, 0, 0, 0, 0]
    
    Low = "Низкая"
    Medium = "Средняя"
    High = "Высокая"
    
    Frequencies = StringVar(value = Medium)
    FirstButton = Radiobutton(
        text = Low,
        value = Low, 
        variable = Frequencies, 
        background = 'gray',
        font = TextFont,
        indicatoron = 0,
        command = CurrentCarSpawnFrequency
    )
    FirstButton.pack()
    SecondButton = Radiobutton(
        text = Medium, 
        value = Medium, 
        variable = Frequencies, 
        background = 'gray',
        font = TextFont,
        indicatoron = 0,
        disabled = "black",
        command = CurrentCarSpawnFrequency
    )
    SecondButton.pack()
    ThirdButton = Radiobutton(
        text = High, 
        value = High,  
        variable = Frequencies, 
        background = 'gray',
        font = TextFont,
        indicatoron = 0,
        command = CurrentCarSpawnFrequency
    )
    ThirdButton.pack()
    canvas.create_window((TextX, WindowY * (70 / 950)), anchor = "center", window = FirstButton)
    canvas.create_window((TextX, WindowY * (110 / 950)), anchor = "center", window = SecondButton)
    canvas.create_window((TextX, WindowY * (150 / 950)), anchor = "center", window = ThirdButton)
    EditButton = Button(
        text = "Редактировать", 
        font = TextFont,
        background = 'gray',
        disabled = "black",
        command = CurrentEditMode
    )
    EditButton.pack()
    canvas.create_window((WindowX * (100 / 1500), WindowY * (40 / 950)), anchor = "center", window = EditButton)
    HelpButton = Button(
        text = "Помощь", 
        font = TextFont,
        background = 'gray',
        disabled = "black",
        command = OutputInformation
    )
    HelpButton.pack()
    canvas.create_window((WindowX * (1000 / 1500), WindowY * (40 / 950)), anchor = "center", window = HelpButton)
    Base(Edges, Nodes, TrafficLights, Information, canvas, WindowX, WindowY)
    CityGraph = [[0] * len(Nodes) for i in range(len(Nodes))]
    CityModeGraph = [[0] * len(Nodes) for i in range(len(Nodes))]
    DefaultCityGraph = [[0] * len(Nodes) for i in range(len(Nodes))]
    CreateAllMatrix()
    for i in range(len(Edges)):
        canvas.tag_bind(Edges[i].object, '<Button>', lambda event: Delete(event, ModeKey))
    canvas.bind('<Button-1>', EditEvents)
    window.mainloop()

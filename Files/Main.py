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
    def __init__(self, object, path):
        self.object = object
        self.path = path

class Node:
    def __init__(self, object, CarCount):
        self.object = object
        self.CarCount = CarCount

class TrafficLight:
    def __init__(self, object, path, mode):
        self.object = object
        self.path = path
        self.mode = mode

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
                    CopyCityGraph[i][j] += int(canvas.itemconfig(Nodes[j].CarCount)["text"][4]) * 5
                    CopyCityGraph[i][j] += int(canvas.itemconfig(Nodes[i].CarCount)["text"][4]) * 5
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
        NewCar.path = [randint(0, 19), randint(0, 19)]
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
        if i % CarSpawnFrequency == 0 and len(Cars) < 500:
            CreateCar(CreateCarMode)

        if i % 150 == 0 and i != 0:
            for i in range(len(TrafficLights)):
                TrafficLights[i].mode += (-1) ** (TrafficLights[i].mode % 2 + 1) 
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
                for TrafficLight in TrafficLights:
                    if TrafficLight.path == car.path[0:2]:
                        if TrafficLight.mode == 2:
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
    for i in range(20):
        canvas.itemconfig(Nodes[i].CarCount, text = "0")
        canvas.itemconfig(Nodes[i].CarCount, fill = "#4de600")
    for i in range(56):
        TrafficLights[i].mode = DefaultTrafficLightMode[i] + 2 * (TrafficLights[i].mode // 3)
        for j in range(2):
                canvas.itemconfig(TrafficLights[i].object[j], fill = TrafficLightColors[TrafficLights[i].mode])
    canvas.itemconfig(Information[0], text = "0")
    canvas.itemconfig(Information[1], text = "0")
    canvas.itemconfig(Information[2], text = "0:00")
    canvas.itemconfig(Information[3], text = "0")
    canvas.itemconfig(Information[4], text = "0")

def Click(Edge, event, ModeKey):
    EdgeColors = {
        'lightgray': "black",
        'black': "lightgray"
    }

    if ModeKey == 0:
        CityModeGraph[Edge.path[0]][Edge.path[1]] = (CityModeGraph[Edge.path[0]][Edge.path[1]] + 1) % 2
        CityModeGraph[Edge.path[1]][Edge.path[0]] = (CityModeGraph[Edge.path[1]][Edge.path[0]] + 1) % 2
        
        for i in range(20):
            for j in range(20):
                CityGraph[i][j] = DefaultCityGraph[i][j] * CityModeGraph[i][j]
        
        if CheckMatrix(CityGraph):
            canvas.itemconfig(Edge.object, fill=EdgeColors[canvas.itemconfig(Edge.object)["fill"][4]])
            for TrafficLight in TrafficLights:
                if Edge.path == TrafficLight.path or Edge.path == TrafficLight.path[::-1]:
                    TrafficLight.mode += 2 * (-1)**(TrafficLight.mode // 3)
                    for i in range(2):
                        canvas.itemconfig(TrafficLight.object[i], fill = TrafficLightColors[TrafficLight.mode])
        else:
            CityModeGraph[Edge.path[0]][Edge.path[1]] = (CityModeGraph[Edge.path[0]][Edge.path[1]] + 1) % 2
            CityModeGraph[Edge.path[1]][Edge.path[0]] = (CityModeGraph[Edge.path[1]][Edge.path[0]] + 1) % 2

def ModeButtonClick():
    global ModeKey
    global CityGraph
    global CityModeGraph
    global DefaultCityGraph

    for i in range(20):
            for j in range(20):
                CityGraph[i][j] = DefaultCityGraph[i][j] * CityModeGraph[i][j]

    if ModeKey == 0:
        ModeKey = (ModeKey + 1) % 2
        ModeButton["text"] = "Стоп"
        
        Simulation()

    elif ModeKey == 1:
        ModeKey = (ModeKey + 1) % 2
        ModeButton["text"] = "Старт"
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

if __name__ == "__main__":
    TrafficLightColors = {
        1: 'green',
        2: 'red',
        3: 'gray',
        4: 'gray'
    }
    CreateCarMode = 'Optimise'
    CarSpawnFrequency = 7
    Cars = []
    ModeKey = 0
    window = Tk()
    WindowX = round(window.winfo_screenwidth() / 1.28)
    WindowY = round(window.winfo_screenheight() / 1.137)
    TextX = round(WindowX * (1250 / 1500))
    window.title("Main")
    window.geometry("{}x{}".format(WindowX, WindowY))
    canvas = Canvas(window, width=WindowX, height=WindowY - 50, bg='white')
    canvas.pack()
    ModeButton = Button(window, text="Старт", height = 2, width = 20, command=ModeButtonClick)   
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
    CityGraph = [[0] * 20 for i in range(20)]
    Nodes = [Node(0, 0) for i in range(20)]
    Edges = [Edge(0, (0, 0)) for i in range(28)]
    TrafficLights = [TrafficLight(0, (0, 0), 0) for i in range(56)]
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
        command = CurrentCarSpawnFrequency)
    SecondButton.pack()
    ThirdButton = Radiobutton(
        text = High, 
        value = High, 
        variable = Frequencies, 
        background = 'gray',
        font = TextFont,
        indicatoron = 0,
        command = CurrentCarSpawnFrequency)
    ThirdButton.pack()
    canvas.create_window((TextX, WindowY * (70 / 950)), anchor = "center", window = FirstButton)
    canvas.create_window((TextX, WindowY * (110 / 950)), anchor = "center", window = SecondButton)
    canvas.create_window((TextX, WindowY * (150 / 950)), anchor = "center", window = ThirdButton)

    Base(Edges, Nodes, TrafficLights, Information, canvas, WindowX, WindowY)
    for i in range(56):
        TrafficLights[i].mode = DefaultTrafficLightMode[i]
        for j in range(2):
            canvas.itemconfig(TrafficLights[i].object[j], fill = TrafficLightColors[TrafficLights[i].mode])

    canvas.tag_bind(Edges[0].object, '<Button>', lambda event: Click(Edges[0], event, ModeKey))
    canvas.tag_bind(Edges[1].object, '<Button>', lambda event: Click(Edges[1], event, ModeKey))
    canvas.tag_bind(Edges[2].object, '<Button>', lambda event: Click(Edges[2], event, ModeKey))
    canvas.tag_bind(Edges[3].object, '<Button>', lambda event: Click(Edges[3], event, ModeKey))
    canvas.tag_bind(Edges[4].object, '<Button>', lambda event: Click(Edges[4], event, ModeKey))
    canvas.tag_bind(Edges[5].object, '<Button>', lambda event: Click(Edges[5], event, ModeKey))
    canvas.tag_bind(Edges[6].object, '<Button>', lambda event: Click(Edges[6], event, ModeKey))
    canvas.tag_bind(Edges[7].object, '<Button>', lambda event: Click(Edges[7], event, ModeKey))
    canvas.tag_bind(Edges[8].object, '<Button>', lambda event: Click(Edges[8], event, ModeKey))
    canvas.tag_bind(Edges[9].object, '<Button>', lambda event: Click(Edges[9], event, ModeKey))
    canvas.tag_bind(Edges[10].object, '<Button>', lambda event: Click(Edges[10], event, ModeKey))
    canvas.tag_bind(Edges[11].object, '<Button>', lambda event: Click(Edges[11], event, ModeKey))
    canvas.tag_bind(Edges[12].object, '<Button>', lambda event: Click(Edges[12], event, ModeKey))
    canvas.tag_bind(Edges[13].object, '<Button>', lambda event: Click(Edges[13], event, ModeKey))
    canvas.tag_bind(Edges[14].object, '<Button>', lambda event: Click(Edges[14], event, ModeKey))
    canvas.tag_bind(Edges[15].object, '<Button>', lambda event: Click(Edges[15], event, ModeKey))
    canvas.tag_bind(Edges[16].object, '<Button>', lambda event: Click(Edges[16], event, ModeKey))
    canvas.tag_bind(Edges[17].object, '<Button>', lambda event: Click(Edges[17], event, ModeKey))
    canvas.tag_bind(Edges[18].object, '<Button>', lambda event: Click(Edges[18], event, ModeKey))
    canvas.tag_bind(Edges[19].object, '<Button>', lambda event: Click(Edges[19], event, ModeKey))
    canvas.tag_bind(Edges[20].object, '<Button>', lambda event: Click(Edges[20], event, ModeKey))
    canvas.tag_bind(Edges[21].object, '<Button>', lambda event: Click(Edges[21], event, ModeKey))
    canvas.tag_bind(Edges[22].object, '<Button>', lambda event: Click(Edges[22], event, ModeKey))
    canvas.tag_bind(Edges[23].object, '<Button>', lambda event: Click(Edges[23], event, ModeKey))
    canvas.tag_bind(Edges[24].object, '<Button>', lambda event: Click(Edges[24], event, ModeKey))
    canvas.tag_bind(Edges[25].object, '<Button>', lambda event: Click(Edges[25], event, ModeKey))
    canvas.tag_bind(Edges[26].object, '<Button>', lambda event: Click(Edges[26], event, ModeKey))
    canvas.tag_bind(Edges[27].object, '<Button>', lambda event: Click(Edges[27], event, ModeKey))

    window.mainloop()

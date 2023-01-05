import tkinter.font as TkFont

NodesCoords = [
        [110, 790, 130, 810],
        [250, 828, 270, 848],
        [400, 868, 420, 888],
        [500, 895, 520, 915],
        [900, 819, 920, 839],
        [1000, 800, 1020, 820],
        [875, 720, 895, 740],
        [500, 650, 520, 670],
        [320, 620, 340, 640],
        [115, 585, 135, 605],
        [70, 480, 90, 500],
        [225, 360, 245, 380],
        [410, 445, 430, 465],
        [560, 485, 580, 505],
        [850, 535, 870, 555],
        [350, 285, 370, 305],
        [480, 210, 500, 230],
        [545, 290, 565, 310],
        [670, 320, 690, 340],
        [810, 325, 830, 345],
    ]

InfoText = """
                                        Общая информация.

Основная цель данной программы – симуляция автомобильного движения в городе. 
Смысл – наглядное сравнение алгоритмов координации автомобильных потоков. 
Наша задача – минимизировать время в пути для всех автомобилистов. 
Все пункты отправления и назначения автомобилей генерируются случайным образом, 
после чего для них рассчитывается маршрут, опираясь на один из алгоритмов:
1) Неоптимизированный: по кратчайшему по расстоянию пути.
2) Оптимизированный: по кратчайшему по времени пути.
Более подробное описание алгоритмов можно найти в приложенной презентации.
Для корректной работы программы необходимо поставить 100% масштаб в Windows.

                                        Рабочая область.

Находится в левой части окна. 
В ней представлены граф (симуляция городских дорог) и кнопки для его настройки, 
которые всплывают при нажатии кнопки «Редактировать».
Добавить – позволяет добавить вершину (нажать в пустой области один раз) 
или добавить дорогу (нажать по одному разу на уже существующие вершины, которые необходимо соединить).
Удалить – позволяет удалить вершину, дорогу или светофор, путем нажатие на них.
Светофор – позволяет добавить светофор или поменять его цвет в начальный момент времени.
При работе со светофорами необходимо нажимать на стрелку светофора(на треугольник).

                                        Информационная область.

Находится в правой части окна. Позволяет настроить параметры симуляции и узнать информацию о ней.
Частота появления машин – параметр, отвечающий за то, с какой интенсивностью появляются автомобили. 
Можно использовать для симуляции разной загруженности дорог.
Алгоритм поиска пути – параметр, определяющий, 
по какому из описанных выше алгоритмов будут строиться маршруты движения автомобилей.
Количество машин – общее количество машин, находящихся в симуляции в данный момент.
Максимальное количество машин в вершине – текущее максимальное количество машин, 
стоящих в какой-либо вершине или едущих в нее по смежной дороге.
Время – количество времени, прошедшего с момента запуска симуляции.
Старт/стоп – запуск/остановка симуляции.
"""
def Base(Edges, Nodes, TrafficLights, Information, canvas, WindowX, WindowY):
    for i in range(len(NodesCoords)):
        NodesCoords[i][1] -= 60
        NodesCoords[i][3] -= 60
        for j in range(4):
            if j == 0: NodesCoords[i][j] = (NodesCoords[i][j] / 1500) * WindowX
            elif j == 1: NodesCoords[i][j] = (NodesCoords[i][j] / 950) * WindowY

    for i in range(len(Nodes)):
        Nodes[i].object = DrawPoint(NodesCoords[i], canvas)
        Nodes[i].CarCount = DrawCarCount(Nodes[i], canvas)
        Nodes[i].Number = i

    EdgesPath = [
        [Nodes[0], Nodes[1]],
        (Nodes[0], Nodes[9]),
        (Nodes[1], Nodes[2]),
        (Nodes[1], Nodes[8]),
        (Nodes[2], Nodes[3]),
        (Nodes[2], Nodes[7]),
        (Nodes[3], Nodes[4]),
        (Nodes[4], Nodes[5]),
        (Nodes[4], Nodes[6]),
        (Nodes[5], Nodes[6]),
        (Nodes[6], Nodes[7]),
        (Nodes[6], Nodes[14]), 
        (Nodes[7], Nodes[8]),
        (Nodes[7], Nodes[13]),
        (Nodes[9], Nodes[8]),
        (Nodes[8], Nodes[11]),
        (Nodes[9], Nodes[10]),
        (Nodes[10], Nodes[11]),
        (Nodes[11], Nodes[15]),
        (Nodes[12], Nodes[13]),
        (Nodes[15], Nodes[12]),
        (Nodes[13], Nodes[14]),
        (Nodes[13], Nodes[18]),
        (Nodes[14], Nodes[19]),
        (Nodes[15], Nodes[16]),
        (Nodes[16], Nodes[17]),
        (Nodes[17], Nodes[18]),
        (Nodes[18], Nodes[19]),
    ]

    DefaultTrafficLightMode = [
        1, 0, 1, 0, 0, 1, 1, 0,
        1, 0, 0, 1, 0, 1, 1, 0,
        0, 1, 0, 0, 0, 0, 1, 0,
        0, 1, 1, 0, 1, 1, 0, 1,
        0, 1, 1, 0, 0, 1, 1, 1,
        0, 1, 1, 1, 0, 1, 0, 1,
        1, 0, 0, 1, 1, 0, 0, 1
    ]
    
    TrafficPath = [
        (0, 1),
        (0, 9),
        (1, 2),
        (1, 8),
        (2, 3),
        (2, 7),
        (3, 4),
        (4, 5),
        (4, 6),
        (5, 6),
        (6, 7),
        (6, 14), 
        (7, 8),
        (7, 13),
        (9, 8),
        (8, 11),
        (9, 10),
        (10, 11),
        (11, 15),
        (12, 13),
        (15, 12),
        (13, 14),
        (13, 18),
        (14, 19),
        (15, 16),
        (16, 17),
        (17, 18),
        (18, 19),
    ]

    TrafficLightColors = {
        1: 'green',
        0: 'red'
    }

    for i in range(len(Edges)):
        Edges[i].NodePath = EdgesPath[i]
        Edges[i].path = NodePathToPath(Edges[i].NodePath, Nodes, canvas)
        Coords = [
            canvas.coords(Edges[i].NodePath[0].object)[0] + 10,
            canvas.coords(Edges[i].NodePath[0].object)[1] + 10,
            canvas.coords(Edges[i].NodePath[1].object)[0] + 10,
            canvas.coords(Edges[i].NodePath[1].object)[1] + 10
        ]
        Edges[i].object = DrawLine(Coords, canvas)

    for i in range(len(TrafficLights)):
        TrafficLights[i].path = TrafficPath[(i // 2)]
        TrafficLights[i].path = [TrafficLights[i].path[0], TrafficLights[i].path[1]]
        if i % 2 == 1:
            TrafficLights[i].path = TrafficLights[i].path[::-1]
        TrafficCoords = NodesCoords[TrafficLights[i].path[0]][0:2] + NodesCoords[TrafficLights[i].path[1]][0:2]
        TrafficLights[i].object = DrawTrafficLight(TrafficLights[i].path, TrafficCoords, canvas)
        TrafficLights[i].mode = DefaultTrafficLightMode[i]
        for j in range(2):
            canvas.itemconfig(TrafficLights[i].object[j], fill = TrafficLightColors[TrafficLights[i].mode])
        TrafficLights[i].NodePath = (Nodes[TrafficLights[i].path[0]], Nodes[TrafficLights[i].path[1]])

    TextX = round(WindowX * (1250 / 1500))
    InformationFont = TkFont.Font(family = "Arial", weight = "bold", size = round((WindowX - TextX) / 12.5))
    InformationOptions = {
        'font': InformationFont,
        'text': 'Кол-во машин:',
        'anchor': 'center',
        'fill': 'black'
    }
    canvas.create_text(TextX, WindowY / 3.2, InformationOptions)
    canvas.create_text(TextX, WindowY / 31.7, InformationOptions, text = "Частота появления машин:")
    canvas.create_text(TextX, WindowY / 5, InformationOptions, text = "Алгоритм поиска пути:")
    canvas.create_text(TextX, WindowY / 2.4, InformationOptions, text = "Макс. кол-во машин в вершине:")
    canvas.create_text(TextX, WindowY / 1.9, InformationOptions, text = "Время:")
    canvas.create_text(TextX, WindowY / 1.5, InformationOptions, text = "Среднее кол-во машин:")
    canvas.create_text(TextX, WindowY / 1.3, InformationOptions, text = "Среднее макс. кол-во\nмашин в вершине:")
    InformationFont = TkFont.Font(family = "Arial", weight = "bold", size = round((WindowX - TextX) / 8))
    InformationOptions = {
        'font': InformationFont,
        'text': '0',
        'anchor': 'center',
        'fill': 'black'
    }
    Information[0] =  canvas.create_text(TextX, WindowY / 2.7, InformationOptions)
    Information[1] =  canvas.create_text(TextX, WindowY / 2.1, InformationOptions)
    Information[2] =  canvas.create_text(TextX, WindowY / 1.7, InformationOptions, text = "0:00")
    Information[3] =  canvas.create_text(TextX, WindowY / 1.4, InformationOptions)
    Information[4] =  canvas.create_text(TextX, WindowY / 1.2, InformationOptions)

def NodePathToPath(NodePath, Nodes, canvas):
    path = [0, 0]
    for j in range(len(Nodes)):
        if canvas.coords(Nodes[j].object) == canvas.coords(NodePath[0].object):
            path[0] = j
        if canvas.coords(Nodes[j].object) == canvas.coords(NodePath[1].object):
            path[1] = j
    return (path[0], path[1])
    
def DrawCarCount(Node, canvas):
    font = TkFont.Font(weight = "bold", size = 15)
    TextOptions = {
        'font': font,
        'text': "0",
        'anchor': 'center',
        'fill': '#4de600'
    }
    y = canvas.coords(Node.object)[1] - 10
    x = round((canvas.coords(Node.object)[0] + canvas.coords(Node.object)[2]) / 2)
    NewX = x
    while len(canvas.find_overlapping(NewX - 15, y, NewX + 15, y)) > 0 and NewX < x + 20:
        NewX += 1
    while len(canvas.find_overlapping(NewX - 15, y, NewX + 15, y)) > 0 and NewX > x - 20:
        NewX -= 1
    if len(canvas.find_overlapping(NewX - 15, y, NewX + 15, y)) > 0:
        NewX = x
    NewCarCount = canvas.create_text(NewX, y, TextOptions)
    return NewCarCount

def DrawLine(Coords, canvas):
    LineOptions = {
        'fill': 'black',
        'width': 5
    }
    NewLine = canvas.create_line(Coords, LineOptions)
    return NewLine

def DrawPoint(Coords, canvas):
    PointOptions = {
        'fill': 'black'
    }
    NewPoint = canvas.create_oval(Coords, PointOptions)
    return NewPoint

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
import tkinter.font as TkFont

def Base(Edges, Nodes, TrafficLights, canvas):
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
    EdgesPath = [
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

    for i in range(28):
        Edges[i].path = EdgesPath[i]
        Edges[i].object = DrawLine(Edges[i].path, NodesCoords, canvas)
    for i in range(56):
        TrafficLights[i].path = EdgesPath[(i // 2)]
        TrafficLights[i].path = [TrafficLights[i].path[0], TrafficLights[i].path[1]]
        if i % 2 == 1:
            TrafficLights[i].path = TrafficLights[i].path[::-1]
        TrafficLights[i].object = CreateTrafficLight(TrafficLights[i].path, NodesCoords, canvas)
        TrafficLights[i].mode = 1

    for i in range(20):
        Nodes[i].object = DrawPoint(NodesCoords[i], canvas)

    font = TkFont.Font(weight = "bold", size = 15)
    TextOptions = {
        'font': font,
        'text': "0",
        'anchor': 'w',
        'fill': '#4de600'
    }

    Nodes[0].CarCount = canvas.create_text(130, 785, TextOptions)
    Nodes[1].CarCount = canvas.create_text(272, 825, TextOptions)
    Nodes[2].CarCount = canvas.create_text(422, 867, TextOptions)
    Nodes[3].CarCount = canvas.create_text(510, 885, TextOptions, anchor = 'center')
    Nodes[4].CarCount = canvas.create_text(900, 816, TextOptions, anchor = 'e')
    Nodes[5].CarCount = canvas.create_text(1010, 790, TextOptions, anchor = 'center')
    Nodes[6].CarCount = canvas.create_text(888, 710, TextOptions)
    Nodes[7].CarCount = canvas.create_text(522, 647, TextOptions)
    Nodes[8].CarCount = canvas.create_text(328, 611, TextOptions)
    Nodes[9].CarCount = canvas.create_text(123, 577, TextOptions)
    Nodes[10].CarCount = canvas.create_text(75, 470, TextOptions, anchor = 'center')
    Nodes[11].CarCount = canvas.create_text(233, 350, TextOptions, anchor = 'center')
    Nodes[12].CarCount = canvas.create_text(420, 438, TextOptions)
    Nodes[13].CarCount = canvas.create_text(575, 475, TextOptions, anchor = 'e')
    Nodes[14].CarCount = canvas.create_text(862, 527, TextOptions)
    TextOptions["anchor"] = 'center'
    Nodes[15].CarCount = canvas.create_text(360, 275, TextOptions)
    Nodes[16].CarCount = canvas.create_text(490, 200, TextOptions)
    Nodes[17].CarCount = canvas.create_text(550, 280, TextOptions, anchor = 'w')
    Nodes[18].CarCount = canvas.create_text(680, 310, TextOptions)
    Nodes[19].CarCount = canvas.create_text(820, 315, TextOptions)

def DrawLine(path, NodesCoords, canvas):
    Coords = NodesCoords[path[0]][0:2] + NodesCoords[path[1]][0:2]
    for i in range(4):
        Coords[i] += 10
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

def CreateTrafficLight(path, NodesCoords, canvas):
    NewTrafficLight = [0, 0]
    LightTrafficOptions = {
        'fill': 'green',
        'width': 6
    }

    LineCoords = NodesCoords[path[0]][0:2] + NodesCoords[path[1]][0:2]
    for i in range(4):
        LineCoords[i] += 10

    LineVector = [LineCoords[2] - LineCoords[0], LineCoords[3] - LineCoords[1]]
    LineLength = (LineVector[0]**2 + LineVector[1]**2)**(1/2)
    LineVector = [LineVector[0] / LineLength, LineVector[1] / LineLength]

    for i in range(2):
        LineCoords[i+2] = LineCoords[i] + LineVector[i] * 25
    NewTrafficLight[0] = canvas.create_line(LineCoords, LightTrafficOptions)

    for i in range(2):
        LineCoords[i+2] = LineCoords[i] + LineVector[i] * 30

    NewLineVector = [-LineVector[1], LineVector[0]]
    TriangleCoords = [
        LineCoords[2],
        LineCoords[3], 
        LineCoords[2] - LineVector[0] * 10 + NewLineVector[0] * 10, 
        LineCoords[3] - LineVector[1] * 10 + NewLineVector[1] * 10,
        LineCoords[2] - LineVector[0] * 10 - NewLineVector[0] * 10, 
        LineCoords[3] - LineVector[1] * 10 - NewLineVector[1] * 10,
    ]
    NewTrafficLight[1] = canvas.create_polygon(TriangleCoords, LightTrafficOptions)
    
    return NewTrafficLight

DefaultTrafficLightMode = [
    2, 1, 2, 1, 1, 2, 2, 1,
    2, 1, 1, 2, 1, 2, 2, 1,
    1, 2, 1, 1, 1, 1, 2, 1,
    1, 2, 2, 1, 2, 2, 1, 2,
    1, 2, 2, 1, 1, 2, 2, 2,
    1, 2, 2, 2, 1, 2, 1, 2,
    2, 1, 1, 2, 2, 1, 1, 2
]
CityModeGraph = [[1] * 20 for i in range(20)]
DefaultCityGraph = [
    [0, 145, 0, 0, 0, 0, 0, 0, 0, 205, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [145, 0, 155, 0, 0, 0, 0, 0, 220, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 155, 0, 105, 0, 0, 0, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 105, 0, 407, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 407, 0, 102, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 102, 0, 148, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 102, 148, 0, 381, 0, 0, 0, 0, 0, 0, 186, 0, 0, 0, 0, 0],
    [0, 0, 240, 0, 0, 0, 381, 0, 182, 0, 0, 0, 0, 176, 0, 0, 0, 0, 0, 0],
    [0, 220, 0, 0, 0, 0, 0, 182, 0, 208, 0, 277, 0, 0, 0, 0, 0, 0, 0, 0],
    [205, 0, 0, 0, 0, 0, 0, 0, 208, 0, 114, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 114, 0, 196, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 277, 0, 196, 0, 0, 0, 0, 146, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 155, 0, 171, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 176, 0, 0, 0, 0, 155, 0, 294, 0, 0, 0, 198, 0],
    [0, 0, 0, 0, 0, 0, 186, 0, 0, 0, 0, 0, 0, 294, 0, 0, 0, 0, 0, 214],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 171, 0, 0, 0, 150, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 150, 0, 103, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 103, 0, 129, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 198, 0, 0, 0, 129, 0, 140],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 214, 0, 0, 0, 140, 0]
]
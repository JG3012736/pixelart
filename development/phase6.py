from cmu_112_graphics import *
import random, math

'''
make undo feature, 
make selection feature (lasso)
make color buttons
'''

##########################################
# Grid Functions
##########################################

# Source Code for pointInGrid, getCell, and getCellBounds: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html #

def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col)

def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight

    return (x0, y0, x1, y1)

##########################################
# Drawing Background Functions
##########################################

def drawBGColor(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, 
                                                fill=app.bGColor)

def drawGrid(app, canvas):                 #draws the grid background
    for row in range(0, app.rows):          #left outline
        for col in range(0, 5):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill=app.gridColor,
                                    outline=app.outlineColor)
    for row in range(0, app.rows):          #right outline
        for col in range(43, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill=app.gridColor,
                                    outline=app.outlineColor)
    for row in range(41, app.rows):        #bottom outline
        for col in range(0, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill=app.gridColor,
                                    outline=app.outlineColor)
    for row in range(0, 2):                 #top outline
        for col in range(0, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill=app.gridColor,
                                    outline=app.outlineColor)

    '''move to button class later, temporary code'''
    for row in range(3, 7):
        for col in range(0, 4):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill="dark gray",
                                    outline="black")
    canvas.create_text(x0, y0, text="drawing button", fill="white")
    for row in range(8, 12):
        for col in range(0, 4):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill="dark gray",
                                    outline="black")
    canvas.create_text(x0, y0, text="erasing button", fill="white")

    '''move following code to buttons as well, temporary'''
    i = 0
    for row in range(42, 44):
        for col in range(5, 43):
            fill = app.colorsList[i]
            if i >= len(app.colorsList)-1:
                i = 0
            i += 1
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1,
                                    fill = fill,
                                    width = 3,
                                    outline="black")

##########################################
# Canvas Class
##########################################

class Canvas():

    #top level functions --> canvas methods#
    getCellBounds_method = getCellBounds
    getCell_method = getCell

    def __init__(self, app):
        #basic variables#
        self.rows = 54
        self.cols = 54
        self.width = app.width
        self.height = app.height
        self.margin = 54
        self.outlineWidth = 0.4
        self.isDrawn = False
        self.isDrawing = True
        self.isErasing = False

        #initializing the canvas#
        self.emptyColor = "white"
        self.canvasBoard = [([self.emptyColor] * self.cols) for row in range(self.rows)]
        self.newCanvas = (Image.new("RGB", 
                            (self.width, self.height), 
                            self.emptyColor))
        
        #drawing functionality#
        self.selection = (-1, -1)
        self.colorsIndex = app.colorIndex
        self.colorsList = app.colorsList
        self.colors = self.colorsList[self.colorsIndex]

        #undoing features#
        self.lastPressed = []
        self.lastPressedColor = []
        self.lastDragged = []
        self.lastDraggedColor = []
        self.wasDragged = False

    def newCanvas(self):
        self.isDrawn = False
        self.lastPressed = []
        self.lastPressedColor = [] 
        self.lastDragged = []
        self.lastDraggedColor = []
        self.rows = 54
        self.cols = 54
        self.colorIndex = 0
        self.colors = self.colorsList[self.colorsIndex]
        self.canvasBoard = [([self.emptyColor] * self.cols) for row in range(self.rows)]

    def drawCanvasImage(self, canvas):  #this function currently does not work
        x0 = 133
        y0 = 66
        draw = ImageDraw.Draw(self.newCanvas)
        canvas.create_image(x0, y0, 
                            image=ImageTk.PhotoImage(self.newCanvas))
    
    def drawCanvasGrid(self, canvas):    #draws the initial empty canvas (from Tetris) 
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds_method(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill=self.canvasBoard[row][col],
                                        outline="lightGray")

    def mousePressedCanvas(self, event):
        (row, col) = self.getCell_method(event.x, event.y)
        (x0, y0, x1, y1) = self.getCellBounds_method(row, col)
        if self.isDrawing:
            self.canvasBoard[row][col] = self.colors
            self.selection = (row, col)
            self.isDrawn = True
            self.lastPressed.append((row, col))
            self.lastPressedColor.append(self.colors)
        else:
            self.canvasBoard[row][col] = self.emptyColor
            self.selection = (row, col)
            self.isDrawn = True
            self.lastPressed.append((row, col))
            self.lastPressedColor.append(self.emptyColor)
        # print(self.lastPressed, self.lastPressedColor)

    def mouseDraggedCanvas(self, event):
        (endRow, endCol) = self.getCell_method(event.x, event.y)
        # print(endRow, endCol)
        if self.isDrawing:
            self.canvasBoard[endRow][endCol] = self.colors
            self.selection = (endRow, endCol)
            self.isDrawn = True
            self.wasDragged = True
            self.lastDragged.append((endRow, endCol))
            self.lastDraggedColor.append(self.colors)
        else:
            self.canvasBoard[endRow][endCol] = self.emptyColor
            self.selection = (endRow, endCol)
            self.isDrawn = True
            self.wasDragged = True
            self.lastDragged.append((endRow, endCol))
            self.lastDraggedColor.append(self.emptyColor)
        # print(self.lastDragged, self.lastDraggedColor)

    def keyPressedCanvas(self, event):
        if event.key == "r":                        #initializes a blank canvas
            Canvas.newCanvas(self)

        if event.key == "e":                        #toggles erasing ability
            self.isDrawing = not self.isDrawing
            self.isErasing = not self.isErasing

        elif (len(self.lastPressed) != 0 and        #undo feature for singles
            len(self.lastPressedColor) != 0 and 
            event.key == "z"):
            undoRow, undoCol = self.lastPressed[-1]
            if self.lastPressedColor[-1] != self.emptyColor:
                self.canvasBoard[undoRow][undoCol] = self.emptyColor
                self.lastPressed.pop()
                self.lastPressedColor.pop()
            elif self.lastPressedColor[-1] == self.emptyColor:
                self.lastPressed.pop()
                self.lastPressedColor.pop()
                # if len(self.lastPressedColor) == 1:
                #     makeColor = self.emptyColor
                makeColor = self.lastPressedColor[-1]
                # print(makeColor)
                self.canvasBoard[undoRow][undoCol] = makeColor

        elif event.key == "a":                      #undo feature for drags
            if (len(self.lastDraggedColor) != 0 and 
                self.lastDraggedColor[0] != self.emptyColor):
                startRow, startCol = self.lastDragged[0]
                endRow, endCol = self.lastDragged[-1]
                # print(self.lastDragged)
                # print(startRow, startCol)
                # print(endRow, endCol)
                for row in range(startRow, endRow+1):
                    for col in range(startCol, endCol+1):
                        # print(f"this is row,col = {row, col}")
                        self.canvasBoard[row][col] = self.emptyColor
            if self.wasDragged == True:
                self.lastDraggedColor = []
                self.lastDragged = []
                self.wasDragged = not self.wasDragged

        elif event.key == "Right":                  #changes color
            if self.colorsIndex < len(self.colorsList)-1:
                self.colorsIndex += 1
                self.colors = self.colorsList[self.colorsIndex]

        elif event.key == "Left":                   #changes color
            if self.colorsIndex > 0:
                self.colorsIndex -= 1
                self.colors = self.colorsList[self.colorsIndex]


        if self.isDrawn != True:                    #stops resizing of canvas
            if event.key == "Up" and self.rows != 54 and self.cols != 54:
                self.rows += 2
                self.cols += 2
            elif event.key == "Down" and self.rows != 2 and self.cols != 2:
                self.rows -= 2
                self.cols -= 2

##########################################
# Button Class
##########################################

class Button(Canvas):       #subclass of Canvas class

    #top level functions --> button methods#
    getCellBounds_method = getCellBounds
    getCell_method = getCell

    def __init__(self, app):
        super().__init__(app)
        self.isButton = False
        self.buttonType = None
    
    def mousePressed(self, app, event):
        (row, col) = self.getCell_method(event.x, event.y)
        print(row, col)
        app.selection = (row, col)
        for row in range(3, 7):
            for col in range(0, 4):
                if app.selection == (row, col):
                    app.canvasObject.isDrawing = True
                    app.canvasObject.isErasing = False
        for row in range(8, 12):
            for col in range(0, 4):
                if app.selection == (row, col):
                    app.canvasObject.isDrawing = False
                    app.canvasObject.isErasing = True
        for row in range(42, 44):
            for col in range(5, 43):
                if app.selection == (row, col):
                    if row == 42:
                        color = app.colorsList[col-5]
                    else:
                        color = app.colorsList[col+row-10]
                    app.canvasObject.colors = color

##########################################
# Main App
##########################################

'''Model'''

def appStarted(app):
    app.margin = 25
    app.bGColor = "light pink"
    app.gridColor = "mistyrose"
    app.rows = 45
    app.cols = 45
    app.selection = (-1, -1)
    app.outlineColor = "black"
    app.colorsList = ["black", "seashell3",
                    "aliceblue", "azure",
                    "mistyrose", "lightyellow",
                    "navajowhite3", "navajowhite4",
                    "burlywood3", "burlywood4",
                    "lightgray", "lightslategray",
                    "darkgray", "dimgray",
                    "cornflowerBlue", "darkslateblue",
                    "skyblue", "deepskyblue",
                    "paleturquoise1", "royalblue1",
                    "lightsteelblue", "slateblue1",
                    "lightcyan1", "cyan",
                    "mediumaquamarine", "teal", 
                    "forestgreen", "lavender",
                    "aquamarine", "darkturquoise",
                    "palegreen1", "palegreen4",
                    "springgreen2", "springgreen4",
                    "darkseagreen", "darkolivegreen",
                    "greenyellow", "lawngreen",
                    "palegreen",
                    "darkolivegreen1", "darkolivegreen4",
                    "wheat", "gold",
                    "peachpuff", "khaki",
                    "yellow", "orange",
                    "gold2", "darkgoldenrod1",
                    "lightsalmon", "orange",
                    "salmon1", "orangered",
                    "lightcoral", "indianred1",
                    "firebrick1", "orangered",
                    "lightPink", "deeppink",
                    "paleVioletRed", "violetRed", 
                    "hotpink", "magenta",
                    "red2", "red4",
                    "crimson", "darkred",
                    "maroon", "violetred",
                    "mediumslateblue", "darkviolet",
                    "mediumpurple", "darkorchid",
                    "plum", "darkmagenta",
                    "tan4"]
    app.colorIndex = 0         #fix this later
    app.currColor = app.colorsList[app.colorIndex]

    #make new objects here#
    app.canvasObject = Canvas(app)
    app.buttonObject = Button(app)

'''View'''

def redrawAll(app, canvas):
    drawBGColor(app, canvas)

    #canvas class calls#
    # app.canvasObject.drawCanvasImage(canvas)  #HELPPPPPP
    app.canvasObject.drawCanvasGrid(canvas)

    drawGrid(app, canvas)

'''Controller'''

def mousePressed(app, event):
    #canvas top level app calls#
    # app.canvasObject.mousePressedCanvas(event)
    app.buttonObject.mousePressed(app, event)

    #from CMU 112 graphics (using for debugging)#
    (row, col) = getCell(app, event.x, event.y)
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    # select this (row, col) unless it is selected
    if (app.selection == (row, col)):
        app.selection = (-1, -1)
    else:
        app.selection = (row, col)
        # print(row, col)
        # print(x0, x1, y0, y1)

    # #my own code#
    # '''move all of the folling into button mouse pressed later'''
    # (row, col) = getCell(app, event.x, event.y)
    # app.selection = (row, col)
    # for row in range(3, 7):
    #     for col in range(0, 4):
    #         if app.selection == (row, col):
    #             app.canvasObject.isDrawing = True
    #             app.canvasObject.isErasing = False
    # for row in range(8, 12):
    #     for col in range(0, 4):
    #         if app.selection == (row, col):
    #             app.canvasObject.isDrawing = False
    #             app.canvasObject.isErasing = True
    # for row in range(42, 44):
    #     for col in range(5, 43):
    #         if app.selection == (row, col):
    #             if row == 42:
    #                 color = app.colorsList[col-5]
    #             else:
    #                 color = app.colorsList[col+row-10]
    #             app.canvasObject.colors = color


def mouseDragged(app, event):
    #canvas top level app calls#
    app.canvasObject.mouseDraggedCanvas(event)
    # app.buttonObject.mouseDraggedButton(event)

def keyPressed(app, event):
    app.canvasObject.keyPressedCanvas(event)

runApp(width=1000, height=1000)
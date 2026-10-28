from cmu_112_graphics import *
import random, math

'''
make undo feature, 
make selection feature (lasso)
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
                                    fill="azure4",
                                    outline="white")
    for row in range(0, app.rows):          #right outline
        for col in range(43, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill="azure4",
                                    outline="white")
    for row in range(41, app.rows):        #bottom outline
        for col in range(0, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill="azure4",
                                    outline="white")
    for row in range(0, 2):                 #top outline
        for col in range(0, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill="azure4",
                                    outline="white")
    '''temporary code'''
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
        self.margin = 50
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
        self.colorsIndex = 0
        self.colorsList = ["black", "cornflowerBlue", 
                            "violetRed", "paleVioletRed",
                            "slateBlue1", "gold", 
                            "lightPink", "plum", "lightGreen"]
        self.colors = self.colorsList[self.colorsIndex]

        #undoing features#
        self.lastPressed = dict()

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
                                        outline="lightGray", width=0)

    def mousePressedCanvas(self, event):
        (row, col) = self.getCell_method(event.x, event.y)
        (x0, y0, x1, y1) = self.getCellBounds_method(row, col)
        if self.isDrawing:
            self.canvasBoard[row][col] = self.colors
            self.selection = (row, col)
            self.isDrawn = True
            # self.lastPressed[(row, col)] = self.colors
            # print(self.lastPressed)
        else:
            self.canvasBoard[row][col] = self.emptyColor
            self.selection = (row, col)
            self.isDrawn = True
            # self.lastPressed[(row, col)] = self.colors
            # print(self.lastPressed)

    def mouseDraggedCanvas(self, event):
        (endRow, endCol) = self.getCell_method(event.x, event.y)
        if self.isDrawing:
            self.canvasBoard[endRow][endCol] = self.colors
            self.selection = (endRow, endCol)
            self.isDrawn = True
        else:
            self.canvasBoard[endRow][endCol] = self.emptyColor
            self.selection = (endRow, endCol)
            self.isDrawn = True
    
    def keyPressedCanvas(self, event):
        if event.key == "r":
            self.isDrawn = False
            self.lastPressedList = []
            self.rows = 54
            self.cols = 54
            self.colors = self.colorsList[0]
            self.canvasBoard = [([self.emptyColor] * self.cols) for row in range(self.rows)]
        if event.key == "e":
            self.isDrawing = not self.isDrawing
            self.isErasing = not self.isErasing
        elif event.key == "z":
            # if self.lastPressed != self.emptyColor:
            #     print("this is working")
            pass
        elif event.key == "Right":
            if self.colorsIndex < len(self.colorsList)-1:
                self.colorsIndex += 1
                self.colors = self.colorsList[self.colorsIndex]
        elif event.key == "Left":
            if self.colorsIndex > 0:
                self.colorsIndex -= 1
                self.colors = self.colorsList[self.colorsIndex]

        if self.isDrawn != True:
            if event.key == "Up" and self.rows != 54 and self.cols != 54:
                self.rows += 2
                self.cols += 2
            elif event.key == "Down" and self.rows != 2 and self.cols != 2:
                self.rows -= 2
                self.cols -= 2

##########################################
# Button Class
##########################################

class Button(Canvas):

    def __init__(self, app):
        super().__init__(app)      #inherits all __init__ attributes of Canvas
        self.drawingButton = True
        self.erasingButton = False
    
    def mousePressedButton(self, event):
        pass

##########################################
# Main App
##########################################

'''Model'''

def appStarted(app):
    app.margin = 25
    app.bGColor = "light pink"
    app.rows = 45
    app.cols = 45
    app.selection = (-1, -1)

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
    app.canvasObject.mousePressedCanvas(event)

    '''move all of the folling into button mouse pressed later'''
    (row, col) = getCell(app, event.x, event.y)
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


def mouseDragged(app, event):
    #canvas top level app calls#
    app.canvasObject.mouseDraggedCanvas(event)
    # app.buttonObject.mouseDraggedButton(event)

def keyPressed(app, event):
    app.canvasObject.keyPressedCanvas(event)

runApp(width=1000, height=1000)
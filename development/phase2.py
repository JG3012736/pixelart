from cmu_112_graphics import *
import random, math

##########################################
# Helper Functions
##########################################

# Source Code for pointInGrid, getCell, and getCellBounds: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html #

def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((0 <= x <= app.width) and
            (0 <= y <= app.height))

def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width
    gridHeight = app.height
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    row = int((y) / cellHeight)
    col = int((x) / cellWidth)

    return (row, col)

def getCellBounds(app, width, height, row, col, rows, cols):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = width
    gridHeight = height
    cellWidth = gridWidth / cols
    cellHeight = gridHeight / rows

    x0 = col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = row * cellHeight
    y1 = (row+1) * cellHeight

    return (x0, y0, x1, y1)

def drawBackgroundColor(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, 
                                                fill=app.backgroundColor)

def drawGridDesign(app, canvas):      #draws the grid background
    for row in range(0, app.rows):
        for col in range(0, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, app.width, app.height, 
                                            row, col, app.rows, app.cols)
            canvas.create_rectangle(x0, y0, x1, y1, outline="white")

##########################################
# Canvas Mode
##########################################

def canvasMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    drawBackgroundColor(app, canvas)
    canvasMode_drawGridDesign(app, canvas)
    canvas.create_text(app.width/2, 150, text='Welcome to canvas mode!', font=font)

    #drawing the canvas#
    app.canvasObject.drawCanvas(app, canvas) # draws the Canvas object

    # #drawing the buttons#
    # buttonObject = Button()
    # buttonObject.drawButtons(app, canvas)

def canvasMode_drawGridDesign(app, canvas): #draws the grid background for canvas mode
    for row in range(0, app.rows):
        for col in range(0, app.cols):
            # if row == num in range(0, )
            (x0, y0, x1, y1) = getCellBounds(app, app.width, app.height, row, col, app.rows, app.cols)
            canvas.create_rectangle(x0, y0, x1, y1, outline="black")

def canvasMode_timerFired(app):
    pass

def canvasMode_mousePressed(app, event):
    #from CMU 112 graphics
    (row, col) = getCell(app, event.x, event.y)
    # select this (row, col) unless it is selected
    if (app.selection == (row, col)):
        app.selection = (-1, -1)
    else:
        app.selection = (row, col)
        print(row, col)
        x0, y0, x1, y1 = app.canvasObject.getCellBounds_method(app.canvasObject.gridWidth, 
                                                    app.canvasObject.gridHeight, 
                                                    app.canvasObject.startRow, 
                                                    app.canvasObject.startCol,
                                                    app.rows, 
                                                    app.cols)
        # print(self.startCol, self.startRow)
        print(x0, y0)
        print(x0*row-1000, y0*col-900)
    # app.canvasObject.mousePressed(event)

def canvasMode_keyPressed(app, event):
    if (event.key == 'Left'):
        app.mode = 'splashScreenMode'

##########################################
# OOP
##########################################

class Canvas():                     #initializes a new canvas

    getCellBounds_method = getCellBounds

    def __init__(self):
        self.cellRows = 20
        self.cellCols = 20
        self.startRow = 3
        self.startCol = 5
        self.pixelColor = "white"
        self.canvasColor = (255, 255, 255)    #white
        self.canvasSelection = (-1, -1) # (row, col), initializes as None
        self.gridWidth = 702
        self.gridHeight = 754
        # self.canvasWidth = 20
        # self.canvasHeight = 20
        self.newCanvas = (Image.new("RGB", 
                            (self.gridWidth, self.gridHeight), 
                            self.canvasColor))

    def drawCanvas(self, app, canvas):
        # print(x0, y0)
        # print(x0*row-1000, y0*col-900)
        x0, y0, x1, y1 = self.getCellBounds_method(self.gridWidth, 
                                                    self.gridHeight, 
                                                    self.startRow, 
                                                    self.startCol,
                                                    app.rows, 
                                                    app.cols)
        print(x0, y0)
        x0 = 17*27
        y0 = 19*26
        # x0 = x0+(27*6)
        # y0 = y0+(26*2)
        # print(x0, y0)
        draw = ImageDraw.Draw(self.newCanvas)
        canvas.create_image(x0, y0, 
                            image=ImageTk.PhotoImage(self.newCanvas))
    
    def drawCanvasGrid(self, app, canvas):
        for row in range(0, self.cellRows):
            for col in range(0, self.cellCols):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1,
                                        outline="red")
    
    def mousePressed(self, event):
    #from CMU 112 graphics
        (row, col) = getCell(self, event.x, event.y)
        # select this (row, col) unless it is selected
        if (self.canvasSelection == (row, col)):
            self.canvasSelection = (-1, -1)
        else:
            self.canvasSelection = (row, col)
            print(row, col)

    #use a 2D list for your canvas, w/ colors as each pixel
    #store coordinate of last pixel pressed

class Button():

    def __init__(self):
        self.button1Row = 3
        self.button1Col = 3
        self.buttonLocation = buttonLocator()
    
    def buttonLocator(self, x, y):
        pass

    def drawButtons(self, app, canvas):
        for row in range(0, self.button1Row):
            for col in range(0, self.button2Col):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill="blue")

##########################################
# Main App
##########################################

def appStarted(app):
    #splash screen#
    app.mode = 'canvasMode'
    app.backgroundColor = "light sky blue"
    app.rows = 34
    app.cols = 36
    app.startButtonX0 = 0
    app.startButtonY0 = 0
    app.startButtonX1 = 0 
    app.startButtonX2 = 0
    app.selection = (-1, -1)

    #make objects here#
    app.canvasObject = Canvas()


runApp(width=1000, height=900)

#720 x 680 also works well
#27 x 26
#1224 total cells
# 34 - 8 = 26   #702
# 36 - 7 = 29   #754
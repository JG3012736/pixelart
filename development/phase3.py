from cmu_112_graphics import *
import random, math

'''
make a canvas class, 
make a button class
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
# Drawing Functions
##########################################

def drawBGColor(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, 
                                                fill=app.bGColor)

def drawGrid(app, canvas):                 #draws the grid background
    for row in range(0, app.rows):
        for col in range(0, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, outline="white")

def drawCanvas(app, canvas):    #draws the initial empty canvas (from Tetris) 
    for row in range(2, 40):
        for col in range(5, 43):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, 
                                    fill=app.canvas[row][col])

##########################################
# Canvas Class
##########################################

class Canvas():

    #top level functions --> canvas methods#
    getCellBounds_method = getCellBounds

    def __init__(self, app):
        self.rows = app.rows
        self.cols = app.cols
        self.width = app.width
        self.height = app.height
        self.margin = 0
        self.emptyColor = "red"
        self.canvasBoard = [([self.emptyColor] * self.cols) for row in range(self.rows)]
    
    def drawCanvas(self, canvas):    #draws the initial empty canvas (from Tetris) 
        for row in range(3, 38):
            for col in range(6, 42):
                (x0, y0, x1, y1) = self.getCellBounds_method(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill=self.canvasBoard[row][col])

##########################################
# Main App
##########################################

'''Model'''

def appStarted(app):
    app.margin = 25
    app.bGColor = "light sky blue"
    app.rows = 45
    app.cols = 45
    app.selection = (-1, -1)
    app.emptyColor = "white"
    app.canvas = [([app.emptyColor] * app.cols) for row in range(app.rows)]

    #make new objects here#
    app.canvasObject = Canvas(app)

'''View'''

def redrawAll(app, canvas):
    drawBGColor(app, canvas)
    drawGrid(app, canvas)
    drawCanvas(app, canvas)
    app.canvasObject.drawCanvas(canvas)

'''Controller'''

def mousePressed(app, event):
    #from CMU 112 graphics
    (row, col) = getCell(app, event.x, event.y)
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    # select this (row, col) unless it is selected
    if (app.selection == (row, col)):
        app.selection = (-1, -1)
    else:
        app.selection = (row, col)
        print(row, col)
        print(x0, x1, y0, y1)

runApp(width=1000, height=1000)
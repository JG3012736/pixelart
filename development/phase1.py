from cmu_112_graphics import *
import random, math

##########################################
# Helper Functions
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
# Splash Screen Mode
##########################################

'''Top Level Splash Mode Functions'''

def splashScreenMode_redrawAll(app, canvas):
    drawBackgroundColor(app, canvas)
    drawGridDesign(app, canvas)
    drawMainBox(app, canvas)
    drawWelcomeText(app, canvas)
    drawLogoBackground(app, canvas)
    drawNewCanvasWebPage(app, canvas)

def splashScreenMode_keyPressed(app, event):
    if (event.key == 'Right'):
        app.mode = 'canvasMode'

'''Drawing the Background Functions'''

def drawBackgroundColor(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, 
                                                fill=app.backgroundColor)

def drawGridDesign(app, canvas):      #draws the grid background
    for row in range(0, app.rows):
        for col in range(0, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, outline="white")

def drawWelcomeText(app, canvas):
    x0 = app.width//2 - app.width//4
    y0 = app.height//10
    x1 = app.width//2 + app.width//4
    y1 = app.height//5.5
    fill1 = "lightgray"
    outline1 = "gray25"

    #shadows#
    canvas.create_rectangle(x0-10//3, y0-10//3, x1+10//3, y1+10//3, 
                                fill="dimgray", width=0)

    #highlights#
    canvas.create_rectangle(x0-10//3, y0-10//3, x1, y1,
                            fill="white", width=0)

    #main box#
    canvas.create_rectangle(x0, y0, x1, y1, fill=fill1, 
                                outline=outline1, width=1)

    x0Text = (x0+x1)//2
    y0Text = (y0+y1)//2

    if y0Text <= 80:
        font = "CourierNew 12 italic"
    elif y0Text >= 115:
        font = "CourierNew 40 italic"
    else:
        font = "CourierNew 25 italic"

    canvas.create_text(x0Text, y0Text, fill="gray30",
                            text="welcome to pixelArt", font=font)

def drawMainBox(app, canvas):
    x0MainBox = (app.width//2 - app.width//4) - 10*2
    y0MainBox = (app.height//10) - 10*2*2
    x1MainBox = (app.width//2 + app.width//4) + 10*2
    y1MainBox = (app.height//5.5 + app.height//2) + 10*2

    #shadows#
    canvas.create_rectangle(x0MainBox-10//3, y0MainBox-10//3, 
                            x1MainBox+10//3, y1MainBox+10//3, 
                                fill="dimgray", width=0)

    #highlights#
    canvas.create_rectangle(x0MainBox-10//3, y0MainBox-10//3, 
                            x1MainBox, y1MainBox, 
                            fill="white", width=0)

    #main box#
    canvas.create_rectangle(x0MainBox, y0MainBox, x1MainBox, y1MainBox,
                                fill="light gray")

    x0Border = (app.width//2 - app.width//4) - 10*2
    y0Border = (app.height//10) - 10*2*2
    x1Border = (app.width//2 + app.width//4) + 10*2
    y1Border = app.width//14       #fix this

    #pink border#
    canvas.create_rectangle(x0Border, y0Border, x1Border, y1Border,
                                fill="pink")

def drawLogoBackground(app, canvas):
    x0 = app.width//2 - app.width//4
    y0 = app.height//10 + app.height//7
    x1 = app.width//2 + app.width//4
    y1 = app.height//5.5 + app.height//2

    #shadows#
    canvas.create_rectangle(x0-10//3, y0-10//3, x1, y1, 
                            fill="dimgray", width=0)

    #main box#
    canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="gray25")

    x0Text = (x0 + x1)//2
    y0Text = (y0 + y1)//2
    
    textList = [
                "Some shortcuts include:\n"
                "\n"
                "Hardpress z to undo multiple times\n"
                "\n"
                "Press s to select a rectangular area\n"
                "\n"
                "Press t to fill that rectangular area\n"
                "\n"
                "If you pressed the eraser button, \n"
                "be sure to press the drawing button again to continue drawing.\n"
                "\n"
                "Pressing the undo button will allow a SINGULAR undo!\n"
                "\n"
                "Press on a color button to pick a color for your fill,\n"
                "BEFORE you press s to select an area!\n"
                "\n"
                "You can only change the size of the canvas, \n"
                "BEFORE drawing or erasing!\n"
                "\n"
                "Press r to create a completely new canvas"
    ]

    #text#
    canvas.create_text(x0Text, y0Text, text=textList[0], 
                                        font="Arial 16 bold",
                                        fill="violetred3")

'''Drawing the Next Page Buttons'''

def drawNewCanvasWebPage(app, canvas):
    x0 = app.width//3 + app.width//3 - app.height//15
    y0 = app.height//3 + app.height//2
    x1 = x0 + app.width//3
    y1 = y0 - app.height//4

    #shadows#
    canvas.create_rectangle(x0-10//3, y0-10//3, 
                            x1+10//3, y1+10//3, 
                                fill="dimgray", width=0)

    #highlight#
    canvas.create_rectangle(x0-10//3, y0, x1, y1, 
                            fill="white", width=0)

    #pink top#
    canvas.create_rectangle(x0, y0, x1, y1, fill="pink")

    #main box#
    canvas.create_rectangle(x0, y0, x1, y1+20,
                                fill="light gray")

##########################################
# Canvas Mode
##########################################

def canvasMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    drawBackgroundColor(app, canvas)
    canvasMode_drawGridDesign(app, canvas)
    canvas.create_text(app.width/2, 150, text='Welcome to canvas mode!', font=font)

    #drawing the canvas#
    canvasObject = Canvas()		         # creates a Canvas object
    canvasObject.drawCanvas(app, canvas) # draws the Canvas object
    canvasObject.drawCanvasPixelCells(app, canvas)

    # #drawing the buttons#
    # buttonObject = Button()
    # buttonObject.drawButtons(app, canvas)

def canvasMode_drawGridDesign(app, canvas): #draws the grid background for canvas mode
    for row in range(0, app.rows):
        for col in range(0, app.cols):
            # if row == num in range(0, )
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, outline="black")

def canvasMode_timerFired(app):
    pass

def canvasMode_mousePressed(app, event):
    pass

def canvasMode_keyPressed(app, event):
    if (event.key == 'Left'):
        app.mode = 'splashScreenMode'

##########################################
# OOP
##########################################

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

class Canvas():                     #initializes a new canvas

    def __init__(self):
        self.gridWidth = 400
        self.gridHeight = 400
        self.cellRows = 20
        self.cellCols = 20
        self.pixelColor = "white"
        self.canvasColor = (255, 255, 255)    #white
        self.canvasSelection = (-1, -1) # (row, col), initializes as None
        self.newCanvas = (Image.new("RGB", 
                            (self.gridWidth, self.gridHeight), 
                            self.canvasColor))
    
    def drawCanvas(self, app, canvas):
        draw = ImageDraw.Draw(self.newCanvas)
        canvas.create_image(self.gridWidth, self.gridHeight, 
                            image=ImageTk.PhotoImage(self.newCanvas))
    
    def drawCanvasPixelCells(self, app, canvas):
        for row in range(0, self.cellRows):
            for col in range(0, self.cellCols):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill=self.pixelColor,
                                        outline="red")
    
    def mousePressed(self, event):
    #from CMU 112 graphics
        (row, col) = getCell(app, event.x, event.y)
        # select this (row, col) unless it is selected
        if (self.canvasSelection == (row, col)):
            self.canvasSelection = (-1, -1)
        else:
            self.canvasSelection = (row, col)

    #use a 2D list for your canvas, w/ colors as each pixel
    #store coordinate of last pixel pressed

##########################################
# Main App
##########################################

def appStarted(app):
    #splash screen#
    app.mode = 'splashScreenMode'
    app.backgroundColor = "light sky blue"
    app.rows = 34
    app.cols = 36
    app.margin = 0
    app.startButtonX0 = 0
    app.startButtonY0 = 0
    app.startButtonX1 = 0 
    app.startButtonX2 = 0

    #make objects here#
    app.canvasObjec = Canvas()

runApp(width=1000, height=1000)

#720 x 680 also works well
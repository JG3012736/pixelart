from cmu_112_graphics import *
import random, math, copy

'''
Jenna Gomes, jsgomes

make undo + redo feature, 
make selection feature (lasso)
fix button class color picker
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

##########################################
# Canvas Class
##########################################

class Canvas():

    '''Initializing Canvas' Functions'''

    #top level functions --> canvas methods#
    getCellBounds_method = getCellBounds
    getCell_method = getCell
    pointInGrid_method = pointInGrid

    def __init__(self, app):
        #basic variables#
        self.rows = 54      #can change
        self.cols = 54
        self.margin = 60    #25
        self.width = app.width  #1000
        self.height = app.height #920

        #booleans#
        self.isDrawn = False
        self.isDrawing = True
        self.isErasing = False
        self.isSelecting = False
        self.wasDragged = False

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
        self.lastDragged = set()
        self.prevBoard = copy.deepcopy(self.canvasBoard)
        self.allBoards = [copy.deepcopy(self.canvasBoard)]
        self.lastDrawn = []

    '''Drawing the Canvas Functions'''

    def drawCanvasImage(self, canvas):  #this function currently does not work
        x0 = 133
        y0 = 66
        draw = ImageDraw.Draw(self.newCanvas)
        canvas.create_image(x0, y0, 
                            image=ImageTk.PhotoImage(self.newCanvas))
    
    def drawCanvasGrid(self, canvas):  #draws the initial empty canvas (from Tetris) 
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds_method(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill=self.canvasBoard[row][col],
                                        outline="lightGray")
    
    '''Interacting w/ the Canvas Functions'''

    def resizeCanvas(self, event):              #resizes the canvas
        if event.key == "Up" and self.rows != 54 and self.cols != 54:
            self.rows += 2
            self.cols += 2
        elif event.key == "Down" and self.rows != 2 and self.cols != 2:
            self.rows -= 2
            self.cols -= 2
    
    def undoLastPressed(self):                  #undoes last mouse clicked
        if isinstance(self.lastDrawn[-1], list) != True:
            (undoRow, undoCol) = self.lastDrawn[-1]
            if self.isDrawing == True:
                self.canvasBoard[undoRow][undoCol] = (
                                    self.allBoards[-1][undoRow][undoCol]
                                                        )
                self.allBoards.pop()
                self.lastDrawn.pop()
            elif self.isErasing == True:
                pass
            #     self.canvasBoard[undoRow][undoCol] = self.allBoards[-1][undoRow][undoCol]
            #     self.allBoards.pop()
            #     self.lastDrawn.pop()

    def undoLastDragged(self):                  #undoes last mouse dragged
        self.allBoards.append(self.prevBoard)
        print(len(self.allBoards))
        print(len(self.prevBoard))
        for elem in self.lastDragged:
            # if isinstance(elem, list):
            (undoRow, undoCol) = elem
            if self.isDrawing == True and self.allBoards != []:
                self.canvasBoard[undoRow][undoCol] = self.allBoards[-2][undoRow][undoCol]
                print(f"new color = {self.allBoards[-1][undoRow][undoCol]}")
                print(f"old color = {self.canvasBoard[undoRow][undoCol]}\n")
            else:
                continue
                #     self.canvasBoard[undoRow][undoCol] = makeColor
        self.allBoards.pop()

    '''Controller Top Level Functions for Canvas Class'''

    def mouseDraggedCanvas(self, event):
        (row, col) = self.getCell_method(event.x, event.y)
        self.wasDragged = True
        self.isDrawn = True
        self.selection = (row, col)
        if self.isDrawing:
            self.canvasBoard[row][col] = self.colors
            self.lastDragged.add(self.selection)
            self.prevBoard = copy.deepcopy(self.canvasBoard)
        else:
            self.canvasBoard[row][col] = self.emptyColor
            # self.lastDrawn = [] #currently stops undo if eraser was used
            # self.lastDragged.add((row, col))

    def mousePressedCanvas(self, event):
        (row, col) = self.getCell_method(event.x, event.y)
        self.wasDragged = False
        self.isDrawn = True
        self.selection = (row, col)
        self.prevBoard = copy.deepcopy(self.canvasBoard)
        self.allBoards.append(self.prevBoard)

        if self.isDrawing:
            self.canvasBoard[row][col] = self.colors
            self.lastDrawn.append((row, col))
        else:
            # self.lastDrawn.append((row, col))
            # self.prevBoard = copy.deepcopy(self.canvasBoard)
            # self.allBoards.append(self.prevBoard)
            self.canvasBoard[row][col] = self.emptyColor

    def keyPressedCanvas(self, app, event):
        if event.key == "r":                      #initializes a blank canvas
            Canvas.__init__(self, app)

        if event.key == "e":                      #toggles erasing ability
            self.isDrawing = not self.isDrawing
            self.isErasing = not self.isErasing

        elif event.key == "z":                    #undo feature
            if self.lastDrawn != [] and len(self.allBoards) != 0:
                Canvas.undoLastPressed(self)
                Canvas.undoLastDragged(self)

        elif event.key == "Right":                  #changes color
            if self.colorsIndex < len(self.colorsList)-1:
                self.colorsIndex += 1
                self.colors = self.colorsList[self.colorsIndex]

        elif event.key == "Left":                   #changes color
            if self.colorsIndex > 0:
                self.colorsIndex -= 1
                self.colors = self.colorsList[self.colorsIndex]

        if self.isDrawn != True:   #stops resizing of canvas
            Canvas.resizeCanvas(self, event)    #calls resize canvas function

##########################################
# Button Class
##########################################

class Button(Canvas):   #subclass of the canvas, creates buttons for interactions

    '''Initializing Button's Functions'''

    def __init__(self, app):
        super().__init__(app)
        super().getCell_method
        super().getCellBounds_method
        super().pointInGrid_method
        self.isButton = False
        self.buttonType = None
        self.margin = app.margin
        self.rows = app.rows
        self.cols = app.cols
        self.width = app.width
        self.height = app.height
        self.colorsList = app.colorsList
        self.selection = app.selection
    
    '''Drawing Functions'''

    def drawDrawingButtons(self, app, canvas):  #draws drawing button
        for row in range(3, 7):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="dark gray",
                                        outline="black")
        canvas.create_text(x0, y0, text="drawing button", fill="red4")

    def drawErasingButton(self, app, canvas):   #draws erasing button
        for row in range(8, 12):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="dark gray",
                                        outline="black")
        canvas.create_text(x0, y0, text="erasing button", fill="red4")

    def drawUndoButton(self, app, canvas):   #draws erasing button
        for row in range(13, 17):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="dark gray",
                                        outline="black")
        canvas.create_text(x0, y0, text="undo button", fill="red4")
    
    def drawSelectButton(self, app, canvas):   #draws erasing button
        for row in range(18, 22):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="dark gray",
                                        outline="black")
        canvas.create_text(x0, y0, text="select button", fill="red4")

    def drawColorButtons(self, app, canvas):    #draws color buttons
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

    '''Bounds Checks'''
    
    def drawingButtonBounds(self, app, event):  #sets brush w/ bounds check
        (row, col) = self.getCell_method(event.x, event.y)
        app.selection = (row, col)
        for row in range(3, 7):
            for col in range(0, 4):
                if app.selection == (row, col):
                    app.canvasObject.isDrawing = True
                    app.canvasObject.isErasing = False
    
    def erasingButtonBounds(self, app, event):  #sets eraser w/ bounds check
        (row, col) = self.getCell_method(event.x, event.y)
        app.selection = (row, col)
        for row in range(8, 12):
            for col in range(0, 4):
                if app.selection == (row, col):
                    app.canvasObject.isDrawing = False
                    app.canvasObject.isErasing = True
    
    def undoButtonBounds(self, app):
        for row in range(13, 17):
            for col in range(0, 4):
                if app.selection == (row, col) and app.canvasObject.lastDrawn != []:
                    Canvas.undoLastPressed(self)
    
    def pickColorButtons(self, app, event): #allows user to pick a diff color
        for row in range(42, self.rows-1):
            for col in range(5, self.cols-2):
                if self.selection == (row, col):
                    if row == 42:
                        color = self.colorsList[col-5]
                    else:
                        color = self.colorsList[col+row-10]
                    app.canvasObject.colors = color
    
    '''Top Level Apps for Button Class'''

    def redrawAll(self, app, canvas):
        Button.drawColorButtons(self, app, canvas)
        Button.drawDrawingButtons(self, app, canvas)
        Button.drawErasingButton(self, app, canvas)
        Button.drawUndoButton(self, app, canvas)
        Button.drawSelectButton(self, app, canvas)

    def mousePressed(self, app, event):
        Button.drawingButtonBounds(self, app, event)
        Button.erasingButtonBounds(self, app, event)
        Button.pickColorButtons(self, app, event)
        Button.undoButtonBounds(self, app)

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
    app.colorIndex = 0
    app.currColor = app.colorsList[app.colorIndex]

    #make new objects here#
    app.canvasObject = Canvas(app)
    app.buttonObject = Button(app)

'''View'''

def redrawAll(app, canvas):
    drawBGColor(app, canvas)
    # app.canvasObject.drawCanvasImage(canvas)  #HELPPPPPP
    app.canvasObject.drawCanvasGrid(canvas)     #from canvas class
    drawGrid(app, canvas)
    app.buttonObject.redrawAll(app, canvas)     #from button class

'''Controller'''

def mousePressed(app, event):
    app.canvasObject.mousePressedCanvas(event)  #from canvas class
    app.buttonObject.mousePressed(app, event)   #from button class

    #from CMU 112 graphics (using for debugging)#
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#
    (row, col) = getCell(app, event.x, event.y)
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    # select this (row, col) unless it is selected
    if (app.selection == (row, col)):
        app.selection = (-1, -1)
    else:
        app.selection = (row, col)
        print(row, col)
        print(x0, x1, y0, y1)
    #my code#
    for row in range(42, 44):               #sets the different color buttons
        for col in range(5, 43):
            if app.selection == (row, col):
                if row == 42:
                    color = app.colorsList[col-5]
                else:
                    color = app.colorsList[col+row-10]
                app.canvasObject.colors = color

def mouseDragged(app, event):
    app.canvasObject.mouseDraggedCanvas(event)      #from canvas class

def keyPressed(app, event):
    app.canvasObject.keyPressedCanvas(app, event)   #from canvas class

runApp(width=1000, height=1000, title='PixelArt')

#article I referenced for using OOP: https://blog.finxter.com/define-a-method-outside-of-the-class-definition/#
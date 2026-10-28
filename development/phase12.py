from cmu_112_graphics import *
import random, math, copy

'''
Jenna Gomes, jsgomes

make undo and selection buttons work, 
make undo for erasing, make redo feature, 
fix color picker button
make floodfill feature, import images
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
        self.origRows = 20
        self.origCols = 20
        self.rows = self.origRows #54      #can change
        self.cols = self.origCols #54
        self.margin = 60 #25
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

        #selection features#
        self.selectedList = []
        self.makeSelectionCoors = []
        self.prevColor = self.emptyColor

        #button booleans#
        self.undoButton = False
        # self.wasUndoClicked = False
        self.selectionButton = False

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
        if (event.key == "Up" and 
            self.rows != self.origRows and 
            self.cols != self.origCols):
                self.rows += 2
                self.cols += 2
        elif event.key == "Down" and self.rows != 2 and self.cols != 2:
            self.rows -= 2
            self.cols -= 2

    def getSelectedCells(self):     #returns a list of all red cell coordinates
        self.selectedCells = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.canvasBoard[row][col] == "red":
                    self.selectedCells.append((row, col))
        # print(f"entire list of selected cells = {self.selectedCells}\n")
        return self.selectedCells
    
    def findNonSelectedCells(self, cell): #returns a list of all nonSelectedCells surroudning selected cells
        selectedCellsList = Canvas.getSelectedCells(self)
        nonSelectedCellsList = []
        (row, col) = cell

        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if (drow, dcol) != (0, 0):
                    newRow, newCol = row+drow, col+dcol
                    if self.canvasBoard[newRow][newCol] != "red":
                        nonSelectedCellsList.append((newRow, newCol))
        return nonSelectedCellsList
    
    def isCellSelected(self, cell):  #check if a non-selected cell is in bounds
        (row, col) = cell
        selectedCellsCount = 0

        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if (drow, dcol) != (0, 0):
                    newRow, newCol = row+drow, col+dcol
                    if self.canvasBoard[newRow][newCol] == "red":
                        selectedCellsCount += 1
        return selectedCellsCount
    
    def isSelectionLegal(self):     #checks if a selection is legal
        selectedCellsList = Canvas.getSelectedCells(self)
        selectedCellsCount = 0
        originalNonCellsCount = 0
        self.makeSelectionCoors = []
        i = 0
        j = 0
        while (i < len(selectedCellsList)):
            selectedCell = selectedCellsList[i]
            # print(f"checking this selectedCell = {selectedCell}")
            nonSelectedCellsList = Canvas.findNonSelectedCells(self, selectedCell)
            # print(f"surrounding white cells list = {nonSelectedCellsList}\n")
            while(j < len(nonSelectedCellsList)):
                nonSelectedCell = nonSelectedCellsList[j]
                originalNonCellsCount = len(nonSelectedCellsList)
                selectedCellsCount = Canvas.isCellSelected(self, nonSelectedCell)
                # print(f"count of this cell {nonSelectedCell} = {selectedCellsCount}\n")
                if selectedCellsCount < 3:
                    nonSelectedCellsList.pop(j)
                    # print(f"new list = {nonSelectedCellsList}\n")
                    if nonSelectedCellsList == []:
                        return False
                else:
                    # print(f"new list = {nonSelectedCellsList}\n")
                    self.makeSelectionCoors.append((nonSelectedCell))
                    j += 1
            j = 0
            i += 1
            if selectedCell == selectedCellsList[-1]: return True
            # print(f'checking this selected cell = {selectedCell}')
            # print(f'updated selected cells list = {selectedCellsList}\n')
        return False

    def makeSelection(self):
        makeSelectionCellsSet = set(self.makeSelectionCoors)
        selectedCellsList = Canvas.getSelectedCells(self)
        firstSelectedCell = selectedCellsList[0]
        lastSelectedCell = selectedCellsList[-1]
        for elem in makeSelectionCellsSet:
            (row, col) = elem
            if (row > firstSelectedCell[0] and col > firstSelectedCell[-1] and
                row < lastSelectedCell[0] and col < lastSelectedCell[-1]):
                self.canvasBoard[row][col] = self.colors
    
    def changeSelectedColor(self):
        selectedCellsList = Canvas.getSelectedCells(self)
        for elem in selectedCellsList:
            (row, col) = elem
            self.canvasBoard[row][col] = self.prevColor
    
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
    
    def masterUndo(self, app, event):
        if self.lastDrawn != [] and len(self.allBoards) != 0:
            Canvas.undoLastPressed(self)
            Canvas.undoLastDragged(self)

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
            Canvas.masterUndo(self, app, event)
        
        elif event.key == "s": #makes a selection
            self.prevColor = self.colors
            self.isSelecting = not self.isSelecting #toggles isSelecting
            if self.isSelecting == True:
                self.colors = "red"
        
        elif event.key == "k" and self.isSelecting == True:
            #print(f'bounds check = {self.isSelectionLegal()}')
            if self.isSelectionLegal() == True:
                Canvas.makeSelection(self)
        
        elif event.key == "t":              #changes entire selection's color
            Canvas.changeSelectedColor(self)

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
            print(self.rows, self.cols)

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

    def drawSaveButton(self, app, canvas):
        for row in range(0, 2):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="dark gray",
                                        outline="black")
        canvas.create_text(x0, y0, text="save button", fill="red4")
    
    def drawGetRefButton(self, app, canvas):
        for row in range(0, 2):
            for col in range(5, 9):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="dark gray",
                                        outline="black")
        canvas.create_text(x0, y0, text="reference button", fill="red4")

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
        canvas.create_text(x0, y0, text="outline button", fill="red4")

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

    def saveButtonBounds(self, app, event):
        (row, col) = self.getCell_method(event.x, event.y)
        for row in range(0, 2):
            for col in range(0, 4):
                if app.selection == (row, col):
                    print("save button pressed")
                    pass
    
    def getRefButtonBounds(self, app, event):
        (row, col) = self.getCell_method(event.x, event.y)
        for row in range(0, 2):
            for col in range(5, 9):
                if app.selection == (row, col):
                    print("get ref button pressed")
                    pass
    
    def drawingButtonBounds(self, app, event):  #sets brush w/ bounds check
        (row, col) = self.getCell_method(event.x, event.y)
        app.selection = (row, col)
        for row in range(3, 7):
            for col in range(0, 4):
                if app.selection == (row, col):
                    return True
    
    def erasingButtonBounds(self, app, event):  #sets eraser w/ bounds check
        (row, col) = self.getCell_method(event.x, event.y)
        app.selection = (row, col)
        for row in range(8, 12):
            for col in range(0, 4):
                if app.selection == (row, col):
                    return True
    
    def undoButtonBounds(self, app, event): #sets a single undo press w/ button
        app.selection = self.getCell_method(event.x, event.y)
        for row in range(13, 17):
            for col in range(0, 4):
                if app.selection == (row, col):
                    app.canvasObject.undoButton = True
                    app.canvasObject.wasUndoClicked = True
    
    def selectionButtonBounds(self, app, event):   #sets selection feature w/ button
        app.selection = self.getCell_method(event.x, event.y)
        for row in range(18, 22):
            for col in range(0, 4):
                if app.selection == (row, col):
                    app.canvasObject.selectionButton = True
    
    '''Top Level Apps for Button Class'''

    def redrawAll(self, app, canvas):       #draws every button in the class
        Button.drawColorButtons(self, app, canvas)
        Button.drawDrawingButtons(self, app, canvas)
        Button.drawErasingButton(self, app, canvas)
        Button.drawUndoButton(self, app, canvas)
        Button.drawSelectButton(self, app, canvas)
        Button.drawSaveButton(self, app, canvas)
        Button.drawGetRefButton(self, app, canvas)

    def mousePressed(self, app, event):
        if Button.drawingButtonBounds(self, app, event) == True:    #draw
            app.canvasObject.isDrawing = True
            app.canvasObject.isErasing = False
            app.canvasObject.isSelecting = False

        elif Button.erasingButtonBounds(self, app, event) == True:  #erase
            app.canvasObject.isDrawing = False
            app.canvasObject.isErasing = True
            app.canvasObject.isSelecting = False

        # elif app.canvasObject.wasUndoClicked == False:              #undo
        #     Button.undoButtonBounds(self, app, event)
        #     app.canvasObject.masterUndo(app, event)

        Button.selectionButtonBounds(self, app, event)              #select

        if app.canvasObject.selectionButton == True:                #outline
            app.canvasObject.prevColor = self.colors
            app.canvasObject.isSelecting = not app.canvasObject.isSelecting
            if app.canvasObject.isSelecting == True:
                app.canvasObject.colors = "red"
                if app.canvasObject.isSelectionLegal() == True:
                    app.canvasObject.makeSelection()
        
        Button.saveButtonBounds(self, app, event)
        Button.getRefButtonBounds(self, app, event)

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

'''Helpers'''

def pickColor(app, event):  #allows user to pick a new color based off clicks
    app.selection = getCell(app, event.x, event.y)
    for row in range(42, 44):
        for col in range(5, 43):
            if app.selection == (row, col):
                if row == 42:
                    color = app.colorsList[col-5]
                else:
                    color = app.colorsList[col+row-10]
                app.canvasObject.colors = color

'''Controller'''

def mousePressed(app, event):
    app.canvasObject.mousePressedCanvas(event)  #from canvas class
    app.buttonObject.mousePressed(app, event)   #from button class
    pickColor(app, event)

    if app.canvasObject.undoButton == True:
        app.canvasObject.masterUndo(app, event)

    #from CMU 112 graphics (using for debugging)#
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#
    (row, col) = getCell(app, event.x, event.y)
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    # select this (row, col) unless it is selected
    if (app.selection == (row, col)):
        app.selection = (-1, -1)
    else:
        app.selection = (row, col)
        # print(row, col)
        # print(x0, x1, y0, y1)

def mouseDragged(app, event):
    app.canvasObject.mouseDraggedCanvas(event)      #from canvas class

def keyPressed(app, event):
    app.canvasObject.keyPressedCanvas(app, event)   #from canvas class

runApp(width=1000, height=1000, title='PixelArt')

#article I referenced for using OOP: https://blog.finxter.com/define-a-method-outside-of-the-class-definition/#

#flood fill --> backtracking, draw in a regular shape, fill all the boxes until it hits the wall#
#index out of range error when making too many cells, changing pixel size#
#undo button does not work properly T-T#
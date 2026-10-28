from cmu_112_graphics import *
import random, math, copy

'''
Jenna Gomes, jsgomes

article I referenced for using OOP: 
https://blog.finxter.com/define-a-method-outside-of-the-class-definition/

article I reference for pixelated images:
https://towardsdatascience.com/convert-photo-into-pixel-art-using-python-d0b9bd235797

source files and names for the images used in my project:
all icons were from Ranah's Pixel Studio (on iStock and iconfinder)

big thanks to my TA for helping me come up with so many ideas and cool algs!
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
        self.canvasBoard = [([self.emptyColor] * self.cols) for 
                                row in range(self.rows)]
        
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
        self.selectionButton = False

    '''Drawing the Canvas Functions'''

    def drawCanvasGrid(self, app, canvas):  #draws the initial empty canvas 
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
        
        elif event.key =="i":
            app.mode = "splashScreenMode"

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

        #images#
        self.pencilImg = app.loadImage("pencil icon.png")
        self.scalePencilImg = app.scaleImage(self.pencilImg, 1/4)
        self.eraserImg = app.loadImage("eraser icon.png")
        self.scaleEraserImg = app.scaleImage(self.eraserImg, 1/15)
        self.undoImg = app.loadImage("undo icon.png")
        self.scaleUndoImg = app.scaleImage(self.undoImg, 1/3.7)
        self.highlighterImg = app.loadImage("highlighter icon.png")
        self.scaleHighImg = app.scaleImage(self.highlighterImg, 1/4)
        self.saveImg = app.loadImage("save file icon.png")
        self.scaleSaveImg = app.scaleImage(self.saveImg, 1/7)
        self.getRefImg = app.loadImage("reference icon.png")
        self.scaleRefImg = app.scaleImage(self.getRefImg, 1/7)
    
    '''Drawing Functions'''

    def drawSaveButton(self, app, canvas):      #draws save file button
        imgX0, imgY0, imgX1, imgY1 = getCellBounds(app, 1, 2)
        for row in range(0, 2):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="pink1",
                                        width=0)
        canvas.create_image(imgX0, imgY0,
                image=ImageTk.PhotoImage(app.buttonObject.scaleSaveImg))
    
    def drawGetRefButton(self, app, canvas):   #draws get reference button
        imgX0, imgY0, imgX1, imgY1 = getCellBounds(app, 1, 7)
        for row in range(0, 2):
            for col in range(5, 9):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="pink1",
                                        width=0)
        canvas.create_image(imgX0, imgY0,
                image=ImageTk.PhotoImage(app.buttonObject.scaleRefImg))

    def drawDrawingButtons(self, app, canvas):  #draws drawing button
        imgX0, imgY0, imgX1, imgY1 = getCellBounds(app, 5, 2)
        for row in range(3, 7):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="pink1",
                                        width=0)
        canvas.create_image(imgX0, imgY0,
                image=ImageTk.PhotoImage(app.buttonObject.scalePencilImg))

    def drawErasingButton(self, app, canvas):   #draws erasing button
        imgX0, imgY0, imgX1, imgY1 = getCellBounds(app, 10, 2)
        for row in range(8, 12):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="pink1",
                                        width=0)
        canvas.create_image(imgX0, imgY0,
                image=ImageTk.PhotoImage(app.buttonObject.scaleEraserImg))

    def drawUndoButton(self, app, canvas):   #draws undo button
        imgX0, imgY0, imgX1, imgY1 = getCellBounds(app, 15, 2)
        for row in range(13, 17):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="pink1",
                                        width=0)
        canvas.create_image(imgX0, imgY0,
                image=ImageTk.PhotoImage(app.buttonObject.scaleUndoImg))
    
    def drawSelectButton(self, app, canvas):   #draws outline button
        imgX0, imgY0, imgX1, imgY1 = getCellBounds(app, 20, 2)
        for row in range(18, 22):
            for col in range(0, 4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, 
                                        fill="pink1",
                                        width=0)
        canvas.create_image(imgX0, imgY0,
                image=ImageTk.PhotoImage(app.buttonObject.scaleHighImg))

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

    def saveButton(self, app, event):         #set save feature
        (row, col) = self.getCell_method(event.x, event.y)
        for row in range(0, 2):
            for col in range(0, 4):
                if app.selection == (row, col):
                    snapshotImage = app.getSnapshot()
                    app.saveSnapshot()

    def getRefButtonBounds(self, app, event):       #sets new splash screen
        (row, col) = self.getCell_method(event.x, event.y)
        for row in range(0, 2):
            for col in range(5, 9):
                if app.selection == (row, col):
                    app.mode = "refMode"
    
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

        Button.undoButtonBounds(self, app, event)                   #undo

        Button.selectionButtonBounds(self, app, event)              #select

        if app.canvasObject.selectionButton == True:
            app.canvasObject.prevColor = self.colors
            app.canvasObject.isSelecting = not app.canvasObject.isSelecting
            if app.canvasObject.isSelecting == True:
                app.canvasObject.colors = "red"
                if app.canvasObject.isSelectionLegal() == True:
                    app.canvasObject.makeSelection()
        
        Button.saveButton(self, app, event)
        Button.getRefButtonBounds(self, app, event)

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
                                                fill="mistyrose")

def drawGridDesign(app, canvas):      #draws the grid background
    for row in range(0, app.rows):
        for col in range(0, app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, outline="pink1")

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
                                fill="pink1")

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
    canvas.create_rectangle(x0, y0, x1, y1, fill="pink1")

    #main box#
    canvas.create_rectangle(x0, y0, x1, y1+20,
                                fill="light gray")

##########################################
# Reference Mode
##########################################

def refMode_redrawAll(app, canvas):
    drawBackgroundColor(app, canvas)
    drawLabels(app, canvas)
    canvas.create_image(app.x0Reference, app.y0, image=ImageTk.PhotoImage(app.ogImage))
    canvas.create_image(app.x0Final, app.y0, image=ImageTk.PhotoImage(app.finalImage))

def refMode_keyPressed(app, event):
    if (event.key == 'Left'):
        app.mode = 'canvasMode'
    if (event.key == "s"):
        snapshotImage = app.getSnapshot()
        app.refSaveImage = app.scaleImage(snapshotImage, 2/5)
        app.saveSnapshot()
    if (event.key == "u"):
        app.tempUrlInput = app.getUserInput("Type a valid url address for images:")
        tempUrl = str(app.tempUrlInput)
        if (app.tempUrlInput == None):
            app.message = "You canceled!"
        else:
            app.url = tempUrl
            makePixelization(app)

def makePixelization(app):    #pixelizes an image using bilinear interpolation

    app.pixelSize = (100, 100)

    app.ogImage = app.loadImage(app.url)

    app.outputSize = app.ogImage.size

    findScale(app)  #func call

    app.resampledImage = app.ogImage.resize(app.pixelSize,Image.Resampling.BILINEAR)

    resizedImage = app.resampledImage.resize(app.outputSize,Image.Resampling.NEAREST)

    app.finalImage = app.scaleImage(resizedImage, 1/1)

    app.ogImage = app.scaleImage(app.ogImage, app.scale)

    app.finalImage = app.scaleImage(app.finalImage, app.scale)

def findScale(app):          #scales the image depending on orig. dimensions
    dimension = app.outputSize[0]
    if 550 <= dimension <= 850:     #med images
        app.scale = 3/5
    elif 150 <= dimension <= 550:   #small images
        app.scale = 2/3
    elif 850 <= dimension <= 1000:  #large images
        app.scale = 1/3 
    else:                           #other images
        app.scale = 1/5

def drawLabels(app, canvas):
    x0OG = app.x0Reference//2 + app.refMargin//20              #rectangle 1
    y0 = 0 + app.refMargin//2
    x1OG = x0OG + app.refMargin
    y1 = y0 - app.refMargin//5
    canvas.create_rectangle(x0OG, y0, x1OG, y1, fill="mistyRose", 
                                    outline="pink1", width=4)
    
    x0Text = (x0OG + x1OG)//2                               #text 1
    y0Text = (y0 + y1)//2

    canvas.create_text(x0Text, y0Text, text="Original Photo!", 
                                font="Arial 24 italic", fill="pink1")

    x0Ref = app.width - app.x0Reference//2 - app.refMargin//20 #rectangel 2
    x1Ref = x0Ref - app.refMargin
    canvas.create_rectangle(x0Ref, y0, x1Ref, y1, fill="mistyRose", 
                                        outline="pink1", width=4)

    x0Text2 = (x0Ref + x1Ref)//2                            #text 2

    canvas.create_text(x0Text2, y0Text, text="Reference Photo!", 
                                font="Arial 24 italic", fill="pink1")

    #instructions for user#
    canvas.create_text(x0Text, app.width-100, fill="violetred3",
                                font="Arial 18 italic",
                                text=app.message)
    canvas.create_text(x0Text2, app.width-100, fill="violetred3",
                                font="Arial 18 italic",
                                text='Press s to saveSnapshot')

##########################################
# Canvas Mode Funcs
##########################################

'''View'''

def canvasMode_redrawAll(app, canvas):
    drawBGColor(app, canvas)
    app.canvasObject.drawCanvasGrid(app, canvas)     #from canvas class
    drawGrid(app, canvas)
    app.buttonObject.redrawAll(app, canvas)          #from button class

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

def canvasMode_mousePressed(app, event):
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
        print(row, col)
        print(x0, x1, y0, y1)

def canvasMode_mouseDragged(app, event):
    app.canvasObject.mouseDraggedCanvas(event)      #from canvas class

def canvasMode_keyPressed(app, event):
    app.canvasObject.keyPressedCanvas(app, event)   #from canvas class

##########################################
# Main App
##########################################

'''Model'''

def appStarted(app):
    app.margin = 25
    app.bgMessage = "Pick a color"
    app.mode = "splashScreenMode"
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

    #reference mode#
    app.refMargin = 1000//4
    app.x0Reference = 0 + app.refMargin
    app.y0 = app.height//2 - app.refMargin//4
    app.x0Final = app.width - app.refMargin
    app.outputSize = (0, 0)
    app.refSaveImage = None
    app.tempUrlInput = None
    app.url = "https://miro.medium.com/max/1400/1*7hmVASeQkXr4V32csJHZLw.jpeg"
    app.message = "Press u to insert url"
    findScale(app)                              #func calls
    makePixelization(app)                       #scale and ref img

    #make new objects here#
    app.canvasObject = Canvas(app)
    app.buttonObject = Button(app)

runApp(width=1000, height=1000, title='PixelArt')
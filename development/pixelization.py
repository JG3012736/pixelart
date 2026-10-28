from cmu_112_graphics import * 
import math 

###########################
### Pixelization     ######
###########################

def appStarted(app):
    app.margin = 1000//4

    app.x0Reference = 0 + app.margin
    app.y0 = app.height//2 - app.margin//4
    app.x0Final = app.width - app.margin

    app.makePixelizationImages = makePixelization(app) #calls pixelization func

#code (lines 30-35) and logic framework is loosely referenced off of this article:
#https://towardsdatascience.com/convert-photo-into-pixel-art-using-python-d0b9bd235797#

def makePixelization(app):    #pixelizes an image using bilinear interpolation

    # app.url = "https://i.redd.it/ghevrggssjh71.jpg"   #small image

    app.url = "https://miro.medium.com/max/1400/1*7hmVASeQkXr4V32csJHZLw.jpeg"    #med image

    # app.url = "https://static.vecteezy.com/system/resources/previews/003/127/913/original/cute-axolotl-illustration-design-free-vector.jpg"
    
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
    x0OG = app.x0Reference//2 + app.margin//20              #rectangle 1
    y0 = 0 + app.margin//2
    x1OG = x0OG + app.margin
    y1 = y0 - app.margin//5
    canvas.create_rectangle(x0OG, y0, x1OG, y1, fill="mistyRose", 
                                    outline="pink1", width=4)
    
    x0Text = (x0OG + x1OG)//2                               #text 1
    y0Text = (y0 + y1)//2

    canvas.create_text(x0Text, y0Text, text="Original Photo!", 
                                font="Arial 24 italic", fill="pink1")

    x0Ref = app.width - app.x0Reference//2 - app.margin//20 #rectangel 2
    x1Ref = x0Ref - app.margin
    canvas.create_rectangle(x0Ref, y0, x1Ref, y1, fill="mistyRose", 
                                        outline="pink1", width=4)

    x0Text2 = (x0Ref + x1Ref)//2                            #text 2

    canvas.create_text(x0Text2, y0Text, text="Reference Photo!", 
                                font="Arial 24 italic", fill="pink1")

def drawInsertImageBox(app, canvas):
    pass

def boundInsertImageBox(app, canvas, event):
    pass

def drawSaveBox(app, canvas):
    pass

def boundSaveBox(app, canvas, event):
    pass

def mousePressed(app, canvas, event):
    if boundSaveBox(app, canvas, event) == True:
        pass
    elif boundInsertImageBox(app, canvas, event) == True:
        pass

def redrawAll(app, canvas):
    #draws the label boxes#
    drawLabels(app, canvas)
    #draws the two images side by side#
    canvas.create_image(app.x0Reference, app.y0, image=ImageTk.PhotoImage(app.ogImage))
    canvas.create_image(app.x0Final, app.y0, image=ImageTk.PhotoImage(app.finalImage))

runApp(width=1000, height=1000)
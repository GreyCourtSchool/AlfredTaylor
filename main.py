import serial,evdev,time,os,sys

def setupScreen():
    global temparray
    temparray=[]
    for i in range(0,19):
        temparray.append("XXXXXXXXX\n")                      
    for i in range(0,19):
        sys.stdout.write(temparray[i])

def updatePixel(x,y,colorcode):
    blank=os.system("clear")
    if colorcode==1:
        temparray[y]=(temparray[y][0:x]+"X"+temparray[y][x+1:10])
    else:
        temparray[y]=(temparray[y][0:x]+"#"+temparray[y][x+1:10])
    for i in reversed(temparray):
        sys.stdout.write(i)
    print("\n")
    #running arduino code using the pi (not sure about implementation yet)
    #COLOR CODES:
    #1 Empty
    #2 White Lettering
    #3 Red Z
    #4 Green S
    #5 Blue J
    #6 Yellow O
    #7 Orange L
    #8 Cyan I
    #9 Purple T

class sprite:
    #sprite is defined with a name, a list of pixels (each with x,y,color values)
    #and a location (x,y) value
    def __init__(self,name,pixels,location):
        self.name=name
        self.pixels=pixels
        self.location=location
    def drawSprite(self):#updates the pixels at the co oridinates of the pixels relative to the position of the piece and makes them the color of the piece
        for pixel in self.pixels:
            updatePixel(pixel[0]+self.location[0],pixel[1]+self.location[1],pixel[2])
    def eraseSprite(self):#updates all the pixels at the co ordinates relative to the position to 0 making them black
        for pixel in self.pixels:
            updatePixel(pixel[0]+self.location[0],pixel[1]+self.location[1],1)

class piece(sprite):
    def __init__(self,name,shape,location,rot):
        self.name=name
        self.shape=shape
        self.location=location
        self.pixels=[]
        self.updateShape(shape,rot)
    def updateShape(self,shape,rot):
        #This long if series sets the pixels of the sprite according to the shape with
        #a lil diagram next to it # is a block and X is the centre
        if shape=="O": #If the shape is an O piece there is no need for rotation
            self.pixels=[[0,0,6],[1,0,6],[0,1,6],[1,1,6]]
        #Normal rotation
        elif rot==0:
            if shape=="I":
                self.pixels=[[-1,0,8],[0,0,8],[1,0,8],[2,0,5]]
                #X##
            elif shape=="J":
                self.pixels=[[-1,1,5],[-1,0,5],[0,0,5],[-1,0,5]]
                #
                #X#
            elif shape=="L":
                self.pixels=[[-1,0,7],[0,0,7],[1,0,7],[1,1,7]]
                  #
                #X#
            elif shape=="S":
                self.pixels=[[-1,0,4],[0,0,4],[0,1,4],[1,1,4]]
                 ##
                #X
            elif shape=="T":
                self.pixels=[[-1,0,9],[0,0,9],[0,1,9],[1,0,9]]
                 #
                #X#
            elif shape=="Z":
                self.pixels=[[-1,1,3],[0,0,3],[0,1,3],[1,0,3]]
                ##
        #        X#

        #Clockwise rotation
        elif rot==1:
            if shape=="I":
                self.pixels=[[1,2,8],[1,0,8],[1,-1,8],[1,-2,5]]
                #
        #      X#
                #
                #
            elif shape=="J":
                self.pixels=[[0,1,5],[1,1,5],[0,0,5],[0,-1,5]]
                ##
        #       X
                #
            elif shape=="L":
                self.pixels=[[-1,0,7],[0,0,7],[1,0,7],[1,1,7]]
                  #
                #X#
            elif shape=="S":
                self.pixels=[[0,1,4],[0,0,4],[0,1,4],[1,-1,4]]
                 #
       #         X#
                  #
            elif shape=="T":
                self.pixels=[[0,1,9],[0,0,9],[1,0,9],[0,-1,9]]
                #
        #       X#
                #
            elif shape=="Z":
                self.pixels=[[1,1,3],[0,0,3],[1,0,3],[0,-1,3]]
                 #
            #   X#
                #

        # Double rotation
        elif rot==2:
            if shape=="I":
                self.pixels=[[-1,-1,8],[0,-1,8],[1,-1,8],[2,-1,8]]
        #       X
               ####
            elif shape=="J":
                self.pixels=[[-1,0,5],[0,0,5],[1,0,5],[2,0,5]]
                #X#
                  #
            elif shape=="L":
                self.pixels=[[-1,-1,7],[-1,0,7],[0,0,7],[1,0,7]]
                #X#
                #
            elif shape=="S":
                self.pixels=[[-1,-1,4],[0,-1,4],[0,0,4],[1,0,4]]
        #        X#
                ##
            elif shape=="T":
                self.pixels=[[-1,0,9],[0,0,9],[0,-1,9],[1,0,-9]]
                #X#
                 #
            elif shape=="Z":
                self.pixels=[[-1,0,3],[0,0,3],[0,-1,3],[1,-1,3]]
                #X
                 ##

        # Anticlockwise rotation
        elif rot==3:
            if shape=="I":
                self.pixels=[[0,1,8],[0,0,8],[0,-1,8],[0,-2,8]]
                #
        #       X
                #
                #
            elif shape=="J":
                self.pixels=[[0,1,5],[0,0,5],[0,-1,5],[-1,-1,5]]
                #
        #       X
               ##
            elif shape=="L":
                self.pixels=[[-1,1,7],[0,1,7],[0,0,7],[0,-1,7]]
                ##
        #        X
                 #
            elif shape=="S":
                self.pixels=[[-1,1,4],[-1,0,4],[0,0,4],[0,-1,4]]
                #
                #X
                 #
            elif shape=="T":
                self.pixels=[[0,1,9],[-1,0,9],[0,0,9],[0,-1,9]]
                 #
                #X
                 #
            elif shape=="Z":
                self.pixels=[[0,1,3],[0,0,3],[-1,0,3],[-1,-1,3]]
                 #
                #X
                #
    def checkTranslation(self,grid,vector):
        for pixel1 in self.pixels:
            x1=pixel1[0]+self.location[0]+vector[0]
            y1=pixel1[1]+self.location[1]+vector[1]
            for pixel2 in grid.pixels:
                x2=pixel2[0]+grid.location[0]
                y2=pixel2[1]+grid.location[1]
                if (x1==x2 and y1==y2):
                    return False
        return True
        #checks if a piece can be moved
    def translatePiece(self,vector):
        self.eraseSprite()
        self.location[0]+=vector[0]
        self.location[1]+=vector[1]
        self.drawSprite()
        #Translates piece
    def rotatePiece(self,grid,dir):
        ###CYCLE 2
        print()
class character(piece):
    #the letter class is like the shape but instead of strings defining the shape, they are defined by integers from 0 to 25 so that they can be scrolled through later
    # 0-A 1-B 2-C 3-D 4-E 5-F 6-G 7-H 8-I 9-J 10-K 11-L 12-M 13-N 14-O 15-P 16-Q 17-R 18-S 19-T 20-U 21-V 22-W 23-X 24-Y 25-Z
    #borrowed from https://robey.lag.net/2010/01/23/tiny-monospace-font.html
    def updateShape(self,shape,rot):
        if shape==0:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[1,4,2]]
             #
            # #
            ###
            # #
        #   X #
        elif shape==1:
            self.pixels=[[0,0,2],[1,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2]]
            ##
            # #
            ##
            # #
        #   X#
        elif shape==2:
            self.pixels=[[1,0,2],[2,0,2],[0,1,2],[0,2,2],[0,3,2],[1,4,2],[2,4,2]]
             ##
            #
            #
            #
        #   X##
        elif shape==3:
            self.pixels=[[0,0,2],[1,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2]]
            ##
            # #
            # #
            # #
        #   X#
        elif shape==4:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            #
            ###
            #
        #   X##
        elif shape==5:
            self.pixels=[[0,0,2],[0,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            #
            ###
            #
        #   X
        elif shape==6:
            self.pixels=[[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[1,4,2],[2,4,2]]
             ##
            #
            ###
            # #
        #   X##
        elif shape==7:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            ###
            # #
        #   X #
        elif shape==8:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[1,1,2],[1,2,2],[1,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
             #
             #
             #
        #   X##
        elif shape==9:
            self.pixels=[[1,0,2],[0,1,2],[2,1,2],[2,2,2],[2,3,1,],[2,4,2]]
              #
              #
              #
            # #
        #   X#
        elif shape==10:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            ##
            # #
        #   X #
        elif shape==11:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[0,2,2],[0,3,2],[0,4,2]]
            #
            #
            #
            #
        #   X##
        elif shape==12:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[1,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            ###
            ###
            # #
        #   X #
        elif shape==13:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[1,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[1,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            ###
            ###
            ###
        #   X #
        elif shape==14:
            self.pixels=[[1,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[1,4,2]]
             #
            # #
            # #
            # #
        #   X#
        elif shape==15:
            self.pixels=[[0,0,2],[0,1,2],[0,2,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2]]
            ##
            # #
            ##
            #
        #   X
        elif shape==16:
            self.pixels=[[1,0,2],[2,0,2],[0,1,2],[1,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[1,4,2]]
             #
            # #
            # #
            ###
        #   X##
        elif shape==17:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[1,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2]]
            ##
            # #
            ###
            ##
        #   X #
        elif shape==18:
            self.pixels=[[0,0,2],[1,0,2],[2,1,2],[1,2,2],[0,3,2],[1,4,2],[2,4,2]]
             ##
            #
             #
              #
        #   X#
        elif shape==19:
            self.pixels=[[1,0,2],[1,1,2],[1,2,2],[1,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
             #
             #
             #
        #   X#
        elif shape==20:
            self.pixels=[[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            # #
            # #
             ##
        elif shape==21:
            self.pixels=[[1,0,2],[1,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            # #
             #
        #   X#
        elif shape==22:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[1,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            ###
            ###
        #   X #
        elif shape==23:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
             #
            # #
        #   X #
        elif shape==24:
            self.pixels=[[1,0,2],[1,1,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
             #
             #
        #   X#
        elif shape==25:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[1,2,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
              #
             #
            #
        #   X##
        elif shape==26:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            # #
            # #
            # #
        #   X##
        elif shape==27:
            self.pixels=[[1,0,2],[1,1,2],[1,2,2],[1,3,2],[1,4,2]]
             #
             #
             #
             #
        #   X#
        elif shape==28:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[0,2,2],[1,2,2][2,2,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
              #
            ###
            #
        #   X##
        elif shape==29:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[2,1,2],[1,2,2],[2,2,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
              #
             ##
              #
        #   X##
        elif shape==30:
            self.pixels=[[2,0,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            ###
              #
        #   X #
        elif shape==31:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            #
            ###
              #
        #   X##
        elif shape==32:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[1,4,2],[2,4,2]]
             ##
            #
            ###
            # #
        #   X##
        elif shape==33:
            self.pixels=[[0,0,2],[0,1,2],[1,2,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
              #
             #
            #
        #   X
        elif shape==34:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            # #
            ###
            # #
        #   X##
        elif shape==35:
            self.pixels=[[0,0,2],[1,0,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            # #
            ###
              #
        #   X#



def removeSprites(items):
    for item in items:
        item.eraseSprite()
    items=[]
def waitForInput(gamepad,t):
    #Returns any buttons pressed after time t, if t is 0 it waits indefinitely
    timeDone=False
    inputRecieved=False
    start=time.clock()
    while(not timeDone or not inputRecieved):
            event=gamepad.read_one()
            if event!=None:
                    if event.type!=0 and event.type!=4:
                            padin=""
                            if (event.type==1 and event.value!=0L):
                                    if event.code==304:
                                            padin="A"
                                    elif event.code==305:
                                            padin="B"
                                    elif event.code==312:
                                            padin="SELECT"
                                    elif event.code==313:
                                            padin="START"
                            elif (event.type==3 and event.value!=127L):
                                    if event.code==1:
                                            if event.value==0L:
                                                    padin="UP"
                                            elif event.value==255L:
                                                    padin="DOWN"
                                    elif event.code==0:
                                            if event.value==0L:
                                                    padin="LEFT"
                                            if event.value==255L:
                                                    padin="RIGHT"
                            inputRecieved=True
                            return(padin)
            if t!=0:
                    if (time.clock()-start>t):
                            timeDone=True
                            return(None)

def runMenu():
    items=[piece("gameSelect","T",[4,13],0),piece("pointer","I",[4,11],0),character("scoreSelect",18,[4,3],0)]
    for item in items:
        item.drawSprite()
    selected="game"
    confirmed=False
    while (not confirmed):
        userin=waitForInput(gamePad,0)
        if (userin=="DOWN" and selected=="game"):
            items[1].translatePiece([0,-10])
            selected="scores"
        if (userin=="UP" and selected=="scores"):
            items[1].translatePiece([0,10])
            selected="game"
        if userin=="A":
            confirmed==True
    removeSprites(items)
    if selected=="game":
        runGame()
    if selected=="scores":
        runScores()

    removeSprites(items)

def runGame():
    items=[sprite("grid",[],[0,0])]
    score=0
    gameover=False
    T=0.5
    userin=""
    allpieces=[piece("iPiece","I",[6,20],0),piece("jPiece","J",[6,20],0),piece("lPiece","L",[6,20],0),piece("sPiece","S",[6,20],0),piece("oPiece","O",[6,20],0),piece("zPiece","Z",[6,20],0),piece("tPiece","T",[6,20],0)]
    nextpiece=random.choice(allpieces)
    bag=[]
    while(not userin=="START"):
        userin=waitforInput(gamePad,0)
    while(not gameover):
        if bag==None:
            bag=random.shuffle(allpieces)
        
            

def runScores():
    items=[]

####################
####MAIN PROGRAM####
####################
setupScreen()
gamePad=evdev.InputDevice("/dev/input/event0") #Placeholder path to device /dev/input/eventN
while True:
    runMenu()

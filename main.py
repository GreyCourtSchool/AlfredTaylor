import serial,evdev,time,os,sys,random,copy

def setupScreen():
    global temparray
    temparray=[]
    for i in range(0,20):
        temparray.append("____________\n")
    for i in reversed(temparray):
            sys.stdout.write(i)
    print("\n")

def updatePixel(x,y,colorcode):
    blank=os.system("clear")
    if (y<20 and x<12 and y>=0 and x>=0): #Allows drawing outside of the screen but wont try and render it
        if colorcode==1:
            temparray[y]=(temparray[y][:x]+"_"+temparray[y][x+1:])
        else:
            temparray[y]=(temparray[y][:x]+"#"+temparray[y][x+1:])
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
        for i in reversed(temparray):
            sys.stdout.write(i)
        print("\n")
    def eraseSprite(self):#updates all the pixels at the co ordinates relative to the position to 0 making them black
        for pixel in self.pixels:
            updatePixel(pixel[0]+self.location[0],pixel[1]+self.location[1],1)
        for i in reversed(temparray):
            sys.stdout.write(i)
        print("\n")

class piece(sprite):
    def __init__(self,name,shape,location,rot):
        self.name=name
        self.shape=shape
        self.location=location
        self.rot=rot
        self.pixels=[]
        self.updateShape()
    def updateShape(self):
        #This long if series sets the pixels of the sprite according to the shape with
        #a lil diagram next to it # is a block and X is the centre
        if self.shape=="O": #If the shape is an O piece there is no need for rotation
            self.pixels=[[0,0,6],[1,0,6],[0,1,6],[1,1,6]]
        #Normal rotation
        elif self.rot==0:
            if self.shape=="I":
                self.pixels=[[-1,0,8],[0,0,8],[1,0,8],[2,0,5]]
                #X##
            elif self.shape=="J":
                self.pixels=[[-1,1,5],[-1,0,5],[0,0,5],[-1,0,5]]
                #
                #X#
            elif self.shape=="L":
                self.pixels=[[-1,0,7],[0,0,7],[1,0,7],[1,1,7]]
                  #
                #X#
            elif self.shape=="S":
                self.pixels=[[-1,0,4],[0,0,4],[0,1,4],[1,1,4]]
                 ##
                #X
            elif self.shape=="T":
                self.pixels=[[-1,0,9],[0,0,9],[0,1,9],[1,0,9]]
                 #
                #X#
            elif self.shape=="Z":
                self.pixels=[[-1,1,3],[0,0,3],[0,1,3],[1,0,3]]
                ##
        #        X#

        #Clockwise rotation
        elif self.rot==1:
            if self.shape=="I":
                self.pixels=[[1,2,8],[1,0,8],[1,-1,8],[1,-2,5]]
                #
        #      X#
                #
                #
            elif self.shape=="J":
                self.pixels=[[0,1,5],[1,1,5],[0,0,5],[0,-1,5]]
                ##
        #       X
                #
            elif self.shape=="L":
                self.pixels=[[-1,0,7],[0,0,7],[1,0,7],[1,1,7]]
                  #
                #X#
            elif self.shape=="S":
                self.pixels=[[0,1,4],[0,0,4],[0,1,4],[1,-1,4]]
                 #
       #         X#
                  #
            elif self.shape=="T":
                self.pixels=[[0,1,9],[0,0,9],[1,0,9],[0,-1,9]]
                #
        #       X#
                #
            elif self.shape=="Z":
                self.pixels=[[1,1,3],[0,0,3],[1,0,3],[0,-1,3]]
                 #
            #   X#
                #

        # Double rotation
        elif self.rot==2:
            if self.shape=="I":
                self.pixels=[[-1,-1,8],[0,-1,8],[1,-1,8],[2,-1,8]]
        #       X
               ####
            elif self.shape=="J":
                self.pixels=[[-1,0,5],[0,0,5],[1,0,5],[2,0,5]]
                #X#
                  #
            elif self.shape=="L":
                self.pixels=[[-1,-1,7],[-1,0,7],[0,0,7],[1,0,7]]
                #X#
                #
            elif self.shape=="S":
                self.pixels=[[-1,-1,4],[0,-1,4],[0,0,4],[1,0,4]]
        #        X#
                ##
            elif self.shape=="T":
                self.pixels=[[-1,0,9],[0,0,9],[0,-1,9],[1,0,-9]]
                #X#
                 #
            elif self.shape=="Z":
                self.pixels=[[-1,0,3],[0,0,3],[0,-1,3],[1,-1,3]]
                #X
                 ##

        # Anticlockwise rotation
        elif self.rot==3:
            if self.shape=="I":
                self.pixels=[[0,1,8],[0,0,8],[0,-1,8],[0,-2,8]]
                #
        #       X
                #
                #
            elif self.shape=="J":
                self.pixels=[[0,1,5],[0,0,5],[0,-1,5],[-1,-1,5]]
                #
        #       X
               ##
            elif self.shape=="L":
                self.pixels=[[-1,1,7],[0,1,7],[0,0,7],[0,-1,7]]
                ##
        #        X
                 #
            elif self.shape=="S":
                self.pixels=[[-1,1,4],[-1,0,4],[0,0,4],[0,-1,4]]
                #
                #X
                 #
            elif self.shape=="T":
                self.pixels=[[0,1,9],[-1,0,9],[0,0,9],[0,-1,9]]
                 #
                #X
                 #
            elif self.shape=="Z":
                self.pixels=[[0,1,3],[0,0,3],[-1,0,3],[-1,-1,3]]
                 #
                #X
                #
    def checkTranslation(self,grid,vector):
        for pixel1 in self.pixels:
            x1=pixel1[0]+self.location[0]+vector[0]
            y1=pixel1[1]+self.location[1]+vector[1]
            if ((x1<0) or (x1>11) or (y1<0)):
                return False
            for pixel2 in grid.pixels:
                x2=pixel2[0]+grid.location[0]
                y2=pixel2[1]+grid.location[1]
                if ((x1==x2 and y1==y2)):
                    return False
        return True
        #checks if a piece can be moved
    def translatePiece(self,vector):
        self.eraseSprite()
        self.location[0]+=vector[0]
        self.location[1]+=vector[1]
        self.drawSprite()
        #Translates piece
    def rotatePiece(self,grid,rotdir):
        if (self.shape!="O"):
            #[0] - I shape data
            #[1] - J,L,S,T,Z shape data
            #[X,0] 0->1
            #[X,1] 1->0
            #[X,2] 1->2
            #[X,3] 2->1
            #[X,4] 2->3
            #[X,5] 3->2
            #[X,6] 3->0
            #[X,7] 0->3
            bigtests=[ [ [ [0,0],[-2,0],[1,0],[-2,1],[1,2] ],[ [0,0],[2,0],[-1,0],[2,1],[-1,2] ],[ [0,0],[-1,0],[2,0],[-1,2],[2,-1] ],[ [0,0],[1,0],[-2,0],[1,-2],[-2,1] ],[ [0,0],[2,0],[-1,0],[2,1],[-1,-2] ],[ [0,0],[-2,0],[1,0],[-2,-1],[1,2] ],[ [0,0],[1,0],[-2,0],[1,-2],[-2,1] ],[ [0,0],[-1,0],[2,0],[-1,2],[2,-1] ] ]
                       , [ [ [0,0],[-1,0],[-1,1],[0,-2],[-1,2] ],[ [0,0],[1,0],[1,-1],[0,2],[1,2] ],[ [0,0],[1,0],[1,-1],[0,2],[1,2] ],[ [0,0],[-1,0],[-1,1],[0,-2],[-1,-2] ],[ [0,0],[1,0],[1,1],[0,-2],[1,-2] ],[ [0,0],[-1,0],[-1,-1],[0,2],[-1,2] ],[ [0,0],[-1,0],[-1,-1],[0,2],[-1,2] ],[ [0,0],[1,0],[1,1],[0,-2],[1,-2] ] ] ]
            tests=[]
            a=0
            b=0
            if self.shape=="I":
                a=0 
            else:
                a=1
            if self.rot==0:
                if rotdir==1:
                    b=0
                else:
                    b=7
            elif self.rot==1:
                if rotdir==1:
                    b=2
                else:
                    b=1
            elif self.rot==2:
                if rotdir==1:
                    b=4
                else:
                    b=3
            elif self.rot==3:
                if rotdir==1:
                    b=6
                else:
                    b=5
            tests=bigtests[a][b]
            i=0
            checking=True
            self.rot+=rotdir
            self.updateShape()
            while checking:
                if self.checkTranslation(grid,tests[i]):
                    self.translatePiece(tests[i])
                    checking=False
                elif i==4:
                    self.rot+=(-rotdir)
                    self.updateShape()
                    checking=False

class character(piece):
    #the letter class is like the shape but instead of strings defining the shape, they are defined by integers from 0 to 25 so that they can be scrolled through later
    # 0-A 1-B 2-C 3-D 4-E 5-F 6-G 7-H 8-I 9-J 10-K 11-L 12-M 13-N 14-O 15-P 16-Q 17-R 18-S 19-T 20-U 21-V 22-W 23-X 24-Y 25-Z
    #borrowed from https://robey.lag.net/2010/01/23/tiny-monospace-font.html
    def updateShape(self):
        if self.shape==0:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[1,4,2]]
             #
            # #
            ###
            # #
        #   X #
        elif self.shape==1:
            self.pixels=[[0,0,2],[1,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2]]
            ##
            # #
            ##
            # #
        #   X#
        elif self.shape==2:
            self.pixels=[[1,0,2],[2,0,2],[0,1,2],[0,2,2],[0,3,2],[1,4,2],[2,4,2]]
             ##
            #
            #
            #
        #   X##
        elif self.shape==3:
            self.pixels=[[0,0,2],[1,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2]]
            ##
            # #
            # #
            # #
        #   X#
        elif self.shape==4:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            #
            ###
            #
        #   X##
        elif self.shape==5:
            self.pixels=[[0,0,2],[0,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            #
            ###
            #
        #   X
        elif self.shape==6:
            self.pixels=[[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[1,4,2],[2,4,2]]
             ##
            #
            ###
            # #
        #   X##
        elif self.shape==7:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            ###
            # #
        #   X #
        elif self.shape==8:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[1,1,2],[1,2,2],[1,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
             #
             #
             #
        #   X##
        elif self.shape==9:
            self.pixels=[[1,0,2],[0,1,2],[2,1,2],[2,2,2],[2,3,1,],[2,4,2]]
              #
              #
              #
            # #
        #   X#
        elif self.shape==10:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            ##
            # #
        #   X #
        elif self.shape==11:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[0,2,2],[0,3,2],[0,4,2]]
            #
            #
            #
            #
        #   X##
        elif self.shape==12:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[1,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            ###
            ###
            # #
        #   X #
        elif self.shape==13:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[1,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[1,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            ###
            ###
            ###
        #   X #
        elif self.shape==14:
            self.pixels=[[1,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[1,4,2]]
             #
            # #
            # #
            # #
        #   X#
        elif self.shape==15:
            self.pixels=[[0,0,2],[0,1,2],[0,2,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2]]
            ##
            # #
            ##
            #
        #   X
        elif self.shape==16:
            self.pixels=[[1,0,2],[2,0,2],[0,1,2],[1,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[1,4,2]]
             #
            # #
            # #
            ###
        #   X##
        elif self.shape==17:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[1,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2]]
            ##
            # #
            ###
            ##
        #   X #
        elif self.shape==18:
            self.pixels=[[0,0,2],[1,0,2],[2,1,2],[1,2,2],[0,3,2],[1,4,2],[2,4,2]]
             ##
            #
             #
              #
        #   X#
        elif self.shape==19:
            self.pixels=[[1,0,2],[1,1,2],[1,2,2],[1,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
             #
             #
             #
        #   X#
        elif self.shape==20:
            self.pixels=[[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            # #
            # #
             ##
        elif self.shape==21:
            self.pixels=[[1,0,2],[1,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            # #
             #
        #   X#
        elif self.shape==22:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[1,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            ###
            ###
        #   X #
        elif self.shape==23:
            self.pixels=[[0,0,2],[2,0,2],[0,1,2],[2,1,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
             #
            # #
        #   X #
        elif self.shape==24:
            self.pixels=[[1,0,2],[1,1,2],[1,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
             #
             #
        #   X#
        elif self.shape==25:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[1,2,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
              #
             #
            #
        #   X##
        elif self.shape==26:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            # #
            # #
            # #
        #   X##
        elif self.shape==27:
            self.pixels=[[1,0,2],[1,1,2],[1,2,2],[1,3,2],[1,4,2]]
             #
             #
             #
             #
        #   X#
        elif self.shape==28:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[0,2,2],[1,2,2][2,2,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
              #
            ###
            #
        #   X##
        elif self.shape==29:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[2,1,2],[1,2,2],[2,2,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
              #
             ##
              #
        #   X##
        elif self.shape==30:
            self.pixels=[[2,0,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[2,4,2]]
            # #
            # #
            ###
              #
        #   X #
        elif self.shape==31:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            #
            ###
              #
        #   X##
        elif self.shape==32:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[2,2,2],[0,3,2],[1,4,2],[2,4,2]]
             ##
            #
            ###
            # #
        #   X##
        elif self.shape==33:
            self.pixels=[[0,0,2],[0,1,2],[1,2,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
              #
             #
            #
        #   X
        elif self.shape==34:
            self.pixels=[[0,0,2],[1,0,2],[2,0,2],[0,1,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            # #
            ###
            # #
        #   X##
        elif self.shape==35:
            self.pixels=[[0,0,2],[1,0,2],[2,1,2],[0,2,2],[1,2,2],[2,2,2],[0,3,2],[2,3,2],[0,4,2],[1,4,2],[2,4,2]]
            ###
            # #
            ###
              #
        #   X#


def drawItems(items):
    for item in items:
        item.drawSprite()
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
    items=[piece("gameSelect","T",[5,13],0),piece("pointer","I",[5,11],0),character("scoreSelect",18,[5,3],0)]
    drawItems(items)
    selected="game"
    choosing=True
    while (choosing):
        userin=waitForInput(gamePad,0)
        if (userin=="DOWN" and selected=="game"):
            items[1].translatePiece([0,-10])
            selected="scores"
        if (userin=="UP" and selected=="scores"):
            items[1].translatePiece([0,10])
            selected="game"
        if (userin=="A"):
            print("A pressed")
            choosing=False
    removeSprites(items)
    if selected=="game":
        print("Running game")
        runGame()
    if selected=="scores":
        print("Running scores")
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
    pick=0
    print("Press start to begin")
    while(userin!="START"):
        userin=waitForInput(gamePad,0)
    while(not gameover):
        items.append(copy.copy(nextpiece))
        drawItems(items)
        if pick<0:
            random.shuffle(allpieces)
            pick=6
        nextpiece=allpieces[pick]
        print("PREVIEW: "+nextpiece.name)
        pick+=-1
        moving=True
        while(moving):
            userin=waitForInput(gamePad,T)
            #CONTROL STUFF
            if userin=="UP":
                items[1].rotatePiece(items[0],1)
            elif userin=="DOWN":
                items[1].rotatePiece(items[0],-1)
            
            if items[1].checkTranslation(items[0],[0,-1]):
                items[1].translatePiece([0,-1])
                #Also need to check for out of bounds
            else:
                moving=False
        for pixel in items[1].pixels:
            items[0].pixels+=[[pixel[0]+items[1].location[0],pixel[1]+items[1].location[1],pixel[2]]]
        items[1].eraseSprite()
        del items[1]
def runScores():
    items=[]

####################
####MAIN PROGRAM####
####################
setupScreen()
gamePad=evdev.InputDevice("/dev/input/event0") #Placeholder path to device /dev/input/eventN
while True:
    runMenu()

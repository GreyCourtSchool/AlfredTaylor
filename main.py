import serial
def updatePixel(x,y,colorcode):
    print("Not implemented")
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
    def drawSprite(self):
        for i in range(0,len(self.pixels)-1):
            updatePixel([self.pixels[i][1]+self.location[1]],[self.pixels[i][2]+self.location[2]],[self.pixels[i][3]])
            #updates the pixels at the co oridinates of the pixels relative to the position of the piece and makes them the color of the piece
    def eraseSprite(self):
        for i in range(0,len(self.pixels)-1):
            updatePixel([self.pixels[i][1]+self.location[1]],[self.pixels[i][2]+self.location[2]],[0])
            #updates all the pixels at the co ordinates relative to the position to 0 making them black

class piece(sprite):
    def __init__(self,name,shape,location,rot):
        self.name=name
        self.shape=shape
        self.location=location
        self.rotation="0"
        self.updatePixels(shape,"0")
    def updateShape(self,shape,rot):
        #This long if series sets the pixels of the sprite according to the shape with
        #a lil diagram next to it # is a block and X is the centre

        if shape=="O": #If the shape is an O piece there is no need for rotation
            self.pixels=[[0,0,6],[1,0,6],[0,1,6],[1,1,6]]
        #Normal rotation
        elif rot=="0":
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
        elif rot=="R":
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
        elif rot=="2":
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
        elif rot=="L":
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

class letter(piece):
    #the letter class is like the shape but instead of strings defining the shape, they are defined by integers from 0 to 25 so that they can be scrolled through later
    # 0-A 1-B 2-C 3-D 4-E 5-F 6-G 7-H 8-I 9-J 10-K 11-L 12-M 13-N 14-O 15-P 16-Q 17-R 18-S 19-T 20-U 21-V 22-W 23-X 24-Y 25-Z
    #borrowed from https://robey.lag.net/2010/01/23/tiny-monospace-font.html
    def updatePixels(self,shape):
        if shape==0:
            self.pixels=[[0,0,1],[2,0,1],[0,1,1],[2,1,1],[0,2,1],[1,2,1],[2,2,1],[0,3,1],[2,3,1],[1,4,1]]
             #
            # #
            ###
            # #
        #   X #
        if shape==1:
            self.pixels=[[0,0,1],[1,0,1],[0,1,1],[2,1,1],[0,2,1],[1,2,1],[0,3,1],[2,3,1],[0,4,1],[1,4,1]]
            ##
            # #
            ##
            # #
        #   X#
        if shape==2:
            self.pixels=[[1,0,1],[2,0,1],[0,1,1],[0,2,1],[0,3,1],[1,4,1],[2,4,1]]
             ##
            #
            #
            #
        #   X##
        if shape==3:
            self.pixels=[[0,0,1],[1,0,1],[0,1,1],[2,1,1],[0,2,1],[2,2,1],[0,3,1],[2,3,1],[0,4,1],[1,4,1]]
            ##
            # #
            # #
            # #
        #   X#
        if shape==4:
            self.pixels=[[0,0,1],[1,0,1],[2,0,1],[0,1,1],[0,2,1],[1,2,1],[2,2,1],[0,3,1],[0,4,1],[1,4,1],[2,4,1]]
            ###
            #
            ###
            #
        #   X##
        if shape==5:
            self.pixels=[[0,0,1],[0,1,1],[0,2,1],[1,2,1],[2,2,1],[0,3,1],[0,4,1],[1,4,1],[2,4,1]]
            ###
            #
            ###
            #
        #   X
        if shape==6:
            self.pixels=[[1,0,1],[2,0,1],[0,1,1],[2,1,1],[0,2,1],[1,2,1],[2,2,1],[0,3,1],[1,4,1],[2,4,1]]
             ##
            #
            ###
            # #
        #   X##
        if shape==7:
            self.pixels=[[0,0,1],[2,0,1],[0,1,1],[2,1,1],[0,2,1],[1,2,1],[2,2,1],[0,3,1],[2,3,1],[0,4,1],[2,4,1]]
            # #
            # #
            ###
            # #
        #   X #
        if shape==8:
            self.pixels=[[0,0,1],[1,0,1],[2,0,1],[1,1,1],[1,2,1],[1,3,1],[0,4,1],[1,4,1],[2,4,1]]
            ###
             #
             #
             #
        #   X##
        if shape==9:
            self.pixels=[[1,0,1],[0,1,1],[2,1,1],[2,2,1],[2,3,1,],[2,4,1]]
              #
              #
              #
            # #
        #   X#
        if shape==10:
            self.pixels=[[0,0,1],[2,0,1],[0,1,1],[2,1,1],[0,2,1],[1,2,1],[0,3,1],[2,3,1],[0,4,1],[2,4,1]]
            # #
            # #
            ##
            # #
        #   X #
        if shape==11:
            self.pixels=[[0,0,1],[1,0,1],[2,0,1],[0,1,1],[0,2,1],[0,3,1],[0,4,1]]
            #
            #
            #
            #
        #   X##
        if shape==12:
            self.pixels=[[0,0,1],[2,0,1],[0,1,1],[2,1,1],[0,2,1],[1,2,1],[2,2,1],[0,3,1],[1,3,1],[2,3,1],[0,4,1],[2,4,1]]
            # #
            ###
            ###
            # #
        #   X #
        if shape==13:
            self.pixels=[[0,0,1],[2,0,1],[0,1,1],[1,1,1],[2,1,1],[0,2,1],[1,2,1],[2,2,1],[0,3,1],[1,3,1],[2,3,1],[0,4,1],[2,4,1]]
            # #
            ###
            ###
            ###
        #   X #
        if shape==14:
            self.pixels=[[1,0,1],[0,1,1],[2,1,1],[0,2,1],[2,2,1],[0,3,1],[2,3,1],[1,4,1]]
             #
            # #
            # #
            # #
        #   X#
        if shape==15:
            self.pixels=[[0,0,1],[0,1,1],[0,2,1],[1,2,1],[0,3,1],[2,3,1],[0,4,1],[1,4,1]]
            ##
            # #
            ##
            #
        #   X
        if shape==16:
            self.pixels=[[1,0,1],[2,0,1],[0,1,1],[1,1,1],[2,1,1],[0,2,1],[2,2,1],[0,3,1],[2,3,1],[1,4,1]]
             #
            # #
            # #
            ###
        #   X##
        if shape==17:
            self.pixels=[[0,0,1],[2,0,1],[0,1,1],[1,1,1],[0,2,1],[1,2,1],[2,2,1],[0,3,1],[2,3,1],[0,4,1],[1,4,1]]
            ##
            # #
            ###
            ##
        #   X #
        if shape==18:
            self.pixels=[[0,0,1],[1,0,1],[2,1,1],[1,2,1],[0,3,1],[1,4,1],[2,4,1]]
             ##
            #
             #
              #
        #   X#
        if shape==19:
            self.pixels=[[1,0,1],[1,1,1],[1,2,1],[1,3,1],[0,4,1],[1,4,1],[2,4,1]]
            ###
             #
             #
             #
        #   X#
        if shape==20:
            self.pixels=[[1,0,1],[2,0,1],[0,1,1],[2,1,1],[0,2,1],[2,2,1],[0,3,1],[2,3,1],[0,4,1],[2,4,1]]
            # #
            # #
            # #
            # #
             ##
        if shape==21:
            self.pixels=[[1,0,1],[1,1,1],[0,2,1],[2,2,1],[0,3,1],[2,3,1],[0,4,1],[2,4,1]]
            # #
            # #
            # #
             #
        #   X#
        if shape==22:
            self.pixels=[[0,0,1],[2,0,1],[0,1,1],[1,1,1],[2,1,1],[0,2,1],[1,2,1],[2,2,1],[0,3,1],[2,3,1],[0,4,1],[2,4,1]]
            # #
            # #
            ###
            ###
        #   X #
        if shape==23:
            self.pixels=[[0,0,1],[2,0,1],[0,1,1],[2,1,1],[1,2,1],[0,3,1],[2,3,1],[0,4,1],[2,4,1]]
            # #
            # #
             #
            # #
        #   X #
        if shape==24:
            self.pixels=[[1,0,1],[1,1,1],[1,2,1],[0,3,1],[2,3,1],[0,4,1],[2,4,1]]
            # #
            # #
             #
             #
        #   X#
        if shape==25:
            self.pixels=[[0,0,1],[1,0,1],[2,0,1],[0,1,1],[1,2,1],[2,3,1],[0,4,1],[1,4,1],[2,4,1]]
            ###
              #
             #
            #
        #   X##
        
def drawScreen(screen):







####################
####MAIN PROGRAM####
####################
objects=[]
drawScreen("menu")


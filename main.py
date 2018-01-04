import serial
def updatePixel(x,y,colorcode):
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

class piece(sprite):
    def __init__(self,name,shape,location,rotation):
        self.name=name
        self.shape=shape
        self.location=location
        self.rotation="0"
        self.updatePixels(shape,"0")
    def updateShape(self,sha,rot)
        #This long if series sets the pixels of the sprite according to the shape with
        #a lil diagram next to it # is a block and X is the centre
        if shape="O": #If the shape is an O piece there is no need for rotation
            self.pixels=[[0,0,6],[1,0,6],[0,1,6],[1,1,6]]
        elif rot="0":
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
        elif rot="R":
            if shape=="I":
                self.pixels=[[0,2,8],[0,0,8],[0,-1,8],[0,-2,5]]
                #
        #       X
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
                self.pixels=[[-1,0,4],[0,0,4],[0,1,4],[1,1,4]]
                 ##
                #X
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
        elif rot="2":
            #blah
        elif rot="L":
            #blah

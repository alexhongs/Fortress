# Alex Hong H seongkwh

import math
import pygame
import os
import random
from PIL import Image

# http://www.pygame.org/docs/

####################################
# Preload Images
####################################
wonPic = pygame.image.load("Source/Emblem/wonPic.jpg")
introImage = pygame.image.load("Source/Emblem/introPage.jpg")
skyBG = pygame.image.load("Source/Map/skyB.jpg")
skyT = pygame.image.load("Source/Map/skyT.gif")
skyIM = Image.open("Source/Map/skyT.gif")
cTank = pygame.image.load("Source/Tanks/CannonTank.gif")
cTank1 = pygame.image.load("Source/Tanks/CannonTank1.gif")
cTankB = pygame.image.load("Source/Tanks/CannonBullet1.png")
interface = pygame.image.load("Source/Interface.png")
interface1 = pygame.image.load("Source/Interface1.png")
currentPlayerimageBank = dict()
currentPlayerimageBank[1] = pygame.image.load("Source/Emblem/CurrentPlayerIcon1.png")
currentPlayerimageBank[2] = pygame.image.load("Source/Emblem/CurrentPlayerIcon.png")
fireImages = dict()
fireImages[0] =  pygame.image.load("Source/Emblem/fire0.png")
fireImages[1] =  pygame.image.load("Source/Emblem/fire1.png")
mImage = pygame.image.load("Source/Emblem/mImage.png")
sImage = pygame.image.load("Source/Emblem/sImage.png")
helps = pygame.image.load("Source/Emblem/helpScreen.png")

# Interface drawn with paint.net external program and Win10 paint
class Interface(object):
    def __init__(self):
        self.image = interface
        self.imageAlpha = interface1
        self.imageWidth = self.image.get_size()[0]
        self.imageHeight = self.image.get_size()[1]
        self.currentPlayerimageBank = currentPlayerimageBank
        self.currentPlayerimageHeight = 45
        self.currentPlayerimageNum = 1
        self.currentPlayerimage = self.currentPlayerimageBank[1]
        self.currentPlayerimage_timer = 50
        self.currentPlayerimage_dy = 0
        self.fireImages = fireImages
        self.fires = []
        self.fireVelocity = []
        self.firePositions = []
        self.fireTimer = 0
        self.generateFire()

    def generateFire(self):
        for i in range(30):
            num = random.choice([0,1])
            size = random.randint(20,50)
            image = pygame.transform.scale(self.fireImages[num],\
                            (size,size))
            self.fires.append(image)

            vx, vy = random.randint(-50,50), random.randint(-60,0)
            self.fireVelocity.append((vx,vy))
            self.firePositions.append([0,0])

    def moveFire(self, startingPosition,time):
        gravity = 10
        for i in range(len(self.firePositions)):
            self.firePositions[i][0] = startingPosition[0] + \
            self.fireVelocity[i][0] * time
            self.firePositions[i][1] = startingPosition[1] + \
            self.fireVelocity[i][1] * time + \
                gravity * time**2 / 2

class CannonTank(object):
    def __init__(self):
        self.imageBank = dict()
        self.imageBank[1] = cTank
        self.imageBank[2] = cTank1
        self.imageBullet = cTankB

class Map(object):
    def __init__(self):
        self.mapPoints = []
        self.blitpoint = 0,0
        self.pointsDirectory = ""

    def setMapPoints(self):
        
        content = readFile(self.pointsDirectory)     
        # Decoding text file
        points = content.splitlines()
        # Every other line is x and y
        for i in range(0,len(points),2):
            groupX = points[i][1:-1].split(",")
            groupY = points[i+1][1:-1].split(",")
            group = []
            for i in range(len(groupX)):
                group.append((int(groupX[i]),int(groupY[i])))
            self.mapPoints.append(group)

class NightMap(Map):
    def __init__(self):
        super().__init__()
        self.imageBG = nightBG
        self.imageT = nightT

        self.im = nightIM
        self.im = self.im.copy().convert("RGBA")

        self.pointsDirectory = "Source/Map/nightpoints.txt"
        self.setMapPoints()
        self.mapWidth = self.imageBG.get_size()[0]
        self.mapHeight = self.imageBG.get_size()[1]

class SkyMap(Map):
    def __init__(self):
        super().__init__()
        self.imageBG = skyBG
        self.imageT = skyT

        self.im = skyIM
        self.im = self.im.copy().convert("RGBA")

        self.pointsDirectory = "Source/Map/skypoints.txt"
        self.setMapPoints()
        self.mapWidth = self.imageBG.get_size()[0]
        self.mapHeight = self.imageBG.get_size()[1]

# From course notes   
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

class Player(object):
    def __init__(self, controller):
        #choice = [CannonTank(),NormalTank(),RockTank(),MissileTank(),OctoTank(),\
        #        SateliteTank()]
        self.type = CannonTank()
        self.controller = controller
        self.original_imageBank = self.type.imageBank
        self.original_bulletImage = self.type.imageBullet
        self.setImage()
        self.setCoordinateInformation()
        self.setMovementInformation()
        self.setBulletInformation()
        self.HP = 100
    def __repr__(self):
        return str(self.controller)
    def __hash__(self):
        return hash(self.controller)

    def setBulletInformation(self):
        self.power = 0
        self.maxPower = 30
        self.damage = 30
        self.isShooting = False
        self.shootAngle = 45
        self.maxAngle,self.minAngle = self.shootAngle + 60, self.shootAngle
        self.bulletX,self.bulletY = 0,0
        self.bulletVx,self.bulletVy = 0,0
        self.bulletSize = 40
        self.bulletBox = None
        self.movedBulletX, self.movedBulletY = 0,0
        self.gotShot = False
    # Set all the coordinate information
    def setCoordinateInformation(self):
        self.slope = 0
        self.orthogonalForm = (0,0) # Slope, y-intercept
        self.angle = 0
        self.x, self.y = None, None

    def setMovementInformation(self):
        self.moveBox = None
        self.direction = -1
        self.falling, self.fallingspeed = False, 5
        self.imageMoveTimer = 15
        self.movedX = 0
        self.movedY = 0
        self.isMoving = False
        self.moveDistance = 0
        self.maxMoveDistance = 30

        self.terrain = None
        self.terrainEnds = (0,0) # Left and Rightmost ends    

    # Get image from the tank class and enlarge them with scale
    def setImage(self):
        self.imageNumber = 1
        enlargeScale = 10
        enlargedwidth = self.type.imageBank[self.imageNumber].get_size()[0] \
                                                                + enlargeScale
        enlargedheight = self.type.imageBank[self.imageNumber].get_size()[1] \
                                                                + enlargeScale
        self.original_imageBank[1] = \
        pygame.transform.scale(self.original_imageBank[1],\
                                        (enlargedwidth,enlargedheight))
        self.original_imageBank[2] = \
        pygame.transform.scale(self.original_imageBank[2],\
                                        (enlargedwidth,enlargedheight))
        
        self.image = self.original_imageBank[self.imageNumber]
        self.imagewidth = self.image.get_size()[0]
        self.imageheight = self.image.get_size()[1]

        enlargedwidth = self.type.imageBullet.get_size()[0] + enlargeScale
        enlargedheight = self.type.imageBullet.get_size()[1] + enlargeScale
        self.original_bulletImage = \
        pygame.transform.scale(self.original_bulletImage,\
                            (enlargedwidth,enlargedheight))
        self.bulletImage = self.original_bulletImage
        self.bulletImagewidth = self.bulletImage.get_size()[0]
        self.bulletImageheight = self.bulletImage.get_size()[1]
        self.bulletRotationAngle = 0
        self.bulletRotationTimer = 0
    # Get player's terrain 
    def getTerrainEnds(self):
        if(self.terrain != None):
            rightEnd = max(self.terrain)[0]
            leftEnd = min(self.terrain)[0]
            self.terrainEnds = (leftEnd,rightEnd)

    def rotateBulletImage(self):
        self.bulletRotationAngle += 20
        if(self.bulletRotationAngle >= 360):
            self.bulletRotationAngle = 0
        self.bulletImage = self.original_bulletImage
        self.bulletImage = pygame.transform.rotozoom(\
                self.bulletImage, self.bulletRotationAngle,1)

####################################
# init
####################################
def init(data):
    data.mode = "introScreen"
    #data.players = [Player("P1"),Player("CP")]
    iS_init(data)
####################################
# mode dispatcher
####################################

# DrawScreen based on different modes
def redrawAll(data,gameDisplay):
    if(data.mode == "introScreen"): iS_redrawAll(data,gameDisplay)
    elif(data.mode == "menuScreen"): mS_redrawAll(data,gameDisplay)
    elif(data.mode == "playScreen"): pS_redrawAll(data,gameDisplay)
    elif(data.mode == "endScreen"): eS_redrawAll(data,gameDisplay)
# Key action when key is pressed based on different
def keyPressed(key,data):
    if(data.mode == "introScreen"): iS_keyPressed(key,data)
    elif(data.mode == "menuScreen"): mS_keyPressed(key,data)
    elif(data.mode == "playScreen"): pS_keyPressed(key,data)
    elif(data.mode == "endScreen"): eS_keyPressed(key,data)
# Mouse action when mouse is pressed
def mousePressed(event,data):
    if(data.mode == "playScreen"): pS_mousePressed(event,data)
# Event as time fires
def timerFired(data):
    if(data.mode == "introScreen"): iS_timerFired(data)
    elif(data.mode == "menuScreen"): mS_timerFired(data)
    elif(data.mode == "playScreen"): pS_timerFired(data)
    elif(data.mode == "endScreen"): eS_timerFired(data)    

####################################
# introScreen mode
####################################
def iS_init(data):
    data.introImage = introImage
    enlargedwidth,enlargedheight = (650,500)
    data.introImage = pygame.transform.scale(data.introImage,\
                (enlargedwidth,enlargedheight))

    data.initText = None
    data.initFont = None

def iS_redrawAll(data,gameDisplay):
    gameDisplay.fill((255,255,255))
    gameDisplay.blit(data.introImage, (70,50))
    if(data.initText == None and data.initFont == None):
        data.initFont = pygame.font.SysFont("Helvetica", 30, True)
        data.initText = data.initFont.render("Press SPACE to Play", 1, (0,0,0))
    gameDisplay.blit(data.initText, (300 , 520))

def iS_keyPressed(key,data):
    if(key[pygame.K_SPACE] != 0):
        data.mode = "menuScreen"
        mS_init(data)
def iS_timerFired(data): pass
####################################
# endScreen mode
####################################
def eS_init(data):
    enlargedwidth,enlargedheight = (650,500)
    
    data.initText = None
    data.initFont = None 
def eS_redrawAll(data,gameDisplay):
    gameDisplay.fill((255,255,255))
    gameDisplay.blit(wonPic, (70,50))
    if(data.initText == None and data.initFont == None):
        data.initFont = pygame.font.SysFont("Helvetica", 30, True)
        data.initText = data.initFont.render("YOU WON", 1, (0,0,0))
    gameDisplay.blit(data.initText, (300 , 520))

def eS_keyPressed(key,data):
    if(key[pygame.K_RETURN] != 0):
        data.mode = "introScreen"
        iS_init(data) 
def eS_timerFired(data): pass

####################################
# menuScreen mode
####################################
def mS_init(data):
    data.currentBox = 0
    data.msTimer = 0
    data.msText = ["SinglePlayer","2Player","PracticeMode","Help",
    "Press Enter to Click"]
    data.helpScreen = False

def drawHelpScreen(data,gameDisplay):
    if(data.helpScreen):
        gameDisplay.fill((0,102,204), rect = (205,105,490,290))
        gameDisplay.fill((153,204,255), rect = (210,110,480,280))
        gameDisplay.blit(helps, (200,100))
        pass

def mS_redrawAll(data,gameDisplay):
    gameDisplay.fill((0,102,204))  
    gameDisplay.fill((153,204,255), rect = (100,100,data.width-200,data.height-200))
    width = 200
    x0,y0 = int(data.width/2 - width/2),130
    font = pygame.font.SysFont("Helvetica", 33, True)
    for i in range(4):
        color = (255,255,255)
        if(i == data.currentBox):
            color = (255,0,0)
        gameDisplay.fill((153,204,255),rect = (x0,y0+i*90,width,65))
        pygame.draw.rect(gameDisplay,color,(x0,y0+i*90,width,65),2)
        text = font.render(data.msText[i], 1, (255,255,255))
        gameDisplay.blit(text, (x0+5 , y0+i*90+10))
    text = font.render(data.msText[4], 1, (255,255,255))
    gameDisplay.blit(text, (100 ,50))      


    gameDisplay.blit(mImage, (100 , 250))
    gameDisplay.blit(sImage, (550, 330))

    drawHelpScreen(data,gameDisplay)

def mS_keyPressed(key,data):
    if(key[pygame.K_RETURN] != 0):
        if(data.currentBox == 3):
            if(data.msTimer > 100):
                data.msTimer = 0
                data.helpScreen = not data.helpScreen
        else:
            setPlayMode(data)
            data.mode = "playScreen"
            pS_init(data)
    elif(key[pygame.K_UP] != 0):
        if(data.msTimer > 100):
            data.currentBox -= 1
            if(data.currentBox < 0):
                data.currentBox = 3
            data.msTimer = 0
    elif(key[pygame.K_DOWN] != 0):
        if(data.msTimer > 100):
            data.currentBox += 1
            data.currentBox = data.currentBox % 4
            data.msTimer = 0
def mS_timerFired(data):
    data.msTimer += 1

def setPlayMode(data):
    if(data.currentBox == 0):
        data.players = [Player("P1"), Player("CP")]
    elif(data.currentBox == 1):
        data.players = [Player("P1"), Player("P2")]
    elif(data.currentBox == 2):
        data.players = [Player("P1"), Player("")]    
####################################
# playScreen mode
####################################
def pS_init(data):
    # Load Tank
    data.mode = "playScreen"
    data.tanks = dict()
    loadTankImage(data)
    data.blittedImage = None
    # Setup map
    data.map = SkyMap()
    data.map.blitpoint = 0,0
    data.interface = Interface()
        
    data.player = data.players[0]
    
    data.phase = "MovePhase" #"ShootPhase" or "MovePhase"
    data.bulletTime = 0
    data.blowUpAnimation = False
    data.collided = False

    data.dx,data.dy = 0, 0
    # Setup player
    setupPlayers(data)
    focusCamera(data) 
    # Setup Camera and Image

    data.damages = [0,0]
    # Update Image
    data.points = []
    data.collisionPoint = None

    data.edgepoints = []

def setupPlayers(data):
    # Setup player
    for player in data.players:
        player.terrain = data.map.mapPoints[random.randint(0,len(data.map.mapPoints)-1)]
        player.getTerrainEnds()
        generatePlayerRandomPlace(player)
       
        player.moveBox = player.image.get_rect()
        getPlayerAngle(data,player)    

# Convert background image to hasten the process
def pS_convertBackgroundImage(data,gameDisplay):
    if(data.mode == "playScreen"):
        data.map.imageBG = data.map.imageBG.convert()
        data.map.imageT = data.map.imageT.convert_alpha()

# Generate player in random place on map
# Updates player position and slope
def generatePlayerRandomPlace(player):
    terrain = player.terrain
    # Get index of the right end of terrain
    maxIndex = 0
    for pindex in range(len(terrain)):
        point = terrain[pindex]
        if(point[0] == player.terrainEnds[1]):
            maxIndex = pindex
            break

    # Pick random two consecutive points in terrain
    i = random.randint(0,maxIndex -1)
    x0,y0 = terrain[i][0], terrain[i][1]
    x1,y1 = terrain[i+1][0], terrain[i+1][1]

    # Place player randomly between the two points
    if(abs(x1 - x0) < 1): # THIS SHOULD NOT HAPPEN.
        player.x = x0
    else:
        player.x = random.randint(min(x0,x1),max(x0,x1))
    player.slope,yintercept = getSlopeandIntercept(x0,y0,x1,y1)
    player.y = player.slope * player.x + yintercept

# Load all tank images
def loadTankImage(data):
    path = "Source/Tanks"
    nameIndex = -4 #name is up to .gif
    for tank in os.listdir(path):
        tankImage = pygame.image.load(str(path + "/" + tank))
        data.tanks[tank[:nameIndex]] = tankImage


# Move player by a step in slope
def pS_movePlayer(data):
    player = data.player
    direction = player.direction
    terrain = player.terrain
    leftEnd, rightEnd = player.terrainEnds[0],player.terrainEnds[1]
    player.isMoving = True
    if(player.moveDistance >= player.maxMoveDistance):
        player.isMoving = False
    if(player.isMoving):
        for i in range(0,len(terrain)-1):
            x0,y0 = terrain[i][0], terrain[i][1]
            x1,y1 = terrain[i+1][0], terrain[i+1][1]
            if(min(x0,x1) <= player.x < max(x0,x1)):
                # Update player
                player.slope, y_intercept = getSlopeandIntercept(x0,y0,x1,y1)
                getPlayerAngle(data,player)
                dx = direction * getXStep(player.slope,1)
                y1 = player.x * player.slope  + y_intercept
                dy = player.y - y1


                setshootAngle(data)

                # Move by 1 step, update y from the slope and intercept
                player.x += dx
                player.movedX = dx
                player.movedY = dy
                player.y = y1
                updatemoveDistance(data)
                break

def setshootAngle(data):
    player = data.player
    player.shootAngle = -player.direction * math.atan(player.slope) * 180 / math.pi
    player.maxAngle = player.shootAngle + 60
    player.minAngle = player.shootAngle    

# Update movedDistance of the moving player. If max, reset to 0
def updatemoveDistance(data):
    player = data.player
    player.moveDistance += 0.3

# fall if the player is off the current terrain. Slide within the air
def fall(data, player):
    leftEnd, rightEnd = player.terrainEnds[0],player.terrainEnds[1]
    slide = 5
    player.falling = False
    if(player.y > data.map.mapHeight):
        data.mode = "endScreen"
        eS_init(data)
    elif(player.x >= rightEnd or player.x <= leftEnd):
        player.falling = True
        # Slide
        if(player.x <= leftEnd and player.x >= leftEnd - slide): # Fall left
            player.x += player.direction
        elif(player.x >= rightEnd and player.x <= rightEnd + slide): # Fall right
            player.x += player.direction
        # Fall
        player.y += player.fallingspeed
        player.movedY = -player.fallingspeed
        getNewTerrain(data,player)
    elif(player.gotShot):
        im = data.map.im
        pixdata = im.load()
        if(pixdata[player.x,player.y][3] == 0):
            # Fall
            player.y += player.fallingspeed
            player.movedY = -player.fallingspeed
            getTerrainAfterShot(data,player)   

# Get a new set of terrain on map for the falling player to land
def getNewTerrain(data,player):
    previous = player.terrain
    # Reset game if the player is off the map for good
    for terrain in data.map.mapPoints:
        if(terrain != previous):
            leftEnd,rightEnd = min(terrain)[0], max(terrain)[0]
            # Find terrains that player can fall on
            if(leftEnd <= player.x <= rightEnd):
                for i in range(len(terrain)-1):
                    p0,p1 = terrain[i],terrain[i+1]
                    # Find the first terrain below previous one
                    if(p0[0] <= player.x <= p1[0]):
                        # Assume two consecutive points are adjacent
                        player.slope,y_intercept = \
                        getSlopeandIntercept(p0[0],p0[1],p1[0],p1[1])
                        y = player.slope * player.x + y_intercept
                        # The landed y - position will be on the line segment
                        if(abs(player.y - y) < player.fallingspeed):
                            #Update terrain and position
                            player.y = y
                            player.terrain = terrain
                            getPlayerAngle(data,player)
                            player.getTerrainEnds()
                            return

def getTerrainAfterShot(data,player):
    # Reset game if the player is off the map for good
    for terrain in data.map.mapPoints:
            leftEnd,rightEnd = min(terrain)[0], max(terrain)[0]
            # Find terrains that player can fall on
            if(leftEnd <= player.x <= rightEnd):
                for i in range(len(terrain)-1):
                    p0,p1 = terrain[i],terrain[i+1]
                    # Find the first terrain below previous one
                    if(p0[0] <= player.x <= p1[0]):
                        # Assume two consecutive points are adjacent
                        player.slope,y_intercept = \
                        getSlopeandIntercept(p0[0],p0[1],p1[0],p1[1])
                        y = player.slope * player.x + y_intercept
                        # The landed y - position will be on the line segment
                        if(abs(player.y - y) < player.fallingspeed):
                            #Update terrain and position
                            player.y = y
                            player.terrain = terrain
                            getPlayerAngle(data,player)
                            player.getTerrainEnds()
                            player.gotShot = False
                            return
# Get slope and intercept of current line connected by two map points
def getSlopeandIntercept(x0,y0,x1,y1):
    if(x1 - x0 == 0):
        slope = 0
    else:
        slope = (y1 - y0)/(x1 - x0)
    y_intercept = y1 - slope * x1
    return slope, y_intercept

# Update orthogonal slope and intercept from the player's slope with respect to
# the player's current position
def getOrthogonalSlopeandIntercept(player):
    if(player.slope == 0):
        player.orthogonalForm = None
        return
    orthslope = -1/player.slope
    orthYint = player.y - player.x*orthslope
    player.orthogonalForm = (orthslope , orthYint)

def getOrthogonalPositions(player):
    height = player.imageheight/2
    orth = player.orthogonalForm
    # This is when slope is 0, orthogonal slope is infinity
    if(orth == None): 
        return player.x, player.y - height
    # On other cases
    orthslope, yintercept =orth[0],orth[1]
    if(orthslope > 0):
        x = player.x - getXStep(orthslope,height)
    else:
        x = player.x + getXStep(orthslope,height)
    y = x * orthslope + yintercept
    return x,y

# Get angle from the slope
def getPlayerAngle(data,player):
    angle = -math.atan(data.player.slope) * 180 / (math.pi)  
    player.angle = angle

# get X step so that the distance moved by 1 dx and 1 dy = increment
def getXStep(slope,increment):
    return (increment**2/(1+slope**2))**0.5

# Rotate image to be parallel to the slope
def rotateImage(data):
    for player in data.players:
        # Refer to default image and flip and rotate to get the wanted rotation
        if(player.imageMoveTimer == 0):
            if(player.imageNumber == 1 and not player.falling and player.isMoving):
                player.imageNumber = 2
            else:
                player.imageNumber = 1
        player.image = player.original_imageBank[player.imageNumber]
        if(player.direction == 1):
            player.image = pygame.transform.flip(player.image,True,False)  
        width,height = player.imagewidth,player.imageheight
        player.image = pygame.transform.rotozoom(player.image, player.angle,1)

# Update image position in reference to the player's position
# It happens to be that after image rotation and all, image's position \
# get mismatched with the player's position
def updateImagePosition(data):
    for player in data.players:
        angle = abs(player.angle)
        getOrthogonalSlopeandIntercept(player)
        x,y = getOrthogonalPositions(player)
        player.moveBox = player.image.get_rect()
        player.moveBox.center = (int(x)+data.dx,int(y)+data.dy)

# Focus Camera when turn goes to the player
def focusCamera(data):
    player= data.player
    px,py = player.x,player.y
    # Default map movement  
    dx,dy = -(px - data.width/2), -(py - data.height/2)
    data.map.blitpoint = 0,0
    oldMapX,oldMapY = data.map.blitpoint[0], data.map.blitpoint[1]
    newMapX, newMapY = (oldMapX + dx), (oldMapY + dy)
    
    # Corner Case for X
    if(0 < newMapX):
        dx = -oldMapX
    elif(newMapX < -data.map.mapWidth + data.width):
        dx = -oldMapX - data.map.mapWidth + data.width

    # Corner Case for Y
    if(0 < newMapY):
        dy = -oldMapY
    elif(newMapY < -data.map.mapHeight + data.height):
        dy = -oldMapY - data.map.mapHeight + data.height
    data.dx,data.dy = dx,dy

    # Update Map position
    data.map.blitpoint = (oldMapX + dx, oldMapY + dy)

# Focus Camera when the player is moving and goes close to edge of the screen
def followCamera_Player(data):
    p = data.player
    movingXmargin, movingYmargin = 200, 150
    px,py = p.moveBox.center[0] , p.moveBox.center[1]
    if(p.isMoving):
        if(movingXmargin >= px and p.direction == -1)             or\
          (px >= data.width - movingXmargin and p.direction == 1) or\
          (py <= movingYmargin or py >= data.height - movingYmargin):
            moveMap(data,-p.movedX,p.movedY)

# Focus Camera when the player is moving and goes close to edge of the screen
def followCamera_Bullet(data):
    p = data.player
    movingXmargin, movingYmargin = 200, 150
    if(p.bulletBox != None):
        px,py = p.bulletBox.center[0] , p.bulletBox.center[1]
        if(p.isShooting and data.phase == "ShootPhase"):
            
            
            if(movingXmargin >= px and p.direction == -1)             or\
              (px >= data.width - movingXmargin and p.direction == 1) or\
              (py <= movingYmargin or py >= data.height - movingYmargin):
                moveMap(data,-p.movedBulletX,-p.movedBulletY)

# Move the map according to an object's moved distance for camera focusing
def moveMap(data,dx,dy):
    x0, y0 = data.map.blitpoint[0], data.map.blitpoint[1]
    if(-data.map.mapWidth + data.width <= x0 + dx <= 0):
        data.dx += dx
        x0 = x0 + dx
    if(-data.map.mapHeight + data.height <= y0+dy <= 0):       
        data.dy += dy
        y0 = y0 + dy
    data.map.blitpoint = (x0, y0)

# Main shooting algorithm
def pS_shoot(data):
    p = data.player
    i = data.interface
    theta,accel,t = p.shootAngle * math.pi/180, 5, data.bulletTime
    scale,epsilon = 3,5
    V = scale * p.power
    x0,y0 = getOrthogonalPositions(p)

    # Get collision location only once
    if(not p.isShooting):
        getCollisionLocation(data)
    # When the location of bullet is at the collision location, change terrain

    elif(not data.collided and (isCollided(data) or bulletoutofBounds(data))):
        if(data.collided):
            updateTerrainImage(data,data.collisionPoint)
            updateTerrain(data)
            checkPlayerHit(data)
            data.blowUpAnimation = True
        else:
            p.moveDistance = 0
            resetTurn(data)

    previousX = p.bulletX
    previousY = p.bulletY

    # Update bullet position every time frame
    p.bulletX = x0 + p.direction * V * math.cos(theta) * t
    p.bulletY = y0 + (-V*math.sin(theta) * t + accel*t**2/2)


    p.movedBulletX = p.bulletX - previousX
    p.movedBulletY = p.bulletY - previousY
    p.bulletBox = p.image.get_rect()
    p.bulletBox.center = (int(p.bulletX+data.dx),int(p.bulletY+data.dy))
    followCamera_Bullet(data)
    #print(p.bulletX,p.bulletY,p.x,p.y)
def checkPlayerHit(data):
    data.damages = [0,0]
    x0, y0 = data.collisionPoint[0],data.collisionPoint[1]
    for i in range(len(data.players)):
        player = data.players[i]
        x1,y1 = player.x,player.y
        distance = ((x1-x0)**2+(y1-y0)**2)**0.5
        if(distance < data.player.bulletSize + 15 ):
            error = data.player.bulletSize - distance
            damage = int(data.player.damage * error / data.player.bulletSize)
            #print(damage,player,error)
            if(len(data.players[1].controller) != 0):
                player.HP -= damage
                data.damages[i] = damage
                player.gotShot = True

def switchPlayer(data):
    if(len(data.players) > 1):
        if(data.players.index(data.player) == 0):
            data.player = data.players[1]
        else:
            data.player = data.players[0]
    
# Update Terrain based on the new terrain after shoot
def updateTerrain(data):
    radius = data.player.bulletSize
    center = data.collisionPoint
    edges = sorted(data.edgepoints) # Sort the edges by increasing x positions
    
    # Get points between the edge points on the circle centered on center
    def getPointsonCircle(data):
        points = []
        p1 = edges[0]
        p2 = edges[1]

        points.append(p1)
        a1 = math.ceil(getAngle(p1) * 180 / math.pi)
        a2 = math.ceil(getAngle(p2) * 180 / math.pi)
        if(a2 < a1): a2 = a2 + 360
        #print(a1,a2)
        for da in range(0,a2-a1-20,20):
            angle = (a1 + da) * math.pi/180
            #print(angle)
            x = center[0] + radius * math.cos(angle)
            y = center[1] - radius * math.sin(angle)
            points.append((x,y))
        points.append(p2)
        return points

    # Get angle of the line created by the center and the point
    def getAngle(point):
        x1, x0 = point[0], center[0]
        y1, y0 = point[1], center[1]
        side = abs(x1 - x0)
        height = -(y1 - y0)
        ratio = side/radius
        while(abs(ratio) >= 1):
            #print(ratio,side, radius)
            if(ratio > 0): 
                ratio-= 1
            else: 
                ratio += 1
        if(x1 - x0 >= 0):
            if(height >= 0): # 1st quadrant
                return math.acos(ratio)
            else: # 2nd quadrant
                return 2 * math.pi - math.acos(ratio)
        else:
            if(height >= 0): # 3rd quadrant
                return math.pi - math.acos(ratio)
            else: # 4th quadrant
                return math.pi + math.acos(ratio)
    
    for j in range(len(data.map.mapPoints)):
        bound = []
        terrain = data.map.mapPoints[j]
        for i in range(len(terrain)-1):
            p1,p2 = terrain[i],terrain[i+1]
            if(len(edges) > 1):
                # WE ARE ASSUMING THERE'S ONLY 2 EDGES SO FAR
                if(min(p1[0],p2[0]) <= edges[0][0] <= max(p1[0],p2[0])):# and\
                    bound.append(i)
                if(min(p1[0],p2[0]) <= edges[1][0] <= max(p1[0],p2[0])):# and\
                    bound.append(i+1)
                #print(bound)
                if(len(bound) == len(edges)):
                    newPoints = getPointsonCircle(data)
                    data.edgepoints = newPoints
                    # Take out portions of old terrain that is replaced
                    for i in range(bound[1] - bound[0]):
                        data.map.mapPoints[j].pop(bound[0]+1)
                    # Put in the portion of changed terrain
                    for point in reversed(newPoints):
                        data.map.mapPoints[j].insert(bound[0]+1,point)

                    # Reset edge points
                    data.edgepoints = []
                    return

# When bullet is out of bounds, return True
def bulletoutofBounds(data):
    p = data.player
    return p.bulletY >= data.map.mapHeight

# True when the bullet reaches the pre-calculated collision point
def isCollided(data):
    p = data.player
    epsilon = 10
    #print(p.movedBulletY)
    data.collided = data.collisionPoint != None and \
                            abs(p.bulletX - data.collisionPoint[0]) <= epsilon\
                            and p.movedBulletY >= 0
    return data.collided
# Pre-calculate the location of collision
def getCollisionLocation(data):
    p = data.player
    #print(p.shootAngle)
    theta = p.shootAngle * math.pi/180
    epsilon, scale = 20,3
    V = scale * p.power
    x0,y0 = getOrthogonalPositions(p)
    #print(x0,p.x)
    vxi, vyi = p.direction * V * math.cos(theta),  - V * math.sin(theta)
    accel, pointsInParabola = 5, []

    # Projectile parabola function
    def y(xf):
        if(abs(vxi) < 0.1):
            return y0
        return y0 + (vyi*(xf - x0)/vxi + accel*((xf - x0)/vxi)**2/2)
    def earliestHit(xf):
        return (xf - x0)/vxi
    def distance(point):
        xf,yf = point[0],point[1]
        return ((xf-x0)**2 + (yf-y0)**2)**0.5 

    # From combining projectile motion parametric equations
    for terrain in data.map.mapPoints:
        for point in terrain:
            xf,yf = point[0],point[1]
            if(abs(vxi) < 5 and distance(point) < 20):
                pointsInParabola.append(point)
            elif(abs(yf - y(xf)) <= epsilon):
                #print("in")
                if(p.shootAngle > 95):
                    if(p.direction == 1 and xf <= x0) or \
                        (p.direction == -1 and xf >= x0):
                        pointsInParabola.append(point)
                elif(p.shootAngle > 85):
                    pointsInParabola.append(point)
                else:
                    if(p.direction == 1 and xf >= x0) or \
                        (p.direction == -1 and xf <= x0):
                        pointsInParabola.append(point)
    #print(pointsInParabola)
    closest = None

    #print(pointsInParabola)

    # Get the closest point in parabola from the player
    if(len(pointsInParabola) != 0):
        closest = pointsInParabola[0]
        for point in pointsInParabola:
            xf,yf = point[0],point[1]
            if(abs(vxi) < 5 and distance(point) < distance(closest)): 
                closest = point
            elif(0 <= earliestHit(xf) <= earliestHit(closest[0])):
                closest = point
    # Update the collision point
    data.collisionPoint = closest
    #print(x0,y0,closest)
# Reset bullet information
def resetBullet(data):
    data.bulletTime = 0 
    data.phase = "MovePhase"
    data.player.power = 0
    data.bulletX,data.bulletY = getOrthogonalPositions(data.player)
    data.collisionPoint = None
    data.player.isShooting = False
    data.collided = False
    data.damages = [0,0]
    data.player.bulletBox = None

"""
CORNER DETECTION STILL HAS SOME ERROR

"""

# Update terrain image after destruction
def updateTerrainImage(data,point):
    radius = data.player.bulletSize 
    def DrawPixel(x,y):
        pixdata[x,y] = (0,255,255,0)
    # Floodfill inside the outlined circle
    def drawInvisibleCircle(x0, y0, radius):
        UL,DL,UR,DR = False,False,False,False
        countL,countR = 0, 0
        # Empty everything side the circle, and 
        # detect upper-left,right, down-left, right corners of terrain
        for y in range(-radius,radius+1,1):
            #the x range of circle is defined by the y values and circle formula
            x_range = math.ceil((radius**2 - y**2)**0.5)
            Lcorner = x0 - x_range + 1
            if(0 < Lcorner <data.map.mapWidth):
                if(pixdata[Lcorner,y+y0][3] != 0 and pixdata[Lcorner-1,\
                        y+y0][3] != 0):
                    if(not UL and pixdata[Lcorner,y+y0-1][3] == 0):
                        UL = True
                        data.edgepoints.append((Lcorner,y+y0))
                    elif(0 < y + y0 + 1 < data.map.mapHeight and not DL and \
                        pixdata[Lcorner,y+y0+1][3] == 0):
                        DL = True
                        data.edgepoints.append((Lcorner,y+y0))
            Rcorner = x0 + x_range - 1   
            if(0 <Rcorner <data.map.mapWidth):
                if(0 < y + y0 < data.map.mapHeight):
                    if(pixdata[Rcorner,y+y0][3] != 0 and pixdata[Rcorner+1,\
                            y+y0][3] != 0):
                        if(not UR and pixdata[Rcorner,y+y0-1][3] == 0):
                            UR = True
                            data.edgepoints.append((Rcorner,y+y0))
                        elif(0 < y + y0 + 1 < data.map.mapHeight and not DR \
                             and pixdata[Rcorner,y+y0+1][3] == 0):
                            DR = True
                            data.edgepoints.append((Rcorner,y+y0))
            # Empty inside the circle
            for x in range(-x_range+1,x_range):
                DrawPixel(x+x0,y+y0)

    x0, y0 = point[0], point[1]
    im = data.map.im
    pixdata = im.load()
    # Edit the image
    drawInvisibleCircle(x0,y0,radius)

    # Convert to pygame image format
    data.map.imageT = pygame.image.fromstring(im.tobytes(),im.size,im.mode)

def playerKeyPressed(key,data):
    player= data. player
    # Action when key not pressed
    pS_keyReleased(key, data)

    player = data.player
    if(not player.falling):
        if (key[pygame.K_RIGHT] != 0 or key[pygame.K_LEFT] != 0):
            if not (key[pygame.K_RIGHT] != 0 and key[pygame.K_LEFT] != 0):
                if(data.phase == "MovePhase"):
                    if(key[pygame.K_RIGHT] != 0): player.direction = 1
                    else: player.direction = -1
                    pS_movePlayer(data)
                    followCamera_Player(data)
        elif(key[pygame.K_UP] != 0):
            if(player.shootAngle < player.maxAngle):
                player.shootAngle += 1
        elif(key[pygame.K_DOWN] != 0):
            if(player.shootAngle > player.minAngle):
                player.shootAngle -= 1
        elif(key[pygame.K_SPACE] != 0 and not player.isShooting):
            data.phase = "ShootPhase"
            if(player.power < player.maxPower):
                player.power += 0.2
        elif(key[pygame.K_c] != 0):
            player.moveDistance = 0
            focusCamera(data)
            resetBullet(data)
    else:
        followCamera_Player(data)    

# Event when key is pressed in playScreen mode
def pS_keyPressed(key,data):
    player = data.player
    if(len(player.controller)>0):
        if(player.controller[0] == "P"):
            playerKeyPressed(key, data)

def computerMove(data):
    player = data.player
    opponent = findotherPlayer(data)

    if(opponent[0] != None):
        x1 = opponent[1]
        if(not player.falling):
            if(data.phase == "ShootPhase"):
                pS_shoot(data)
                player.isShooting = True
            else:
                resetBullet(data)
        if(not player.isShooting):
            distance = x1 - player.x
            if((x1 - player.x) > 0):
                player.direction = 1
            else:
                player.direction = -1
            power = int(abs(distance * 5)**0.5/3)
            player.power = random.randint(power - 2, power + 2)
            player.shootAngle = 45 
            data.phase = "ShootPhase"
            player.bulletBox = player.image.get_rect()
def findotherPlayer(data):
    for player in data.players:
        if(player.controller != data.player.controller):
            return player, player.x

# Event when key is not pressed
def pS_keyReleased(key, data):
    player = data.player
    if(not player.falling):
        if(key[pygame.K_SPACE] == 0):
            if(data.phase == "ShootPhase"):
                pS_shoot(data)
                player.isShooting = True
            else:
                resetBullet(data)
        if not (key[pygame.K_RIGHT] != 0 or key[pygame.K_LEFT] != 0):
            player.isMoving = False

def pS_mousePressed(event,data):
    data.points.append(pygame.mouse.get_pos())

def isDummy(player):
    return len(player.controller) == 0

def pS_timerFired(data):
    player = data.player
    interface = data.interface
    if(player.controller == "CP"):
        computerMove(data)

    fall(data, data.player)
    if(isDummy(player)):
        resetTurn(data)
    # Update Image
    rotateImage(data)
    updateImagePosition(data)

    if(data.phase == "ShootPhase" and player.isShooting):
        data.bulletTime += 0.1
        player.bulletRotationTimer += 1
        if(player.bulletRotationTimer > 10):
            player.rotateBulletImage()
    if(player.imageMoveTimer < 0):
        player.imageMoveTimer = 15
    player.imageMoveTimer -= 1
    if(interface.currentPlayerimage_timer <= 0):
        interface.currentPlayerimage_timer = 50
    interface.currentPlayerimage_timer -= 1

    if(data.blowUpAnimation):
        interface.fireTimer += 0.1
        interface.moveFire(\
            [data.collisionPoint[0],data.collisionPoint[1]],\
                            interface.fireTimer)
        if(interface.fireTimer > 5):
            data.blowUpAnimation = False
            interface.fireTimer = 0
            player.moveDistance = 0
            resetTurn(data)
def resetTurn(data):
    if(data.player.HP <= 0):
        data.mode = "endScreen"
        eS_init(data)
        return
    resetBullet(data)
    switchPlayer(data)
    focusCamera(data)    

def pS_drawPlayer(data, gameDisplay):
    for player in data.players:
        gameDisplay.blit(player.image, player.moveBox)

        x, y= player.x + data.dx, player.y + data.dy
        width = 50
        height = 8
        gameDisplay.fill((255,255,255), \
            rect = [int(x - width/2),int(y + height),width,height])
        
        # Color depending on current HP
        RED, ORANGE, GREEN = (255,0,0) , (255,153,51), (0,204,0)

        percentage = player.HP / 100
        if(percentage < 0.33):
            color = RED
        elif(percentage < 0.66):
            color = ORANGE
        else:
            color = GREEN
        HPwidth = player.HP * width/100
        margin = 1
        gameDisplay.fill(color, rect = \
            [int(x - width/2+margin),int(y + height+margin),\
            HPwidth - 2 * margin,height - 2*margin])
    
    drawDamage(data,gameDisplay)
    #drawOrthogonalLine(data, gameDisplay)

def drawDamage(data, gameDisplay):
    
    for i in range(len(data.players)):
        player = data.players[i]
        damage = -data.damages[i] * 10
        if(damage != 0):
            font = pygame.font.SysFont("Helvetica", 20, True)
            text = font.render(str(damage), 1, (255,0,0))
            gameDisplay.blit(text, \
                    (player.x + data.dx - 10 , player.y + data.dy - 70))     

def drawOrthogonalLine(data, gameDisplay):
    player = data.player
    if(data.player.orthogonalForm != None):
        orth = player.orthogonalForm
        yo = (player.x+80) * orth[0] + orth[1]
        y1 = (player.x-80) * orth[0] + orth[1]

        pygame.draw.line(gameDisplay,(0,0,255),(player.x+80+data.dx,yo+data.dy),\
        (player.x-80+data.dx,y1+data.dy),1)

def pS_drawAllTanks(data, gameDisplay):
    scale = 20
    for tank in data.tanks:
        gameDisplay.blit(data.tanks[tank],(scale,data.height - 40))
        scale += 60

def pS_drawMap(data, gameDisplay):
    gameDisplay.blit(data.map.imageBG,data.map.blitpoint)
    gameDisplay.blit(data.map.imageT,data.map.blitpoint)
def pS_drawInterface(data,gameDisplay):
    p = data.player
    i = data.interface
    drawPlayerPointer(data,gameDisplay)
    
    if(p.moveBox[1] > 400):
        gameDisplay.blit(i.imageAlpha,(0,0))
    else:
        gameDisplay.blit(i.image,(0,0))
    RED = (246,0,24)
    BLUE = (0,191,255)
    height,width = 10,300
    # Power bar
    x0, y0 = 288, 526
    gameDisplay.fill(RED, rect = [x0,y0,10*p.power,height])
    # Movement bar
    y1 = 564   
    gameDisplay.fill(BLUE, rect = [x0,y1,300 - 10*p.moveDistance,height])   

    drawAngleBars(data,gameDisplay)
    drawParallelBars(data,gameDisplay)
    drawBlowupAnimation(data,gameDisplay)
    drawRadar(data,gameDisplay)

def drawPlayerPointer(data,gameDisplay):
    p = data.player
    i = data.interface
    if(i.currentPlayerimage_timer <= 0):
        if(i.currentPlayerimageNum == 1):
           i.currentPlayerimage = i.currentPlayerimageBank[2]
           i.currentPlayerimageNum = 2
           i.currentPlayerimage_dy = 0
        else:
            i.currentPlayerimageNum = 1
            i.currentPlayerimage = i.currentPlayerimageBank[1]
            i.currentPlayerimage_dy = -10
    gameDisplay.blit(i.currentPlayerimage,\
        (p.moveBox[0]+15, p.moveBox[1] - i.currentPlayerimageHeight + \
                    i.currentPlayerimage_dy))

def drawAngleBars(data, gameDisplay):
    p = data.player
    x0,y0 = 35, 507
    width = 50
    RED = (246,0,24)
    # Angle Horizontal bar
    pygame.draw.line(gameDisplay,(255,255,255),(x0,y0),(x0+width,y0),2)
    pygame.draw.line(gameDisplay,(255,255,255),(x0+width+12,y0),(x0+2*width+13,y0), 2)
    # Angle Shoot bar
    x0 = x0 + width + 6
    angle = p.shootAngle * math.pi/180
    centersize = 6.3
    x0 = x0 + p.direction * (centersize) * math.cos(angle)
    y0 = y0 - centersize * math.sin(angle)
    x1 = x0 + p.direction * (width+centersize-7) * math.cos(angle)
    y1 = y0 - (width+centersize-7) * math.sin(angle) 
    pygame.draw.line(gameDisplay,RED,(x0,y0),(x1,y1))

    angle = p.maxAngle * math.pi/180
    x0 = 35 + width + 6 + p.direction * (centersize) * math.cos(angle)
    y0 = 507 - centersize * math.sin(angle)
    x1 = x0 + p.direction * (width+centersize-7) * math.cos(angle)
    y1 = y0 - (width+centersize-7) * math.sin(angle) 
    pygame.draw.line(gameDisplay,(255,215,0),(x0,y0),(x1,y1))

def drawParallelBars(data,gameDisplay):
    p = data.player
    width = 50
    # Draw Parallel bar
    angle = -p.direction * math.atan(p.slope)
    centersize = 6.3
    x0 = 35 + width + 6 + p.direction * (centersize) * math.cos(angle)
    y0 = 507 - centersize * math.sin(angle)
    x1 = x0 + p.direction * (width+centersize-7) * math.cos(angle)
    y1 = y0 - (width+centersize-7) * math.sin(angle) 
    pygame.draw.line(gameDisplay,(255,255,255),(x0,y0),(x1,y1))
    x0 = 35 + width + 6 + -p.direction * (centersize) * math.cos(angle)
    y0 = 507 + centersize * math.sin(angle)
    x1 = x0  -p.direction * (width+centersize-7) * math.cos(angle)
    y1 = y0 + (width+centersize-7) * math.sin(angle) 
    pygame.draw.line(gameDisplay,(255,255,255),(x0,y0),(x1,y1))

def drawBlowupAnimation(data,gameDisplay):
    I = data.interface
    if(data.blowUpAnimation):
        for i in range(len(I.firePositions)):
            gameDisplay.blit(I.fires[i],\
                (I.firePositions[i][0]+data.dx,
                     I.firePositions[i][1]+data.dy))


def pS_drawShooting(data, gameDisplay):
    p = data.player
    if(p.isShooting and not data.blowUpAnimation):
        gameDisplay.blit(p.bulletImage, p.bulletBox)
# Redraw in playScreen mode
def pS_redrawAll(data, gameDisplay):
    WHITE = (255,255,255)
    LIGHTBLUE = (204,255,255)
    BLACK = (0,10,0)
    GREEN = (50,205,50)
    RED = (255,0,0)
    #gameDisplay.fill(LIGHTBLUE)
    pS_drawMap(data, gameDisplay)
    pS_drawShooting(data, gameDisplay)
    pS_drawPlayer(data, gameDisplay) 
    pS_drawInterface(data, gameDisplay)

def drawRadar(data,gameDisplay):
    x0,y0 = 650,430#460
    for player in data.players:
        x = x0 + int(player.x * 115 / data.map.mapWidth)
        y = y0 + int(player.y * 100 / data.map.mapHeight)
        if(player.controller == data.player.controller):
            color = (0,255,0)
        else:
            color = (255,0,0)
        pygame.draw.circle(gameDisplay,color,(x,y),3,1)        
####################################
# run function
####################################
# Structure taken from course notes
def run(width = 800 , height= 600):
    # Main game loop until game is done
    # Structure learned from 
    # https://www.youtube.com/watch?v=nE5EeQPiznU&index=4&list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
    def mainloop(data):
        gameExit = False
        while not gameExit:
            clock.tick_busy_loop(FPS)

            key = pygame.key.get_pressed()
            keyPressed(key,data)
            timerFired(data)
            # All the events in a list of pygame event
            for event in pygame.event.get():
                # When x button or esc key is clicked, close window
                if(event.type == pygame.QUIT or 
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    gameExit = True
        
                elif(event.type == pygame.MOUSEBUTTONDOWN): # Mouse pressed
                    mousePressed(event,data)
                
            redrawAll(data, gameDisplay)

            # Update every page that is being updated
            pygame.display.update()

    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.title = "Fortress"
    init(data)

    # Initialize pygame and screen
    pygame.init()
    pygame.display.set_mode((data.width, data.height))
    pygame.display.set_caption(data.title) # Entitle
    gameDisplay = pygame.display.get_surface()
    clock = pygame.time.Clock()
    FPS = 300

    pS_convertBackgroundImage(data,gameDisplay)

    # Mainloop
    mainloop(data)

    pygame.quit()
run()
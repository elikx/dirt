import random, sys, copy, os, pygame, time
from pygame.locals import *

# FUNCTIONS AND
def drawTile(tileType, x, y):
    imageLoad = (pygame.transform.scale(pygame.image.load('tiles/'+tileType+'.png'), (tileSizeX, tileSizeY))).convert()
    DISPLAYSURF.blit((imageLoad), (x-camera.x, y-camera.y))
            
def drawRow(layer, row):
    layerMap = layer.split(',')
    for i in range(len(layerMap)):
        if layerMap[i] == '+':
            drawTile('sky', i, row)
            print('sky')
        if layerMap[i] == '=':
            drawTile('grass', i, row)
            print('grass')
        if layerMap[i] == '-':
            drawTile('dirt', i, row)
            print('dirt')

class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(tileSizeX*5, 100, playerSizeX, playerSizeY)
    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for solid in solids:
            if self.rect.colliderect(solid.rect):
                if dx > 0:
                    self.rect.right = solid.rect.left
                if dx < 0:
                    self.rect.left = solid.rect.right
                if dy > 0:
                    self.rect.bottom = solid.rect.top
                if dy < 0:
                    self.rect.top = solid.rect.bottom
        if self.rect.left < tileSizeX*4:
            camera.x += dx
            cammov = True
            self.rect.left = tileSizeX*4
        if self.rect.right > screenX-(tileSizeX*4):
            camera.x += dx
            cammov = True
            self.rect.right = screenX-(tileSizeX*4)
        if self.rect.bottom > screenY-(tileSizeY*3):
            camera.y += dy
            self.rect.bottom = screenY-(tileSizeY*3)
            cammov = True

class NPC(object):
    def __init__(self,xx,yy):
        self.rect = pygame.Rect(xx, yy, npcSizeX, npcSizeY)
    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for solid in solids:
            if self.rect.colliderect(solid.rect):
                if dx > 0:
                    self.rect.right = solid.rect.left
                if dx < 0:
                    self.rect.left = solid.rect.right
                if dy > 0:
                    self.rect.bottom = solid.rect.top
                if dy < 0:
                    self.rect.top = solid.rect.bottom
        if self.rect.left < tileSizeX*4:
            camera.x += dx
            self.rect.left = tileSizeX*4
        if self.rect.right > screenX-(tileSizeX*4):
            camera.x += dx
            self.rect.right = screenX-(tileSizeX*4)
        if self.rect.bottom > screenY:
            self.rect.bottom = 0
            self.rect.top = -100
    def draw(npcName, x, y):
        imageLoad = pygame.transform.scale((pygame.image.load('sprites/'+npcName+'.png')), (npcSizeX, npcSizeY)).convert_alpha()
        DISPLAYSURF.blit(imageLoad, (x-camera.x, y-camera.y))

class Solid(object):
    def __init__(self, pos):
        solids.append(self)
        self.rect = pygame.Rect(pos[0]-camera.x, pos[1]-camera.y, tileSizeX, tileSizeY)

# SET UP
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
tileSizeX, tileSizeY = 72, 72
screenX, screenY = tileSizeX*16, tileSizeY*9
playerSizeX, playerSizeY = 27, 72
flags = DOUBLEBUF | HWACCEL
DISPLAYSURF = pygame.display.set_mode((screenX, screenY), flags)
pygame.display.set_caption('Dirt')
FPS = 30
fpsClock = pygame.time.Clock()
gravity = 10
vg = 0
tv = 100
bsc = 0
camera = pygame.rect.Rect(0, 0, screenX, screenY)
font = pygame.font.Font(None, 36)

# SPRITES
pLeft = pygame.transform.scale((pygame.image.load('sprites/playerleft.png')), (playerSizeX+15, playerSizeY)).convert_alpha()
pRight = pygame.transform.scale((pygame.image.load('sprites/playerright.png')), (playerSizeX+15, playerSizeY)).convert_alpha()
pLeftBA = pygame.transform.scale((pygame.image.load('sprites/playerleftba.png')), (playerSizeX+15, playerSizeY)).convert_alpha()
pRightBA = pygame.transform.scale((pygame.image.load('sprites/playerrightba.png')), (playerSizeX+15, playerSizeY)).convert_alpha()
pLeftWA = pygame.transform.scale((pygame.image.load('sprites/playerleftwa.png')), (playerSizeX+15, playerSizeY)).convert_alpha()
pRightWA = pygame.transform.scale((pygame.image.load('sprites/playerrightwa.png')), (playerSizeX+15, playerSizeY)).convert_alpha()
pLeftWB = pygame.transform.scale((pygame.image.load('sprites/playerleftwb.png')), (playerSizeX+15, playerSizeY)).convert_alpha()
pRightWB = pygame.transform.scale((pygame.image.load('sprites/playerrightwb.png')), (playerSizeX+15, playerSizeY)).convert_alpha()
pRightSA = pygame.transform.scale((pygame.image.load('sprites/playerrightsa.png')), (playerSizeX+15, playerSizeY)).convert_alpha()
pLeftSA = pygame.transform.scale((pygame.image.load('sprites/playerleftsa.png')), (playerSizeX+15, playerSizeY)).convert_alpha()

pRightWalk = {'walk0':pRightWA, 'walk1':pRight, 'walk2':pRightWB, 'walk3':pRight}
pLeftWalk = {'walk0':pLeftWA, 'walk1':pLeft, 'walk2':pLeftWB, 'walk3':pLeft}
playerSprite = pRight
icon = pygame.image.load('sprites/icon.png')
pygame.display.set_icon(icon)

# PLAYER STUFF
playerx = 10
playery = 10
movespeed = 15
newLevel = 1
jumpspeed = 15
player = Player()
moveDirH = 'NONE'
moveDirV = 'NONE'
moveDirHL = 'NONE'
walkFrame = 0
wCount = 0
breakspeed = 10
playerOnGround = False

# ETC
solids = []
npcHere = {}
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
cammov = False

# START MAIN LOOP
while True:
    if moveDirH == 'NONE':
        commov = False
    # READ LEVEL
    if newLevel != False:
        levelFile = open('levels/level'+str(newLevel)+'.txt', 'r')
        rowC = 0
        levelMap = []
        for line in levelFile.readlines():
            levelMap.append(line.strip())
            drawRow(line, rowC)
            rowC += 1  
        levelFile.close()
        newLevel = False
    # DRAW MAP
    DISPLAYSURF.fill((0, 220, 255))
    x = y = 0
    solids = []
    for row in levelMap:
        for col in row:
            if col == '+':
                drawTile('sky', x, y)

            elif col == '0':
                drawTile('stone', x, y)
                Solid((x, y))
            elif col == '=':
                drawTile('grass', x, y)
                Solid((x, y))
            elif col == '-':
                drawTile('dirt', x, y)
                Solid((x, y))
            elif col == 'x':
                drawTile('dug', x, y)
                
            elif col == '$':
                npcSizeX = 27+15
                npcSizeY = 72
                drawTile('dug', x, y)
                NPC(x, y)
                NPC.draw('playerleft', x, y)
            x += tileSizeX
        y += tileSizeY
        x = 0
    if cammov == True:
        print(cammov)
        
    # GRAVITY
    playerOnGround = False
    if vg > tv:
        vg = tv
    else:
        vg += gravity
    for solid in solids:
        if player.rect.right > solid.rect.left and player.rect.left < solid.rect.right:
            if player.rect.bottom == solid.rect.top:
                vg = 0
                playerOnGround = True
            if player.rect.top == solid.rect.bottom:
                vg = gravity
    # QUIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                bsc = 0
                moveDirH = 'NONE'
                moveDirHL = 'LEFT'
                playerSprite = pLeft
            if event.key == K_RIGHT:
                bsc = 0
                moveDirH = 'NONE'
                moveDirHL = 'RIGHT'
                playerSprite = pRight
            if event.key == K_DOWN:
                bsc = 0
                moveDirV = 'NONE'
                if moveDirHL == 'LEFT':
                    playerSprite = pLeft
                elif moveDirHL == 'RIGHT':
                    playerSprite = pRight

        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                bsc = 0
            if event.key == K_RIGHT:
                bsc = 0
            if event.key == K_DOWN:
                bsc = 0

            
    # PLAYER MOVE
    key = pygame.key.get_pressed()
    
    if key[pygame.K_LEFT]:
        moveDirH = 'LEFT'
        playerSprite = pLeft
        player.move(-movespeed, 0)
        for solid in solids:
            if player.rect.bottom == solid.rect.bottom and player.rect.left == solid.rect.right:
                bsc += breakspeed
                if bsc >= 100:
                    colt = (solid.rect.left+camera.x)//tileSizeX
                    rowt = (solid.rect.top+camera.y)//tileSizeY
                    tt = []
                    tc = 0
                    for char in levelMap[rowt]:
                        if tc == colt and char != '+':
                            tt.append('x')
                        else:
                            tt.append(char)
                        tc += 1
                    levelMap[rowt]=''.join(tt)
                    solids = []
                    bsc = 0
                break
    
    if key[pygame.K_RIGHT]:
        moveDirH = 'RIGHT'
        playerSprite = pRight
        player.move(movespeed, 0)
        for solid in solids:
            if player.rect.bottom == solid.rect.bottom and player.rect.right == solid.rect.left:
                bsc += breakspeed
                if bsc >= 100 and playerOnGround:
                    colt = (solid.rect.left+camera.x)//tileSizeX
                    rowt = (solid.rect.top+camera.y)//tileSizeY
                    tt = []
                    tc = 0
                    for char in levelMap[rowt]:
                        if tc == colt and char != '+':
                            tt.append('x')
                        else:
                            tt.append(char)
                        tc += 1
                    levelMap[rowt]=''.join(tt)
                    solids = []
                    bsc = 0
                break
        
    if key[pygame.K_UP] and playerOnGround == True:
        player.move(0, -12)
        vg -= 30
        bsc = 0
    if key[pygame.K_DOWN] and playerOnGround == True and not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
        moveDirV = 'DOWN'
        for solid in solids:
            if player.rect.bottom == solid.rect.top and player.rect.right <= solid.rect.right and player.rect.left >= solid.rect.left:
                bsc += breakspeed
                if bsc >= 100 and playerOnGround:
                    colt = (solid.rect.left+camera.x)//tileSizeX
                    rowt = (solid.rect.top+camera.y)//tileSizeY
                    tt = []
                    tc = 0
                    for char in levelMap[rowt]:
                        if tc == colt and char != '+':
                            tt.append('x')
                        else:
                            tt.append(char)
                        tc += 1
                    levelMap[rowt]=''.join(tt)
                    solids = []
                    bsc = 0
                break
    # FALL
    player.move(0, vg)

    # WALKING ANIMATION
    if playerOnGround:
        if moveDirH == 'RIGHT':
            if bsc > 0:
                wCount += 1
                if wCount%3 != 0:
                    playerSprite = pRight
                else:
                    playerSprite = pRightBA
            else:       
                playerSprite = pRightWalk['walk'+str(walkFrame)]
                walkFrame += 1
                if walkFrame > 3:
                    walkFrame = 0
        elif moveDirH == 'LEFT':
            if bsc > 0:
                wCount += 1
                if wCount%3 != 0:
                    playerSprite = pLeft
                else:
                    playerSprite = pLeftBA
            else:       
                playerSprite = pLeftWalk['walk'+str(walkFrame)]
                walkFrame += 1
                if walkFrame > 3:
                    walkFrame = 0
        elif moveDirV == 'DOWN':
            if bsc > 0:
                wCount += 1
                if moveDirHL == 'RIGHT':
                    if wCount%4 == 0:
                        playerSprite = pRight
                    else:
                        playerSprite = pRightSA
                if moveDirHL == 'LEFT':
                    if wCount%4 == 0:
                        playerSprite = pLeft
                    else:
                        playerSprite = pLeftSA
        elif moveDirHL == 'RIGHT':
            playerSprite = pRight
        elif moveDirHL == 'LEFT':
            playerSprite = pLeft

        else:
            walkFrame = 0
            wCount = 0

    else:
        if moveDirH == 'LEFT':
            playerSprite = pLeftWalk['walk0']
        elif moveDirH == 'RIGHT':
            playerSprite = pRightWalk['walk0']
        elif moveDirHL == 'LEFT':
            playerSprite = pLeftWalk['walk0']
        elif moveDirHL == 'RIGHT':
            playerSprite = pRightWalk['walk0']
        bsc = 0
    
    DISPLAYSURF.blit(playerSprite, (player.rect.x-7, player.rect.y))
    fpsClock.tick(FPS)
    showfps = font.render(str(int(fpsClock.get_fps())), 1, (10, 10, 10))
    DISPLAYSURF.blit(showfps, (10, 10))
    pygame.display.update(0, 0, screenX, screenY)
    

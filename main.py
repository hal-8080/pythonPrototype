import pygame as pg
import random
pg.init()

class Segment: 
    def __init__(self, screen, offset):
        self.screen = screen
        self.offset = offset
        self.on = (255, 0, 0)
        self.off = (225, 225, 225)
        self.createRects()
        self.rectsColors = [0, 0, 0, 0, 0, 0, 0]
    
    def createRects(self):
        self.rects = []
        """
            A
        F        B
            G
        E       C
            D    

        pg.Rect(left, top, width, height)
        """
        A = pg.Rect(self.offset + 50, 25, 75, 25)
        B = pg.Rect(self.offset + 125, 50, 25, 75)
        C = pg.Rect(self.offset + 125, 150, 25, 75)
        D = pg.Rect(self.offset + 50, 225, 75, 25)
        E = pg.Rect(self.offset + 25, 150, 25, 75)
        F = pg.Rect(self.offset + 25, 50, 25, 75)
        G = pg.Rect(self.offset + 50, 125, 75, 25)
        self.rects = [A, B, C, D, E, F, G]
        self.state = 0

    def setState(self, state):
        if state == 0b000:
            self.rectsColors = [0, 0, 0, 0, 0, 0, 0]
        elif state == 0b001: #Upper seg
            self.rectsColors = [1, 0, 0, 0, 0, 0, 0]
        elif state == 0b010: #Middle seg
            self.rectsColors = [0, 0, 0, 0, 0, 0, 1]
        elif state == 0b100: #Lower seg
            self.rectsColors = [0, 0, 0, 1, 0, 0, 0]
        elif state == 0b011: #Upper + middle seg
            self.rectsColors = [1, 0, 0, 0, 0, 0, 1]
        elif state == 0b101: #Upper + lower seg
            self.rectsColors = [1, 0, 0, 1, 0, 0, 0]
        elif state == 0b110: #Middle + lower seg
            self.rectsColors = [0, 0, 0, 1, 0, 0, 1]
        elif state == 0b111: #All on
            self.rectsColors = [1, 0, 0, 1, 0, 0, 1]
    
    def setChar(self, c):
        if c == "0" or c.lower() == "o":
            self.rectsColors = [1, 1, 1, 1, 1, 1, 0]
        elif c == "1":
            self.rectsColors = [0, 1, 1, 0, 0, 0, 0]
        elif c == "2":
            self.rectsColors = [1, 1, 0, 1, 1, 0, 1]
        elif c == "3":
            self.rectsColors = [1, 1, 1, 1, 0, 0, 1]
        elif c == "4":
            self.rectsColors = [0, 1, 1, 0, 0, 1, 1]
        elif c == "5" or c.lower() == "s":
            self.rectsColors = [1, 0, 1, 1, 0, 1, 1]
        elif c == "6":
            self.rectsColors = [1, 0, 1, 1, 1, 1, 1]
        elif c == "7":
            self.rectsColors = [1, 1, 1, 0, 0, 0, 0]
        elif c == "8":
            self.rectsColors = [1, 1, 1, 1, 1, 1, 1]
        elif c == "9":
            self.rectsColors = [1, 1, 1, 1, 0, 1, 1]
        elif c.lower() == "l":
            self.rectsColors = [0, 0, 0, 1, 1, 1, 0]
        elif c.lower() == "e":
            self.rectsColors = [1, 0, 0, 1, 1, 1, 1]
        elif c.lower() == "r":
            self.rectsColors = [0, 0, 0, 0, 1, 0, 1]
        elif c == "-":
            self.rectsColors = [0, 0, 0, 0, 0, 0, 0]


        
    def draw(self):
        for i in range(len(self.rects)):
            if self.rectsColors[i] == 0:
                pg.draw.rect(screen, self.off, self.rects[i])
            if self.rectsColors[i] == 1:
                pg.draw.rect(screen, self.on, self.rects[i])

singleSegWidth = 175
screen = pg.display.set_mode([singleSegWidth*6, 275])
screen.fill((255, 255, 255))

segArray = []
for i in range(6):
    segArray.append(Segment(screen, singleSegWidth*i))

playerstate = 0b010
seg0 = 0b000
seg1 = 0b000
seg2 = 0b000
seg3 = 0b000
seg4 = 0b000
seg5 = 0b000

firstFewInput = 0

score = 0
timerloop = 0
timerloopMAX = 1000
blinktimerMAX = 100
playerblink = 1
t0 = pg.time.get_ticks()
t1 = pg.time.get_ticks()
blink0 = pg.time.get_ticks()
blink1 = pg.time.get_ticks()

def gameloop():
    global playerstate
    global seg0
    global t0
    global timerloop
    global timerloopMAX
    global score
    global blink0
    global blink1
    global playerblink
    t1 = pg.time.get_ticks()
    blink1 = pg.time.get_ticks()
    if (blink1 - blink0) > blinktimerMAX:
        blink0 = pg.time.get_ticks()
        blink1 = pg.time.get_ticks()
        playerblink = not playerblink
    updatePlayer()
    if (t1 - t0) > timerloopMAX:
        t0 = t1
        timerloopMAX -= 10
        updateGame()
        score += 1
    collission = playerstate & seg0
    if collission:
        dead()
    drawSegments()
    #jump gameloop

def updatePlayer():
    global playerstate
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        playerstate = 0b001
    elif keys[pg.K_DOWN]:
        playerstate = 0b100
    else:
        playerstate = 0b010
    #return to caller

def updateGame():
    global seg0
    global seg1
    global seg2
    global seg3
    global seg4
    global seg5
    global firstFewInput
    
    seg0 = seg1
    seg1 = seg2
    seg2 = seg3
    seg3 = seg4
    seg4 = seg5
    if seg4 == 0b000:
        seg5 = random.choice([0b001, 0b010, 0b100, 0b011, 0b110, 0b101])
    elif seg3 == 0b000:
        seg5 = seg4
    else:
        seg5 = 0b000
    #jump back to caller

def drawSegments():
    firstSegment = seg0 | playerstate*playerblink
    segStateArray = [firstSegment, seg1, seg2, seg3, seg4, seg5]
    for i in range(6):
        segArray[i].setState(segStateArray[i])
        segArray[i].draw()
    pg.display.flip()

def dead():
    global score
    print("You're dead. Score: " + str(score))
    #if inputUP == 0 and inputDOWN == 0: jump dead
    global timerloop
    global timerloopMAX
    global t0
    
    global seg0
    global seg1
    global seg2
    global seg3
    global seg4
    global seg5
    global segArray

    scorestring = str(score)

    dead = True
    dead0 = pg.time.get_ticks()
    dead1 = pg.time.get_ticks()
    sendScore = 0
    loserArray = ["l", "o", "s", "e", "r", "-"]
    output = loserArray
    while dead:
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_DOWN]:
            dead = False
        
        dead1 = pg.time.get_ticks()
        if (dead1 - dead0) > 500:
            dead0 = dead1
            if sendScore == 1:
                output = ["-"] * 6
                for i in range(len(scorestring)):
                    output[i] = scorestring[i]
            else:
                output = loserArray
            
            for i in range(6):
                segArray[i].setChar(output[i])
                segArray[i].draw()
            sendScore = not sendScore
        pg.display.flip()

    seg0 = 0b000
    seg1 = 0b000
    seg2 = 0b000
    seg3 = 0b000
    seg4 = 0b000
    seg5 = 0b000
    score = 0
    timerloop = 0
    timerloopMAX = 1000
    t0 = pg.time.get_ticks()
    #jump gameloop

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    gameloop()
    #update segment display
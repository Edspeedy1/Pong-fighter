"Pong Bash v0.6.0"

import pygame, math
from random import randint, random
pygame.init()

screenSize = (1900,1060)
mapSelect = 4
players = 2
SPEED = 60

mainScreen = pygame.display.set_mode()
SCREEN = pygame.surface.Surface((1800,1000))
totalMaps = 5

class playerClass:
    def __init__(self,num):
        self.tankType = 'basic'
        self.num = num
        self.isDead = False
        self.size = (150,75)
        self.speed = 2.5*150/SPEED
        self.x = 900
        self.y = [950, 125][num%2]
        self.cooldown = 20
        self.cooldownMax = 200 
        self.health = 3
        self.shieldW = 15
        self.shieldH = 12
        self.images = [pygame.transform.scale( pygame.image.load(f'PongBash\\Tanks\\{self.tankType}{num}{i+1}.png'), (self.size[0]+20, self.size[1]+40)) for i in range(self.health)]

    def left(self):
        self.x = max(self.x-self.speed, 300)
    def right(self):
        self.x = min(self.x+self.speed, 1500)
    def render(self):
        if not self.isDead: SCREEN.blit(self.images[self.health-1], (self.x-self.size[0]/2-12, self.y-self.size[1]/2-65+20*(self.num%2==1)))
    def shoot(self):
        if self.cooldown == 0 and not self.isDead:
            if self.num%2 == 0: bulletList.append(bulletClass(self.x, self.y-100, 0))
            else: bulletList.append(bulletClass(self.x, self.y+20, 180))
            self.cooldown = self.cooldownMax

class speedTank(playerClass):
    def __init__(self, num):
        super().__init__(num)
        self.tankType = 'speed'
        self.size = (150,50)
        self.speed = 4.3*150/SPEED
        self.y = [950, 125][num%2] - 20*(num%2==1)
        self.cooldownMax = 300
        self.health = 2
        self.images = [pygame.transform.scale( pygame.image.load(f'PongBash\\Tanks\\{self.tankType}{num}{i+1}.png'), (self.size[0]+20, self.size[1]+40)) for i in range(self.health)]
    def shoot(self):
        '''if self.cooldown == 0 and not self.isDead:
            if self.num%2 == 0: bulletList.append(bulletClass(self.x, self.y-100, 0,speed=8,size=10))
            else: bulletList.append(bulletClass(self.x, self.y+20, 180,speed=8,size=10))
            self.cooldown = self.cooldownMax'''
        if self.cooldown == 0 and not self.isDead:
            if self.num%2 == 0: 
                bulletList.append(bulletClass(self.x, self.y-100, 0,speed=8))
                bulletList.append(bulletClass(self.x+30, self.y-120, 10,speed=8))
                bulletList.append(bulletClass(self.x-30, self.y-140, 350,speed=8))
            else: 
                bulletList.append(bulletClass(self.x, self.y+20, 180,speed=8))
                bulletList.append(bulletClass(self.x+35, self.y+40, 170,speed=8))
                bulletList.append(bulletClass(self.x-35, self.y+60, 190,speed=8))
            self.cooldown = self.cooldownMax/4

class defTank(playerClass):
    def __init__(self, num):
        super().__init__(num)
        self.tankType = 'tank'
        self.size = (155,90)
        self.speed = 1.8*150/SPEED
        self.cooldownMax = 120
        self.health = 4
        self.shieldWidth = 25
        self.images = [pygame.transform.scale( pygame.image.load(f'PongBash\\Tanks\\{self.tankType}{num}{i+1}.png'), (self.size[0]+20, self.size[1]+40)) for i in range(self.health)]
    def shoot(self):
        if self.cooldown == 0 and not self.isDead:
            if self.num%2 == 0: bulletList.append(bulletClass(self.x, self.y-100, 0,speed=3,size=20))
            else: bulletList.append(bulletClass(self.x, self.y+20, 180,speed=3,size=20))
            self.cooldown = self.cooldownMax

class gunTank(playerClass):
    def __init__(self, num):
        super().__init__(num)
        self.tankType = 'gunner'
        self.size = (150,75)
        self.speed = 2.3*150/SPEED
        self.cooldownMax = 180
        self.images = [pygame.transform.scale( pygame.image.load(f'PongBash\\Tanks\\{self.tankType}{num}{i+1}.png'), (self.size[0]+20, self.size[1]+40)) for i in range(self.health)]
    def shoot(self):
        if self.cooldown == 0 and not self.isDead:
            if self.num%2 == 0: 
                bulletList.append(bulletClass(self.x, self.y-100, 0))
                bulletList.append(bulletClass(self.x+30, self.y-120, 10))
                bulletList.append(bulletClass(self.x-30, self.y-140, 350))
            else: 
                bulletList.append(bulletClass(self.x, self.y+20, 180))
                bulletList.append(bulletClass(self.x+35, self.y+40, 170))
                bulletList.append(bulletClass(self.x-35, self.y+60, 190))
            self.cooldown = self.cooldownMax


class bulletClass:
    def __init__(self,x,y,direction,size=15,speed=5):
        self.x = x
        self.y = y
        self.speed = speed*150/SPEED
        self.radius = size
        self.direction = direction
        self.timeSinceCollision = 0
        self.errorStack = 0

    def move(self):
        self.x += self.speed*math.sin(math.radians(self.direction))
        self.y -= self.speed*math.cos(math.radians(self.direction))
        if self.timeSinceCollision < 20:
            self.timeSinceCollision += 1
            if self.timeSinceCollision >= 10:
                self.errorStack = 0
        else:
            self.errorStack = 0

    def bounce(self,angle):
        self.direction = 2*angle - self.direction
        if self.timeSinceCollision <= 1:
            self.errorStack += 1
        if self.errorStack >= 10 and self in bulletList:
            bulletList.remove(self)
        self.timeSinceCollision = 0

class particleClass:
    def __init__(self,x,y,power):
        self.x = x
        self.y = y
        self.direction = 360*random()
        self.speed = (power/3*(0.6+random()))*150/SPEED
        self.persistance = power
        self.size = power*1.5
        self.color = 254
    
    def move(self):
        self.x += self.speed*math.sin(math.radians(self.direction))
        self.y -= self.speed*math.cos(math.radians(self.direction))

    def reduce(self):
        self.speed -= (1/(2*self.persistance))*150/SPEED
        self.size -= (1/self.persistance)*150/SPEED

def renderPlayer(player):
    colors = (  ((5,20,50),(30,120,120),(0,150,200),(100,170,220)),
                ((30,5,0),(130,50,30),(230,150,0)),
                ((0,50,30),(50,150,80),(0,250,150)),
                ((50,0,35),(150,50,100),(255,10,180)))
    gunColors = ([0,50,220],[200,50,0],[20,50,10],[80,0,30])

    rect = pygame.rect.Rect(player.x-player.size[0]/2, player.y-player.size[1], player.size[0], player.size[1])
    shield1Rect = pygame.rect.Rect(player.x-player.size[0]/2-10, player.y-player.size[1]-player.shieldH/2, player.shieldW, player.size[1]+player.shieldH/1)
    shield2Rect = pygame.rect.Rect(player.x+player.size[0]/2-10, player.y-player.size[1]-player.shieldH/2, player.shieldW, player.size[1]+player.shieldH/1)
    
    if player.num%2 == 0: gunRect = pygame.rect.Rect(player.x-10, player.y-player.size[1]-15, 20, 40)
    else: gunRect = pygame.rect.Rect(player.x-10, player.y-22, 20, 40)

    pygame.draw.rect(SCREEN, gunColors[player.num], gunRect)
    pygame.draw.rect(SCREEN, colors[player.num][player.health-1], rect)
    pygame.draw.rect(SCREEN, (255,255,255), shield1Rect)
    pygame.draw.rect(SCREEN, (255,255,255), shield2Rect)

def renderBullet(bullet):
    pygame.draw.circle(SCREEN, (250,250,250), (bullet.x,bullet.y), bullet.radius)

def reduceCooldowns():
    for player in playerList:
        player.cooldown = max(player.cooldown-150/SPEED,0)


def sideShot(num):
    x = sphereList[num%2][0]+[90,-90][num%2]
    y = sphereList[num%2][1]
    shot = bulletClass(x, y, [90,-90][num%2])
    shot.move()
    bulletList.append(shot)

def bulletColision(bullet):
    for i in sphereList:
        x = bullet.x - i[0]
        y = bullet.y - i[1]
        hype = (x**2+y**2)**(1/2)
        if hype <= i[2] + bullet.radius:
            try: angle = math.degrees(math.atan((y)/x))
            except: angle = 90
            bullet.bounce(angle)
            for k in range(randint(4, 8)): particaleList.append(particleClass(bullet.x, bullet.y, 5))
            bullet.move()
    for i in bulletList:
        x = bullet.x - i.x
        y = bullet.y - i.y
        hype = (x**2+y**2)**(1/2)
        if hype <= i.radius + bullet.radius and hype != 0:
            for k in range(randint(5, 10)): particaleList.append(particleClass(i.x, i.y, 8))
            bulletList.remove(i)
            bulletList.remove(bullet)
    
    for i in range(len(rectList)):
        rect = rectList[i][1:]
        for j in range(len(rect)):
            if circle_line_segment_intersection((bullet.x,bullet.y), bullet.radius, rect[j], rect[(j+1)%(len(rect))]): 
                for k in range(randint(5, 9)): particaleList.append(particleClass(bullet.x, bullet.y, 6))
                if abs(bullet.direction-anglesList[i][j]) <= 5: bullet.direction += 10
                bullet.bounce(anglesList[i][j])
                bullet.move()

    for player in playerList:
        if player.isDead: continue
        shield1Rect = pygame.rect.Rect(player.x-player.size[0]/2-10-bullet.radius/2, player.y-player.size[1]-3-bullet.radius/2, 15+bullet.radius, player.size[1]+6+bullet.radius)
        shield2Rect = pygame.rect.Rect(player.x+player.size[0]/2-10-bullet.radius/2, player.y-player.size[1]-3-bullet.radius/2, 15+bullet.radius, player.size[1]+6+bullet.radius)
        bodyrect = pygame.rect.Rect(player.x-player.size[0]/2, player.y-player.size[1], player.size[0], player.size[1])
        if shield1Rect.collidepoint(bullet.x, bullet.y) or shield2Rect.collidepoint(bullet.x, bullet.y):
            for k in range(randint(5, 10)): particaleList.append(particleClass(bullet.x, bullet.y, 8.5))
            try: bulletList.remove(bullet)
            except: pass
            sideShot(player.num)
            for k in range(randint(5, 10)): particaleList.append(particleClass(bulletList[len(bulletList)-1].x, bulletList[len(bulletList)-1].y, 6.5))
            player.cooldown = 0
        if bodyrect.collidepoint(bullet.x, bullet.y):
            try: bulletList.remove(bullet)
            except: pass
            player.health = player.health - 1
            for k in range(randint(10, 20)): particaleList.append(particleClass(bullet.x, bullet.y, 10))
            if player.health <= 0:
                playerList[playerList.index(player)].isDead = True
                if players == 2:
                    endScreen(player.num)
                else:
                    if player2.isDead and player4.isDead:
                        endScreen(1)
                    if player1.isDead and player3.isDead:
                        endScreen(0)

def circle_line_segment_intersection(circle_center, circle_radius, pt1, pt2, full_line=False, tangent_tol=1e-9):
    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2)**.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2
    if discriminant < 0: return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
            intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections

def moveParticles():
    for i in particaleList:
        i.move()
        i.reduce()
        if i.size <= 0.3: particaleList.remove(i)
        pygame.draw.circle(SCREEN, (i.color,i.color,i.color), (i.x,i.y), i.size)

def moveObjects():
    if mapSelect == 0:
        for i in range(4):
            if sphereList[i][4] == 0:
                sphereList[i][1] = sphereList[i][1]+0.5*150/SPEED
                if sphereList[i][1] >= 700: sphereList[i][4] = 1
            else:
                sphereList[i][1] = sphereList[i][1]-0.5*150/SPEED
                if sphereList[i][1] <= 300: sphereList[i][4] = 0
    elif mapSelect == 1:
        for i in range(4):
            if sphereList[i][4] == 0:
                sphereList[i][1] = sphereList[i][1]+0.5*150/SPEED
                if sphereList[i][1] >= 700: sphereList[i][4] = 1
            else:
                sphereList[i][1] = sphereList[i][1]-0.5*150/SPEED
                if sphereList[i][1] <= 300: sphereList[i][4] = 0
    elif mapSelect == 2:
        for i in range(8):
            if sphereList[i][4] == 0:
                sphereList[i][1] = sphereList[i][1]+0.75*150/SPEED
                if sphereList[i][1] >= 800: sphereList[i][4] = 1
            elif sphereList[i][4] == 1:
                sphereList[i][1] = sphereList[i][1]-0.75*150/SPEED
                if sphereList[i][1] <= 200: sphereList[i][4] = 0
            elif sphereList[i][4] == 2:
                sphereList[i][0] = sphereList[i][0]+0.25*150/SPEED
                if sphereList[i][0] >= 550: sphereList[i][4] = 3
            elif sphereList[i][4] == 3:
                sphereList[i][0] = sphereList[i][0]-0.25*150/SPEED
                if sphereList[i][0] <= 250: sphereList[i][4] = 2
            elif sphereList[i][4] == 4:
                sphereList[i][0] = sphereList[i][0]-0.25*150/SPEED
                if sphereList[i][0] <= 1250: sphereList[i][4] = 5
            elif sphereList[i][4] == 5:
                sphereList[i][0] = sphereList[i][0]+0.25*150/SPEED
                if sphereList[i][0] >= 1550: sphereList[i][4] = 4
    elif mapSelect == 3:
        for i in range(4):
            if sphereList[i][4] == 0:
                sphereList[i][1] = sphereList[i][1]+0.4*150/SPEED
                if sphereList[i][1] >= 770: sphereList[i][4] = 1
            elif sphereList[i][4] == 1:
                sphereList[i][1] = sphereList[i][1]-0.4*150/SPEED
                if sphereList[i][1] <= 230: sphereList[i][4] = 0
        for i in range(2,26):
            if sphereList[i+4][4] == 0:
                sphereList[i+4][1] = sphereList[i+4][1]+0.4*150/SPEED
                if sphereList[i+4][1] >= 750: sphereList[i+4][4] = 1
            elif sphereList[i+4][4] == 1:
                sphereList[i+4][1] = sphereList[i+4][1]-0.4*150/SPEED
                if sphereList[i+4][1] <= 250: sphereList[i+4][4] = 0           
            if sphereList[i+4][5] == 0:
                sphereList[i+4][0] = sphereList[i+4][0]+0.4*150/SPEED
                if sphereList[i+4][0] >= 1600: sphereList[i+4][5] = 1
            elif sphereList[i+4][5] == 1:
                sphereList[i+4][0] = sphereList[i+4][0]-0.4*150/SPEED
                if sphereList[i+4][0] <= 200: sphereList[i+4][5] = 0  
    elif mapSelect == 4:
        for i in range(4):
            if sphereList[i][4] == 0:
                sphereList[i][1] = sphereList[i][1]+0.5*150/SPEED
                if sphereList[i][1] >= 450 + (i%2)*450: sphereList[i][4] = 1
            else:
                sphereList[i][1] = sphereList[i][1]-0.5*150/SPEED
                if sphereList[i][1] <= 100 + (i%2)*450: sphereList[i][4] = 0
        for i in range(7):
            try: sphereList[i+4][0] += 1*150/SPEED
            except: pass    
            if sphereList[i+4][0] >= 1920: sphereList[i+4][0] = -320
            elif sphereList[i+4][0] <= -320: sphereList[i+4][0] = 1920
        

    for i in range(len(rectList)):
        pygame.draw.polygon(SCREEN, rectList[i][0], rectList[i][1:])

def gameReset(resetPlayers=True):
    global player1,player2,playerList,bulletList,sphereList,rectList,anglesList,a,d,w,l,r,u,f,t,h,j,k,l2
    bulletList = []
    if resetPlayers:
        playerList = [playerClass(0),playerClass(1)]
        player1 = playerList[0]
        player2 = playerList[1]
        if players == 4:
            global player3, player4
            player3 = playerClass(2)
            player4 = playerClass(3)
            playerList = [player1,player2,player3,player4]
    a,d,w = False,False,False
    l,r,u = False,False,False
    f,t,h = False,False,False
    j,k,l2 = False,False,False
    
    if mapSelect == 0:
        sphereList = [[50,500,75,(10,10,10),0],[1750,500,75,(10,10,10),1],[50,500,50,(210,210,210),0],[1750,500,50,(210,210,210),1],(900,500,50,(200,50,200)),(1050,650,100,(200,50,200)),(750,350,100,(200,50,200)),(-30,-30,200,(200,150,0)),(1830,-30,200,(200,150,0)),(-30,1030,200,(0,150,200)),(1830,1030,200,(0,150,200)),[325,650,75,(10,20,60),0],[1475,350,75,(40,5,0),1]]
        rect1 = ((100,220,100),(200,350),(250,325),(650,575),(600,600))
        rect2 = ((100,220,100),(1100,350),(1150,325),(1550,575),(1500,600))
        rectList = (rect1,rect2)
        anglesList = ((65,125,245,305),(65,125,245,305))
    elif mapSelect == 1:
        sphereList = [[50,500,75,(10,10,10),0],[1750,500,75,(10,10,10),1],[50,500,50,(210,210,210),0],[1750,500,50,(210,210,210),1],(900,500,50,(200,50,200)),(1050,650,100,(200,50,200)),(750,350,100,(200,50,200)),(-30,-30,200,(200,150,0)),(1830,-30,200,(200,150,0)),(-30,1030,200,(0,150,200)),(1830,1030,200,(0,150,200)),[325,650,75,(10,20,60),0],[1475,350,75,(40,5,0),1]]
        rect1 = ((100,220,100),(200,350),(250,325),(650,575),(600,600))
        rect2 = ((100,220,100),(1100,350),(1150,325),(1550,575),(1500,600))
        rectList = (rect1,rect2)
        anglesList = ((65,125,245,305),(65,125,245,305))
    elif mapSelect == 2:
        sphereList = [[50,500,75,(10,10,10),0],[1750,500,75,(10,10,10),1],[50,500,50,(210,210,210),0],[1750,500,50,(210,210,210),1],[550,650,100,(20,150,200),3],[250,350,100,(200,150,20),2],[1250,350,100,(200,150,20),5],[1550,650,100,(20,150,200),4],(0,0,150,(255,50,50)),(0,1000,150,(50,50,255)),(1800,0,150,(255,50,50)),(1800,1000,150,(50,50,255)),(400,500,50,(0,200,0)),(1400,500,50,(0,200,0))]
        rect1 = ((100,220,100),(700,500),(900,700),(1100,500),(900,300))
        tri1 = ((255,50,50),(725,500),(900,325),(1075,500),(900,425))
        tri2 = ((50,50,255),(725,500),(900,675),(1075,500),(900,575))
        diamond = ((200,50,200),(775,500),(900,550),(1025,500),(900,450))
        rectList = [rect1,diamond,tri1,tri2]
        anglesList = [(-45,45,-45,45)]
    elif mapSelect == 3:
        sphereList = [[50,500,75,(10,10,10),0],[1750,500,75,(10,10,10),1],[50,500,50,(210,210,210),0],[1750,500,50,(210,210,210),1],(-150,500,230,(0,200,0)),(1950,500,230,(0,200,0)),[900,500,40,(100,250,100),1,1],[870,470,40,(50,250,50),1,1],[840,440,40,(100,250,100),1,1],[810,410,40,(50,250,50),1,1],[780,380,40,(100,250,100),1,1],[750,350,40,(50,250,50),1,1],[720,320,40,(100,250,100),1,1],[690,290,40,(50,250,50),1,1],[660,260,40,(100,250,100),1,1],[630,270,40,(50,250,50),0,1],[600,300,40,(100,250,100),0,1],[570,330,40,(50,250,50),0,1],[900,500,40,(50,250,50),0,0],[930,530,40,(100,250,100),0,0],[960,560,40,(50,250,50),0,0],[990,590,40,(100,250,100),0,0],[1020,620,40,(50,250,50),0,0],[1050,650,40,(100,250,100),0,0],[1080,680,40,(50,250,50),0,0],[1110,710,40,(100,250,100),0,0],[1140,740,40,(50,250,50),0,0],[1170,740,40,(100,250,100),1,0],[1200,710,40,(50,250,50),1,0],[1230,680,40,(100,250,100),1,0],[900,500,125,(250,50,250)],(600,-200,300,(250,0,50)),(1200,1200,300,(50,0,250)), (900,500,100,(100,12,170))]
        rectList = [((200,200,200),(750,500),(900,650),(1050,500),(900,350)),((150,150,150),(300,325),(450,475),(600,325),(450,275)),((150,150,150),(1500,675),(1350,525),(1200,675),(1350,725)),((250,150,0),(0,20),(0,170),(250,0)),((250,150,0),(1800,20),(1800,170),(1550,0)),((0,150,250),(0,980),(0,830),(250,1000)),((0,150,250),(1800,980),(1800,830),(1550,1000))]
        anglesList = ((-45,45,-45,45),(-45,45,-58,58),(-45,45,-58,58),(0,60,0,0),(0,-60,0,0),(0,-30,0,0),(0,30,0,0))
    elif mapSelect == 4:
        sphereList = [[50,400,75,(10,10,10),0],[1750,600,75,(10,10,10),1],[50,400,50,(210,210,210),0],[1750,600,50,(210,210,210),1],[0,500,80,(150,200,150)],[960,500,80,(150,200,150)],[320,500,80,(150,200,150)],[1280,500,80,(150,200,150)],[640,500,80,(150,200,150)],[1600,500,80,(150,200,150)],[-320,500,80,(150,200,150)], (0,0,150,(250,180,20)), (1800,0,150,(255,100,0)),(0,0,120,(250,215,50)), (1800,0,120,(225,40,0)), (1800,1000,150,(20,180,250)), (0,1000,150,(0,100,255)),(1800,1000,120,(50,215,250)), (0,1000,120,(0,40,225)), (1325,1815,900,(0,250,150)),(475,-815,900,(150,250,0)),(900,500,120,(150,12,210)),(690,50,40,(220,100,0)),(1110,960,40,(0,40,200))]
        rectList = [((1,100,100),(33,520),(120,660),(33,820),(-20,660)),((100,30,1),(1760,480),(1680,340),(1760,180),(1820,340))]
        anglesList = [(-32,32,122,32),(-32,32,0,0)]

def updateScreen(mainScreen):
    mainScreen.blit(pygame.transform.scale(SCREEN, screenSize), (0,0))
    pygame.display.update()

def endScreen(winTeam):
    global running,mapSelect
    running2 = True
    mapSelect = randint(1, 4)
    while running2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
                running2 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running2 = False
                    gameReset()
        if winTeam == 1: SCREEN.blit(pygame.image.load('PongBash\\PongBlueWins.png'), (0,0))
        else: SCREEN.blit(pygame.image.load('PongBash\\PongRedWins.png'), (0,0))
        updateScreen(mainScreen)

def pauseMenu():
    global running, mapSelect, playerList
    running2 = True
    changes = False
    rowSelected = 0
    arrow = pygame.image.load('PongBash\\arrow.png')
    fontName = 'Arial Bold'
    while running2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
                running2 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running2 = False
                    if changes: gameReset(resetPlayers=False)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s: rowSelected = min(rowSelected+1, 2 + 2*(players==4))
                if event.key == pygame.K_UP or event.key == pygame.K_w: rowSelected = max(rowSelected-1, 0)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: 
                    changes = True
                    if rowSelected == 0:
                        mapSelect  = (mapSelect-1)%totalMaps
                    else:
                        val = ['basic','tank','speed','gunner'].index(playerList[rowSelected-1].tankType)
                        playerList[rowSelected-1] = [playerClass(rowSelected-1),defTank(rowSelected-1),speedTank(rowSelected-1),gunTank(rowSelected-1)][(val + 1) % 4]
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                    changes = True
                    if rowSelected == 0:
                        mapSelect  = (mapSelect+1)%totalMaps
                    else:
                        val = ['basic','tank','speed','gunner'].index(playerList[rowSelected-1].tankType)
                        playerList[rowSelected-1] = [playerClass(rowSelected-1),defTank(rowSelected-1),speedTank(rowSelected-1),gunTank(rowSelected-1)][(val - 1) % 4]
            
        SCREEN.blit(pygame.font.SysFont(fontName, 190).render('Pause', True, (255,255,255),(85,60,30)),(700,20))
        pygame.draw.rect(SCREEN, (100,70,30), (190,140,1420, 570 + 250*(players==4)))
        pygame.draw.rect(SCREEN, (140,110,90), (200,150,1400, 550 + 250*(players==4)))
        pygame.draw.rect(SCREEN, (180,140,100), (800, 200+rowSelected*140, 500, 150))
        SCREEN.blit(pygame.font.SysFont(fontName, 100).render('Map Select :', True, (255,255,255)),(300,240))
        SCREEN.blit(pygame.font.SysFont(fontName, 100).render('Blue Tank :', True, (255,255,255)),(300,380))
        SCREEN.blit(pygame.font.SysFont(fontName, 100).render('Orange Tank :', True, (255,255,255)),(300,520))
        if players==4: 
            SCREEN.blit(pygame.font.SysFont(fontName, 100).render('Green Tank :', True, (255,255,255)),(300,660))
            SCREEN.blit(pygame.font.SysFont(fontName, 100).render('Pink Tank :', True, (255,255,255)),(300,800))
        for i in range(3 + 2*(players==4)):
            SCREEN.blit(arrow, (835, 240+i*140))
            SCREEN.blit(pygame.transform.flip(arrow, True, False), (1230, 240+i*140))
        SCREEN.blit(pygame.transform.scale(pygame.image.load(f'PongBash\\map{mapSelect}Icon.png'), (230,120)), (940, 220))

        for i in range(2 + 2*(players==4)):
            for j in range(20):
                try: SCREEN.blit(pygame.transform.scale(pygame.image.load(f'PongBash\\tanks\\{playerList[i].tankType}{i}{j+1}.png'), (230,120)), (940, 360+i*140))
                except: break
        updateScreen(mainScreen)


gameReset()
bg = pygame.image.load("Backdrop.png")
running = True
particaleList = []
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pauseMenu()
            if event.key == pygame.K_a: a = True
            if event.key == pygame.K_d: d = True
            if event.key == pygame.K_w: w = True
            if event.key == pygame.K_LEFT: l = True
            if event.key == pygame.K_RIGHT: r = True
            if event.key == pygame.K_UP: u = True
            if event.key == pygame.K_DOWN: u = True
            if event.key == pygame.K_f: f = True
            if event.key == pygame.K_h: h = True
            if event.key == pygame.K_t: t = True
            if event.key == pygame.K_j: j = True
            if event.key == pygame.K_l: l2 = True
            if event.key == pygame.K_k: k = True
            if event.key == pygame.K_i: k = True
            if event.key == pygame.K_SPACE:pass

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: a = False
            if event.key == pygame.K_d: d = False
            if event.key == pygame.K_w: w = False
            if event.key == pygame.K_LEFT: l = False
            if event.key == pygame.K_RIGHT: r = False
            if event.key == pygame.K_DOWN: u = False
            if event.key == pygame.K_UP: u = False
            if event.key == pygame.K_f: f = False
            if event.key == pygame.K_h: h = False
            if event.key == pygame.K_t: t = False
            if event.key == pygame.K_j: j = False
            if event.key == pygame.K_l: l2 = False
            if event.key == pygame.K_k: k = False
            if event.key == pygame.K_i: k = False
    SCREEN.blit(bg, (0,0))
    if a: playerList[0].left()
    if d: playerList[0].right()
    if w: playerList[0].shoot()
    if l: playerList[1].left()
    if r: playerList[1].right()
    if u: playerList[1].shoot()
    if players == 4:
        if f: playerList[2].left()
        if h: playerList[2].right()
        if t: playerList[2].shoot()
        if j: playerList[3].left()
        if l2: playerList[3].right()
        if k: playerList[3].shoot()

    for player in playerList:
        # renderPlayer(player)
        player.render()
    for i in bulletList:
        i.move()
        bulletColision(i)
        renderBullet(i)
        if 50 > i.x or i.x > 1750:
            for _ in range(randint(10, 20)): particaleList.append(particleClass(i.x, i.y, 5))
            i.bounce(0)
        elif 75 > i.y or i.y > 925:
            for _ in range(randint(10, 20)): particaleList.append(particleClass(i.x, i.y, 5))
            i.bounce(90)
    reduceCooldowns()
    moveObjects()
    moveParticles()
    for i in sphereList:
        pygame.draw.circle(SCREEN, i[3], (i[0],i[1]), i[2])
    updateScreen(mainScreen)
    clock.tick(SPEED)
 
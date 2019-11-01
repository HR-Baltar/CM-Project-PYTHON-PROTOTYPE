import pygame, sys, math
from random import randint

##### controls and notes
#space to shoot (its easier to hold space rather than tapping it)
#arrows to move (diagonal movement is allowed)
#you do not have to kill every enemy in the room

#known bugs##
##do NOT hold space when tranversig between room doors/passages

class projectile(object):
    def __init__ (self, user, radius, aim):

        self.x = user.rect.x + user.width//2
        self.y = user.rect.y + user.height//2
        self.radius = radius
        self.aim = aim
        self.vel = 10
        self.user = user
        self.bulletLife = 0

    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius +1)
        pygame.draw.circle(win, self.user.color, (self.x,self.y), self.radius)
    def update(self):
        self.x += round(self.vel * self.aim[0])
        self.y += round(self.vel * self.aim[1])

class sniper(projectile): 
    def __init__(self, user, radius, aim):
        super().__init__(user, radius, aim)
        self.aim = aim
        self.vel = 120
        self.x = user.rect.x + user.width//2
        self.y = user.rect.y + user.height//2
        self.bulletLife = 0
        self.time = 0
        self.angle = findAngle(self) 
        self.line = [(self.x, self.y), (bot.rect.centerx, bot.rect.centery)]     
        self.power = math.sqrt((self.line[1][1]-self.line[0][1])**2 +(self.line[1][0]-self.line[0][1])**2)/8 

    def update(self):
        self.time = 0.1 
        path = self.Path(self.x, self.y, self.vel, self.angle, self.time)
        self.x = path[0]
        self.y = path[1]

    @staticmethod
    def Path(startx, starty, power, ang, time):
        angle = ang
        velx = math.cos(angle) * power
        vely = math.sin(angle) * power
        distX = velx * -time
        distY = (vely * -time)
        newx = round(distX + startx)
        newy = round(starty - distY)
        return (newx, newy)

# class sprites
class Boss1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 150
        self.height = 150
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.color = red
        self.returnColor = red
        self.stunColor = white
        self.core = (self.rect.x + 2, self.rect.y + 2, self.width - 4, self.height - 4)
        self.maxLife = 33 #life
        self.life = self.maxLife
        self.isAlive = True
        self.stun = False
        self.shootLoop = 1
        self.stunLoop = 0
        self.ammo = []
        self.ammoS = []
        self.scoreCount = 1000
        self.pos = ['L', 'D']
        self.direction = randint(0,1)
        self.mode = 1 #Test mode
        self.moveLoop = 0
        self.changeLoop = 0
        self.change = True
        self.isMove = True
        self.wait = False
        self.centerLine = (400, 300)
        self.ammoCap = 3
        self.moveCount = 0
        self.exp = 0
        self.daze = False
        self.dazeLoop = 0
        self.hurt = False
        self.visible = True
        self.waitCap = 0


    def hit(self):
        if not self.daze:
            self.life -= 1


            if self.life >= 1:
                self.stun = True
                self.stunLoop = 1 
            else:
                self.isAlive = False
                self.visible = False

            ###phase change
            if self.life <= (self.maxLife * 1/3) and self.mode == 2:
                self.visible = False
                self.hurt = True
                self.dazeLoop = 1 
                self.color = green
                self.returnColor = green
                self.mode = 3     
                self.isMove = True  
                self.wait = True
                
            elif self.life <= (self.maxLife * 2/3) and self.mode == 1:
                self.visible = False
                self.hurt = True
                self.dazeLoop = 1 
                self.color = blue
                self.returnColor = blue
                self.mode = 2
        
    

    def update(self):
        #invinciblity 
        if self.hurt:
            self.daze = True
            if self.dazeLoop > 0:
                self.dazeLoop += 1
            if self.dazeLoop % 10 == 0:
                self.visible = True
            if self.dazeLoop % 6 == 0:
                self.visible = False
            if self.dazeLoop > 100:
                self.dazeLoop = 0
                self.hurt = False
                self.visible = True
                self.daze = False

        if self.mode == 1:
            self.vel = 8
            self.firerate = 25
            self.ammoCap = 2
            self.moveCap = 1 #new
            self.waitCap = 100
        if self.mode == 2:
            self.firerate = 15
            self.vel = 12
            self.ammoCap = 3
            self.moveCap = 2 #new
            self.waitCap = 80
        if self.mode == 3:
            self.firerate = 55
            self.vel = 9
            
        ##### update
        self.move()
        if not self.daze:
            self.action()
        pygame.draw.rect(win, (50,50,50), (200, 585, 400, 10))
        if self.isAlive:
            pygame.draw.rect(win, red, (200, 585, 400 - ((400/self.maxLife)*(self.maxLife-self.life)), 10))
        for bullet in self.ammoS:
            bullet.bulletLife += 1
            if bullet.bulletLife > 100:
                self.ammoS.pop(self.ammoS.index(bullet))
        for bullet in self.ammo:
            bullet.bulletLife += 1
            if bullet.bulletLife > 100:
                self.ammo.pop(self.ammo.index(bullet))
        if self.stunLoop > 0:
            self.color = self.stunColor
            self.stunLoop += 1
        if self.stunLoop > 6:
            self.stunLoop = 0
            self.stun = False
            self.color = self.returnColor

        if self.mode != 3: #
            if self.wait:
                self.moveLoop += 1
            if self.moveLoop >= self.waitCap:
                self.moveLoop = 0
                self.isMove = True
                self.wait = False


    def move(self):
        if self.isMove:
            if self.pos[self.direction] == 'D':
                end = 570
                if not (self.rect.bottom >= end - self.vel):
                    self.rect.y += self.vel
                else:
                    if self.rect.x > self.centerLine[0]:
                        self.pos = ['L', 'U']
                    else:
                        self.pos = ['R', 'U']
                    self.moveCount += 1
                    self.direction = randint(0, 1)
                    if self.mode != 3 and self.moveCount > self.moveCap: #new
                        self.isMove = False
                        self.wait = True
                        self.moveCount = 0
            elif self.pos[self.direction] == 'L':
                end = 40
                if not (self.rect.left <= end + self.vel):
                    self.rect.x -= self.vel
                else:
                    if self.rect.bottom < self.centerLine[1]:
                        self.pos = ['R', 'D']
                    else:
                        self.pos = ['R', 'U']
                    self.moveCount += 1
                    self.direction = randint(0, 1)
                    if self.mode != 3 and self.moveCount > self.moveCap: #new
                        self.isMove = False
                        self.wait = True
                        self.moveCount = 0
            elif self.pos[self.direction] == 'U':
                end = 30   
                if not (self.rect.y <= end + self.vel):
                    self.rect.y -= self.vel
                else:
                    if self.rect.x > self.centerLine[0]:
                        self.pos = ['L', 'D']
                    else:
                        self.pos = ['R', 'D']
                    self.moveCount += 1
                    self.direction = randint(0, 1)
                    if self.mode != 3 and self.moveCount > self.moveCap: #new
                        self.isMove = False
                        self.wait = True
                        self.moveCount = 0
            elif self.pos[self.direction] == 'R':
                end = 770
                if not (self.rect.right >= end - self.vel):
                    self.rect.x += self.vel
                else:
                    if self.rect.y < self.centerLine[1]:
                        self.pos = ['L', 'D']
                    else:
                        self.pos = ['L', 'U']
                    self.moveCount += 1
                    self.direction = randint(0, 1)
                    if self.mode != 3 and self.moveCount > self.moveCap: #new
                        self.isMove = False
                        self.wait = True
                        self.moveCount = 0

    def action(self):
        if self.shootLoop > 0:
            self.shootLoop += 1
        if self.shootLoop > self.firerate:

            self.shootLoop = 0
##        if self.mode == 1:
##            if bot.rect.x + bot.width >= self.rect.x + 50 and bot.rect.x <= self.rect.x + self.width -50:
##                if self.rect.y > bot.rect.y:
##                    aiming = (0, -1)
##                else:
##                    aiming = (0, 1)
##                self.attack(aiming)
##            if bot.rect.y + bot.height >= self.rect.y + 50 and bot.rect.y <= self.rect.y + self.height - 50:
##                if self.rect.x > bot.rect.x:
##                    aiming = (-1, 0)
##                else:
##                    aiming = (1, 0)
##                self.attack(aiming)
##        if self.mode == 2 or self.mode == 3:

        
        aiming = None ##dedent
        self.attack(aiming)            

    def attack(self, face):
        if self.shootLoop == 0:
                    
##            if self.mode == 1:
##                if len(self.ammo) < 3:
##                    self.shootLoop = 1
##                    self.ammo.append(projectile(self, 10, face))
                    
  #          if self.mode == 2 or self.mode == 3:
            face = 0 #dedent
            if len(self.ammoS) < self.ammoCap and self.wait:
                self.shootLoop = 1
                self.ammoS.append(sniper(self, 20, face))

class player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 30
        self.height = 30
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = yellow
        self.core = (self.rect.x + 2, self.rect.y + 2, self.width - 4, self.height - 4)
        self.changeX = 0
        self.changeY = 0
        self.vel = 5
        self.power = 3
        self.maxLife = 3
        self.life = self.maxLife
        self.isAlive = True
        self.hurt = False
        self.stun = False
        self.visible = True
        self.stunLoop = 0
        self.firerate = 10
        self.exp = 0
        self.expMax = 50
        self.level = 1
        self.text = None
    
    def levelUp(self):
        if self.level < 5:
            if self.exp >= self.expMax:
                self.exp -= self.expMax
                #self.expMax += 50
                self.level += 1
                if self.level == 2:
                    self.vel += 1
                    self.text = 'Speed Increased'
                if self.level == 3:
                    self.vel += 1
                    self.text = 'Speed Increased'
                if self.level == 4:
                    self.power += 2
                    self.text = 'Bullet Size Incresed'
                if self.level == 5:
                    self.maxLife += 1
                    self.text = 'Max HP Increased'
                self.life = self.maxLife
                ###level up display
                font3 =  pygame.font.SysFont('conicsans', 100)     
                text1 = font3.render('Level Up', 1, blue)
                text2 = font3.render(self.text, 1, blue)
                win.blit(text1, (400 - (text1.get_width()/2), 200))
                win.blit(text2, (400 - (text2.get_width()/2), 400))
                pygame.display.update()
                i = 0
                while i < 100:
                    pygame.time.delay(10) #10/1000Seconds
                    i += 1
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            i = 101
                            pygame.quit()
                            break

    def changespeed(self, x, y):
        ###mobility
        self.changeX =  x*self.vel
        self.changeY =  y*self.vel
        self.rect.x += self.changeX



        ###wall collision
        wallHit = pygame.sprite.spritecollide(self, roomNow.wallList, False)
        for wall in wallHit:
            if self.changeX > 0:
                self.rect.right = wall.rect.left - 3
            elif self.changeX < 0:
                self.rect.left = wall.rect.right + 3
                
        self.rect.y += self.changeY
        
        wallHit = pygame.sprite.spritecollide(self, roomNow.wallList, False)
        for wall in wallHit:
            if self.changeY > 0:
                self.rect.bottom = wall.rect.top -3
            else:
                self.rect.top = wall.rect.bottom +3
        
    def update(self):
        #damaged
        self.levelUp()
        if self.hurt:
            self.stun = True
            if self.stunLoop > 0:
                self.stunLoop += 1
            if self.stunLoop % 10 == 0:
                self.visible = True
            if self.stunLoop % 6 == 0:
                self.visible = False
            if self.stunLoop > 32:
                self.stunLoop = 0
                self.hurt = False
                self.visible = True
                self.stun = False

    def hit(self):
        if not self.stun:
            self.life -= 1
            self.visible = False
            self.hurt = True
            self.stunLoop = 1

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
class Virus(pygame.sprite.Sprite):
    def __init__(self, x, y, end, mode, ext):
        super().__init__()
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y
        self.end = end
        self.ext = ext
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.core = (self.rect.x + 2, self.rect.y + 2, self.width - 4, self.height - 4)
        self.mode = mode
        self.stun = False
        self.stunLoop = 0
        self.isAlive = True
        self.ammo = []
        self.life = 3
        self.vel = 5
        self.shootLoop = 0
        self.firerate = 0
        self.acc = 10


        if self.mode == 1:
            self.path = [x, self.end]
        if self.mode == 2:
            self.path = [y, self.end]
        if self.mode == 3:
            self.path = [x, y, self.end, (self.rect.y + self.ext)]

    def hit(self):
        self.life -= 1
        if self.life >= 1:
            self.stun = True
            self.stunLoop = 1  
        else:
            self.isAlive = False
    def update(self):
        if self.shootLoop > 0:
            self.shootLoop += 1
        if self.shootLoop > self.firerate:
            self.shootLoop = 0
        if self.stunLoop > 0:
            self.color = self.stunColor
            self.stunLoop += 1
        if self.stunLoop > 6:
            self.stunLoop = 0
            self.color = self.returnColor

        if self.mode == 1:
            if self.vel > 0:
                if self.rect.right < self.path[1]:
                    self.rect.x += self.vel
                else:
                    self.vel = self.vel*-1
            else:
                if self.path[0] < self.rect.x - self.vel:
                    self.rect.x += self.vel
                else:
                    self.vel = self.vel* -1
        if self.mode == 2:
            if self.vel > 0:
                if self.rect.bottom < self.path[1]:
                    self.rect.y += self.vel
                else:
                    self.vel = self.vel*-1
            else:
                if self.path[0] < self.rect.y - self.vel:
                    self.rect.y += self.vel
                else:
                    self.vel = self.vel* -1
        if self.mode == 3:
            if self.vel > 0:
                if self.rect.x < self.path[2]:
                    self.rect.x += self.vel
                elif self.rect.y < self.path[3]:
                    self.rect.y += self.vel
                else:
                    self.vel *= -1
            else:
                if self.rect.x - self.vel > self.path[0]:
                    self.rect.x += self.vel
                elif self.rect.y > self.path[1]:
                    self.rect.y += self.vel
                else:self.vel *= -1
        self.action()
        
    def action(self):
        if bot.rect.x + bot.width >= self.rect.x +self.acc and bot.rect.x <= self.rect.x + self.width -self.acc:
            if self.rect.y > bot.rect.y:
                aiming = (0, -1)
            else:
                aiming = (0, 1)
            self.attack(aiming)
        if bot.rect.y + bot.height >= self.rect.y +self.acc and bot.rect.y <= self.rect.y + self.height -self.acc:
            if self.rect.x > bot.rect.x:
                aiming = (-1, 0)
            else:
                aiming = (1, 0)
            self.attack(aiming)

    def attack(self, face):            
        if self.shootLoop == 0:
            self.shootLoop = 1
            self.ammo.append(projectile(self, 5, face))   
            
class Red(Virus):
    def __init__(self, x, y, end, mode, ext):
        super().__init__(x, y, end, mode, ext)
        self.color = red
        self.returnColor = red
        self.stunColor = (250, 0, 0)
        self.vel = 3
        self.firerate = 40
        self.scoreCount = 50
        self.exp = 10


class Blue(Virus):
    def __init__(self, x, y, end, mode, ext):
        super().__init__(x, y, end, mode, ext)
        self.color = blue
        self.returnColor = blue
        self.stunColor = (0, 0, 255)
        self.life = 5
        self.vel = 5
        self.firerate = 7
        self.scoreCount = 100
        self.exp = 20
        # self.rangeBox = (self.rect.x - 17, self.rect.y - 11, 50, 52)

class Green(Virus):
    def __init__(self, x, y, end, mode, ext):
        super().__init__(x,y,end,mode,ext)
        self.color = green
        self.returnColor = green
        self.stunColor = (0, 255, 0)
        self.life = 3
        self.vel = 3
        self.firerate = 5
        self.scoreCount = 150
        self.exp = 15     
        self.acc = -150   

    def action(self):
        if self.mode ==1:
            if bot.rect.x + bot.width >= self.rect.x +self.acc and bot.rect.x <= self.rect.x + self.width -self.acc:
                if self.rect.y > bot.rect.y:
                    aiming = (0, -1)
                else:
                    aiming = (0, 1)
                self.attack(aiming)
        if self.mode ==2:
            if bot.rect.y + bot.height >= self.rect.y + self.acc and bot.rect.y <= self.rect.y + self.height - self.acc:

                if self.rect.x > bot.rect.x:
                    aiming = (-1, 0)
                else:
                    aiming = (1, 0)
                self.attack(aiming)        

class Room(object):
    wallList = None
    virusList = None
    allList = None
    bossList = None
    
    def __init__(self):
        self.wallList = pygame.sprite.Group()
        self.virusList = pygame.sprite.Group()
        self.allList = pygame.sprite.Group()
        self.bossList = pygame.sprite.Group()

class Room1(Room):
    def __init__(self):
        super().__init__()
        walls = [[0, 0, 20, 600],[780, 20, 20, 580], [0,100,300,20],[500,100,300,20],#[0,100,300,20],
                 [20, 0, 500, 20], [650, 0, 150, 20], [100,200, 150,100], [550,200,150,100],
                 [20, 580, 780, 20],[390, 20, 20, 400], [100, 420, 600, 20]]         
            
        self.enemies = [[100, 360, 385,1, 0], #[30, 150, 400,2, 0],
                        [440, 150, 750, 1, 0], [440, 150, 400, 2, 0], [600, 440, 570,2, 0]]
##        self.blueenemies = [[30, 150, 400,2, 0],[100, 360, 385,1, 0],
##                    [440, 150, 750, 1, 0], [440, 150, 400, 2, 0], [600, 440, 570,2, 0]]
        for w in walls:
            wall = Wall(w[0],w[1],w[2],w[3])
            self.wallList.add(wall)
            self.allList.add(wall)

        for v in self.enemies:
            virus = Red(v[0],v[1],v[2], v[3], v[4])
            self.virusList.add(virus)
            self.allList.add(virus)
##        for v in self.blueenemies:
##            virus = Blue(v[0],v[1],v[2], v[3], v[4])
##            self.virusList.add(virus)   
            
class Room2(Room):
    def __init__(self):
        super().__init__()
        walls = [[0, 0, 20, 600],[780, 0, 20, 100], [300,80, 20, 220], [500, 480, 20, 150],
                 [20, 0, 780, 20], [650, 580, 150, 20], [0,300,100,20], [200, 300, 600, 100],
                 [20, 580, 500, 20], [780, 200, 20,400], [90, 90, 140, 140], [100, 380, 100,20], 
                 [300, 450, 20, 80], [100, 450, 20, 80], [520, 480, 100,20], [600, 80, 20, 170]]
        for w in walls:
            wall = Wall(w[0],w[1],w[2],w[3])
            self.wallList.add(wall)

        self.blueenemies = [[40, 40, 250, 3, 200]]
        self.enemies = [[50, 400, 570, 2, 0], [200, 410, 400, 3, 130], [540, 40, 650, 3, 220]]
        for v in self.blueenemies:
            virus = Blue(v[0],v[1],v[2], v[3], v[4])
            self.virusList.add(virus)   
        for v in self.enemies:
            virus = Red(v[0],v[1],v[2], v[3], v[4])     
            self.virusList.add(virus)   
            
class Room3(Room):
    def __init__(self):
        super().__init__()
        walls = [[0, 0, 20, 100], [0,200,20,400], [780, 20, 20, 580], [300, 100, 50, 20],
                 [20, 0, 500, 20], [650, 0, 250, 20], [600, 80, 20, 170], [300, 520, 50, 20],
                 [20, 580, 780, 20], [150, 80, 20, 170],[300, 200, 20, 170], [100, 520, 50, 20],
                  [450, 0, 20, 470], [450,370, 170, 20], [0, 370, 320, 20], [550, 450, 250,20],
                  [100, 450, 350, 20] ]
        for w in walls:
            wall = Wall(w[0],w[1],w[2],w[3])
            self.wallList.add(wall)

        self.blueenemies = [[230, 50, 360, 3, 100], [530, 40, 650, 3, 230]]
        self.enemies = [[50, 400, 570, 2, 0], [220, 480, 370, 3, 65]]

        for v in self.blueenemies:
            virus = Blue(v[0],v[1],v[2], v[3], v[4])
            self.virusList.add(virus)   
        for v in self.enemies:
            virus = Red(v[0],v[1],v[2], v[3], v[4])     
            self.virusList.add(virus)  

class Room4(Room):
    def __init__(self):
        super().__init__()
        walls = [[0, 0, 20, 200], [0, 300, 20, 300], [780, 20, 20, 580],
                 [20, 0, 780, 20], [100,100,100,100], [300,100,100,100],[500,100,100,100],
                 [20, 580, 500, 20], [650, 580, 150, 20], [100,400,100,100], [300,400,100,100],
                 [500,400,100,100], [0, 450, 100, 20], [150, 200, 20, 200]]
        for w in walls:
            wall = Wall(w[0], w[1], w[2], w[3])
            self.wallList.add(wall)
        self.blueenemies = [[250, 50, 650, 3, 160], [230, 300, 690,1,0],
                             [250, 50, 450, 3, 460]]
        self.greenenemies = [[740, 30, 570, 2, 0]]

        for v in self.blueenemies:
            virus = Blue(v[0],v[1],v[2], v[3], v[4])
            self.virusList.add(virus)
        for v in self.greenenemies:
            virus = Green(v[0],v[1],v[2], v[3], v[4])
            self.virusList.add(virus) 
##        for v in self.enemies:
##            virus = Red(v[0],v[1],v[2], v[3], v[4])     
##            self.virusList.add(virus)  
class Room5(Room): ###peace room
    def __init__(self):
        super().__init__()
        walls = [[0, 0, 20, 600], [460, 0, 340, 20], 
                 [780, 0, 20, 200], [780, 300, 20, 300],
                 [0, 0, 350, 20], [300, 0, 20, 200], [500, 0, 20, 200],
                 [20, 580, 780, 20]]
        for w in walls:
            wall = Wall(w[0], w[1], w[2], w[3])
            self.wallList.add(wall) 
class Room6(Room): ###relaced peace room
    def __init__(self):
        super().__init__()
        #self.acc = 0
        walls = [[0, 0, 20, 200], [0,300, 20, 300],##left
                 [0, 0, 800, 20], ##up
                 [780, 0, 20, 200], [780, 300, 20, 300], ##right
                 [20,70,50,40], [180,70,100,40], [400,70,180,40], [730,70,50,40],
                 [180,110,20,130], [640,110,20,470-110], [180,300,20,490-300],
                 [20,490,50,40], [180,490,100,40], [400,490,180,40], [730,490,50,40],##other
                 [20, 580, 780, 20]] ##bottom
        for w in walls:
            wall = Wall(w[0], w[1], w[2], w[3])
            self.wallList.add(wall) 
        self.greenenemies = [ [750,25,25,2,0], [750,535,535,2,0],
                        [350, 25, 745, 1, 0], [25,25,450,1,0],
                        [350, 535, 745, 1, 0], [25,535, 450,1,0]]
        self.enemies = [[205,115,550,3,455-115]]

        for v in self.greenenemies:
            virus = Green(v[0],v[1],v[2], v[3], v[4])
            #virus.acc = self.acc
            self.virusList.add(virus)   
            
        for v in self.enemies:
            virus = Red(v[0],v[1],v[2], v[3], v[4])     
            self.virusList.add(virus)  

class RoomB(Room):
    def __init__(self):
        super().__init__()
        self.bossBattle = True
        self.startBattle = False
        # self.boss = Boss1(250,30)   # virus = Virus(v[0],v[1],v[2], v[3])
        self.walls = [[0, 0, 20, 600], [780, 20, 20, 580],
                 [20, 0, 780, 20],
                 [0, 580, 350, 20], [460, 580, 340, 20]]
        for w in self.walls:
            wall = Wall(w[0],w[1],w[2],w[3])
            self.wallList.add(wall)

    # def update(self):
    #     if self.bossBattle:
    #         self.virusList.add(self.boss)

def findAngle(user):
    pos = [user.x, user.y]
    sX = bot.rect.centerx
    sY = bot.rect.centery
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle

def reset(map):
    map[0] = Room1()
    map[1] = Room2()
    map[2] = Room3()
    map[3] = Room4()
    map[4] = Room6()
    map[5] = Room5()
    map[6] = RoomB()

def main():
# game initialize
    pygame.init()
    global win
    offset = 20

    winH = 600
    winW = 800
    win = pygame.display.set_mode((winW, winH))

    pygame.display.set_caption("Computer Tower")
    clock = pygame.time.Clock()
    music = pygame.mixer.music.load('CT.mp3')
    pygame.mixer.music.play(-1)
    hitSound = pygame.mixer.Sound('hit.wav')

    # global stuff
    # color
    global black, white, yellow, red, green, blue
    black = (0, 0, 0)
    white = (255, 255, 255)
    yellow = (255, 255, 0)
    red = (200, 0, 0)
    green = (0, 200, 0)
    blue = (0, 0, 200)

    win.fill(white)
    
    #loops
    deathLoop = 0
    deathLoopB = 0
    shootLoop = 0

    # sprites
    global bot, wallList, score
    score = 0 #######
    checkpoint = [100, 50]
    roomCheck = 0
    hero = pygame.sprite.Group()
    wallList = pygame.sprite.Group()
    aiming = (1, 0)

    bot = player(100, 50)
    hero.add(bot)
    #dummy bullet
    dummy = projectile(bot, bot.power, (0,0))
    dummy.x = -offset +5
    dummy.y = -offset +5
    ammo = [dummy]

    #rooms
    global roomNow
    roomcheck = 0
    rooms = []
    room1 = Room1()
    rooms.append(room1)
    room2 = Room2()
    rooms.append(room2)
    room3 = Room3()
    rooms.append(room3)
    room4 = Room4()
    rooms.append(room4)
    ### new rooms
    room6 = Room6()
    rooms.append(room6) 
    room5 = Room5()
    rooms.append(room5)   
    ###
    roomB = RoomB()
    rooms.append(roomB)
    roomIndex = 0 ###### change to Test rooms
    roomNow = rooms[roomIndex]

    font = pygame.font.SysFont('coniscans', 30, True)    # (font,size,bold,italisized)
    font2 = pygame.font.SysFont('coniscans', 20) 

### Game ###    
    run = True
    while run:
            # controls

        keys = pygame.key.get_pressed()

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > bot.firerate:
            shootLoop = 0
            
        if keys[pygame.K_SPACE] and shootLoop == 0:
            shootLoop = 1
            if bot.changeX < 0:
                aiming = (-1, 0)
            if bot.changeX > 0:
                aiming = (1,0)
            if bot.changeY < 0:
                aiming = (0, -1)
            if bot.changeY > 0:
                aiming = (0, 1)
            gun = projectile(bot, bot.power, aiming)##debug
            gun.vel = 12 ##debug
            # if not bot.stun:
            ammo.append(gun)

        if keys[pygame.K_LEFT]:
            bot.changespeed(-1, 0)
        if keys[pygame.K_RIGHT]:
            bot.changespeed(1, 0)
        if keys[pygame.K_UP]:
            bot.changespeed(0,-1)
        if keys[pygame.K_DOWN]:
            bot.changespeed(0,1)
            
        # room change

        if roomIndex == 0:
            checkpoint = [100, 50]
            roomCheck = 0
            if bot.rect.y < -15:
                roomIndex = 1
                roomNow = rooms[roomIndex]
                bot.rect.y = 590

        if roomIndex == 1:
            checkpoint = [550 ,590]
            roomCheck = 1
            if bot.rect.x > 805:
                roomIndex = 2
                roomNow = rooms[roomIndex]
                bot.rect.x = -5
            if bot.rect.y > 605:
                roomIndex = 0
                roomNow = rooms[roomIndex]
                bot.rect.y = 0
        if roomIndex == 2:
            checkpoint = [50, 100]
            roomCheck = 2
            if bot.rect.x < -15:
                roomIndex = 1
                roomNow = rooms[roomIndex]
                bot.rect.x = 790
            if bot.rect.y < -15:
                roomIndex = 3
                roomNow = rooms[roomIndex]
                bot.rect.y = 590
        if roomIndex == 3:
            checkpoint = [550 ,590]
            roomCheck = 3
            if bot.rect.y > 605:
                roomIndex = 2
                roomNow = rooms[roomIndex]
                bot.rect.y = -5
            if bot.rect.x < -5:
                roomIndex = 4
                roomNow = rooms[roomIndex]
                bot.rect.x = 800     
                #music = pygame.mixer.music.load('CTPart2.mp3')
                #pygame.mixer.music.play(-1)
        if roomIndex == 4: ###replaced peace room

            checkpoint = [780, 250]
            roomCheck = 4
            if bot.rect.x > 805:
                roomIndex = 3      
                roomNow = rooms[roomIndex]  
                bot.rect.x = -4
                #pygame.mixer.music.play(-1)
            if bot.rect.x < -5:
                roomIndex = 5
                roomNow = rooms[roomIndex] 
                bot.rect.x = 800
        if roomIndex == 5: ### peace room
            pygame.mixer.music.pause()
            checkpoint = [400, 300]
            roomCheck = 5
            if bot.rect.x > 805:
                roomIndex = 4      
                roomNow = rooms[roomIndex] 
                bot.rect.x = -4   
                music = pygame.mixer.music.load('CT.mp3')
                pygame.mixer.music.play(-1)
            if bot.rect.y < -5:
                roomIndex = 6
                roomNow = rooms[roomIndex] 
                bot.rect.y = 605
        if roomIndex == 6:

            if bot.rect.bottom < 580:
                if roomNow.bossBattle:
                    music = pygame.mixer.music.load('CTboss.mp3')
                    pygame.mixer.music.play(-1)
                    win.fill(black)
                    font1 = pygame.font.SysFont('conicsans', 100)
                    text = font1.render('Boss Battle', 1, (250, 0, 0))
                    win.blit(text, (400 - (text.get_width() / 2), 200))
                    pygame.display.update()
                    i = 0
                    while i < 300:
                        pygame.time.delay(10)  # 10/1000Seconds
                        i += 1
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                i = 300 + 2
                                pygame.quit()
                                break
                    boss1 = Boss1(250,30) 
                    boss1.life = boss1.maxLife
                    for wall in roomNow.wallList:
                        roomNow.wallList.remove(wall)
                    walls = [[0, 0, 20, 600], [780, 20, 20, 580],
                            [20, 0, 780, 20], [0,580, 800, 20]]
                    roomNow.virusList.add(boss1)
                    for w in walls:
                        wall = Wall(w[0],w[1],w[2],w[3])
                        roomNow.wallList.add(wall)
                    roomNow.bossBattle = False
                    roomNow.startBattle = True

        #collision
        
        for bullets in ammo:
            if bullets.x > winW + offset or bullets.x < 0 -offset :
                ammo.pop(ammo.index(bullets)) 
            if bullets.y > winH + offset or bullets.y < 0 - offset :
                ammo.pop(ammo.index(bullets))
            for wall in roomNow.wallList:
                if bullets.x + bullets.radius >= wall.rect.x and bullets.x - bullets.radius <= wall.rect.x + wall.width:
                    if bullets.y + bullets.radius >= wall.rect.y and bullets.y - bullets.radius <= wall.rect.y + wall.height:
                        ammo.pop(ammo.index(bullets)) 
                        
            for enemy in roomNow.virusList:
                if bullets.x + bullets.radius >= enemy.rect.x and bullets.x - bullets.radius <= enemy.rect.x + enemy.width:
                    if bullets.y + bullets.radius >= enemy.rect.y and bullets.y - bullets.radius <= enemy.rect.y + enemy.height:
                        ammo.pop(ammo.index(bullets)) 
                        enemy.hit()
                        hitSound.play()

        
        enemyHit = pygame.sprite.spritecollide(bot, roomNow.virusList, False)
        for enemy in enemyHit:
            bot.hit()


        #player health
        if bot.isAlive:

            hero.update()

        #if you die
        if deathLoop > 0:
            deathLoop += 1
        if bot.isAlive:
            if bot.life <= 0:
                bot.visible = False
                bot.isAlive = False
                deathLoop = 1
        if deathLoop > 10:
            ammo = []
            score -= 150
            bot.exp -= 5
            i = 0
            while i < 50:
                pygame.time.delay(10)  # 10/1000Seconds
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 50 + 2
                        pygame.quit()
                        break
            win.fill(black)
            font1 = pygame.font.SysFont('conicsans', 100)
            text = font1.render('DEAD', 1, (250, 0, 0))
            win.blit(text, (400 - (text.get_width() / 2), 200))
            pygame.display.update()
            i = 0
            while i < 300:
                pygame.time.delay(10)  # 10/1000Seconds
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 300 + 2
                        pygame.quit()
                        break
            bot.rect.x = checkpoint[0]
            bot.rect.y = checkpoint[1]
            bot.visible = True
            bot.isAlive = True
            bot.life = bot.maxLife
            deathLoop = 0
            reset(rooms)
            roomIndex = roomCheck
            roomNow = rooms[roomIndex]
            # roomB.bossBattle = True

####display 
        win.fill(white)
        roomNow.wallList.draw(win)
        roomNow.virusList.update()
        roomNow.virusList.draw(win)
        pygame.draw.rect(win, (50,50,50), (5, 5, 100, 10))

        ##health bar
        if bot.isAlive:
            pygame.draw.rect(win, yellow, (5, 5, 100 - ((100/bot.maxLife)*(bot.maxLife-bot.life)), 10))

        ##attack conditions 
        for enemy in roomNow.virusList:
            if not enemy.isAlive:
                score += enemy.scoreCount
                bot.exp += enemy.exp
                roomNow.virusList.remove(enemy)
            for bullets in enemy.ammo:
                if bullets.x > winW or bullets.x < 0  :
                    enemy.ammo.pop(enemy.ammo.index(bullets))
                if bullets.y > winH or bullets.y < 0  :
                    enemy.ammo.pop(enemy.ammo.index(bullets))
                for wall in roomNow.wallList:
                    if bullets.x + bullets.radius >= wall.rect.x and bullets.x - bullets.radius <= wall.rect.x + wall.width:
                        if bullets.y + bullets.radius >= wall.rect.y and bullets.y - bullets.radius <= wall.rect.y + wall.height:   
                            enemy.ammo.pop(enemy.ammo.index(bullets))
                    
                if bullets.x + bullets.radius >= bot.rect.x and bullets.x - bullets.radius <= bot.rect.x + bot.width:
                    if bullets.y + bullets.radius >= bot.rect.y and bullets.y - bullets.radius <= bot.rect.y + bot.height:
                        # enemy.ammo.pop(enemy.ammo.index(bullets))
                        bot.hit()

            for bullets in enemy.ammo:
                bullets.update()
                bullets.draw(win)
                
        for bullet in ammo:
            bullet.update()
            bullet.draw(win)

        ##boss conditions    
        if roomIndex == 6 and roomNow.startBattle:
            for bullets in boss1.ammoS:
                if bullets.x + bullets.radius >= bot.rect.x and bullets.x - bullets.radius <= bot.rect.x + bot.width:
                    if bullets.y + bullets.radius >= bot.rect.y and bullets.y - bullets.radius <= bot.rect.y + bot.height:
                        boss1.ammoS.pop(boss1.ammoS.index(bullets))
                        bot.hit()
                bullets.update()
                bullets.draw(win)
            if boss1.visible:
                boss1.core = (boss1.rect.x + 2, boss1.rect.y + 2, boss1.width - 4, boss1.height - 4)
                pygame.draw.rect(win, boss1.color, boss1.core)
            if not boss1.isAlive: 
                deathLoopB += 1
                if deathLoopB >10:
                    i = 0
                    while i < 300:
                        pygame.time.delay(10)  # 10/1000Seconds
                        i += 1
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                i = 300 + 2
                                pygame.quit()
                                break 
                    win.fill(black)
                    font3 =  pygame.font.SysFont('conicsans', 100)
                    text2 = font3.render('Congrats!', 1, blue)
                    text3 = font3.render('Try again?', 1, blue)
                    win.blit(text2, (400 - (text2.get_width()/2), 200))
                    win.blit(text3, (400 - (text3.get_width()/2), 400))    
                    pygame.display.update() 
                    i = 0
                    while i < 400:
                        pygame.time.delay(10)  # 10/1000Seconds
                        i += 1
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                i = 400 + 2
                                pygame.quit()
                                break
                    deathLoopB = 0
                    hero.remove(bot)
                    bot = player(100, 50)
                    checkpoint = [100, 50]
                    hero.add(bot)
                    reset(rooms)
                    roomIndex = 0
                    roomNow = rooms[roomIndex]
                    music = pygame.mixer.music.load('CT.mp3')
                    pygame.mixer.music.play(-1)


        # player status display
        if bot.visible:
            hero.draw(win)
            bot.core = (bot.rect.x + 2, bot.rect.y + 2, bot.width - 4, bot.height - 4)
            pygame.draw.rect(win, bot.color, bot.core)
        # enemy status display
        if not roomIndex == 6:
            for enemy in roomNow.virusList:
                enemy.core = (enemy.rect.x + 2, enemy.rect.y + 2, enemy.width - 4, enemy.height - 4)
                pygame.draw.rect(win, enemy.color, enemy.core)
        #### HUD     
        text = font.render('Score: ' + str(score), 1, (0,250,0)) #########
        win.blit(text, (0, 580)) #################
        exp = font.render('Exp: ' + str(bot.exp), 1, (0,250,0))
        win.blit(exp, (700, 580))
        Lvl = font.render('LvL:' + str(bot.level), 1, (0,0,250))
        win.blit(Lvl, (700, 0))
        health = font2.render('Life: ' + str(bot.life), 1, (0,0,250))
        win.blit(health, (5, 4))

###run
        pygame.display.flip()
        clock.tick(60)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            break
    pygame.quit()

if __name__ == "__main__":
   main()

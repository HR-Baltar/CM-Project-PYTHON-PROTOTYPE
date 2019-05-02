import pygame, sys

    
class projectile(object):
    def __init__ (self, user, radius):
        self.x = user.rect.x + user.w//2
        self.y = user.rect.y + user.h//2
        self.radius = radius
        self.changeX = 0
        self.changeY = 0
##        self.color = color
##        self.directx = directx
##        self.directy = directy
        self.vel = 15
##        self.velx = self.vel * directx
##        self.vely = self.vel * directy
##
    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius +1)
        pygame.draw.circle(win, green, (self.x,self.y), self.radius)
    def update(self):
        self.x += self.vel * self.changeX
        self.y += self.vel * self.changeY
    def direction(self, x, y):
        self.changeX = x
        self.changeY = y

# class sprites
class player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.w = 30
        self.h = 30
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = yellow
        self.core = (self.rect.x + 2, self.rect.y + 2, self.w - 4, self.h - 4)
        self.changeX = 0
        self.changeY = 0
        self.vel = 5
        self.maxLife = 2
        self.life = 2
        self.isAlive = True
        self.hurt = False
        self.stun = False
        self.visible = True
        self.stunLoop = 0

    def changespeed(self, x, y):
        self.changeX +=  x*self.vel
        self.changeY +=  y*self.vel


    def update(self, walls):
        self.rect.x += self.changeX

        wallHit = pygame.sprite.spritecollide(self, walls, False)
        for wall in wallHit:
            if self.changeX > 0:
                self.rect.right = wall.rect.left
            elif self.changeX < 0:
                self.rect.left = wall.rect.right

        self.rect.y += self.changeY 
        wallHit = pygame.sprite.spritecollide(self, walls, False)
        for wall in wallHit:
            if self.changeY > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

        self.changeX = 0
        self.changeY = 0

        #damaged
        if self.hurt:
            self.stun = True
            if self.stunLoop > 0:
                self.stunLoop += 1
            if self.stunLoop % 10 == 0:
                self.visible = True
            if self.stunLoop % 6 == 0:
                self.visible = False
            if self.stunLoop > 50:
                self.stunLoop = 0
                self.hurt = False
                self.visible = True
                self.stun = False

    def hit(self):
        if not self.stun:
            self.life -= 1
            self.visible = False
            if self.life >= 1:
                self.hurt = True
                self.stunLoop = 1
            else:

                self.visible = False
                self.isAlive = False
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
                win.blit(text, (250 - (text.get_width() / 2), 200))
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
                self.rect.x = 50
                self.rect.y = 50
                self.visible = True
                self.isAlive = True
                self.life = self.maxLife


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, width, y, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Virus(pygame.sprite.Sprite):
    def __init__(self, x, y, end, mode):
        super().__init__()
        self.w = 30
        self.h = 30
        self.x = x
        self.y = y
        self.end = end
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = red
        self.core = (self.rect.x + 2, self.rect.y + 2, self.w - 4, self.h - 4)
        self.vel = 5
        self.mode = mode
        if self.mode == 1:
            self.path = [x, self.end]
        if self.mode == 2:
            self.path = [y, self.end]

    def update(self):
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
            

def delay(time):
    i = 0
    while i < time:
        pygame.time.delay(10)  # 10/1000Seconds
        i += 1

              
class Room(object):
    wallList = None
    virusList = None
    
    def __init__(self):
        self.wallList = pygame.sprite.Group()
        self.virusList = pygame.sprite.Group()
class Room1(Room):
    def __init__(self):
        super().__init__()
        walls = [[0, 20, 0, 600],[780, 20, 20, 580],
                 [20, 500, 0, 20], [650, 250, 0, 20],
                 [20, 780, 580, 20],[400,20, 20, 400]]        
        for w in walls:
            wall = Wall(w[0],w[1],w[2],w[3])
            self.wallList.add(wall)
            
        enemies = [[100, 100, 300,1],[250, 200, 345,1],
                   [400, 450, 560,2]]
        for v in enemies:
            virus = Virus(v[0],v[1],v[2], v[3])
            self.virusList.add(virus)
            
class Room2(Room):
    def __init__(self):
        super().__init__()
        walls = [[0, 20, 0, 600],[780, 20, 0, 100],
                 [20, 780, 0, 20], [650, 250, 580, 20],
                 [20, 500, 580, 20], [780, 20, 200,400] ]
        for w in walls:
            wall = Wall(w[0],w[1],w[2],w[3])
            self.wallList.add(wall)

        enemies = []
        for v in enemies:
            virus = Virus(v[0],v[1],v[2], v[3])
            self.virusList.add(virus)        
            
class Room3(Room):
    def __init__(self):
        super().__init__()
        walls = [[0, 20, 0, 100], [0,20,200,400],[780, 20, 20, 580],
                 [20, 500, 0, 20], [650, 250, 0, 20],
                 [20, 780, 580, 20] ]
        for w in walls:
            wall = Wall(w[0],w[1],w[2],w[3])
            self.wallList.add(wall)

##def main():
# game initialize
pygame.init()
global win
winH = 600
winW = 800
win = pygame.display.set_mode((winW, winH))
pygame.display.set_caption("Computer Tower")
clock = pygame.time.Clock()

# global stuff
# color
global black, white, yellow, red, green
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)

#loops
deathLoop = 0

# sprites
global bot, wallList
allSpr = pygame.sprite.Group()
hero = pygame.sprite.Group()
virusList = pygame.sprite.Group()
wallList = pygame.sprite.Group()
ammo = []

bot = player(50, 50)
hero.add(bot)
bullet = projectile(bot, 5)
ammo.append(bullet)

#rooms
rooms = []
room1 = Room1()
rooms.append(room1)
room2 = Room2()
rooms.append(room2)
room3 = Room3()
rooms.append(room3)
roomIndex = 0 ###### change to Test rooms
roomNow = rooms[roomIndex]

# game run
run = True
while run:
    # controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
            sys.exit()

        # controls

    keys = pygame.key.get_pressed()

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
        if bot.rect.y < -15:
            roomIndex = 1
            roomNow = rooms[roomIndex]
            bot.rect.y = 590

    if roomIndex == 1:
        if bot.rect.x > 800:
            roomIndex = 2
            roomNow = rooms[roomIndex]
            bot.rect.x = -5
        if bot.rect.y > 600:
            roomIndex = 0
            roomNow = rooms[roomIndex]
            bot.rect.y = 0
    if roomIndex == 2:
        if bot.rect.x < -15:
            roomIndex = 1
            roomNow = rooms[roomIndex]
            bot.rect.x = 790

    enemyHit = pygame.sprite.spritecollide(bot, roomNow.virusList, False)
    for enemy in enemyHit:
        bot.hit()

    # display
    if bot.isAlive:
        hero.update(roomNow.wallList)
    
    roomNow.virusList.update()
    win.fill(white)
    allSpr.draw(win)
    roomNow.wallList.draw(win)
    roomNow.virusList.draw(win)
    bullet.update()
    bullet.draw(win)

    # player status display
    if bot.visible:
        hero.draw(win)
        bot.core = (bot.rect.x + 2, bot.rect.y + 2, bot.w - 4, bot.h - 4)
        pygame.draw.rect(win, bot.color, bot.core)
    # enemy status display
    for enemy in roomNow.virusList:
        enemy.core = (enemy.rect.x + 2, enemy.rect.y + 2, enemy.w - 4, enemy.h - 4)
        pygame.draw.rect(win, enemy.color, enemy.core)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

##if __name__ == "__main__":
##    main()

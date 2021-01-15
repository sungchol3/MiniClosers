"I Love CLOSERS"
__author__="sungchol3@daum.net"

import pygame, random, time
import numpy as np

FPS=60
WHITE=(255,255,255)
RED=(255,0,0)
pad_width=1024
pad_height=512
background_width=1024
aircraft_width=90
aircraft_height=55
bat_width=110
bat_height=67
fireball1_width=140
fireball1_height=60
fireball2_width=86
fireball2_height=60

'''
class Magic():

    width = 1024
    height = 512
    t = 0

    def F(self):
        global bus
        explane="bus shoot"
        drawObject(bus,aircraft_width+200,aircraft_height)
'''
def drawScore(count,masg="Monster Passed: ",point=(0,0)):
    global gamepad

    font=pygame.font.SysFont(None,25)
    text=font.render(masg+str(count),True,WHITE)
    gamepad.blit(text,point)

def gameOver():
    global gamepad
    disMessage("GAME OVER")

def textObj(text,font):
    textSurface=font.render(text,True,RED)
    return textSurface,textSurface.get_rect()

def disMessage(text):
    global gamepad

    largeText=pygame.font.Font("freesansbold.ttf",155)
    TextSurf,TextRect=textObj(text,largeText)
    TextRect.center=((pad_width/2),(pad_height/2))
    gamepad.blit(TextSurf,TextRect)
    pygame.display.update()
    time.sleep(2)
    runGame()

def crash():
    global gamepad
    disMessage("Crashed!")

def drawObject(obj,x,y=0):
    global gamepad
    if isinstance(x,pygame.Rect):
        gamepad.blit(obj,x)
    else: gamepad.blit(obj,(x,y))


def runGame():
    global gamepad, aircraft,clock, background1,background2
    global bat,fires,bullet,boom,bus,bus_sound1,bus_sound2, ultimate_skill_effect

    bus_sound_list=[bus_sound1,bus_sound2]
    bus_show=False
    
    isShotBat=False
    boom_count=0
    hit_count=0
    bat_passed=0
    time_count=0

    bullet_xy=[]

    x=pad_width*0.05
    y=pad_height*0.8
    y_change=0

    background1_x=0
    background2_x=background_width
    
    bat_x=pad_width
    bat_y=random.randrange(0,pad_height)

    fire_x=pad_width
    fire_y=random.randrange(0,pad_height)
    random.shuffle(fires)
    fire=fires[0]

    t = 0
    ultimate_skill_do = False
    unshown_width = 640
    length_time = 7
    pos = pygame.Rect(0, 0, 1024, 512)
    pos.centery = pad_height/2
    pos0x = pad_width/2 - unshown_width 
    step = 0.1
    
    crashed=False
    while not crashed:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                crashed=True

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    y_change=-5
                elif event.key==pygame.K_DOWN:
                    y_change=5

                elif event.key==pygame.K_x:
                    bullet_x=x+aircraft_width
                    bullet_y=y+aircraft_height/2
                    bullet_xy.append([bullet_x,bullet_y])

                elif event.key==pygame.K_f and hit_count>=10:
                    # magic=Magic()
                    # magic.F()
                    ultimate_skill_do = True
                    bus_show=False
                    hit_count-=10
                    bus_x,bus_y=x+200,y-pad_height/3*2
                    random.shuffle(bus_sound_list)
                    bus_sound_list[0].play()
                    
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    y_change=0
        
        gamepad.fill(WHITE)

        background1_x-=2
        background2_x-=2

        if background1_x==-background_width:
            background1_x=background_width

        if background2_x==-background_width:
            background2_x=background_width

        drawObject(background1,background1_x,0)
        drawObject(background2,background2_x,0)

        drawScore(bat_passed)
        drawScore(hit_count,"Hit point: ",(170,0))

        if bus_show:
            (bus_x,bus_y)=(bus_x+5,bus_y)
            drawObject(bus,bus_x,bus_y)
            time_count+=1
            if time_count>99:
                time_count=0
                bus_show=False
        
        if bat_passed>2:
            gameOver()

        y += y_change
        if y<0: y=0
        elif y>pad_height-aircraft_height: y=pad_height-aircraft_height
        
        bat_x-=7
        if bat_x<=0:
            bat_passed+=1
            bat_x=pad_width
            bat_y=random.randrange(0,pad_height)

        if fire[1]==None:
            fire_x-=30
        else:
            fire_x-=15

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0,pad_height)
            random.shuffle(fires)
            fire = fires[0]
        
        #Bullets Position
        if len(bullet_xy)!=0:
            for i,bxy in enumerate(bullet_xy):
                bxy[0]+=15
                bullet_xy[i][0]=bxy[0]

                if bxy[0]>bat_x:
                    if bxy[1]>bat_y and bxy[1]<bat_y+bat_height:
                        bullet_xy.remove(bxy)
                        isShotBat=True
                        hit_count+=1

                if bxy[0]>=pad_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        if x+aircraft_width>bat_x:
            if(y>bat_y and y<bat_y+bat_height) or\
            (y+aircraft_height>bat_y and y+aircraft_height<bat_y+bat_height):
                crash()

        if fire[1]!=None:
            if fire[0]==0:
                fireball_width = fireball1_width
                fireball_height = fireball1_height
            elif fire[0]==1:
                fireball_width = fireball2_width
                fireball_height = fireball2_height

            if x+aircraft_width>fire_x:
                if(y>fire_y and y<fire_y+fireball_height)or\
                (y+aircraft_height>fire_y and y+aircraft_height<fire_y+fireball_height):
                    crash()
        
        drawObject(aircraft,x,y)

        if len(bullet_xy)!=0:
            for bx,by in bullet_xy:
                drawObject(bullet,bx,by)

        if not isShotBat:
            drawObject(bat,bat_x,bat_y)
        else:
            drawObject(boom,bat_x,bat_y)
            boom_count+=1
            if boom_count>5:
                boom_count=0
                bat_x=pad_width
                bat_y=random.randrange(0,pad_height-bat_height)
                isShotBat=False
                
        if fire[1]!=None:
            drawObject(fire[1],fire_x,fire_y)
        
        #Ultimate Skill

        if ultimate_skill_do:
            if t <= length_time + step:
                t += step
                pos.centerx = pos0x + 4/(length_time**2)*unshown_width*t*(length_time-t)
                drawObject(ultimate_skill_effect,pos)
            else:
                t = 0
                ultimate_skill_do = False
                bus_show = True
        
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def initGame():
    global gamepad, aircraft, clock,background1,background2
    global bat,fires,bullet,boom, bus, bus_sound1,bus_sound2, ultimate_skill_effect

    fires=[]
    
    pygame.init()

    #Music
    Volume = 1000
    pygame.mixer.music.load("music/ClosersBGM.mp3")
    pygame.mixer.music.play(-1)
    bus_sound1=pygame.mixer.Sound("music/시내버스다.wav")
    bus_sound1.set_volume(Volume)
    bus_sound2=pygame.mixer.Sound("music/버스폭격이다.wav")
    bus_sound2.set_volume(Volume)
    
    #MainBoard
    gamepad=pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('MiniCLOSERS')

    #Image
    aircraft=pygame.image.load('images/gameleesulbe.png')
    background1=pygame.image.load('images/background_closers.png')
    background2=background1.copy()
    bat=pygame.image.load('images/bat2.png')
    ultimate_skill_effect = pygame.transform.scale(pygame.image.load('images/townbus.png'),(pad_width,pad_height))
    
    wind_knife = pygame.transform.scale(pygame.image.load('images/windknife2.png'),(fireball1_width,fireball1_height))
    fire_ball = pygame.transform.scale(pygame.image.load('images/fireball.png'),(fireball2_width,fireball2_height))

    fires.append((0,wind_knife))
    fires.append((0,fire_ball))

    boom=pygame.image.load("images/boom.png")

    for i in range(3):
        fires.append((i+2,None))

    bullet=pygame.image.load("images/bullet.png")
    
    #결정기
    bus=pygame.image.load("images/BusShoot.png")
    
    #Start Game
    clock=pygame.time.Clock()
    runGame()

if __name__=='__main__':
    initGame()

#SNAKE GAME!

import pygame #graphics, sounds, event handling
import sys #system(for exiting purposes)
import random #for placing food at random position
import time #for delay

#check initializing errors
check_errors=pygame.init() #to initialize pygame #(6,0)=(no. of modules checked, errors)

if check_errors[1]>0:
    print("(!) Had {0} initialoizing errors, exiting...".format(check_errors[1])) #{0} is like %d of scanf followed by format
    sys.exit(-1) #to exit
else:
    print("(+) PyGame successfully initialized!")

#Play Surface
playSurface = pygame.display.set_mode((720,460)) #height,width in form of a tuple since the func accepts only one argument
pygame.display.set_caption('Snake Game!') #title of window

#Colors
red = pygame.Color(255,0,0) #r,g,b values #gameover
green = pygame.Color(0,255,0) #snake
black = pygame.Color(0,0,0) #background
white = pygame.Color(255,255,255) #score
brown = pygame.Color(165,42,42) #food

#FPS (Frame per second) Controller
fpsController=pygame.time.Clock()

#Important variables
snakePos = [100,50] #<size of window
snakeBody = [[100,50],[90,50],[80,50]] #list of lists
foodPos = [random.randrange(1,71)*10,random.randrange(1,45)*10] #x,y=multiples of 10 generated since snakeBody
foodSpawn = True
direction = 'RIGHT'
changeTo = direction
score=0

#Game Over Function
def gameOver():
    myFont = pygame.font.SysFont('monaco',72) #(name,size)
    #print can only be used to print text on the console
    GOsurf = myFont.render('* GAME OVER *', 1, red) #draw text on a new surface (text, anti-alias,color, background)
    
    #In computer graphics, antialiasing is a software technique for diminishing jaggies - stairstep-like lines that should be smooth.
    
    GOrect = GOsurf.get_rect() #get the rectangular component of the GO surface toposition where the text will be
    GOrect.midtop=(360,20)
    playSurface.blit(GOsurf,GOrect) #draw one image on another
    showScore(0)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit() #for pygame window exit
    sys.exit() #for console exit

def showScore(choice=1):
    sFont=pygame.font.SysFont('monaco',30) 
    sSurf = sFont.render('Score : {0}'.format(score), True, white)
    sRect = sSurf.get_rect()
    if choice == 1:
        sRect.midtop =(80,10)
    else:
        sRect.midtop =(360,120)
    playSurface.blit(sSurf,sRect)
    
#Main Logic of Game
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN: #key down event
            if event.key == pygame.K_RIGHT or event.key == ord('d'): #ord gives the ASCII values of characters
                changeTo = "RIGHT"
            if event.key == pygame.K_LEFT or event.key == ord('a'): 
                changeTo = "LEFT"
            if event.key == pygame.K_UP or event.key == ord('w'): 
                changeTo = "UP"
            if event.key == pygame.K_DOWN or event.key == ord('s'): 
                changeTo = "DOWN"
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT)) #create event
                
    #Validation of direction (snake cannot move left while moving towards right)
    if changeTo == 'RIGHT' and not direction == 'LEFT':
        direction='RIGHT'
    if changeTo == 'LEFT' and not direction == 'RIGHT':
        direction='LEFT'
    if changeTo == 'UP' and not direction == 'DOWN':
        direction='UP'
    if changeTo == 'DOWN' and not direction == 'UP':
        direction='DOWN'
    
    #Changing Position of Snake[x,y]
    if direction == 'RIGHT':
        snakePos[0] += 10 #x coordinate
    if direction == 'LEFT':
        snakePos[0] -= 10 
    if direction == 'UP':
        snakePos[1] -= 10 #y coordinate
    if direction == 'DOWN':
        snakePos[1] += 10
                
    #Snake Body Mechanism
    snakeBody.insert(0,list(snakePos)) #func to add to a list
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score+=10
        foodSpawn = False
    else:
        snakeBody.pop() #delete from list
    
    #Food Spawn      
    if foodSpawn == False:
        foodPos = [random.randrange(1,71)*10,random.randrange(1,45)*10]
    foodSpawn = True
    
    #Background
    playSurface.fill(black) #background of window
    
    #Draw Snake and Food
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0],pos[1],10,10)) #pygame.Rect(x coordinate,y, size_x,size_y)
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0],foodPos[1],10,10))  
    #Check Boundary
    if snakePos[0]>=720 or snakePos[0]<0:
        gameOver()
    if snakePos[1]>=460 or snakePos[1]<0:
        gameOver()
    
    #Self-Hit
    for block in snakeBody[1:]: #position 1 till the end
        if snakePos[0]== block[0] and snakePos[1] == block[1]:
            gameOver()
    
    #Common Stuff
    showScore()
    pygame.display.flip()
    fpsController.tick(20)
    
    #implement menus (settings), background music, images instead of block in snake, change the icon of game
    #pyinstaller - to make it an executable file
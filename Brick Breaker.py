import pygame
import math
import random
from pygame.locals import(
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT
)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
PAD_SPEED = 0.4

FPS = 30
fpsClock = pygame.time.Clock()

colour = {'black':(0,0,0),'white':(255,255,255),'yellow':(255,255,0),'orange':(255,165,0),'red':(255,0,0)}
health_col = {1:colour['red'],2:colour['orange'],3:colour['yellow']}
BRICK_HEIGHT = 40
BRICK_WIDTH = 90
class Ball:
    def __init__(self, x_pos,y_pos):
        self.x = x_pos
        self.y = y_pos
        self.radius = 5
        self.v_x = 0.3
        self.v_y = 0.15
        

class Pad:
    def __init__(self, x_pos = 0):
        self.x = x_pos
        self.width = 150
        self.height = 20
        self.y = SCREEN_HEIGHT - self.height
        
        self.rect = pygame.Rect(self.x,self.y, self.width,self.height)

    def rect_update(self):
        self.rect = pygame.Rect(self.x,self.y, self.width,self.height)

class Brick:
    def __init__(self, x_pos,y_pos,health):
        self.x = x_pos
        self.y = y_pos
        self.width = 40  
        self.height = 20    
        self.hp = health
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)


pad = Pad()
ball = Ball(pad.x + pad.width/2,pad.y-10)
pygame.init()


def display():
    screen.fill(colour['black'])
    
    pygame.draw.rect(screen,colour['white'], pad.rect)
    pygame.draw.circle(screen,colour['white'],(ball.x,ball.y),ball.radius)

    for brick in brick_Li:
        pygame.draw.rect(screen,health_col[brick.hp],brick.rect)

def update():
    pad.rect_update()
    ball.v_x = round(ball.v_x,2)
    ball.v_y = round(ball.v_y,2)
    brick_copy = brick_Li[:]
    brick_Li.clear()
    i = 0
    for brick in brick_copy:
        if brick.hp == 0:
            continue
        else:
            brick_Li.append(brick)
        

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pressed_key = dict.fromkeys(['left','right'],False)
brick_Li = []
x,y = 10,10

#generating bricks with random healths
for r in range(5):
    for c in range(5):
       brick_Li.append(Brick(x,y,random.randint(0,3)))
       x += 10 + BRICK_WIDTH
    x = 10
    y += 10 + BRICK_HEIGHT

running = True
while running:
    update()
    display()
    pad_move = 0
    fps = fpsClock.get_fps()
    
    #event handling
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_RIGHT:
                
                pressed_key['right'] = True   
            elif event.key == K_LEFT:
                
                pressed_key['left'] = True
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                pressed_key['right'] = False
            elif event.key == K_LEFT:
                pressed_key['left'] = False
        elif event.type == QUIT:
            running = False
    #motion of the pad
    if pressed_key['right'] == True:
        pad_move += PAD_SPEED*fps
    if pressed_key['left'] == True:
        pad_move -= PAD_SPEED*fps
    pad.x += pad_move
    if pad.x < 0:
        pad.x = 0
    elif pad.x > SCREEN_WIDTH-pad.width:
        pad.x = SCREEN_WIDTH-pad.width

    #motion of ball
    ball.x += ball.v_x * fps
    ball.y += ball.v_y * fps
    
    #checking for collisions with left top and right walls (bottom is not checked since that is losing condition)
    if ball.x >= SCREEN_WIDTH-ball.radius or ball.x <= ball.radius:
        ball.v_x *= -1
    if ball.y <= ball.radius:
        ball.v_y *= -1

    #checking for collision with the pad
    if ball.y >= pad.y - ball.radius:
        if pad.x <= ball.x <= pad.x + pad.width:
            ball.v_y *= -1
            ball.v_x += (ball.x - pad.x - (pad.width/2))/1000  #adding a little x speed depending on where the ball hits the pad
                        


    for brick in brick_Li:
        #find closest point to brick from ball
        if brick.x > ball.x:
            closestx = brick.x
        elif brick.x + BRICK_WIDTH < ball.x:
            closestx = brick.x + BRICK_WIDTH
        else:
            closestx = ball.x
        if brick.y > ball.y:
            closesty = brick.y
        elif brick.y + BRICK_HEIGHT < ball.y:
            closesty = brick.y + BRICK_HEIGHT
        else:
            closesty = ball.y
    
        distance = math.sqrt(math.pow(ball.x-closestx,2) + math.pow(ball.y-closesty,2))
        if distance <= ball.radius:
            brick.hp -= 1
            if brick.x <= ball.x <= brick.x + BRICK_WIDTH:
                ball.v_y *= -1
            if brick.y <= ball.y <= brick.y + BRICK_HEIGHT:
                ball.v_x *= -1  
            break

    if ball.y >= SCREEN_HEIGHT-ball.radius:
        running = False
        print("L Moment")                                                           
    
    if len(brick_Li)==0:
        running = False
        print("W Moment")


    pygame.display.flip()
    fpsClock.tick(FPS)
pygame.quit()



'''
    #checking for collision with the bricks
    for brick in brick_Li:
        if(brick.x <= ball.x <= brick.x + BRICK_WIDTH) and ((brick.y + ball.v_y > ball.y + ball.radius >= brick.y) or (brick.y + BRICK_HEIGHT - ball.v_y < ball.y - ball.radius <= brick.y + BRICK_HEIGHT)):
            ball.v_y *= -1
            brick.hp -= 1
            break
        elif(brick.y <= ball.y <= brick.y + BRICK_HEIGHT) and ((ball.x + ball.radius == brick.x) or (ball.x - ball.radius == brick.x + BRICK_WIDTH)):
            ball.v_x *= -1
            brick.hp -= 1
            break  
        '''
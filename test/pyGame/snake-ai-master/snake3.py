#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from ai_snake import AiSnake
import pygame, sys, random
from pygame.locals import*
import time

FPS = 90
WINDOWWIDTH =640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height muset be multiple of cell size"
CELLWIDTH = WINDOWWIDTH / CELLSIZE
CELLHEIGHT = WINDOWHEIGHT / CELLSIZE

CELL_NUMS = CELLWIDTH * CELLHEIGHT

#RGB
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 #很巧妙的运用


#main function
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    ai = AiSnake(CELLWIDTH, CELLHEIGHT)
##    with open('snake3_%s.log' % (os.getpid()), 'a') as wf:
##        ai.log_file = wf
##        runGame(ai, test=True)

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')


    showStartScreen()  #显示起始画面
    ret = True
    while ret:
##        with open('snake3_%s.log' % (os.getpid()), 'a') as wf:
##            #ai.log_file = wf
        ret = runGame(ai)    #运行游戏主体
        
    showGameOverScreen()    #显示游戏结束画面

def runGame(ai=None, test=False):
    #设置蛇身开始在随机位置
    startx = random.randint(5, CELLWIDTH-6)
    starty = random.randint(5, CELLHEIGHT-6)
    wormCoods = [(startx, starty),
                 (startx-1, starty),
                 (startx-2,  starty)]
    direction = RIGHT    #蛇初始方向向右

    #得到一个随机苹果的位置
    apple = getRandomLocation(wormCoods)


    while True:
        if len(wormCoods)>=CELL_NUMS-5:
            return True #game restart

        move = None
        if not test:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:        #处理蛇的移动方向
                    if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                        move = LEFT
                    elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                        move = RIGHT
                    elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                        move = UP
                    elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                        move = DOWN
                    elif event.key == K_ESCAPE:
                        terminate()

        if(ai and not move):
            move = ai.find_move(wormCoods, apple)

        direction = move if move else direction
        #看蛇身是否撞击到自己或四周墙壁
        if wormCoods[HEAD][0] == -1 or wormCoods[HEAD][0] == CELLWIDTH or \
            wormCoods[HEAD][1] == -1 or wormCoods[HEAD][1] == CELLHEIGHT:
            return False #game over
        for wormBody in wormCoods[1:]:
            if wormBody[0] == wormCoods[HEAD][0] and wormBody[1] == wormCoods[HEAD][1]:
                return False #game over
        #蛇是否迟到苹果
        if wormCoods[HEAD][0] == apple[0] and wormCoods[HEAD][1] == apple[1]:
            #不删除蛇身尾段
            apple = getRandomLocation(wormCoods) #设置一个新的苹果
        else:
            del wormCoods[-1] #删除蛇身尾段
        #添加蛇身头段
        if direction == UP:
            newHead = (wormCoods[HEAD][0], wormCoods[HEAD][1]-1)
        elif direction == DOWN:
            newHead = (wormCoods[HEAD][0], wormCoods[HEAD][1]+1)
        elif direction == LEFT:
            newHead = (wormCoods[HEAD][0]-1, wormCoods[HEAD][1])
        elif direction == RIGHT:
            newHead = (wormCoods[HEAD][0]+1, wormCoods[HEAD][1])
        wormCoods.insert(0,newHead)

        if not test:
            DISPLAYSURF.fill(BGCOLOR)
            drawGrid() #画格子
            drawWorm(wormCoods) #画蛇身
            drawApple(apple) #画苹果
            drawScore(len(wormCoods) - 3)#显示得到分数
            pygame.display.update()
            FPSCLOCK.tick(FPS)

#提示按键消息
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT-30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

#检测按键
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

#显示开始界面
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1,rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2,rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return None
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3
        degrees2 += 7

#游戏结束
def terminate():
    pygame.quit()
    sys.exit()

#得到随机苹果位置
def getRandomLocation(wormCoods):
    point = (random.randint(0, CELLWIDTH - 1), random.randint(0, CELLHEIGHT - 1))
    for item in wormCoods:
        if item[0]==point[0] and item[1]==point[1]:
            return getRandomLocation(wormCoods)
    return  point

#显示游戏结束画面
def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('GAME', True, WHITE)
    overSurf = gameOverFont.render('OVER', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' %(score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawWorm(wormCoods):
    rgb = lambda n: 0 if n<=0 else (255 if n>=255 else n)
    for idx, coord in enumerate(wormCoods):
        x = coord[0] * CELLSIZE
        y = coord[1] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE-8)
        if idx<=512:
            idx = 512 - idx - 1
            TMP = ( rgb(4*(idx/8)), 255, rgb(4*(idx/8)) )
            pygame.draw.rect(DISPLAYSURF, TMP, wormInnerSegmentRect)
        else:
            pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

def drawApple(coord):
    x = coord[0] * CELLSIZE
    y = coord[1] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

if __name__ == '__main__':
    main()




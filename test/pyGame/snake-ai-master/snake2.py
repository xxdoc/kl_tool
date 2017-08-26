#!/usr/bin/env python
# -*- coding:utf-8 -*-
# vim: ft=python
#    Filename:    snake.py
#    Author:        Chen Qinbo
#    Date:        02Apr2016
#    Description:
'''
module snake.py
'''
#import builtin/3rd party/other ourself
import curses
import datetime
import os
from time import sleep
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

# 蛇运动的场地长宽，不含边界
HEIGHT = 10
WIDTH = 20
FIELD_SIZE = HEIGHT * WIDTH
# food:食物位置(0~FIELD_SIZE-1),初始在(3, 3)
FOOD = 3 * WIDTH + 3
# 初始化蛇头在(0,0)的地方，以一维表示二维
SNAKE = [3,2,1,0]


# 由于snake是一维数组，所以对应元素直接加上以下值就表示向四个方向移动
LEFT = -1
RIGHT = 1
UP = -WIDTH
DOWN = WIDTH
# 运动方向数组
MOV = [LEFT, RIGHT, UP, DOWN]
KEY_TIMEOUT = 10  # ms

def SET_VAL(_WIDTH, _HEIGHT):
    global HEIGHT, WIDTH, FIELD_SIZE, LEFT, RIGHT, UP, DOWN, MOV
    HEIGHT = _HEIGHT
    WIDTH = _WIDTH
    FIELD_SIZE = HEIGHT * WIDTH

    LEFT = -1
    RIGHT = 1
    UP = -WIDTH
    DOWN = WIDTH
    MOV = [LEFT, RIGHT, UP, DOWN]

def point2food(i):
    x, y = i
    return (y) * WIDTH + (x)

def point2sanke(list_in):
    return [point2food(i) for i in list_in]

def find_move(wormCoods, apple):
    snake = point2sanke(wormCoods)
    food = point2food(apple)

    tmp = ai_move(snake, food)

    cmd = ('left', 'right', 'up', 'down')
    for i,t in enumerate(MOV):
        if tmp==t:
            return cmd[i]
    return None

def _LOG(msg_in, time_now=False, new_line=True):
    if time_now:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg_in = '%s => %s' % (time_str, msg_in)
    if getattr(_LOG, 'log_file', None):
        _LOG.log_file.write(msg_in)
        _LOG.log_file.flush()

    #if new_line:
    #    print msg_in
    #else:
    #    print msg_in,



def do_randint(_min, _max):
	return randint(_min, _max)


def log_dist(dist, snake, food):
    msg = dist2str(dist, snake, food)
    _LOG(msg)
    pass

def dist2str(dist, snake, food):
    s = ''
    s += "food " + str(food)+" x=  "+str(food%WIDTH) + "   y= "+str(food/WIDTH) +'\n'
    for i in xrange(HEIGHT):
        for j in xrange(WIDTH):
            if i*WIDTH+j == snake[0]:
                s += ("  A")
            elif len(snake) > 1 and i*WIDTH+j == snake[1]:
                s += ("  B")
            elif len(snake) > 2 and i*WIDTH+j == snake[2]:
                s += ("  C")
            elif i*WIDTH+j == snake[len(snake)-3]:
                s += ("  X")
            elif i*WIDTH+j == snake[len(snake)-2]:
                s += ("  Y")
            elif i*WIDTH+j == snake[len(snake)-1]:
                s += ("  Z")
            else:
                tmp = dist[i*WIDTH+j]
                tmp = 99 if tmp==999 else (98 if tmp==998 else tmp)
                s += ("%3d"%(tmp,))
        s += ('\n')
    s += ('\n')
    s += ('\n')
    s += ('\n')
    return s


# 计算出board中每个非SNAKE元素到达食物的路径长度

def cal_freecell_to_food_size(snake, food):
    queue = [food, ]
    dist = [998 for i in range(FIELD_SIZE)]
    for i in snake:
        dist[i] = 999
    dist[food] = 0
    ret = None
    while queue:
        idx = queue.pop(0)
        for i in MOV:
            if next_move_is_out_border(idx, i):
                continue
            idxx = idx + i
            if idxx == snake[0]:
                ret = True
            if dist[idxx] == 998:
                dist[idxx] = dist[idx] + 1
                queue.append(idxx)
    log_dist(dist, snake, food)
    return dist, ret

def mov_for_tail(snake):
    #replace the tail for food
    dist, found = cal_freecell_to_food_size(snake[:-1], snake[-1])
    if found:
        ret = _find_ret_dist(snake, dist)
        return _find_max_move(ret, snake)

def _find_max_move(ret, snake):
    if not ret:
        return None

    max_val = max(ret.values())
    last = snake[0] - snake[1]
    if ret.get(last, -1)==max_val:
        return last
    else:
        for k, v in ret.items():
            if v==max_val:
                return k

def _find_ret_dist(snake, dist):
    ret = {}
    for item in MOV:
        if not next_move_is_invalid(snake, item):
            last = snake[0] + item
            if dist[last] < 998:
                ret[item] = dist[last]

    return ret

def _find_min_move(ret, snake):
    if not ret:
        return None

    min_val = min(ret.values())
    last = snake[0] - snake[1]
    if ret.get(last, -1)==min_val:
        return last
    else:
        for k, v in ret.items():
            if v==min_val:
                return k

def ai_move(_snake, _food):
    snake = _snake[:]
    food = _food
    dist, found = cal_freecell_to_food_size(snake, food)
    if found:
        tmp = _get_move(snake, food, dist)
        if tmp :
            return tmp

    move = mov_for_tail(snake)
    if move:
        _LOG("goto_tail\n")
        return move

    raise RuntimeError('Cannot find best move!')

def _get_move(snake, food, dist):
    ret = _find_ret_dist(snake, dist)
    while ret:
        tmp = _find_min_move(ret, snake)
        if not tmp:
            break

        ret.pop(tmp)
        snake_tmp, food_tmp =  snake_move(snake, food, tmp)
        move = mov_for_tail(snake_tmp)
        if move:
            _LOG("goto_food\n")
            return tmp


def event2key(move, event):
    if event == KEY_LEFT and move != RIGHT:
        move = LEFT
    elif event == KEY_RIGHT and move != LEFT:
        move = RIGHT
    elif event == KEY_UP and move != DOWN:
        move = UP
    elif event == KEY_DOWN and move != UP:
        move = DOWN
    return move

def next_move_is_out_border(pos, move):
    if move == RIGHT and pos % WIDTH == WIDTH - 1:
        return True
    elif move == LEFT and pos % WIDTH == 0:
        return True
    elif move == DOWN and pos / WIDTH == HEIGHT - 1:
        return True
    elif move == UP and pos / WIDTH == 0:
        return True
    return False

def next_move_is_invalid(snake, move):
    if next_move_is_out_border(snake[0], move):
        return True
    elif snake[0] + move != snake[len(snake)-1] and snake[0] + move in snake: # can move to the tail
        return True
    return False

def next_mov_is_food(snake, food, move):
    return snake[0] + move == food

def new_food(snake):
    food = do_randint(0, FIELD_SIZE - 1)
    while food in snake:
        food = do_randint(0, FIELD_SIZE - 1)
    return food

def snake_move(snake, food, move):
    if next_mov_is_food(snake, food, move):
        snake_tmp= snake[:]
        snake_tmp.insert(0, food)
        newfood = new_food(snake_tmp)
        return snake_tmp, newfood
    else:
        snake_tmp= snake[:]
        snake_tmp.insert(0, snake[0] + move)
        return snake_tmp[:-1], food

def update_win(win, snake, food):
    for i in xrange(FIELD_SIZE):
        win.addch(i/WIDTH + 1, i%WIDTH + 1, ' ')
    for i in xrange(len(snake)):
        if i == 0:
            win.addch(snake[i]/WIDTH +1,  snake[i]%WIDTH + 1, 'A')
        elif i == 1:
            win.addch(snake[i]/WIDTH +1,  snake[i]%WIDTH + 1, 'B')
        elif i == 2:
            win.addch(snake[i]/WIDTH +1,  snake[i]%WIDTH + 1, 'C')
        else:
            win.addch(snake[i]/WIDTH +1,  snake[i]%WIDTH + 1, '#')
    win.addch(food/WIDTH +1 , food%WIDTH + 1, '@')
    win.refresh()

def do_snake(win, snake, food):
    win.keypad(1)
    win.timeout(10)
    event = win.getch()
    # 第一次默认接收到的键
    move = RIGHT
    while event != 27:
        move = ai_move(snake, food)
        if not move:
            break
        snake, food = snake_move(snake, food, move)
        update_win(win, snake, food)
        win.timeout(KEY_TIMEOUT)
        event = win.getch()
        move = event2key(move, event)

    return snake


def main():

    # 初始化蛇头在(0,0)的地方，以一维表示二维
    snake= SNAKE[:]
    food = FOOD

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)

    win = curses.newwin(HEIGHT+2, WIDTH+2, 0, 1)
    win.border(0)
    win.nodelay(1)

    with open('snake_%s.log' % (os.getpid()), 'a') as wf:
        _LOG.log_file = wf
        snake = do_snake(win, snake, food)

    #sleep(2)
    curses.nocbreak();
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    print "Score: " , len(snake)

if __name__ == "__main__":
    main()

#!/usr/bin/python3
# coding=utf-8

'''
    desc    : iMotion firmware uploader with orangepi SBC
    date    : 2020/04/13
    version : 0.2
    author  : cosmas eric s (cosmas.eric.septian@polytron.co.id)

'''


from drawer import Frame
import sys, os
import pygame as pg
import constant as c
import logging

# adjust position 
if sys.platform == 'win32' :
    x = 0
    y = 0
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

elif sys.platform == 'linux':
    os.environ["SDL_MOUSEDEV"] = "/dev/input/event3"

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)
    return logger

log = setup_custom_logger("logger")

pg.init() 
if(c.OPS_FULLSCREEN == True) :
    screen = pg.display.set_mode(size=(0,0), flags= pg.NOFRAME)
else:
    screen = pg.display.set_mode(c.SCREEN_SIZE) 

pg.mouse.set_visible(False)
clock = pg.time.Clock()
SCREEN_W = screen.get_rect().width
SCREEN_H = screen.get_rect().height

log.info("Create frame")
log.info("Frame size : {} x {}".format(SCREEN_W, SCREEN_H))
frame = Frame(screen=screen, screen_w=SCREEN_W, screen_h=SCREEN_H)


def main():
    run = True

    while run:
        frame.run()
        clock.tick(60)

if __name__ == "__main__":
    main()
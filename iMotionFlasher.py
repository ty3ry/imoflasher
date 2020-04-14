#!/usr/bin/python3
# coding=utf-8

'''
    desc    : iMotion firmware uploader with orangepi SBC
    date    : 2020/04/13
    version : 0.2
    author  : cosmas eric s (cosmas.eric.septian@polytron.co.id)

'''


import serial
import pygame as pg
import logging
import sys, os

# adjust position 
if sys.platform == 'win32' :
    x = 0
    y = 0
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

elif sys.platform == 'linux':
    os.environ["SDL_MOUSEDEV"] = "/dev/input/event2"
    

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

log = setup_custom_logger("logger")

LOGIN_COLOR = (120, 104, 192)
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 20)
OPS_FULLSCREEN = True
SCREEN_SIZE = (960,540)


log.info("init pygame")
pg.init() 



log.info("Set display {}".format("Fullscreen" if (OPS_FULLSCREEN) else "Set to {}".format(SCREEN_SIZE)))
if(OPS_FULLSCREEN == True) :
    screen = pg.display.set_mode(size=(0,0), flags= pg.NOFRAME)
else:
    screen = pg.display.set_mode(SCREEN_SIZE) 

pg.mouse.set_visible(False)
clock = pg.time.Clock()

# load resource
img_fail = pg.image.load("resource/failed.png")
img_pass = pg.image.load("resource/pass.png")
#img_pass.convert()

# scale image
#pg.transform.scale(img_fail, (0,0))
# pg.transform.scale(img_pass, (80,20))


SCREEN_W = screen.get_rect().width
SCREEN_H = screen.get_rect().height

log.info("Screen size : {} x {} ".format(SCREEN_W, SCREEN_H))


def draw_frame_line():
    global img_fail, img_pass
    w , h = SCREEN_W, SCREEN_H  - 100
    text_frame_h = 280
    border_width = 3

    # progress value
    line1_progress = 0.2
    line2_progress = 0.5
    line3_progress = 0.7
    line4_progress = 1

    

    # text template
    # control text
    control_name = pg.font.SysFont('comicsansms', 30)
    control_name.set_bold(False)

    # progress text template
    label_progress_template = pg.font.SysFont('comicsansms', 25)
    label_progress_template.set_bold(False)

    # percentage label template
    label_percentage_template = pg.font.SysFont('comicsansms', 25)
    label_percentage_template.set_bold(False)

    label_status_template = pg.font.SysFont('comicsansms', 35)
    label_status_template.set_bold(False)

    # label status value
    label_status_value_template = pg.font.SysFont('comicsansms', 50)
    label_status_value_template.set_bold(False)

    # label filename
    label_filename_template = pg.font.SysFont('comicsansms', 25)
    label_filename_template.set_bold(False)

    # label filename value
    label_filename_value_template = pg.font.SysFont('comicsansms', 50)
    label_filename_value_template.set_bold(True)

    # label system state
    label_system_state_template = pg.font.SysFont('comicsansms', 25)
    label_system_state_template.set_bold(False)

    # label system state value
    label_system_state_value_template = pg.font.SysFont('comicsansms', 40)
    label_system_state_value_template.set_bold(False)

    # line 1 frame
    pg.draw.rect(screen, WHITE, (0,0, w/2, h/2), border_width)
    pg.draw.rect(screen, BLACK, (0 + border_width, 
                                0 + border_width, 
                                (w/2) - border_width, 
                                ((h/2)-text_frame_h) - border_width))
    line_control1_label = control_name.render("Line 1", 1, WHITE)
    label_progress = label_progress_template.render("Progress", 1, WHITE)
    label_percentage = label_percentage_template.render("{} %".format(round(line1_progress * 100)), 1, WHITE)
    label_status = label_status_template.render("Status : ", 1 , WHITE)
    label_status_value = label_status_value_template.render("IDLE", 1 , WHITE)
    label_filename = label_filename_template.render("Filename : ", 1 , WHITE)
    label_filename_value = label_filename_value_template.render("ABCDEFG.xxx", 1 , YELLOW)
    label_system_state = label_system_state_template.render("State :", 1, WHITE)
    label_system_state_value = label_system_state_value_template.render("Lorem ipsum dolor sit amet, consectetur adipisicing elit, ...", 1 , WHITE)


    screen.blit(line_control1_label, (
                                (((w/2)/2) - (line_control1_label.get_width()/2)), 
                                20))

    screen.blit(label_progress, (
            20,
            (h/2) - 55
        ))


    # label status
    screen.blit(label_status, (
            20,
            0 + 160
        ))

    # label status value
    screen.blit(label_status_value, (
            label_status.get_width() + 80,
            0 + 160
        ))

    pg.draw.rect(screen, WHITE, pg.Rect(
            label_progress.get_width() + 40, 
            (h/2) - 60, 
            ((w/3) - border_width)* line1_progress, 
            30
        ))

    # border progress bar
    pg.draw.rect(screen, GRAY, pg.Rect(
            label_progress.get_width() + 40, 
            (h/2) - 60, 
            ((w/3) - border_width)*1, 
            30
        ), 2)

    # percentage
    screen.blit(label_percentage,
        (
            (label_progress.get_width() + 40 + (w/3) + 20),
            (h/2) - 55
        ))

    # merge picture
    # img_fail = pg.transform.scale(img_fail, (250,100))
    # screen.blit(img_fail, (160, 80))
    

    # line 2 frame
    pg.draw.rect(screen, WHITE, (w/2,0, w/2, h/2), border_width)
    pg.draw.rect(screen, BLACK, ((w/2) + border_width, 
                                0 + border_width, 
                                (w/2) - border_width-2, 
                                ((h/2)-text_frame_h) - border_width))
    line_control1_label = control_name.render("Line 2", 1, WHITE)
    label_percentage = label_percentage_template.render("{} %".format(round(line2_progress * 100)), 1, WHITE)

    screen.blit(line_control1_label, (
                                (w - ((w/2)/2) - (line_control1_label.get_width()/2)), 
                                20))
    screen.blit(label_progress, (
            (w/2) + 20,
            (h/2) - 55
        ))

    # label status
    screen.blit(label_status, (
            (w/2) + 20,
            0 + 160
        ))

    # label status value
    screen.blit(label_status_value, (
            (w/2) + label_status.get_width() + 80,
            0 + 160
        ))

    pg.draw.rect(screen, WHITE, pg.Rect(
            (w/2) + label_progress.get_width() + 40, 
            (h/2) - 60, 
            ((w/3) - border_width)*line2_progress, 
            30
        ))
    # border progress bar
    pg.draw.rect(screen, GRAY, pg.Rect(
            (w/2) + label_progress.get_width() + 40, 
            (h/2) - 60, 
            ((w/3) - border_width)*1, 
            30
        ),
        2)
    # percentage
    screen.blit(label_percentage,
        (
            ((w/2) + label_progress.get_width() + 40 + (w/3) + 20),
            (h/2) - 55
        ))


    # line 3 frame
    pg.draw.rect(screen, WHITE, (0, h/2, w/2, h/2), border_width)
    pg.draw.rect(screen, BLACK, (0 + border_width,                       # x
                                (h/2) + border_width,                   # y
                                (w/2) - border_width,                   # w
                                ((h/2)-text_frame_h) - border_width))   # h
    line_control1_label = control_name.render("Line 3", 1, WHITE)
    label_percentage = label_percentage_template.render("{} %".format(round(line3_progress * 100)), 1, WHITE)
    screen.blit(line_control1_label, (
                                (((w/2)/2) - (line_control1_label.get_width()/2)), 
                                ((h/2) + border_width) + 20))
    screen.blit(label_progress, (
            20,
            ((h/2)*2) - 55
        ))

    # label status
    screen.blit(label_status, (
            20,
            (h/2) + 160
        ))

    # label status value
    screen.blit(label_status_value, (
            label_status.get_width() + 80,
            (h/2) + 160
        ))

    pg.draw.rect(screen, WHITE, pg.Rect(
            label_progress.get_width() + 40, 
            ((h/2) *2) - 60, 
            ((w/3) - border_width)*line3_progress, 
            30
        ))
    # border progress bar
    pg.draw.rect(screen, GRAY, pg.Rect(
            label_progress.get_width() + 40, 
            ((h/2)*2) - 60, 
            ((w/3) - border_width)*1, 
            30
        ), 2)
    
    # percentage
    screen.blit(label_percentage,
        (
            (label_progress.get_width() + 40 + (w/3) + 20),
            ((h/2) *2) - 55
        ))

    # line 4 frame
    pg.draw.rect(screen, WHITE, (w/2, h/2, w/2, h/2), border_width)
    pg.draw.rect(screen, BLACK, ((w/2) + border_width,                   # x
                                (h/2) + border_width,                   # y
                                (w/2) - border_width -2,                   # w
                                ((h/2)-text_frame_h) - border_width+2))   # h
    line_control1_label = control_name.render("Line 4", 1, WHITE)
    label_percentage = label_percentage_template.render("{} %".format(round(line4_progress * 100)), 1, WHITE)
    screen.blit(line_control1_label, (
                                (w - ((w/2)/2) - (line_control1_label.get_width()/2)), 
                                ((h/2) + border_width) + 20))

    screen.blit(label_progress, (
            (w/2) + 20,
            ((h/2)*2) - 55
        ))

    # label status
    screen.blit(label_status, (
            (w/2) + 20,
            (h/2) + 160
        ))

    # label status value
    screen.blit(label_status_value, (
            (w/2) + label_status.get_width() + 80,
            (h/2) + 160
        ))

    pg.draw.rect(screen, WHITE, pg.Rect(
            ((w/2) + label_progress.get_width() + 40), 
            ((h/2) *2) - 60, 
            ((w/3) - border_width)*line4_progress, 
            30
        ))
    # border progress bar
    pg.draw.rect(screen, GRAY, pg.Rect(
            ((w/2) + label_progress.get_width() + 40), 
            ((h/2)*2) - 60, 
            ((w/3) - border_width)*1, 
            30
        ), 2)

    # percentage
    screen.blit(label_percentage,
        (
            ((w/2) + label_progress.get_width() + 40 + (w/3) + 20),
            ((h/2)*2) - 55
        ))


    w1_x = 0
    w1_y = h/2 * 2

    pg.draw.rect(screen, BLACK, (
                                w1_x, 
                                w1_y, 
                                w, 
                                h - (h-(h/2*2))))
    pg.draw.rect(screen, WHITE, (w1_x, 
                                w1_y, 
                                w, 
                                h - (h-(h/2*2))), 
                                2)
    

    # draw in taskbar
    # 1. filename
    # 2. overall status
    
    # label filename
    screen.blit(label_filename,
        (
            20,
            ((h/2) * 2) + 20,
        ))

    screen.blit(label_filename_value,
        (
            (20),
            (((h/2) * 2) + 20) + 20
        ))

    # label system state
    screen.blit(label_system_state,
        (
            (w/2) + 20,
            ((h/2) * 2) + 20,
        ))

    screen.blit(label_system_state_value,
        (
            (w/2) + 20,
            (((h/2) * 2) + 20) + 20,
        ))


def main():
    run = True

    while run:
        # fill screen with blue color
        screen.fill(NAVYBLUE) 
        draw_frame_line()

        for event in pg.event.get():
           if event.type == pg.QUIT:
               return
           elif event.type == pg.KEYDOWN:
               if event.key == pg.K_ESCAPE:
                   pg.quit()
                   return

        try :
            #pg.display.flip()
            pg.display.update()
        except pg.error as err:
            log.error("Pygame : {}".format(err))

        clock.tick(60)
        pass

if __name__ == "__main__":
    main()
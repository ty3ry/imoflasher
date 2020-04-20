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
from filehandler import FileHandler

# adjust position 
if sys.platform == 'win32' :
    x = 0
    y = 0
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

elif sys.platform == 'linux':
    os.environ["SDL_MOUSEDEV"] = "/dev/zero"

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
filehandler = FileHandler()

def main():
    run = True
    counter = 0
    c_usb_scan = 0
    c_usb_insertion_detect = 0

    progbar_line1, progbar_line2, progbar_line3, progbar_line4 = (0,0,0,0)
    scan_state = False
    system_state = c.SYSTEM_STATE_IDLE
    system_state_msg = ""
    flag_ready = False

    # debug filehandler
    log.info("Config file \t : {}".format(filehandler.check_config_file()))
    log.info("firmware file \t : {}".format(filehandler.check_firmware()))
    log.info("MD5 status \t : {}".format(filehandler.check_firmware_validity()))

    if filehandler.check_config_file() == 0 and \
        filehandler.check_firmware() == 0 and \
        filehandler.check_firmware_validity() == 1:
            project_name = filehandler.get_project_name()
            frame.update_filename(project_name)
            system_state = c.SYSTEM_STATE_READY
            log.info("System ready")
            flag_ready = True
    else :
        frame.update_filename("No file available")
        log.info("Firmware not exist in current directory.")
        flag_ready = False

    ''' main while '''
    while run:

        '''
        usb insertion detection
        '''
        if c_usb_insertion_detect > 40:
            c_usb_insertion_detect = 0
            if filehandler.check_usb_plug() :
                if scan_state == False:
                    log.info("(USB) Plugin")
                    system_state_msg = "(USB) Plugin"
                    scan_state = True
                    flag_ready = False
            else:
                if scan_state == True:
                    log.info("(USB) Plugout")
                    system_state_msg = "(USB) Plugout"
                    scan_state = False
            log.info("System state : {}".format(system_state))
        c_usb_insertion_detect = c_usb_insertion_detect + 1

        # - IDLE -
        if system_state == c.SYSTEM_STATE_IDLE:
            
            if scan_state == True and flag_ready == False:
                system_state = c.SYSTEM_STATE_USB_SCAN
            else:
                system_state = c.SYSTEM_STATE_IDLE
                if flag_ready == True:
                    system_state_msg = "System ready to flash"
                else:
                    system_state_msg = "Current file empty, please update via USB Disk"
            
        # - USB SCAN -
        elif system_state == c.SYSTEM_STATE_USB_SCAN:
            if c_usb_scan > 50:
                c_usb_scan = 0

                if scan_state == True:
                    try:
                        usb_scan_state = filehandler.usb_scan()

                        if usb_scan_state == c.USB_SCAN_STATE_IDLE:
                            system_state_msg = "(USB) Read"
                        elif usb_scan_state == c.USB_SCAN_STATE_CHECK_CONFIG_FILE:
                            system_state_msg = "(USB) Check config file"
                        elif usb_scan_state == c.USB_SCAN_STATE_CHECK_FIRMWARE_FILE:
                            system_state_msg = "(USB) Check firmware file"
                        elif usb_scan_state == c.USB_SCAN_STATE_CHECK_MD5:
                            system_state_msg = "(USB) Check MD5"
                        elif usb_scan_state == c.USB_SCAN_STATE_COPY_DIRECTORY:
                            system_state_msg = "(USB) Copy directory to local target"
                            system_state = c.SYSTEM_STATE_CHECK_FIRMWARE_EXISTANCE
                        else :
                            pass

                    except Exception as err:
                        system_state = c.SYSTEM_STATE_IDLE
                        log.error("Err : {}".format(err))
                        system_state_msg = "Error :" + err

            c_usb_scan = c_usb_scan + 1

        # - Check file validity
        elif system_state == c.SYSTEM_STATE_CHECK_FIRMWARE_EXISTANCE:
            if filehandler.check_config_file() == 0 \
                and filehandler.check_firmware() == 0   \
                and filehandler.check_firmware_validity() == 1:
                    system_state = c.SYSTEM_STATE_READY
                    system_state_msg = "Done"
            else:
                system_state = c.SYSTEM_STATE_IDLE

        elif system_state == c.SYSTEM_STATE_READY:
            project_name = filehandler.get_project_name()
            frame.update_filename(project_name)
            system_state_msg = "Ready"
            flag_ready = True
            system_state = c.SYSTEM_STATE_IDLE
        else:
            pass
        
        frame.run()
        frame.update_status("RUN", "RUN", "RUN", "RUN")
        frame.update_system_state(system_state_msg)

        if counter > 10:
            #log.info("tick")
            counter = 0
            
            progbar_line1 = progbar_line1 + 1
            progbar_line2 = progbar_line2 + 1
            progbar_line3 = progbar_line3 + 1
            progbar_line4 = progbar_line4 + 1

            if progbar_line1 > 100:
                progbar_line1 = 0
            if progbar_line2 > 100:
                progbar_line2 = 0
            if progbar_line3 > 100:
                progbar_line3 = 0
            if progbar_line4 > 100:
                progbar_line4 = 0

            # update progress bar
            frame.update_progress_bar(progbar_line1, progbar_line2, progbar_line3, progbar_line4)
            frame.update_time(progbar_line1, progbar_line2, progbar_line3, progbar_line4)

        counter = counter + 1
        clock.tick(60)

if __name__ == "__main__":
    main()
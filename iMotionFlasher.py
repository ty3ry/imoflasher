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
from downloader import Downloader
from task_manager import TaskManager, Message
from multiprocessing import Pipe, current_process

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

# downloader init
dl_line1 = Downloader(log, '/dev/ttyS2')
task_manager = TaskManager()
pipe_parent_line1, pipe_child_line1 = Pipe(duplex=True)

# pygame init
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
    c_system_state = 0
    c_usb_insertion_detect = 0
    c_filename_empty_blink , flag_filename_blink = 0, False
    filename_backup = ""

    progbar_line1, progbar_line2, progbar_line3, progbar_line4 = (0,30,70,90)
    scan_state = False
    system_state = c.SYSTEM_STATE_IDLE
    # string buffer
    str_system_state = ""
    str_filename = ""
    # msg status line
    str_status_line1, str_status_line2, str_status_line3, str_status_line4 = ("IDLE", "IDLE", "IDLE", "IDLE")

    flag_ready = False
    flag_usb_scan_done = False

    # debug filehandler
    # log.info("Config file \t : {}".format(filehandler.check_config_file()))
    # log.info("firmware file \t : {}".format(filehandler.check_firmware()))
    # log.info("MD5 status \t : {}".format(filehandler.check_firmware_validity()))

    if filehandler.check_config_file() == 0 and \
        filehandler.check_firmware() == 0 and \
        filehandler.check_firmware_validity() == 1:
            project_name = filehandler.get_project_name()
            #frame.update_filename(project_name, c.YELLOW)
            str_filename = project_name
            system_state = c.SYSTEM_STATE_READY
            log.info("(Check on startup) System ready")
            flag_ready = True
    else :
        #frame.update_filename("No file available", c.RED)
        str_filename = "Empty"
        log.info("Firmware not exist in current directory.")
        flag_ready = False

    # update filename/project name
    frame.update_filename(str_filename, 
            c.YELLOW if flag_ready == True else c.RED)

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
                    str_system_state = "(USB) Plugin"
                    scan_state = True
                    flag_usb_scan_done = False
                    flag_ready = False
            else:
                if scan_state == True:
                    log.info("(USB) Plugout")
                    str_system_state = "(USB) Plugout"
                    scan_state = False
                    
            log.info("System state : {}".format(system_state))
        c_usb_insertion_detect = c_usb_insertion_detect + 1

        if c_system_state > 50:
            c_system_state = 0
            # - IDLE -
            if system_state == c.SYSTEM_STATE_IDLE:
                
                if scan_state == True and flag_usb_scan_done == False:
                    system_state = c.SYSTEM_STATE_USB_SCAN             
                else:
                    system_state = c.SYSTEM_STATE_IDLE
                    if flag_ready == True:
                        str_system_state = "System ready to flash"
                    else:
                        str_system_state = "Current file empty, please update via USB Disk"
                
            # - USB SCAN -
            elif system_state == c.SYSTEM_STATE_USB_SCAN:

                if scan_state == True:
                    try:
                        usb_scan_state = filehandler.usb_scan()

                        if usb_scan_state == c.USB_SCAN_STATE_IDLE:
                            str_system_state = "(USB) Read"
                        elif usb_scan_state == c.USB_SCAN_STATE_CHECK_CONFIG_FILE:
                            str_system_state = "(USB) Check config file"
                        elif usb_scan_state == c.USB_SCAN_STATE_CHECK_FIRMWARE_FILE:
                            str_system_state = "(USB) Check firmware file"
                        elif usb_scan_state == c.USB_SCAN_STATE_CHECK_MD5:
                            str_system_state = "(USB) Check MD5"
                        elif usb_scan_state == c.USB_SCAN_STATE_COPY_DIRECTORY:
                            str_system_state = "(USB) Copy directory to local target"
                            system_state = c.SYSTEM_STATE_CHECK_FIRMWARE_EXISTANCE
                        else :
                            pass

                    except Exception as err:
                        system_state = c.SYSTEM_STATE_ERROR
                        log.error("Err : {}".format(err))
                        str_system_state = "Error : " + str(err)

            # - Check file validity
            elif system_state == c.SYSTEM_STATE_CHECK_FIRMWARE_EXISTANCE:
                if filehandler.check_config_file() == 0 \
                    and filehandler.check_firmware() == 0   \
                    and filehandler.check_firmware_validity() == 1:
                        system_state = c.SYSTEM_STATE_READY
                        str_system_state = "Done"
                else:
                    system_state = c.SYSTEM_STATE_IDLE

            # - ERROR -
            elif system_state == c.SYSTEM_STATE_ERROR:
                flag_ready = False
                if filehandler.check_flasher_directory():
                    log.info("remove flasher directory")
                    filehandler.remove_current_directory()
                    #frame.update_filename("Empty")
                    str_filename = "Empty"
                system_state = c.SYSTEM_STATE_IDLE
                flag_usb_scan_done = True

            elif system_state == c.SYSTEM_STATE_READY:
                project_name = filehandler.get_project_name()
                #frame.update_filename(project_name)
                str_filename = project_name
                str_system_state = "Ready"
                flag_ready = True
                flag_usb_scan_done = True
                system_state = c.SYSTEM_STATE_IDLE
            else:
                pass
        
        c_system_state = c_system_state + 1
        
        frame.update_status(str_status_line1, str_status_line2, str_status_line3, str_status_line4)
        frame.update_system_state(str_system_state)
        # filename / project name blink state
        frame.update_filename_blink(str_filename, flag_ready)
        frame.run()
        # update progress bar
        frame.update_progress_bar(progbar_line1, progbar_line2, progbar_line3, progbar_line4)
        frame.update_time(progbar_line1, progbar_line2, progbar_line3, progbar_line4)

def test_donwloader():

    while True:
        if not task_manager.is_task_created("tline1"):
            log.info("Create task tline1")
            task_manager.create("tline1", func=run_line1, args=(pipe_parent_line1, pipe_child_line1,) )
            task_manager.start("tline1")
        
        if not task_manager.is_alive("tline1"):
            log.info("Terminate task tline1")
            # terminate task
            task_manager.terminate('tline1')



def run_line1(p_conn, c_conn):
    log.info("Start task line1")
    run = True
    pipe_messages = Message()

    while run:
        dl_line1.run()
        run = False


if __name__ == "__main__":
    #main()
    test_donwloader()
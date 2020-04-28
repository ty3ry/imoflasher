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
from datetime import datetime
from control import Control
import wiringpi

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
dl_line1 = Downloader(log, '/dev/ttyS0')    # 1
dl_line2 = Downloader(log, '/dev/ttyS1')    # 2
dl_line3 = Downloader(log, '/dev/ttyS2')
dl_line4 = Downloader(log, '/dev/ttyS3')


task_manager = TaskManager()
pipe_message = Message()
pipe_parent_line1, pipe_child_line1 = Pipe(duplex=True)
pipe_parent_line2, pipe_child_line2 = Pipe(duplex=True)
pipe_parent_line3, pipe_child_line3 = Pipe(duplex=True)
pipe_parent_line4, pipe_child_line4 = Pipe(duplex=True)

pipe_parent_msgs = []
pipe_parent_msgs.append(pipe_parent_line1)
pipe_parent_msgs.append(pipe_parent_line2)
pipe_parent_msgs.append(pipe_parent_line3)
pipe_parent_msgs.append(pipe_parent_line4)

ctrl_line1 = Control()
ctrl_line2 = Control()
ctrl_line3 = Control()
ctrl_line4 = Control()

# pin setup
result = wiringpi.wiringPiSetup()
log.info("Wiring init result : {}".format("OK" if result==0 else "FAIL"))
wiringpi.pinMode(c.BUTTON_START_PIN, 0)                 # set as input
wiringpi.pullUpDnControl(c.BUTTON_START_PIN, 2)         # set internal pullup


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
    system_usb_scan_state = 0
    c_usb_insertion_detect = 0
    c_filename_empty_blink , flag_filename_blink = 0, False

    #progbar_line1, progbar_line2, progbar_line3, progbar_line4 = (0,30,70,90)
    ctrl_line1.progress_value, ctrl_line2.progress_value, ctrl_line3.progress_value, ctrl_line4.progress_value = (0, 0, 0, 0)
    scan_state = False
    system_state = c.SYSTEM_USB_SCAN_IDLE
    # string buffer
    str_system_state = ""
    str_filename = ""
    file_check_status = 0
    
    # msg status line
    #str_status_line1, str_status_line2, str_status_line3, str_status_line4 = ("IDLE", "IDLE", "IDLE", "IDLE")
    ctrl_line1.string_status, ctrl_line2.string_status, ctrl_line3.string_status, ctrl_line4.string_status = \
            ("IDLE", "IDLE", "IDLE", "IDLE")

    flag_ready = False
    flag_usb_scan_done = False
    flag_button_pressed = False

    systick_pre = 0

    # debug filehandler
    # log.info("Config file \t : {}".format(filehandler.check_config_file()))
    # log.info("firmware file \t : {}".format(filehandler.check_firmware()))
    # log.info("MD5 status \t : {}".format(filehandler.check_firmware_validity()))
    file_check_status = filehandler.check_file()

    if file_check_status == 0:
        project_name = filehandler.get_project_name()
        #frame.update_filename(project_name, c.YELLOW)
        str_filename = project_name
        system_state = c.SYSTEM_USB_SCAN_READY
        log.info("(Check on startup) System ready")
        flag_ready = True
    else :
        #frame.update_filename("No file available", c.RED)
        str_filename = "kosong"
        str_system_state = {
            -1 : c.ERROR_CURRFILE_FLASHER_DIR_NOT_FOUND,
            -2 : c.ERROR_CURRFILE_CONFIG_FILE_NOT_FOUND,
            -3 : c.ERROR_CURRFILE_TARGET_FIRMWARE_NOT_FOUND,
            -4 : c.ERROR_CURRFILE_MD5_NOT_MATCH,
        }.get(file_check_status, "Error unknown..")

        log.info("Firmware not exist in current directory.")
        flag_ready = False

    # update filename/project name
    frame.update_filename(str_filename, c.YELLOW if flag_ready == True else c.RED)

    ''' main while '''
    while run:
        
        ''' button start pressed event '''
        if wiringpi.digitalRead(c.BUTTON_START_PIN) == 0:
            if flag_button_pressed == False:
                log.info("Button pressed")
                flag_button_pressed = True

                ''' start if only system ready'''
                if flag_ready == True:
                    ''' Check file validity first '''
                    file_check_status = filehandler.check_file()
                    if file_check_status == 0:
                        # start task
                        if not task_manager.is_task_created(c.TASK_LINE1_NAME):
                            task_manager.create(c.TASK_LINE1_NAME, func=dl_line1.run, args=(pipe_parent_line1, pipe_child_line1,) )
                            task_manager.start(c.TASK_LINE1_NAME)
                            ctrl_line1.run = True

                        if not task_manager.is_task_created(c.TASK_LINE2_NAME):
                            task_manager.create(c.TASK_LINE2_NAME, func=dl_line2.run, args=(pipe_parent_line2, pipe_child_line2,) )
                            task_manager.start(c.TASK_LINE2_NAME)
                            ctrl_line2.run = True

                        if not task_manager.is_task_created(c.TASK_LINE3_NAME):
                            task_manager.create(c.TASK_LINE3_NAME, func=dl_line3.run, args=(pipe_parent_line3, pipe_child_line3,) )
                            task_manager.start(c.TASK_LINE3_NAME)
                            ctrl_line3.run = True

                        if not task_manager.is_task_created(c.TASK_LINE4_NAME):
                            task_manager.create(c.TASK_LINE4_NAME, func=dl_line4.run, args=(pipe_parent_line4, pipe_child_line4,) )
                            task_manager.start(c.TASK_LINE4_NAME)
                            ctrl_line4.run = True
                    else :
                        log.error("File check failed : {}".format(file_check_status))
        else:
            flag_button_pressed = False

        ''' terminate task if task is done '''
        if task_manager.is_task_created(c.TASK_LINE1_NAME) and \
            not task_manager.is_alive(c.TASK_LINE1_NAME):
            # terminate task
            task_manager.terminate(c.TASK_LINE1_NAME)
            ctrl_line1.run = False

        if task_manager.is_task_created(c.TASK_LINE2_NAME) and \
            not task_manager.is_alive(c.TASK_LINE2_NAME):
            # terminate task
            task_manager.terminate(c.TASK_LINE2_NAME)
            ctrl_line2.run = False

        if task_manager.is_task_created(c.TASK_LINE3_NAME) and \
            not task_manager.is_alive(c.TASK_LINE3_NAME):
            # terminate task
            task_manager.terminate(c.TASK_LINE3_NAME)
            ctrl_line3.run = False

        if task_manager.is_task_created(c.TASK_LINE4_NAME) and \
            not task_manager.is_alive(c.TASK_LINE4_NAME):
            # terminate task
            task_manager.terminate(c.TASK_LINE4_NAME)
            ctrl_line4.run = False

        ''' Check message for from another process / task '''
        for child_msg in pipe_message.receive(pipe_parent_msgs):
            source , msg, payload = child_msg
                
            # Control Line 1
            if source == c.TASK_LINE1_NAME:
                if msg == c.MESSAGE_DOWNLOADER_UPLOAD_PROGRESS :
                    ctrl_line1.progress_value = payload
                elif msg == c.MESSAGE_DOWNLOADER_START_TIMER:
                    ctrl_line1.tick_time = 0
                    ctrl_line1.tick_start_state = True
                    ctrl_line1.error_show = False
                    ctrl_line1.string_status = "RUN"
                    ctrl_line1.progress_value = 0
                elif msg == c.MESSAGE_DOWNLOADER_END_TIMER:
                    ctrl_line1.tick_start_state = False
                elif msg == c.MESSAGE_DOWNLOADER_FINISH_UPLOAD:
                    ctrl_line1.tick_start_state = False
                    ctrl_line1.string_status = "SUCCESS"
                elif msg == c.MESSAGE_DOWNLOADER_ERROR:
                    ctrl_line1.string_status = "Failed"
                    ctrl_line1.string_error_value = payload
                    ctrl_line1.error_show = True
                    ctrl_line1.tick_start_state = False
                
            # Control Line 2
            elif source == c.TASK_LINE2_NAME:
                if msg == c.MESSAGE_DOWNLOADER_UPLOAD_PROGRESS :
                    ctrl_line2.progress_value = payload
                elif msg == c.MESSAGE_DOWNLOADER_START_TIMER:
                    ctrl_line2.tick_time = 0
                    ctrl_line2.tick_start_state = True
                    ctrl_line2.error_show = False
                    ctrl_line2.string_status = "RUN"
                    ctrl_line2.progress_value = 0
                elif msg == c.MESSAGE_DOWNLOADER_END_TIMER:
                    ctrl_line2.tick_start_state = False
                elif msg == c.MESSAGE_DOWNLOADER_FINISH_UPLOAD:
                    ctrl_line2.tick_start_state = False
                    ctrl_line2.string_status = "SUCCESS"
                elif msg == c.MESSAGE_DOWNLOADER_ERROR:
                    ctrl_line2.string_status = "Failed"
                    ctrl_line2.string_error_value = payload
                    ctrl_line2.error_show = True
                    ctrl_line2.tick_start_state = False

            # Control Line 3
            elif source == c.TASK_LINE3_NAME:
                if msg == c.MESSAGE_DOWNLOADER_UPLOAD_PROGRESS :
                    ctrl_line3.progress_value = payload
                elif msg == c.MESSAGE_DOWNLOADER_START_TIMER:
                    ctrl_line3.tick_time = 0
                    ctrl_line3.tick_start_state = True
                    ctrl_line3.error_show = False
                    ctrl_line3.string_status = "RUN"
                    ctrl_line3.progress_value = 0
                elif msg == c.MESSAGE_DOWNLOADER_END_TIMER:
                    ctrl_line3.tick_start_state = False
                elif msg == c.MESSAGE_DOWNLOADER_FINISH_UPLOAD:
                    ctrl_line3.tick_start_state = False
                    ctrl_line3.string_status = "SUCCESS"
                elif msg == c.MESSAGE_DOWNLOADER_ERROR:
                    ctrl_line3.string_status = "Failed"
                    ctrl_line3.string_error_value = payload
                    ctrl_line3.error_show = True
                    ctrl_line3.tick_start_state = False

                # Control Line 4
            elif source == c.TASK_LINE4_NAME:
                if msg == c.MESSAGE_DOWNLOADER_UPLOAD_PROGRESS :
                    ctrl_line4.progress_value = payload
                elif msg == c.MESSAGE_DOWNLOADER_START_TIMER:
                    ctrl_line4.tick_time = 0
                    ctrl_line4.tick_start_state = True
                    ctrl_line4.error_show = False
                    ctrl_line4.string_status = "RUN"
                    ctrl_line4.progress_value = 0
                elif msg == c.MESSAGE_DOWNLOADER_END_TIMER:
                    ctrl_line4.tick_start_state = False
                elif msg == c.MESSAGE_DOWNLOADER_FINISH_UPLOAD:
                    ctrl_line4.tick_start_state = False
                    ctrl_line4.string_status = "SUCCESS"
                elif msg == c.MESSAGE_DOWNLOADER_ERROR:
                    ctrl_line4.string_status = "Failed"
                    ctrl_line4.string_error_value = payload
                    ctrl_line4.error_show = True
                    ctrl_line4.tick_start_state = False

        ''' System tick to calculate process takt time '''
        if systick_pre != datetime.now().second:
            systick_pre = datetime.now().second
            if ctrl_line1.tick_start_state:
                ctrl_line1.tick_time = ctrl_line1.tick_time + 1
            if ctrl_line2.tick_start_state:
                ctrl_line2.tick_time = ctrl_line2.tick_time + 1
            if ctrl_line3.tick_start_state:
                ctrl_line3.tick_time = ctrl_line3.tick_time + 1
            if ctrl_line4.tick_start_state:
                ctrl_line4.tick_time = ctrl_line4.tick_time + 1    

        ''' usb insertion detection '''
        if c_usb_insertion_detect > 40:
            c_usb_insertion_detect = 0
            ''' USB plugin '''
            if filehandler.check_usb_plug() \
                and ctrl_line1.run == False and ctrl_line2.run == False \
                and ctrl_line3.run == False and ctrl_line4.run == False:
                if scan_state == False:
                    log.info("(USB) Plugin")
                    str_system_state = "(USB) Plugin"
                    scan_state = True
                    flag_usb_scan_done = False

                    ''' Reset flag ready when usb plugin event '''
                    flag_ready = False
            else:
                if scan_state == True:
                    log.info("(USB) Plugout")
                    str_system_state = "(USB) Plugout"
                    scan_state = False
        ''' usb insertion counter periode '''
        c_usb_insertion_detect = c_usb_insertion_detect + 1

        ''' usb scan process section '''
        if system_usb_scan_state > 50:
            system_usb_scan_state = 0
            # - IDLE -
            if system_state == c.SYSTEM_USB_SCAN_IDLE:
                
                if scan_state == True and flag_usb_scan_done == False:
                    system_state = c.SYSTEM_USB_SCAN_PROCESS             
                else:
                    system_state = c.SYSTEM_USB_SCAN_IDLE
                    if flag_ready == True:
                        str_system_state = "Siap program"
                    else:
                        str_system_state = c.ERROR_FIRMWARE_FILE_FAIL#"Firmware tidak tersedia, update dengan USB"
                
            # - USB SCAN -
            elif system_state == c.SYSTEM_USB_SCAN_PROCESS:

                if scan_state == True:
                    try:
                        usb_scan_state = filehandler.usb_scan()

                        if usb_scan_state == c.USB_SCAN_STATE_IDLE:
                            str_system_state = "(USB) Baca"
                        elif usb_scan_state == c.USB_SCAN_STATE_CHECK_CONFIG_FILE:
                            str_system_state = "(USB) Periksa file konfigurasi"
                        elif usb_scan_state == c.USB_SCAN_STATE_CHECK_FIRMWARE_FILE:
                            str_system_state = "(USB) Periksa file firmware"
                        elif usb_scan_state == c.USB_SCAN_STATE_CHECK_MD5:
                            str_system_state = "(USB) Periksa Checksum MD5"
                        elif usb_scan_state == c.USB_SCAN_STATE_COPY_DIRECTORY:
                            str_system_state = "(USB) Salin file ke lokal"
                            system_state = c.SYSTEM_USB_SCAN_CHECK_FIRMWARE
                        else :
                            pass

                    except Exception as err:
                        system_state = c.SYSTEM_USB_SCAN_ERROR
                        log.error("Err : {}".format(err))
                        str_system_state = "Error : " + str(err)

            # - Check file validity
            elif system_state == c.SYSTEM_USB_SCAN_CHECK_FIRMWARE:
                if filehandler.check_config_file() == 0 \
                    and filehandler.check_firmware() == 0   \
                    and filehandler.check_firmware_validity() == 1:
                        system_state = c.SYSTEM_USB_SCAN_READY
                        str_system_state = "Selesai"
                else:
                    system_state = c.SYSTEM_USB_SCAN_IDLE

            # - ERROR -
            elif system_state == c.SYSTEM_USB_SCAN_ERROR:
                flag_ready = False
                if filehandler.check_flasher_directory():
                    log.info("remove flasher directory")
                    filehandler.remove_current_directory()
                    #frame.update_filename("Empty")
                    str_filename = "kosong"
                system_state = c.SYSTEM_USB_SCAN_IDLE
                flag_usb_scan_done = True

            # - Firmware file ready -
            elif system_state == c.SYSTEM_USB_SCAN_READY:
                project_name = filehandler.get_project_name()
                #frame.update_filename(project_name)
                str_filename = project_name
                str_system_state = "Siap"
                flag_ready = True
                flag_usb_scan_done = True
                system_state = c.SYSTEM_USB_SCAN_IDLE
            else:
                pass

        ''' USB scan periode '''
        system_usb_scan_state = system_usb_scan_state + 1
        
        frame.update_status(ctrl_line1.string_status, ctrl_line2.string_status,\
            ctrl_line3.string_status, ctrl_line4.string_status)

        # update system error status
        frame.update_error_line1(ctrl_line1.string_error_value, ctrl_line1.error_show)
        frame.update_error_line2(ctrl_line2.string_error_value, ctrl_line2.error_show)
        frame.update_error_line3(ctrl_line3.string_error_value, ctrl_line3.error_show)
        frame.update_error_line4(ctrl_line4.string_error_value, ctrl_line4.error_show)

        # update system state
        frame.update_system_state(str_system_state)

        # filename / project name blink state
        frame.update_filename_blink(str_filename, flag_ready)

        # update progress bar
        frame.update_progress_bar(ctrl_line1.progress_value, ctrl_line2.progress_value,\
            ctrl_line3.progress_value, ctrl_line4.progress_value)
        frame.update_time(ctrl_line1.tick_time, ctrl_line2.tick_time, \
            ctrl_line3.tick_time, ctrl_line4.tick_time)
        frame.run()


if __name__ == "__main__":
    main()
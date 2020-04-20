from os import path
import configparser
import constant as c
import hashlib
import shutil, os
from subprocess import call, DEVNULL, STDOUT

class FileHandler():
    def __init__(self):
        self._flasher_dir = "./flasher/"
        self._config_filename = "flasher.ini"

        # usbmount firmware location directory
        self._usb_mount_directory = "/media/usb/flasher/"

        # get config from config file
        self.config = configparser.ConfigParser()

        self.usb_scan_state = c.USB_SCAN_STATE_IDLE
        self.firmware_filename = ""
        self._copy_done = False
        self.usb_event = c.USB_SCAN_STATE_IDLE

    def set_firmware_filename(self, firmware_filename):
        self.firmware_filename = firmware_filename
    
    def check_usb_plug(self):
        # get usb plug status with subprocess on /device
        args = [0] * 2
        args[0] = "ls"
        args[1] = "/dev/sda"
        if call([args[0], args[1]], stdout=DEVNULL, stderr=STDOUT) == 0:
            return 1
        else :
            return 0

    def check_config_file(self):
        status = 0
        if path.isdir("./flasher") :
            if path.isfile("./flasher/flasher.ini"):
                status = 0
            else :
                status = -1
        else :
            status = -2
        return status

    def check_firmware(self):
        status = 0
        if path.isdir("./flasher") :
            if path.isfile("./flasher/target.ldf"):
                status = 0
            else :
                status = -1
        else :
            status = -2
        return status

    def check_firmware_validity(self):
        result = 0
        # read config file
        self.config.read('./flasher/flasher.ini')
        md5_config = self.config['file']['md5']
        try :
            f = open('./flasher/target.ldf', "rb").read()
            md5_target = hashlib.md5(f).hexdigest()
            # print("ref : {}".format(md5_config))
            # print("cur : {}".format(md5_target))

            if md5_config == md5_target:
                result = 1
            else :
                result = 0
        except Exception :
            result = 0
        
        return result 


    def get_project_name(self):
        self.config.read('./flasher/flasher.ini')
        return self.config['project']['name']



    def usb_scan(self):

        # state machine for usb scan
        if self.usb_scan_state == c.USB_SCAN_STATE_IDLE:
            self.usb_event = c.USB_SCAN_STATE_IDLE

            # do check directory
            if path.isdir(self._usb_mount_directory):
                '''
                * 
                '''
                if self._copy_done == False:
                    self.usb_scan_state = c.USB_SCAN_STATE_CHECK_CONFIG_FILE
                else:
                    self.usb_event = None 
            else:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE
                # reset flag done
                self._copy_done = False

            # return event
            return self.usb_event

        elif self.usb_scan_state == c.USB_SCAN_STATE_CHECK_CONFIG_FILE:
            self.usb_event = c.USB_SCAN_STATE_CHECK_CONFIG_FILE
            # check config file
            if path.isfile(self._usb_mount_directory + "flasher.ini"):
                self.usb_scan_state = c.USB_SCAN_STATE_CHECK_FIRMWARE_FILE
                self.config.read(self._usb_mount_directory + 'flasher.ini')
            else:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE
                raise Exception("Config file not found/missing..")
                
            return self.usb_event

        elif self.usb_scan_state == c.USB_SCAN_STATE_CHECK_FIRMWARE_FILE:
            self.usb_event = c.USB_SCAN_STATE_CHECK_FIRMWARE_FILE
            # read config file
            self.firmware_filename = self.config['file']['name']

            # check file
            if path.isfile(self._usb_mount_directory + self.firmware_filename):
                self.usb_scan_state = c.USB_SCAN_STATE_CHECK_MD5
            else:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE
                raise Exception("Firmware file ({}) not found".format(self.firmware_filename))
                
            return self.usb_event

        elif self.usb_scan_state == c.USB_SCAN_STATE_CHECK_MD5:
            self.usb_event = c.USB_SCAN_STATE_CHECK_MD5

            # open file
            try:
                f = open(self._usb_mount_directory + self.firmware_filename, "rb").read()
            except Exception:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE

            md5_ref = self.config['file']['md5']
            md5_cur = hashlib.md5(f).hexdigest()

            if md5_ref == md5_cur :
                self.usb_scan_state = c.USB_SCAN_STATE_COPY_DIRECTORY
            else:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE
                raise Exception("MD5 Not match..")
                
            return self.usb_event

        elif self.usb_scan_state == c.USB_SCAN_STATE_COPY_DIRECTORY:
            '''
            - check directory if exist so delete it first
            '''
            self.usb_event = c.USB_SCAN_STATE_COPY_DIRECTORY
            if path.isdir("./flasher"):
                shutil.rmtree('./flasher')

            # copy directory from current usb location to destination directory (local)
            try:
                # create directory
                os.mkdir('flasher')
                # copy config file
                shutil.copy(self._usb_mount_directory + 'flasher.ini', './flasher/')
                shutil.copy(self._usb_mount_directory + self.firmware_filename, './flasher/target.ldf')
                self._copy_done = True
            except Exception as err:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE
                raise Exception("{}".format(err))
            finally:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE

            return self.usb_event

        else:
            pass

    def usb_scan_result(self):
        pass
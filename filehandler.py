from os import path
import configparser
import constant as c
import hashlib
import shutil, os

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

    def set_firmware_filename(self, firmware_filename):
        self._firmware_filename = firmware_filename

    def scan(self):
        '''
        scan file upgrade, 
        '''
        try:
            with open(self._flasher_root_dir + self._config_filename, "r") as config_file:
                print("Config file found")
        except Exception as err:
            print("Config file not found ..")

    def check_md5(self, md5_ref, md5_des):
        pass

    def scan_is_current_config_file_exist(self):
        status = 0
        if path.isdir("./flasher") :
            if path.isfile("./flasher/flasher.ini"):
                status = 0
            else :
                status = -1
        else :
            status = -2
        return status

    def scan_is_current_file_exist(self):
        status = 0
        if path.isdir("./flasher") :
            if path.isfile("./flasher/target.ldf"):
                status = 0
            else :
                status = -1
        else :
            status = -2
        return status

    def get_project_name(self):
        self.config.read('./flasher/flasher.ini')
        return self.config['project']['name']

    
    def do_copy(self):
        # check directory is firmware directory exist
        pass

    def usb_scan(self):
        usb_event = c.USB_SCAN_STATE_IDLE

        # state machine for usb scan
        if self.usb_scan_state == c.USB_SCAN_STATE_IDLE:
            usb_event = c.USB_SCAN_STATE_IDLE
            # do check directory
            if path.isdir(self._usb_mount_directory):
                self.usb_scan_state = c.USB_SCAN_STATE_CHECK_CONFIG_FILE
            else:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE

            # return event
            return usb_event

        elif self.usb_scan_state == c.USB_SCAN_STATE_CHECK_CONFIG_FILE:
            usb_event = c.USB_SCAN_STATE_CHECK_CONFIG_FILE
            # check config file
            if path.isfile(self._usb_mount_directory + "flasher.ini"):
                self.usb_scan_state = c.USB_SCAN_STATE_CHECK_FIRMWARE_FILE
                self.config.read(self._usb_mount_directory + 'flasher.ini')
            else:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE

            return usb_event

        elif self.usb_scan_state == c.USB_SCAN_STATE_CHECK_FIRMWARE_FILE:
            usb_event = c.USB_SCAN_STATE_CHECK_FIRMWARE_FILE
            # read config file
            self.firmware_filename = self.config['file']['name']

            # check file
            if path.isfile(self._usb_mount_directory + self.firmware_filename):
                self.usb_scan_state = c.USB_SCAN_STATE_CHECK_MD5
            else:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE

            return usb_event

        elif self.usb_scan_state == c.USB_SCAN_STATE_CHECK_MD5:
            usb_event = c.USB_SCAN_STATE_CHECK_MD5

            # open file
            try:
                print("Filename : {}".format(self._usb_mount_directory + self.firmware_filename))
                #with open(self._usb_mount_directory + self.firmware_filename, "rb") as f:
                f = open(self._usb_mount_directory + self.firmware_filename, "rb").read()

                md5_ref = self.config['file']['md5']
                md5_cur = hashlib.md5(f).hexdigest()

                if md5_ref == md5_cur :
                    self.usb_scan_state = c.USB_SCAN_STATE_COPY_DIRECTORY
                else:
                    self.usb_scan_state = c.USB_SCAN_STATE_IDLE
            except Exception as err:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE
            
            return usb_event

        elif self.usb_scan_state == c.USB_SCAN_STATE_COPY_DIRECTORY:
            '''
            - check directory if exist so delete it first
            '''
            usb_event = c.USB_SCAN_STATE_COPY_DIRECTORY
            if path.isdir("./flasher"):
                shutil.rmtree('./flasher')


            # copy directory from current usb location to destination directory (local)
            try:
                # create directory
                os.mkdir('flasher')
                # copy config file
                shutil.copy(self._usb_mount_directory + 'flasher.ini', './flasher/')
                shutil.copy(self._usb_mount_directory + self.firmware_filename, './flasher/target.ldf')
                
            except Exception as err:
                print("Error Copying.. {}".format(err))
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE
            finally:
                self.usb_scan_state = c.USB_SCAN_STATE_IDLE
            return usb_event

        else:
            pass


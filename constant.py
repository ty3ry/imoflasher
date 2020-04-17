'''
- constant data resources
'''

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


# usb scan state
USB_SCAN_STATE_IDLE = 0
USB_SCAN_STATE_CHECK_CONFIG_FILE = 1
USB_SCAN_STATE_CHECK_FIRMWARE_FILE = 2
USB_SCAN_STATE_CHECK_MD5 = 3
USB_SCAN_STATE_COPY_DIRECTORY = 4



# system state
SYSTEM_STATE_IDLE = 0
'''
if current flasher directory contain config file and firmware 
and contain valid 
'''
SYSTEM_STATE_READY = 1

'''
if there is any usb plug on to update current firmware
check directory contain config file and firmware file
check validity with md5 checksum
copy file config file and firmware file to current local
firmware directory
'''
SYSTEM_STATE_USB_SCAN = 2
SYSTEM_STATE_BUSY = 3



# system state message definition


# error message definition
MESSAGE_USB_SCAN_NO_ERROR = 0
MESSAGE_USB_SCAN_ERR_CONFIG_FILE_NOT_FOUND = 1
MESSAGE_USB_SCAN_ERR_FIRMWARE_FILE_NOT_FOUND = 2
MESSAGE_USB_SCAN_ERR_MD5_NOT_MATCH = 3
MESSAGE_USB_SCAN_ERR_COPYING = 4
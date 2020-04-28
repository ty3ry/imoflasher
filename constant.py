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

# usb event
USB_EVENT_IDLE = 0
USB_EVENT_READING = 1
USB_EVENT_CHECK_CONFIG_FILE = 2
USB_EVENT_CHECK_FIRMWARE_FILE = 3
USB_EVENT_CHECK_MD5 = 4
USB_EVENT_COPYING_FILE = 5



# system state
SYSTEM_USB_SCAN_IDLE = 0
'''
if current flasher directory contain config file and firmware 
and contain valid 
'''
SYSTEM_USB_SCAN_READY = 1

'''
if there is any usb plug on to update current firmware
check directory contain config file and firmware file
check validity with md5 checksum
copy file config file and firmware file to current local
firmware directory
'''
SYSTEM_USB_SCAN_PROCESS = 2

'''
check current firmware existance and check file validity
with MD5 checksum
'''
SYSTEM_USB_SCAN_CHECK_FIRMWARE = 3


'''
state when proses update firmware failed or something wrong
'''
SYSTEM_USB_SCAN_ERROR = 4

SYSTEM_STATE_BUSY = 5


# multiprosessing system message
MESSAGE_DOWNLOADER_CLASS = 0x00
MESSAGE_DOWNLOADER_APPLICATION_MODE = (MESSAGE_DOWNLOADER_CLASS + 1)
MESSAGE_DOWNLOADER_BOOTLOADER_MODE = (MESSAGE_DOWNLOADER_CLASS + 2)
MESSAGE_DOWNLOADER_CONFIG_MODE = (MESSAGE_DOWNLOADER_CLASS + 3)

MESSAGE_DOWNLOADER_CHECK_COMM = (MESSAGE_DOWNLOADER_CLASS + 4)
MESSAGE_DOWNLOADER_SWITCH_TO_SBSL = (MESSAGE_DOWNLOADER_CLASS + 5)
MESSAGE_DOWNLOADER_PARSE_FILE = (MESSAGE_DOWNLOADER_CLASS + 6)
MESSAGE_DOWNLOADER_FBSL_ID = (MESSAGE_DOWNLOADER_CLASS + 7)
MESSAGE_DOWNLOADER_START_UPLOADING_FIRMWARE  = (MESSAGE_DOWNLOADER_CLASS + 8)
MESSAGE_DOWNLOADER_ERROR = (MESSAGE_DOWNLOADER_CLASS + 9)
MESSAGE_DOWNLOADER_UPLOAD_PROGRESS = (MESSAGE_DOWNLOADER_CLASS + 10)
MESSAGE_DOWNLOADER_PARAMETER_UPLOAD = (MESSAGE_DOWNLOADER_CLASS + 11)
MESSAGE_DOWNLOADER_SCRIPT_UPLOAD = (MESSAGE_DOWNLOADER_CLASS + 12)
MESSAGE_DOWNLOADER_FINISH_UPLOAD = (MESSAGE_DOWNLOADER_CLASS + 13)
MESSAGE_DOWNLOADER_START_TIMER = (MESSAGE_DOWNLOADER_CLASS + 14)
MESSAGE_DOWNLOADER_END_TIMER = (MESSAGE_DOWNLOADER_CLASS + 15)

'''
Flashing process Error note
show in each line control window
'''
ERROR_UNKNOWN_MODE = "Error unknown mode"
ERROR_APP_MODE_COMM_FAIL = "Error communication fail"
ERROR_CANNOT_ENTER_SBSL_MODE = "Error Cannot enter bootloader mode"
ERROR_SBSL_AUTOBAUD_FAIL = "Error bootloader autobaudrate failed"
ERROR_FIRMWARE_UPLOAD = "Error firmware upload"
ERROR_CONFIG_MODE_AUTOBAUD_FAIL = "Error autobaudrate in config mode failed"
ERROR_PARAMETER_UPLOAD = "Error on parameter upload"
ERROR_SCRIPT_UPLOAD = "Error on script uploading"
ERROR_SWITCH_APP_MODE = "Error when switching to application mode"

'''
Current file Error definition
show in system state
'''
ERROR_CURRFILE_FLASHER_DIR_NOT_FOUND = "Error : Directori flasher tidak ditemukan"
ERROR_CURRFILE_CONFIG_FILE_NOT_FOUND = "Error : File config tidak ditemukan"
ERROR_CURRFILE_TARGET_FIRMWARE_NOT_FOUND = "Error : Firmware target tidak ditemukan"
ERROR_CURRFILE_MD5_NOT_MATCH = "Error : MD5 tidak sesuai"

'''
usb scan error definition
show in system state
'''
ERROR_USB_SCAN_FILE_FIRMWARE_NOT_FOUND = "File firmware tidak ditemukan"
ERROR_USB_SCAN_FILE_CONFIG_NOT_FOUND = "File konfigurasi tidak ditemukan"
ERROR_USB_SCAN_MD5_NOT_MATCH = "Checksum MD5 tidak sesuai"
ERROR_FIRMWARE_FILE_FAIL = "FIrmware tidak ditemukan, update dengan USB"

'''
Task name
'''
TASK_LINE1_NAME = "task_line1"
TASK_LINE2_NAME = "task_line2"
TASK_LINE3_NAME = "task_line3"
TASK_LINE4_NAME = "task_line4"

'''
GPIO pin definition
'''
BUTTON_START_PIN = 25


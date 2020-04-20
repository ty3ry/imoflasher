
import serial
import time
import sys
from datetime import datetime
import logging

class Downloader():
    def __init__(self, log=None, uart_dev='/dev/ttyS0', uart_baud=115200):
        
        if log == None:
            self.log = self.setup_custom_logger("logger")
        else :
            self.log = log
        self.log.info("init uart on : {}".format(uart_dev))
        self.log.info("uart baud : {}".format(uart_baud))
        self.uart_dev = uart_dev
        self.uart_baud = uart_baud

        # location of firmware file
        self.firmware_path = "./flasher/target.ldf"

        # init uart
        try:
            self.ser = serial.Serial(self.uart_dev, baudrate=self.uart_baud)
            self.ser.flush()
        except Exception as err:
            self.log.error("{}".format(err))

    def setup_custom_logger(self, name):
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(screen_handler)
        return logger


    def uart_init(self):
        pass

    def run(self):
        '''

        '''
        self.ser.timeout = 2
        self.log.info("Auto detecting mode...")
        msg = b'\x00\x6c'
        self.ser.write(msg)
        ans = self.ser.read()
        if (ans == b'\x5d'):
            # sbsl mode
            uploading_state = 1
            en_autobaudrate = 0
        elif (ans == b'\xcd'):
            # config mode
            uploading_state = 2
            en_autobaudrate = 0
        elif (ans == b''):
            # application mode (timeout)
            uploading_state = 0
            en_autobaudrate = 1
        else:
            # error
            self.log.error('Unknown mode, fail...')
            self.log.info('ans: {}'.format(ans.hex()))
            sys.exit(1)
        
        if (uploading_state == 0) :
            self.log.info('In application mode, communication checking...')
            self.ser.timeout = 1
            count = 0
            # try to check communication mode
            while (count < 4):
                msg = b'\x7e\x13\x7e\x13'
                self.ser.write(msg)
                ans = self.ser.read(4)
                if (ans == b'\x7e\x17\x7e\x17') or (ans == b'\x7e\x1b\x7e\x1b'):
                    break
                count = count + 1
            else:
                self.log.error('Communication fail...')
                self.log.info('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                sys.exit(1)

            # change to bootloader mode
            self.log.info("Switching to sbsl mode ...")
            count = 0
            while (count < 4):
                msg = b'\x7e\x02\x80\x31\x51\x81\x10\xfa\xf8\x7e\x87'
                self.ser.write(msg)
                ans = self.ser.read()
                if (ans == b'\xfe'):
                    break
                if (ans == b'\x7e'):
                    ans = self.ser.read(self.ser.in_waiting)
                    print('in_waiting: 7e {}'.format(ans.hex()))
                    break
                count = count + 1
            else:
                self.log.error('Cannot enter sbsl mode...')
                self.log.info('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                sys.exit(1)

            uploading_state = 1
            time.sleep(1)

        # read and parse input file
        self.log.info('Reading and parsing input file...')
        parse_mode = 0
        firmware_cmd = []
        parameter_cmd = []
        script_cmd = []

        with open(self.firmware_path, "r") as f:
            for line in f:
                if line[0] == '%':
                    if '%:Firmware Data Section Begin' in line:
                        parse_mode = 0
                    elif '%:Parameters Data Section Begin' in line:
                        parse_mode = 1
                    elif '%:Script Data Section Begin' in line:
                        parse_mode = 2
                elif line[0] == '#':
                    pass
                elif line[0] == '\n':
                    pass
                else:
                    if parse_mode == 0:
                        firmware_cmd.append(bytes.fromhex(line))
                    elif parse_mode == 1:
                        parameter_cmd.append(bytes.fromhex(line))
                    elif parse_mode == 2:
                        script_cmd.append(bytes.fromhex(line))

        if uploading_state == 1:
            # connect and do autobaudrate
            self.ser.timeout = 3
            if en_autobaudrate == 1:
                self.log.info('In sbsl mode, auto baudrate configuration...')
                msg = b'\x00\x6c'
                self.ser.write(msg)
                ans = self.ser.read()
                if (ans != b'\x5d'):
                    self.log.info('SBSL auto baudrate fail...')
                    self.log.info('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                    sys.exit(1)

            # read SBSL status (Flash erase)
            self.log.info('Get sbsl status & id, flash erasing...')
            msg = b'\xa0\x10\x00\x00\x27'
            self.ser.write(msg)
            ans = self.ser.read(42)
            #check timeout, Status byte and parse the return value (SBSL id)
            fdtc = ans[21]
            sbsl_id = ans[24:40]
            self.log.info('FDTC : {}'.format(fdtc))
            self.log.info('SBSL id : {}'.format(sbsl_id.hex()))

            # firmware uploading to device
            self.log.info('Firmware uploading...')
            msg_count = 1
            msg_count_max = len(firmware_cmd)
            for msg in firmware_cmd:
                self.ser.write(msg)
                if msg[1] == 0x20:
                    ans = self.ser.read(3)
                    if ans[-2:] != b'\x90\x00':
                        self.log.error('Error firmware uploading...')
                        self.log.info('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                        sys.exit(1)
                elif msg[1] == 0x21:
                    ans = self.ser.read(3) ###
                    if ans[-2:] != b'\x90\x00':
                        self.log.error('Error firmware uploading...')
                        self.log.info('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                        sys.exit(1)
                else:
                    pass

                # set progress bar
                # sys.stdout.write('\r')
                # sys.stdout.write("[%-20s] %d%%" % ('='*int((msg_count/msg_count_max)*20), (msg_count/msg_count_max)*100))
                # sys.stdout.flush()
                self.log.info("({})".format(int((msg_count/msg_count_max)*100)))
                msg_count += 1
                time.sleep(.100)
            uploading_state = 2
            en_autobaudrate = 1
            # entering config mode
            time.sleep(.500)

        if uploading_state == 2:
            # run autobaudrate
            if en_autobaudrate == 1:
                self.log.info('In config mode, auto baudrate configuration...')
                msg = b'\x00\x6c'
                self.ser.write(msg)
                ans = self.ser.read()
                if (ans != b'\xcd'):
                    self.log.error('Config mode auto baudrate fail...')
                    self.log.info('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                    sys.exit(1)

            # parameter uploading to device
            self.log.info('Parameter uploading...')
            for msg in parameter_cmd:
                self.ser.write(msg)
                if msg[1] == 0x20:
                    ans = self.ser.read(3)
                elif msg[1] == 0x21:
                    ans = self.ser.read(2)
                elif msg[1] == 0x22:
                    ans = self.ser.read(2)
                else:
                    pass
                if ans[-2:] != b'\x90\x00':
                    self.log.error('Error parameter uploading...')
                    self.log.info('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                    sys.exit(1)
                time.sleep(.100)

            # script uploading to device
            self.log.info('Script uploading...')
            for msg in script_cmd:
                self.ser.write(msg)
                if msg[1] == 0x20:
                    ans = self.ser.read(3)
                elif msg[1] == 0x21:
                    ans = self.ser.read(2)
                elif msg[1] == 0x22:
                    ans = self.ser.read(2)
                else:
                    pass
                if ans[-2:] != b'\x90\x00':
                    self.log.eror('Error script uploading...')
                    self.log.info('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                    sys.exit(1)
                time.sleep(.100)

            # change boot mode to application (0xAD)
            self.log.info('Switching to application mode...')
            msg = b'\xa0\x18\xad\x52\x00'
            self.ser.write(msg)
            ans = self.ser.read(3)
            if ans != b'\x90\x00\xff':
                self.log.error('Fail to switch to Application mode...')
                self.log.info('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                sys.exit(1)
            self.log.info('Finish uploading...')
            self.log.info('Success')
        end_time = datetime.now()
        #self.log.info('Duration: {}'.format(end_time - start_time))
        self.log.info('(c)2020 Marklin')
        sys.exit(0)
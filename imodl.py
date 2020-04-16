# coding=utf-8
''' iMotion Downloader

    Author: Markus Setya Budi Soetikno
    Company: PT Hartono Istana Teknologi (Polytron)
    Dept.: Research and Development
    Module: Main Application / console app
    Version: 0.1
    Date:   06/04/2020
'''
import serial
import time
import sys
from datetime import datetime
import configparser

if __name__ == '__main__':
    # initialization
    start_time = datetime.now()
    print('iMotion Downloader Tool')
    print('-----------------------')
    config = configparser.ConfigParser()
    config.read('imodl.ini')
    com_port = config['default']['port']
    com_baudrate = config.getint('default', 'baudrate')
    input_filename = config['default']['input_file']
    uploading_state = config.getint('default', 'start_state')
    
    # configure serial communication
    ser = serial.Serial(com_port, baudrate=com_baudrate)
    ser.flush()

    # do auto detect mode, assume in fab out mode (sbsl mode) for production
    # check/connect and do autobaudrate
    ser.timeout = 2
    print('Auto detecting mode...')
    msg = b'\x00\x6c'
    ser.write(msg)
    ans = ser.read()
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
        print('Unknown mode, fail...')
        print('ans: {}'.format(ans.hex()))
        sys.exit(1)

    if (uploading_state == 0):
        # in application mode
        # waiting for 'ff' or 'ad' after device power up
        '''
        print('Waiting for device power up response (in application mode)...')
        ans = ser.read()
        if (ans != b'\xff') and (ans != b'\xad'):
            print('Not in application Mode...')
            sys.exit(1)
        ''' 
        # check communication
        print('In application mode, communication checking...')
        ser.timeout = 1
        count = 0
        while (count < 4):
            msg = b'\x7e\x13\x7e\x13'
            ser.write(msg)
            ans = ser.read(4)
            if (ans == b'\x7e\x17\x7e\x17') or (ans == b'\x7e\x1b\x7e\x1b'):
                break
            count = count + 1
        else:
            print('Communication fail...')
            print('msg: {} --> {}'.format(msg.hex(), ans.hex()))
            sys.exit(1)

        # change to bootloader mode (SBSL)
        print('Switching to sbsl mode...')
        count = 0
        while (count < 4):
            msg = b'\x7e\x02\x80\x31\x51\x81\x10\xfa\xf8\x7e\x87'
            ser.write(msg)
            ans = ser.read()
            if (ans == b'\xfe'):
                break
            if (ans == b'\x7e'):
                ans = ser.read(ser.in_waiting)
                print('in_waiting: 7e {}'.format(ans.hex()))
                break
            count = count + 1
        else:
            print('Cannot enter sbsl mode...')
            print('msg: {} --> {}'.format(msg.hex(), ans.hex()))
            sys.exit(1)
        uploading_state = 1
        time.sleep(1)

    # read and parse input file
    print('Reading and parsing input file...')
    parse_mode = 0
    firmware_cmd = []
    parameter_cmd = []
    script_cmd = []
    with open(input_filename, "r") as f:
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
        ser.timeout = 3
        if en_autobaudrate == 1:
            print('In sbsl mode, auto baudrate configuration...')
            msg = b'\x00\x6c'
            ser.write(msg)
            ans = ser.read()
            if (ans != b'\x5d'):
                print('SBSL auto baudrate fail...')
                print('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                sys.exit(1)

        # read SBSL status (Flash erase)
        print('Get sbsl status & id, flash erasing...')
        msg = b'\xa0\x10\x00\x00\x27'
        ser.write(msg)
        ans = ser.read(42)
        #check timeout, Status byte and parse the return value (SBSL id)
        fdtc = ans[21]
        sbsl_id = ans[24:40]
        print('FDTC : {}'.format(fdtc))
        print('SBSL id : {}'.format(sbsl_id.hex()))

        # firmware uploading to device
        print('Firmware uploading...')
        msg_count = 1
        msg_count_max = len(firmware_cmd)
        for msg in firmware_cmd:
            ser.write(msg)
            if msg[1] == 0x20:
                ans = ser.read(3)
                if ans[-2:] != b'\x90\x00':
                    print('Error firmware uploading...')
                    print('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                    sys.exit(1)
            elif msg[1] == 0x21:
                ans = ser.read(3) ###
                if ans[-2:] != b'\x90\x00':
                    print('Error firmware uploading...')
                    print('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                    sys.exit(1)
            else:
                pass
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" % ('='*int((msg_count/msg_count_max)*20), (msg_count/msg_count_max)*100))
            sys.stdout.flush()
            msg_count += 1
            time.sleep(.100)
        uploading_state = 2
        en_autobaudrate = 1
        print('')
        # entering config mode
        time.sleep(.500)

    if uploading_state == 2:
        # run autobaudrate
        if en_autobaudrate == 1:
            print('In config mode, auto baudrate configuration...')
            msg = b'\x00\x6c'
            ser.write(msg)
            ans = ser.read()
            if (ans != b'\xcd'):
                print('Config mode auto baudrate fail...')
                print('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                sys.exit(1)

        # parameter uploading to device
        print('Parameter uploading...')
        for msg in parameter_cmd:
            ser.write(msg)
            if msg[1] == 0x20:
                ans = ser.read(3)
            elif msg[1] == 0x21:
                ans = ser.read(2)
            elif msg[1] == 0x22:
                ans = ser.read(2)
            else:
                pass
            if ans[-2:] != b'\x90\x00':
                print('Error parameter uploading...')
                print('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                sys.exit(1)
            time.sleep(.100)

        # script uploading to device
        print('Script uploading...')
        for msg in script_cmd:
            ser.write(msg)
            if msg[1] == 0x20:
                ans = ser.read(3)
            elif msg[1] == 0x21:
                ans = ser.read(2)
            elif msg[1] == 0x22:
                ans = ser.read(2)
            else:
                pass
            if ans[-2:] != b'\x90\x00':
                print('Error script uploading...')
                print('msg: {} --> {}'.format(msg.hex(), ans.hex()))
                sys.exit(1)
            time.sleep(.100)

        # change boot mode to application (0xAD)
        print('Switching to application mode...')
        msg = b'\xa0\x18\xad\x52\x00'
        ser.write(msg)
        ans = ser.read(3)
        if ans != b'\x90\x00\xff':
            print('Fail to switch to Application mode...')
            print('msg: {} --> {}'.format(msg.hex(), ans.hex()))
            sys.exit(1)
        print('Finish uploading...')
        print('Success')
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    print('(c)2020 Marklin')
    sys.exit(0)

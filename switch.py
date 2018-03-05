################################################################################
#	File : switch.py
#	Purpose : Base class for networking switches
#	Author : Jonathan Weatherspoon
#	Date : Mar 05, 2018
################################################################################

import serial
import time

import switchcode
import switchreader
import switchwriter

################################################################################
#	Class : Switch
#	Purpose : Base class for switch object. Handles generic read / write
################################################################################


class Switch(object):
    '''
    Switch: A base class for modeling switch configuration interactions through python.
    '''

    def __init__(self, port, baud):
        self.__port = port
        self.__baud = baud

        self.__serial = None
        self.__reader = None
        self.__writer = None
        self.__code = None

    def connect(self):
        ''' 
        Purpose : Initialize the serial connection to a switch 
        Parameters : 
            None
        Returns: True if connection successful, False otherwise
        '''
        try:
            self.__serial = serial.Serial(
                port=self.__port, baudrate=self.__baud)
            self.__writer = switchwriter.SwitchWriter(self.__serial)
            self.__reader = switchreader.SwitchReader(self.__serial)
            return True
        except Exception:
            print "Failed to connect to switch over port", self.__port
            return False

    def sendCommand(self, command, enter=True):
        ''' 
        Purpose : Send a command over the configured serial port
        Parameters : 
            command: The command as a string
            enter: Determines if a carriage return should be sent (default: True)
        Returns: None
        '''
        if self.__writer is not None:
            self.__writer.cmd(command, enter)

    def enter(self, repeat=1, delay=0.1):
        ''' 
        Purpose : Send a carriage return to the switch
        Parameters : 
            repeat: The number of times to send the command
            delay: The time to wait before sending another command
        Returns: None
        '''
        self.__specialCmd("<Enter>", "\r", repeat, delay)

    def space(self, repeat=1, delay=0.1):
        ''' 
        Purpose : Send a space to the switch
        Parameters : 
            repeat: The number of times to send the command
            delay: The time to wait before sending another command
        Returns: None
        '''
        self.__specialCmd("<Space>", " ", repeat, delay)

    def tab(self, repeat=1, delay=0.1):
        ''' 
        Purpose : Send a tab to the switch
        Parameters : 
            repeat: The number of times to send the command
            delay: The time to wait before sending another command
        Returns: None
        '''
        self.__specialCmd("<Tab", "\t", repeat, delay)

    def __specialCmd(self, label, cmd, repeat, delay):
        if self.__writer is not None:
            for i in range(repeat):
                print label
                self.__writer.cmd(cmd, True)
                if repeat > 1:
                    time.sleep(delay)

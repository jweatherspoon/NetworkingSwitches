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

################################################################################
#	Class : Switch 
#	Purpose : Base class for switch object. Handles generic read / write
################################################################################


class Switch(object):
    '''
    Switch: A base class for modeling switch configuration interactions through python.
    '''

    def __init__(self, port, baud):
        ''' 
        Purpose : Initialize a Switch object
        Parameters : 
            port: The serial port to communicate over (string)
            baud: The baud rate for the serial communication (int)
        Returns: None
        ''' 
        self.__port = port
        self.__baud = baud

        self.__serial = None
        self.__reader = None
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
            self.__reader = switchreader.SwitchReader(self.__serial)
            self.__reader.start()
            return True
        except Exception as ex:
            print ex.message
            print "Failed to connect to switch over port", self.__port
            return False

    def setCode(self, modelName, codeFile):
        ''' 
        Purpose : Initialize the switches SwitchCode object for use in configuration
        Parameters : 
            modelName: The model name of the switch 
            codeFile: The name of the file which contains the code filenames.
                      Format: <lowercase model name> <boot code> <primary code> <poe firmware (optional)>
        Returns: None
        ''' 
        self.__code = switchcode.SwitchCode(modelName.lower(), codeFile)

    def sendCommand(self, command, enter=True):
        ''' 
        Purpose : Send a command over the configured serial port
        Parameters : 
            command: The command as a string
            enter: Determines if a carriage return should be sent (default: True)
        Returns: None
        '''
        if self.__serial.isOpen():
            self.__serial.write(command)
            if enter:
                self.__serial.write('\r')

    def readline(self):
        ''' 
        Purpose : Read a line from the switch
        Parameters : 
            None
        Returns: A string containing the output of the switch. None if there is no output
        ''' 
        return self.__reader.readline()

    def waitForOutput(self, out, exact=False):
        ''' 
        Purpose : Wait for the switch to send a certain output to the serial port
        Parameters : 
            out: The output to search for
            exact: Determines if the out should be an exact match (Default: False)
        Returns: None
        ''' 
        # Clear the queue
        self.__reader.clearQueue()
        while True:
            content = self.__reader.readline()

            if content is None:
                continue

            if exact and out == content:
                break 
            elif out.lower() in content.lower():
                break 

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

    def ctrlC(self, repeat=1, delay=0.1):
        ''' 
        Purpose : Send a control+C command to the switch
        Parameters : 
            repeat: The number of times to send the command
            delay: The time to wait before sending another command
        Returns: None
        ''' 
        self.__specialCmd("<Control-C>", "\x03", repeat, delay)

    def reload(self):
        ''' 
        Purpose : Reload a switch
        Parameters : 
            None
        Returns: None
        ''' 
        self.sendCommand("reload")
        self.sendCommand('y', False)
        self.sendCommand('y', False)

    def close(self):
        ''' 
        Purpose : Close a serial connection to a switch
        Parameters : 
            None
        Returns: None
        ''' 
        if self.__serial.isOpen():
            self.__reader.stop()
            self.__serial.close() 
            # self.__reader.join()

    def getBoot(self):
        ''' 
        Purpose : Get the filename for the boot code
        Parameters : 
            None
        Returns: String containing the filename or None
        ''' 
        return self.__code.getBoot()
    
    def getPri(self):
        ''' 
        Purpose : Get the filename for the primary code
        Parameters : 
            None
        Returns: String containing the filename or None
        '''
        return self.__code.getPri()

    def getPOE(self):
        ''' 
        Purpose : Get the filename for the POE firmware
        Parameters : 
            None
        Returns: String containing the filename or None
        '''
        return self.__code.getPOE()

    def __specialCmd(self, label, cmd, repeat, delay):
        if self.__serial is not None:
            for i in range(repeat):
                print label
                self.sendCommand(cmd)
                if repeat > 1:
                    time.sleep(delay)

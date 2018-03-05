################################################################################
#	File : switchwriter.py
#	Purpose : Handles asynchronous write operations to a switch over serial
#	Author : Jonathan Weatherspoon
#	Date : March 05, 2018
################################################################################

import threading 
from Queue import Queue 

class SwitchWriter(threading.Thread):
    '''
    Handles asynchronous writing to a switch
    '''
    def __init__(self, serialObj):
        ''' 
        Purpose : Initialize a SwitchWriter object
        Parameters : 
            serialObj: The serial connection to write to
        Returns: None
        ''' 
        super(SwitchWriter, self).__init__(self)
        self.__serial = serialObj
        self.__cmdQueue = Queue()

    def run(self):
        ''' 
        Purpose : Continuously write to the switch when commands are available
        Parameters : 
            None
        Returns: None
        ''' 
        while self.__serial.isOpen():
            if not self.__cmdQueue.empty():
                command = self.__cmdQueue.get()
                self.__serial.write(command) 

    def cmd(self, command, enter):
        ''' 
        Purpose : Add a command to the queue
        Parameters : 
            command: The command to write to the switch
            enter: True if a carriage return should be sent as well 
        Returns: None
        ''' 
        self.__cmdQueue.put(command)
        if enter:
            self.__cmdQueue.put('\r')
    
################################################################################
#	File : switchreader.py
#	Purpose : Handles asynchronous reading from a switch over serial port
#	Author : Jonathan Weatherspoon
#	Date : March 05, 2018
################################################################################

import threading
from Queue import Queue

class SwitchReader(threading.Thread):
    '''
    Handles asynchronous read operations on a switch over a serial connection
    '''
    def __init__(self, serialObj):
        ''' 
        Purpose : Initialize a SwitchReader object
        Parameters : 
            serialObj: The serial connection to read from 
        Returns: None
        ''' 
        super(SwitchReader, self).__init__()
        self.__serial = serialObj 
        self.__outQueue = Queue()
        self.__stopCondition = threading.Event()

        self.setDaemon(True)

    def run(self):
        ''' 
        Purpose : Read all output from a switch and put it into a queue for retrieval
        Parameters : 
            None
        Returns: None
        ''' 
        while not self.stopped():
            #Try reading a line and storing it in the outQueue
            output = self.__serial.readline() 
            if output != "":
                print output 
                self.__outQueue.put(output) 
        print "stopping..."

    def readline(self):
        ''' 
        Purpose : Read a line from the reader queue
        Parameters : 
            None
        Returns: A string containing the last unread line, or None if the queue is empty
        ''' 
        if not self.__outQueue.empty():
            return self.__outQueue.get() 
        else: 
            return None

    def clearQueue(self):
        while not self.__outQueue.empty():
            self.__outQueue.get()

    def stop(self):
        self.__stopCondition.set()

    def stopped(self):
        return self.__stopCondition.isSet()
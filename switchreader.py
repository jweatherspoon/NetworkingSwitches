################################################################################
#	File : switchreader.py
#	Purpose : Handles asynchronous reading from a switch over serial port
#	Author : Jonathan Weatherspoon
#	Date : March 05, 2018
################################################################################

class SwitchReader(object):
    '''
    Handles asynchronous read operations on a switch over a serial connection
    '''
    def __init__(self, serialObj):
        self.__serial = serialObj 

    
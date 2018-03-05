################################################################################
#	File : switchwriter.py
#	Purpose : Handles asynchronous write operations to a switch over serial
#	Author : Jonathan Weatherspoon
#	Date : March 05, 2018
################################################################################

class SwitchWriter(object):
    def __init__(self, serialObj):
        self.__serial = serialObj

    def cmd(self, command, enter):
        pass
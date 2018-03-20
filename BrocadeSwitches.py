################################################################################
#	File : BrocadeSwitches.py
#	Purpose : Contains non-generic brocade switch objects
#	Author : Jonathan Weatherspoon
#	Date : March 19, 2018
################################################################################

from brocade import Brocade
import time

class ICX7150(Brocade):
    '''
    Models an ICX7150 switch
    '''
    def __init__(self, port, baud, codefile):
        super(ICX7150, self).__init__(port, baud)
        self.setCode("ICX7150", codefile)

    def installPoEFirmware(self):
        ''' 
        Purpose : Install PoE firmware on a brocade switch (may move to generic class later)
        Parameters : 
            None
        Returns: None
        ''' 
        poeFile = self.getPOE()
        if poeFile is not None:
            cmd = "inline power install-firmware all tftp 192.168.1.2 {0}".format(poeFile)
            self.sendCommand(cmd)
            time.sleep(0.5)
            self.waitForOutput("")
        

class ICX7250(Brocade):
    '''
    Models an ICX7250 switch
    '''
    def __init__(self, port, baud, codefile):
        super(ICX7250, self).__init__(port, baud)
        self.setCode("ICX7250", codefile)
        

class ICX6450(Brocade):
    '''
    Models an ICX6450 switch
    '''
    def __init__(self, port, baud, codefile):
        super(ICX6450, self).__init__(port, baud)
        self.setCode("ICX6450", codefile)
        

class ICX7450(Brocade):
    '''
    Models an ICX7450 switch
    '''
    def __init__(self, port, baud, codefile):
        super(ICX7450, self).__init__(port, baud)
        self.setCode("ICX7450", codefile)


class FWS(Brocade):
    '''
    Models a FWS switch
    '''
    def __init__(self, port, baud, codefile):
        super(FWS, self).__init__(port, baud)
        self.setCode("FWS", codefile)
        

class FCX(Brocade):
    '''
    Models a FCX switch
    '''
    def __init__(self, port, baud, codefile):
        super(FCX, self).__init__(port, baud)
        self.setCode("FCX", codefile)

################################################################################
#	File : brocade.py
#	Purpose : Models generic brocade / ruckus switches
#	Author : Jonathan Weatherspoon
#	Date : March 16, 2018  
################################################################################

from switch import Switch 

################################################################################
#	Class : Brocade
#	Purpose : Models a generic Brocade / Ruckus switch
################################################################################
class Brocade(Switch):
    def __init__(self, port, baud):
        # Call the base class constructor
        super(Brocade, self).__init__( port, baud)

    def handleBoot(self):
        self.waitForOutput("'b' to stop at")
        self.sendCommand('b', False)
        self.sendCommand("no password")
        self.sendCommand("boot system flash primary")
        self.waitForOutput("initialization is done")
        self.enter()

    def wipe(self):
        flag = True 
        while(flag):
            self.handleBoot()
            self.enter()
            self.sendCommand("enable")
            self.enter()

            snFlag = True
            while snFlag:
                snFlag = False

                switchName = self.readline()
                if switchName is not None:
                    if "[MEMBER]" in switchName:
                        # Unconfigure stack member, reload, then wipe again
                        self.sendCommand("stack unconfigure me")
                    else:
                        # Wipe the startup and reload 
                        self.sendCommand("erase start")
                        flag = False 
                    self.reload()
                else:
                    print "Got None as Switch Name. Trying again..."
                    snFlag = True

        

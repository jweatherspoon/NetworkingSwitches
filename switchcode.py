################################################################################
#	File : switchcode.py
#	Purpose : Contains the code used for default switch configuration
#	Author : Jonathan Weatherspoon
#	Date : March 05, 2018
################################################################################

class SwitchCode(object):
    '''
    Container object for storing code filenames for switch configuration.
    '''
    def __init__(self, modelName, codeFile):
        ''' 
        Purpose : Initialize a SwitchCode object
        Parameters : 
            modelName: The model name of a switch. Used to parse codeFile
            codeFile: Name of the file that stores code filenames for given 
                      switches. Format should be:
                          <lowercase model name> <boot code> <primary code> <poe firmware (optional)>
        Returns: None
        ''' 
        self.__poe = None 
        self.__pri = None 
        self.__boot = None 

        self.__model = modelName
        self.__initCode(codeFile)

    def getPri(self):
        ''' 
        Purpose : Get the primary / secondary code file for this switch
        Parameters : 
            None
        Returns: A string containing the filename of the primary flash. None if 
                 it could not be found.
        ''' 
        return self.__pri 
    
    def getBoot(self):
        ''' 
        Purpose : Get the boot code file for this switch
        Parameters : 
            None
        Returns: A string containing the filename of the boot flash. None if 
                 it could not be found.
        '''
        return self.__boot 

    def getPOE(self):
        ''' 
        Purpose : Get the poe firmware code file for this switch
        Parameters : 
            None
        Returns: A string containing the filename of the firmware flash. None if 
                 it could not be found.
        '''
        return self.__poe 

    def __initCode(self, codeFN):
        try:
            fin = open(codeFN)
            for line in fin:
                #Try to find this model in the code file 
                tokens = line.split()
                tokens = [x.strip() for x in tokens]

                if len(tokens) > 2:
                    self.__boot = tokens[1]
                    self.__pri = tokens[2]
                    if len(tokens) > 3:
                        self.__poe = tokens[3]
        except:
            print "Cannot find", self.__model, "in codefile", codeFN 

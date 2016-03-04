'''
CMPUT291, Project 1

Copyright 2016, Zhaorui CHEN, Nicholas LI, Jiaxuan YUE

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

class Connection:
    def __init__(self):
        # FROM Kriti
        # get username
	user = input("Username [%s]: " % getpass.getuser())
	if not user:
    		user=getpass.getuser()
	
	# get password
	pw = getpass.getpass()

	# The URL we are connnecting to
	conString=''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'
        self.connection = cx_Oracle.connect(conString)

    def disconnect(self):
        self.connection.close()

    def executeStmt(self, stmt):
        curs = self.connection.cursor()
        curs.execute(stmt)
        curs.close()
    
    def fetchResult(self, query):
        curs = self.connection.cursor()
        rows = curs.fetchall() #list??
        curs.close()

    def createInsertion(self, table, data):
        pass

    def createQuery(self, columns, tables, conditions):
        pass

    def checkUnique(self, table, data):
        pass

class application:
    def __init__(self):
        self.connection =  Connection()

    def selectMenu(self):
        pass

    def checkFormat(self, value, inputType, misc):
        '''
        helper function to validate the input
        '''
        if inputType=='char': # validate the input for CHAR
            while True:
                if len(value)>=misc:
                    print('Too looooooooooong')
                    value = input('Please re-input: ').strip()
                else: 
                    return value
        elif inputType=='integer': # validate the input for INTEGER
            while True:
                if not value.isdigit():
                    value = input('Please re-input').strip()
                else:
                    return value
        elif inputType=='number': # validate the input for NUMBER
            while True:
                # check if is a float
                try:
                    val = float(value)
                except ValueError:
                    print('Not Float')
                    value = input('Please re-input: ').strip()
                    continue
                    
                # check if has the correct length
                if len(value)>misc[0]+1:
                    print('Too looooooooooong')
                    value = input('Please re-input: ').strip()
                    continue

                # check if has the correct decimal length
                if not value[-(misc[1]+1)]=='.':
                    value = input('Please re-input: ').strip()
                    continue
                return value
        elif inputType=='date': #validate the input for DATE
            pass
        ####################################################

    def newVehicleRegistration(self):
        '''
        First program.
        '''
        inputVal = input('Please enter the serial number: ').strip()
        serialNo = checkFormat(inputVal, 'char', 15)
        if isSerialNoExist(serialNo):
            print('Vehicle already exist.')
            # need re-input?

        inputVal = input('Please enter SIN of the owner').strip()
        sin = checkFormat(inputVal, 'char', 15)
        if not isSinExist(sin):
            print('Sin NOT VALID.')
            newPeopleRegistration(sin)

        inputVal = input('Please enter the maker of the vehicle: ').strip()
        maker = checkFormat(inputVal, 'char', 20)

        inputVal = input('Please enter the model of the vehicle: ').strip()
        model = checkFormat(inputVal, 'char', 20)

        inputVal = input('Please enter the year of production of the vehicle: ').strip()
        year = checkFormat(inputVal, 'date', 0)

        inputVal = input('Please enter the color of the vehicle: ').strip()
        color = checkFormat(inputVal, 'char', 10)
        
        

    def newPeopleRegistration(self, sin):
        '''
        helper function. Only triggered when specific sin
        is not found in the database
        '''
        pass

    def isSerialNoExist(self, serialNo):
        return True

    def isSinExist(self, sin):
        return True

    def hasLicence(self, sin):
        return True

    def newDriverRegistration(self):
        pass

    def autoTransaction(self):
        pass

    def violationRecord(self):
        pass

if __name__ == '__main__':
    app = application()
    app.selectMenu()

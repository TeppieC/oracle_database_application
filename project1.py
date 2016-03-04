'''
Project 1

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
import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it

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
        return rows

    def createInsertion(self, table, data):
        pass

    def createDeletion(self, table, data):
        pass

    def createQuery(self, columns, tables, conditions):
        '''
        Args:
        columns(str)
        tables(str)
        conditions(str)

        return:
        (str): sql query statement
        '''
        return 'SELECT'+columns+'FROM'+tables+'WHERE'+conditions

    def ifExist(self, table, keyAttr, value):
        '''
        check if the tuple already existed in the table

        Args:
        table(str)
        keyAttr(str):the name of the primary key attribute
        value(str): the value of query key attribute
        
        Return: Bool
        '''
        query = createQuery(keyAttr, table, keyAttr+'='+value)
        if self.fetchResult(query)==[]:
            return False
        else:
            return True

    def checkUnique(self, table, data):
        pass

class application:
    def __init__(self):
        self.connection =  Connection()

    def selectMenu(self):
        selection = 0
        while not selection:
            print('#'*80)
            print('Please select from the following programs: ')
            print('1. New Vehicle Registration')
            print('2. Auto Transaction')
            print('3. Driver Licence Registration')
            print('4. Violation Record')
            print('5. Search Engine')
            print('[Q] Quit')
            inputStr = input('Your choice: ')
            selection = {
                '1': 1,
                '2': 2,
                '3': 3,
                '4': 4,
                '5': 5,
                'Q': 'Q'
            }.get(inputStr,0)
            #print('Your choice is '+inputStr)
            if selection==0:
                print('Your input is not valid, please try again')
        return selection

    def end(self):
        print('See you')
        # close cursor if needed
        self.connection.disconnect()
        sys.exit()

    def main(self):
        selection = 0
        while not selection:
            selection = self.selectMenu()
            if selection==1:
                selection = self.newVehicleRegistration() #if finished, return  
            elif selection==2:
                selection = self.autoTransaction()# if quit, return 'Q'
            elif selection==3:
                selection = self.driverLicenceRegistration()
            elif selection==4:
                selection = self.violationRecord()
            elif selection==5:
                selection = self.searchEngine()
            elif selection=='Q':
                self.end()
        self.end()
        

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
        serialNo = self.checkFormat(inputVal, 'char', 15)
        if self.isSerialNoExist(serialNo):
            print('Vehicle already exist.')
            # need re-input?

        inputVal = input('Please enter SIN of the owner').strip()
        sin = self.checkFormat(inputVal, 'char', 15)
        if not self.isSinExist(sin):
            print('Sin NOT VALID.')
            #newPeopleRegistration(sin)

        inputVal = input('Please enter the maker of the vehicle: ').strip()
        maker = self.checkFormat(inputVal, 'char', 20)

        inputVal = input('Please enter the model of the vehicle: ').strip()
        model = self.checkFormat(inputVal, 'char', 20)

        inputVal = input('Please enter the year of production of the vehicle: ').strip()
        year = self.checkFormat(inputVal, 'date', 0)

        inputVal = input('Please enter the color of the vehicle: ').strip()
        color = self.checkFormat(inputVal, 'char', 10)

        ###################

        if input('Re-select the program?[y/n]')=='y':
            return 0
        
        

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
    app.main()

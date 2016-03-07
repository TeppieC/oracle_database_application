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
        check if the key is already existed in the table

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
                selection = self.newVehicleRegistration() # return 0 to re-select
            elif selection==2:
                selection = self.autoTransaction()
            elif selection==3:
                selection = self.driverLicenceRegistration()
            elif selection==4:
                selection = self.violationRecord()
            elif selection==5:
                selection = self.searchEngine()
            elif selection=='Q':
                self.end()
        self.end() #can remove?...
        

    def checkFormat(self, value, inputType, misc):
        '''
        helper function to validate the input
        
        Args:
        value(str): the input string
        inputType(str): the sql type which the input string should be cast into
        misc(list/int): the list of miscellaneous properties, eg. length of the integer

        Return:
        the casted input which is in the correct type
        '''
        value = value.strip()
        while value='': #check if the input is blank
            print('Oops, you are not entering anything...')
            value = input('Please re-input: ').strip()

        if inputType=='char': # validate the input for CHAR
            while True:
                if len(value)>=misc:
                    print('Input is too long. Input should have %d characters' % misc)
                    value = input('Please re-input: ').strip()
                else: 
                    return value
        elif inputType=='integer': # validate the input for INTEGER
            while True:
                if not value.isdigit():
                    print('Input is not a numeric type')
                    value = input('Please re-input').strip()
                else:
                    return value
        elif inputType=='number': # validate the input for NUMBER
            while True:
                # check if is a float
                # NUMBER(a,b)
                # misc[0]:a, misc[1]:b
                try:
                    val = float(value)
                except ValueError:
                    print('Input is not a numeric type')
                    value = input('Please re-input: ').strip()
                    continue
                    
                # check if has the correct length
                if len(value)>misc[0]+1:
                    print('Input is too long. Input should have %d digits(including decimal)' % misc[0])
                    value = input('Please re-input: ').strip()
                    continue

                # check if has the correct decimal length
                if not value[-(misc[1]+1)]=='.':
                    print('Input should have %d decimal digits' % misc[1])
                    value = input('Please re-input: ').strip()
                    continue
                return value
        elif inputType=='date': #validate the input for DATE
            while True: # proper format: DD-MM-YYYY
                if not len(value)==10:
                    # if is not in the correct length
                    print('Your input should follow "DD-MM-YYYY"')
                    value = input('Please re-input: ').strip()
                    continue
                if value[2]!='-' or value[5]!='-':
                    # if is not using '-' to connect date, month and years
                    print('Your input should follow "DD-MM-YYYY"')
                    value = input('Please re-input: ').strip()
                    continue
                if not (value[:2].isdigit() and value[3:5].isdigit() and value[6:].isdigit()):
                    # if DD, MM or YYYY is not expressed in integers
                    print('Your input should follow "DD-MM-YYYY"')
                    value = input('Please re-input: ').strip()
                    continue
                if int(value[:2])<1 or int(value[3:5])<1 \
                        or int(value[:2])>31 or int(value[3:5])>12:
                    # if DD or MM is out of range
                    print('Date or month is out of range')
                    value = input('Please re-input: ').strip()
                    continue
                else:
                    # convert 'MM' to characters
                    month = {
                        '01': 'JUN',
                        '02': 'FEB',
                        '03': 'MAR',
                        '04': 'APR',
                        '05': 'MAY',
                        '06': 'JUN',
                        '07': 'JUL',
                        '08': 'AUG',
                        '09': 'SEP',
                        '10': 'OCT',
                        '11': 'NOV',
                        '12': 'DEC',
                        }.get(value[3:5])
                    return ('%s-%s-%s'%(value[:2],month, value[6:])) # may cause bug...

    def checkReference(self, table, keyAttr, value, inputType, misc):
        '''
        helper function to validate input and check if the reference key is valid
        '''
        while not self.connection.ifExist(table, keyAttr, value):
            print('The key "%s" is not exist in the reference table "%s"'%(value, table))
            value = input('Please re-input: ').strip()
        return value

    def newVehicleRegistration(self):
        '''
        First program.
        '''
        inputVal = input('Please enter the serial number: ')
        serialNo = self.checkFormat(inputVal, 'char', 15)
        while self.ifSerialNumExist(serialNo):
            print('Vehicle already exist.')
            inputVal = input('Please enter another serial number: ')
            serialNo = self.checkFormat(inputVal, 'char', 15)

        inputVal = input('Please enter SIN of the owner')
        sin = self.checkFormat(inputVal, 'char', 15)
        if not self.ifSinExist(sin):
            print('Sin NOT VALID.')
            while
            #newPeopleRegistration(sin)

        inputVal = input('Please enter the maker of the vehicle: ')
        maker = self.checkFormat(inputVal, 'char', 20)

        inputVal = input('Please enter the model of the vehicle: ')
        model = self.checkFormat(inputVal, 'char', 20)

        inputVal = input('Please enter the year of production of the vehicle: ')
        year = self.checkFormat(inputVal, 'date', 0)

        inputVal = input('Please enter the color of the vehicle: ')
        color = self.checkFormat(inputVal, 'char', 10)

        inputVal = input('Please enter the type id of the vehicle: ')
        typeId = self.checkReference('vehicle_type','type_id',inputVal, 'number', 1)
        
        #insertion = self.connection.createInsertion()
        #self.connection.executeStmt(insertion)
        print('Succeed')

        if input('Re-select the program?[y/n]')=='y':
            return 0 # select other programs
        else:
            return 'Q' # quit


    def newPeopleRegistration(self, sin):
        '''
        helper function. Only triggered when specific sin
        is not found in the database
        '''
        pass

    def ifSerialNumExist(self, serialNo):
        return self.connection.ifExist('vehicle','serial_no',serialNo)

    def ifSinExist(self, sin):
        return self.connection.ifExist('people','sin',sin)

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

'''
Project 1

Copyright 2016, Zhaorui CHEN(Teppie), Nicholas LI, Jiaxuan YUE

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
import time

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
        self.connection.commit()
        curs.close()
    
    def fetchResult(self, query):
        curs = self.connection.cursor()
        curs.execute(query)
        rows = curs.fetchall() #list??
        curs.close()
        return rows

    def createInsertion(self, table, *args):
        '''
        Return the sql INSERT statement in string
        '''
        insertion = 'INSERT INTO %s VALUES (' % table
        for i in range(0, len(args)-1):
            insertion += args[i]
            insertion += ', '

        insertion+= args[-1]
        insertion+=')'

        return insertion

    def createDeletion(self, table, keyAttr, value):
        return 'DELETE FROM '+table+' WHERE '+keyAttr+'='+value+';'

    def createQuery(self, columns, tables, conditions):
        '''
        Args:
        columns(str)
        tables(str)
        conditions(str)

        return:
        (str): sql query statement
        '''
        return 'SELECT '+columns+' FROM '+tables+' WHERE '+conditions

    def ifExist(self, table, keyAttr, value):
        '''
        check if the key is already existed in the table

        Args:
        table(str)
        keyAttr(str):the name of the primary key attribute
        value(str): the value of query key attribute
        
        Return: Bool
        '''
        query = self.createQuery(keyAttr, table, keyAttr+'='+value)
        print(query)
            #############################################
        if not self.fetchResult(query)==[]:
            return True
        else:
            return False
        #except cx_Oracle.DatabaseError:
        #    return False

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
        (str) the validated input
        '''
        value = value.strip()
        while value=='': #check if the input is blank
            print('Oops, you are not entering anything...')
            value = input('Please re-input: ').strip()

        if inputType=='char': # validate the input for CHAR
            while True:
                if len(value)>=misc:
                    print('Input is too long. Input should have %d characters' % misc)
                    value = input('Please re-input: ').strip()
                else: 
                    return '\''+value+'\''
        elif inputType=='integer': # validate the input for INTEGER
            while True:
                if not value.isdigit():
                    print('Input is not a numeric type')
                    value = input('Please re-input: ').strip()
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

                # if the required decimal length is 0
                if misc[1]==0:
                    while len(value)!=misc[0] or not value.isdigit():
                        print('Input is not valid')
                        value = input('Please re-input: ').strip()
                    return value
                    
                # check if has the correct length
                if len(value)>misc[0]+1:
                    print('Input is too long. Input should have %d digits(including decimal)' % misc[0])
                    value = input('Please re-input: ').strip()
                    continue

                # check if has the correct decimal length
                if not value[-(misc[1]+1)]=='.':
                    print('Input should have length of %d, and %d decimal digits' % (misc[0],misc[1]))
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
            value = self.checkFormat(value, inputType, misc)
        return value

    def newVehicleRegistration(self):
        '''
        First program.
        '''
        print('#'*80)
        inputVal = input('Please enter the serial number: ')
        serialNo = self.checkFormat(inputVal, 'char', 15) #should accept letters
        while self.ifSerialNumExist(serialNo):
            print('Vehicle already exist.')
            inputVal = input('Please enter another serial number: ')
            serialNo = self.checkFormat(inputVal, 'char', 15)

        inputVal = input('Please enter SIN of the owner: ')
        sin = self.checkFormat(inputVal, 'char', 15)# should accept letters
        while not self.ifSinExist(sin):
            print('Sin NOT VALID.')
            check = 0
            while check!='1' and check!='2':
                check = input('Re-input sin [1] OR register this person to database [2]? ').strip()
            if check=='1':
                inputVal = input('Please enter SIN of the owner: ')
                sin = self.checkFormat(inputVal, 'char', 15)
            else:
                self.newPeopleRegistration(sin) ############

        inputVal = input('Please enter the maker of the vehicle: ')
        maker = self.checkFormat(inputVal, 'char', 20)

        inputVal = input('Please enter the model of the vehicle: ')
        model = self.checkFormat(inputVal, 'char', 20)

        inputVal = input('Please enter the year of production of the vehicle: ')
        year = self.checkFormat(inputVal, 'number', [4,0])

        inputVal = input('Please enter the color of the vehicle: ')
        color = self.checkFormat(inputVal, 'char', 10)

        inputVal = input('Please enter the type id of the vehicle: ')
        typeId = self.checkReference('vehicle_type','type_id',inputVal, 'integer', 1)
        
        insertion = self.connection.createInsertion('vehicle', serialNo, maker,\
                                                    model, year, color, typeId)
        self.connection.executeStmt(insertion)
        insertion = self.connection.createInsertion('owner', sin, serialNo, "'y'")
        self.connection.executeStmt(insertion)

        print('Succeed!!!!!!!')

        if input('Re-select the program?[y/n]')=='y':
            return 0 # select other programs
        else:
            return 'Q' # quit


    def newPeopleRegistration(self, sin):
        '''
        helper function. Only triggered when specific sin
        is not found in the database
        '''
        inputVal = input('Please enter the name of this person: ')
        name = self.checkFormat(inputVal, 'char', 40)

        inputVal = input('Please enter the height of this person: ')
        height = self.checkFormat(inputVal, 'number', [5,2])

        inputVal = input('Please enter the weight of this person: ')
        weight = self.checkFormat(inputVal, 'number', [5,2])

        inputVal = input('Please enter the eye color of this person: ')
        eyeColor = self.checkFormat(inputVal, 'char', 10)

        inputVal = input('Please enter the hair color of this person: ')
        hairColor = self.checkFormat(inputVal, 'char', 10)
        
        inputVal = input('Please enter the address of this person: ')
        addr = self.checkFormat(inputVal, 'char', 50)

        gender = input('Please enter the gender of this person[m/f]: ')
        while self.isGenderCorrect(gender):
            print('Input not correct. Please use "m" or "f" for male or female')
            gender = input('Please re-input[m/f]: ')
            
        inputVal = input('Please enter the birthday[DD-MM-YYYY]:')
        birthday = self.checkFormat(inputVal, 'date', 0) ####

        insertion = self.connection.createInsertion('people',\
                                                        sin, name, height, weight,\
                                                        eyeColor, hairColor, addr,\
                                                        gender, birthday)
        self.connection.executeStmt(insertion)
        print('New people has been successfully registered')
        return

    def isGenderCorrect(self, gender):
        return gender=='m' or gender=='f' or gender=='M' or gender=='F'

    def isPrimaryOwnerCorrect(self, pri):
        return pri=='n' or pri=='y' or pri=='Y' or pri=='N'

    def ifTransactionIdExist(self, tId):
        return self.connection.ifExist('auto_sale','t_id',tId)

    def ifTicketNoExist(self, tNo):
        return self.connection.ifExist('ticket','ticket_no', tNo)

    def ifSerialNumExist(self, serialNo):
        return self.connection.ifExist('vehicle','serial_no',serialNo)

    def ifSinExist(self, sin):
        return self.connection.ifExist('people','sin',sin)

#    def generateTransactionId(self):
#        # example: 420150904221533001
#        tId = '4'+time.strftime('%Y%m%d')+time.strftime('%H:%M:%S')
#        count = self.connection.executeStmt(\
#            self.connection.getCount('auto_sale', 'transaction_id', tId+'%'))
#        return '4'+time.strftime('%Y%m%d')+time.strftime('%H:%M:%S')

 #   def generateTicketNo(self, officer):
 #       return time.strftime('%Y%m%d')+seller+serialNo

    def getCurrentDate(self):
        day = time.strftime('%d')
        year = time.strftime('%Y')
        mon = time.strftime('%m')
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
                        }.get(mon)
        return day+'-'+month+'-'+year
        
    def newDriverRegistration(self):
        pass

    def autoTransaction(self):
        # need preventing input errors?
        inputVal = input('Please enter SIN of the seller: ')
        sId = self.checkReference('people', 'sin', inputVal, 'char', 15)

        inputVal = input('Please enter SIN of the buyer: ')
        bId = self.checkReference('people', 'sin', inputVal, 'char', 15)

        inputVal = input('Please enter the serial number: ')
        vId = self.checkReference('vehicle', 'serial_no', inputVal, 'char', 15)
        
        #generate the transaction id
        #tId = self.generateTransactionId(sId, vId)
        
        #input the transaction id
        tId = self.checkFormat(input('Please enter the transaction ID: '), 'integer',1)
        while self.ifTransactionIdExist(tId):
            print('Transaction ID already exist.')
            inputVal = input('Please enter another transaction ID: ')
            tId = self.checkFormat(inputVal, 'integer', 1)

        #get the date
        sDate = self.getCurrentDate()

        inputVal = input('Please enter the price of the transction: ')
        price = self.checkFormat(inputVal, 'integer', [9,2])
        
        insertion = self.connection.createInsertion('auto_sale', tId, \
                                                        sId, bId, vId, sDate, price)
        self.connection.executeStmt(insertion)

        deletion = self.connection.createDeletion('owner', \
                                                      '(owner_id, vehicle_id)', \
                                                      '(%s, %s)'%(sId, vId))
        self.connection.executeStmt(deletion)

        insertion = self.connection.createInsertion('owner', bId, vId, 'y')
        self.connection.executeStmt(insertion)

        print('Succeed')

        if input('Re-select the program?[y/n]')=='y':
            return 0 # select other programs
        else:
            return 'Q' # quit

    def violationRecord(self):
        print('#'*80)
        print('Welcome to violation record system.')

        # input the ticket number
        tNo = self.checkFormat(input('Please enter the ticket number: '), 'integer',1)
        while self.ifTicketNumerExist(tNo):
            print('Ticket number already exist.')
            inputVal = input('Please enter another ticket number: ')
            tNo = self.checkFormat(inputVal, 'integer', 1)

        inputVal = input('Please enter SIN of the officer: ')
        officerId = self.checkReference('people', 'sin', inputVal, 'char', 15)
        
        inputVal = input('Please enter SIN of the violator: ')
        violatorId = self.checkReference('people', 'sin', inputVal, 'char', 15)
        
        inputVal = input('Please enter the serial number of the vehicle: ')
        vId = self.checkReference('vehicle', 'serial_no', inputVal, 'char', 15)

        inputVal = input('Please enter the violation type: ')
        vType = self.checkReference('ticket_type', 'vtype', inputVal, 'char', 10)

        #get the date
        sDate = self.getCurrentDate()
        print('Violation date is at %s'%sDate)

        inputVal = input('Please enter the place: ')
        place = self.checkFormat(inputVal, 'char', 20)
        
        inputVal = input('Please enter the description: ')
        descr = self.checkFormat(inputVal, 'char', 1024)

        insertion = self.connection.createInsertion('owner', bId, vId, 'y')
        self.connection.executeStmt(insertion)

        print('Succeed')

        if input('Re-select the program?[y/n]')=='y':
            return 0 # select other programs
        else:
            return 'Q' # quit
        

    def searchEngine(self):
        pass

if __name__ == '__main__':
    app = application()
    app.main()

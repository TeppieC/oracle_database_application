#This file is for search engine testing.
#Please let Nicholas know if you want to modify it.

#1. use regular expression to determine what input it is or use manu to nevigate to target
#	sin: char(15),name:varchar(40),licence no:char(15),serial_no:char(15)
#2. if name input: List the name, licence_no, addr, birthday, driving class, driving_condition, and the expiring_data
#   if licence no input: List the name, licence_no, addr, birthday, driving class, driving_condition, the expiring_data, all violation records received by a person
#   if sin input: List all violation records received
#   if serial no input: Print out the vehicle_history, including the number of times that a vehicle has been changed hand, the average price, and the number of 
#   violations it has been involved
import re

namePattern = re.compile('[A-Z][a-z]{0,40}')
idPattern = re.compile('\w{15}')
select = 0
print('#'*80)
print('Welcome to violation record system.\nPlease select what you want to search for:')
while not select:
	print('1. Personal information')
	print('2. Violation record')
	print('3. Vehicle history')
	print('Q. Back to main menu')
	inputStr = input('Your choice: ')
	select = {'1': 1 , '2': 2 , '3': 3 , 'Q': 'Q'}.get(inputStr,0)
	if not select:
		select = 0
		print('Your input is invalid, please try again:')

if select == 1:
	while True:
		key = input('Please input a last name or a licence number:')  #Possible bug: name is with the same length of licence number(15)
		if namePattern.match(key): #here we dont use self.checkFormat since it has 'auto repair' in the function which will ask user to correct if input is invalid
			name = self.checkFormat(key,'char',40)
			#TODO
			break
		elif idPattern.match(key):
			licenceNo = self.checkFormat(key,'char','15')
			#TODO
			break
		else:
			print('The name/id you input is invalid, please try again:')
elif select == 2:
	key = input('Would you like to use SIN [1] or licence number [2] to check:')
	if key == 1:
		inputVal = input('Please input a SIN:')
		SIN = self.checkFormat(inputVal, 'char', 15)
		while not self.ifSinExist(SIN):
			inputVal = input('SIN not valid, please try again:')
			SIN = self.checkFormat(inputVal,'char',15)
		#TODO
	elif key == 2:
		inputVal = input('Please input a licence number:')
		licenceNo = self.checkFormat(inputVal, 'char', 15)
		while not self.ifLicenceNoExist(licenceNo):
			inputVal = input('Licence number not valid, please try again:')
			licenceNo = self.checkFormat(inputVal,'char',15)
		#TODO
elif select == 3:
	inputVal = input('Please input a serial number:')
	serialNo = self.checkFormat(inputVal,'char',15)
	while not self.ifSerialNoExist(serialNo):
		inputVal = input('Serial number not valid, please try again:')
		serialNo = self.checkFormat(inputVal,'char',15)
	#TODO
elif select == 'Q':
	self.end()













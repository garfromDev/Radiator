*** Settings ***
Documentation	doit être connecté au HW pour ce test
Library		testLibs/CurrentTemperatureLibrary.py

*** Test Cases ***
#just checking no exception raised, value returned depends from hw
Read actual temperature
  read temperature
  
# checks calculation from voltage through returned value in degree
Read simulated temperature
	simulate temperature	25
  read temperature
  temperature should be	25
  
many temperature  
	[Template]	check simulated temperature 
	3.2
	25
	39.1

*** Keywords ***
check simulated temperature
	[Arguments]    ${expected}
	simulate temperature	${expected}
	read temperature
	temperature should be 	${expected}

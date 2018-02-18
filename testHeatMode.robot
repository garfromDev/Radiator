*** Settings ***
Documentation	Essais de robot pour tester HeatMode
Library		testLibs/HeatModeLibrary.py

*** Test Cases ***
Confort Mode
	set mode to confort
	output plus should be	 LOW


*** Settings ***
Documentation	Essais de robot pour tester HeatMode
Library		testLibs/HeatModeLibrary.py

*** Test Cases ***
Confort Mode
	set mode to confort
	output plus should be	 LOW
	output minus should be	 LOW

Eco Mode
	set mode to eco
	output plus should be	 HIGH
	output minus should be	 HIGH





*** Settings ***
Documentation	Testing Heat Calendrar libray
Library		testLibs/HeatCalendarLibrary.py
Test Setup	set calendar	test.json

*** Test Cases ***
mode eco
	set time to	Monday	02:45
	result should be	eco

mode confort
	set time to	Sunday	12:11
	result should be	confort

out of range
	set time to	Tuesday	02:45
	result should be	unknow


 

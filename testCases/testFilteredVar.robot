*** Settings ***
Library	testLibs/FilteredVarLibrary.py

*** Test Cases ***
Getting Value
	set source value	5
	set filtered var
	filtered var should be	5
  
Caching value
	set source value	5
	set filtered var
	filtered var should be	5
	set source value	other
	filtered var should be	5
	Wait Until Keyword Succeeds	2sec	0.2 sec	filtered var should be	other
	
Wrong getter
	set source value	5
	set filtered var with wrong getter
	Run Keyword And Expect Error	*	filtered var should be	5	

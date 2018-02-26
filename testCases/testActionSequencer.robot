*** Settings ***
Documentation	Testing ActionSequencer libray
Library		testLibs/ActionSequencerLibrary.py

*** Test Cases ***
Not loaded
	create action sequencer with 0 actions 
	start it
	stop it

Loaded during init
	create action sequencer with 2 actions
	start it
	action should be	1
	stop it
	start it
	action should be	2
	
Loaded during start
	create action sequencer
	start it with 3 actions
	action should be 1
	action should be	2	

Not ending execution
	create action sequencer with 2 actions
	start it
	action should be	1
	action should be	2	
	action should be	1
	action should be	2	
	action should be	1	
	action should be	2	
	
Many actions
	create action sequencer with 2500 actions
	start it
	action should be	1
	action should be	2	
	action should be	3	


*** Keywords ***
action should be
	[Arguments]	${action}
	Wait Until Keyword Succeeds	2 sec.	0.1 sec.	executed action should be	${action}
	
start it with ${nb} actions
	start current sequencer with	${nb}

create action sequencer with ${nb} actions
	create default action sequencer	${nb}
	


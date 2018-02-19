*** Settings ***
Documentation	doit être connecté au HW pour ce test
Library		testLibs/CurrentTemperatureLibrary.py

*** Test Cases ***
Read actual temperature
  read temperature
  
Read simulated temperature
  simulate temperature  25
  read temperature
  

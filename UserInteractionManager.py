#
# this module allow to interface with user about
# overruling the calendar (vacation, day at home, ...)
# it will fetch the user decision in a json file 
class UserInteractionManager:
  def __init__(userJson):
    self._jsonFile = CST.JSON_PATH + userJson
    
  def isOverruled(self):
  

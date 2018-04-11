#
# this module allow to interfec with user about
# orverruling the calendar (vacation, day at home, ...)

class UserOverrule:
  def __init__(userJson):
    self._jsonFile = CST.JSON_PATH + userJson
    
  def isOverruled(self):
  

# -*- coding: utf-8 -*-

class FeltTemperature:
  """
    this class proovide calculation of felt temperature from environmental condition
    use : 
    - create an object initialized with proper target temperature (real air temperature under normal condition)
    - at init, give it access to requested information (getter function)
    - use feltHot(), f
    .. warning:: version provisoire non entierement fonctionnelle
    
  """
  
  def __init__(self, 
               insideTemperature,
               outsideSunLevel,
               insideSunLevel,
               humidity,
               outsideTemperature,
               targetTemp = 19):
    """
      :param insideTemperature: the room temperature in Celsius
      :param targetTemp: the target felt temperature (Celsius), similar to the air temperature without sun load under comfortable humidity
    """
    self.targetTemp = targetTemp
  
  def feltTempCold(self):
    """
      :return: True if user will feel cold versus target temperature
    """
    return False # TODO: implement!
  
  
  def feltTempHot(self):
    """
      :return: True if user will feel hot versus target temperature
    """
    return False # TODO: implement!
    
    
    def feltTempSuperHot(self):
    """
      :return: True if user will feel really hot versus target temperature
    """
    return False # TODO: implement!
    

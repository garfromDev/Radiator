# -*- coding: utf-8 -*-
import const
const.RI = 0.125

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
               targetTemp = 19,
               wallTransmissionCoeff = 0.146 ):
    """
      :param insideTemperature: a function returning the room temperature in Celsius
      :param outsideSunLevel: a function returning the sun level outside (HIGH, MEDIUM, LOW, NONE)
      :param insideSunLevel: a function returning the sun level (light level) inside (HIGH, MEDIUM, LOW, NONE)
      :param humidity: a function returning the humidity level inside in %RH
      :param outsideTemperature: a function returning the outside temperature in Celsius
      :param targetTemp: the target felt temperature (Celsius), similar to the air temperature without sun load under comfortable humidity
      :param wall: an object of type WallStackUp giving thermal property of wall material and insulation
    """
    self.targetTemp = targetTemp
    self.insideTemperature = insideTemperature
    self.outsideSunLevel = outsideSunLevel
    self.humidity = humidity
    self.outsideTemperature = outsideTemperature
    self.targetTemp = targetTemp
    self.wallTransmissionCoeff = wallTransmissionCoeff
    
    
  def feltTempCold(self):
    """
      :return: True if user will feel cold versus target temperature
      user feel cold when :
      - inside air temp is too low OR
      - wall temperature is lower than air temperature and no sun OR
      - humidity is high and no sun
      - 
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
      if self.insideTemperature() - targetTemp > CST.SUPER_HOT_DELTA:
        return true
      return False 
    
    def _wallTemperature(self):
      """
      :return the calculated wall temperature based on wall transmission coeff
      """
      delta = outsideTemperature() - insideTemperature()
      phi = delta * self.wallTransmissionCoeff
      return insideTemperature() + phi * const.RI 

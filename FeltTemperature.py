# -*- coding: utf-8 -*-
import const
const.RI = 0.125
const.WINDOW_Ri = 0.13
const.FELT_TEMP_COLD_DELTA = -1.0
const.FELT_TEMP_HOT_DELTA = +0.8
const.SUPER_HOT_DELTA = 2

#factors define the ratio that is applied to the effect
const.WALL_FACTOR = 0 #to change when outside temp available
const.LIGHT_FACTOR = 0.2
const.WINDOW_FACTOR = 0 #to change when outside temp available
const.INSIDE_TEMP_FACTOR = 0.4
const.SUN_FACTOR = 0.8
const.HUMIDITY_FACTOR = 0.6
const.MAX_INSIDE_TEMP_EFFECT = 2 #max value of effect of delta inside temp vs target temp
const.MIN_INSIDE_TEMP_EFFECT = -2 #min value of effect of delta inside temp vs target temp

class FeltTemperature:
  """
    this class provide calculation of felt temperature from environmental condition
    use : 
    - create an object initialized with proper target temperature (real air temperature under normal condition)
    - at init, give it access to requested information (getter function)
    - use feltHot(), f
    .. warning:: version provisoire non entierement fonctionnelle, prise en compte temp et lumière uniquement
    
  """
  
  def __init__(self, 
               insideTemperature,
               outsideSunLevel = lambda x: "NONE",
               insideSunLevel = lambda x: "NONE",
               humidity = lambda x: None,
               outsideTemperature = lambda x: None,
               targetTemp = 19,
               wallTransmissionCoeff = 0.146,
               windowTransmissionCoeff = 0.855):
    """
      :param insideTemperature: a function returning the room temperature in Celsius
      :param outsideSunLevel: a function returning the sun level outside (HIGH, MEDIUM, LOW, NONE)
      :param insideSunLevel: a function returning the sun level (light level) inside (HIGH, MEDIUM, LOW, NONE)
      :param humidity: a function returning the humidity level inside in %RH
      :param outsideTemperature: a function returning the outside temperature in Celsius
      :param targetTemp: the target felt temperature (Celsius), similar to the air temperature without sun load under comfortable humidity
      :param wallTransmissionCoeff: wall material and insulation property
      :param windowTransmissionCoeff: window insulation property
    """
    self.targetTemp = targetTemp
    self.insideTemperature = insideTemperature
    self.outsideSunLevel = outsideSunLevel
    self.insideSunLevel = insideSunLevel
    self.humidity = humidity
    self.outsideTemperature = outsideTemperature
    self.wallTransmissionCoeff = wallTransmissionCoeff
    self.windowTransmissionCoeff = windowTransmissionCoeff
   
  
  def feltTempCold(self):
    """
      :return: True if user will feel cold versus target temperature
      user feel cold when :
      - inside air temp is too low OR
      - wall temperature is lower than air temperature and no sun OR
      - humidity is high and no sun
      - 
    """
    return ( self._feltTemperature() < (self.targetTemp + const.FELT_TEMP_COLD_DELTA) )
  
  
  def feltTempHot(self):
    """
      :return: True if user will feel hot versus target temperature
    """
    return ( self._feltTemperature() > (self.targetTemp + const.FELT_TEMP_HOT_DELTA) )
    
    
    def feltTempSuperHot(self):
      """
      :return: True if user will feel really hot versus target temperature
      """
      return (  self._feltTemperature()  > self.targetTemp + const.SUPER_HOT_DELTA)
    
    
    def _feltTemperature(self):
      """
      :return: the calculated felt temperature taking into account the different parameters
      """
      felt = self.insideTemperature()\
        + self._wallTemperatureEffect() * const.WALL_FACTOR \
        + self._windowTemperatureEffect() * const.WINDOW_FACTOR \
        + self._insideTemperatureEffect() * const.INSIDE_TEMP_FACTOR\
        + self._lightEffect() * const.SUN_FACTOR\
        + self._humidityEffect() * const.HUMIDITY_FACTOR
      return felt or self.insideTemperature()
      
      
    #==  Effect on felt temperature  ==
    
    def  _wallTemperatureEffect(self):
      return 0 #TODO: implement
      
     
    def _windowTemperatureEffect(self):
      return 0 #TODO: implement

    
    def _insideTemperatureEffect(self)
      """ the effect is the difference vs target temp, truncated at MAX_INSIDE_TEMP_EFFECT / MIN_INSIDE_TEMP_EFFECT """
      return max(min((self.insideTemperature()-self.targetTemp), const.MAX_INSIDE_TEMP_EFFECT), const.MIN_INSIDE_TEMP_EFFECT)
    
    
    def _lightEffect(self):
      """ effect is +1 when "SUN", zero otherwise """
      return 1 if self.insideSunLevel()=="SUN" else 0
   
  
     def _humidityEffect(self):
      return 0 #TODO: implement

     
    #== Calculation of raw temperatures ==  
    def _wallTemperature(self):
    """
      :return the calculated wall temperature based on wall transmission coeff
      """
      return _surfaceTemperature(self.wallTransmissionCoeff, const.RI)

    
    def _windowTemperature(self):
      """
      :return the calculated window surface temperature based on window transmission coeff
      """
      return _surfaceTemperature(self.windowTransmissionCoeff, const.WINDOW_Ri)
    
    
    def _surfaceTemperature(U, Ri):
      """
      :param U: the total transmission coeff of the wall or window in W / m2 K
      :return the surface temperature in °C
      """
      delta = outsideTemperature() - insideTemperature()
      phi = delta * U
      return insideTemperature() + phi * Ri

    
    
if __name__ == '__main__':
    print("testing Felt Temperature manually")
    mock_temp = 21
    test = FeltTemperature(insideTemperature=lambda x: mock_temp)
    print("temp:{} -> feltTempCold:{} feltTempHot{} feltTempSuperHot:{}".format(mock_temp,
                                                                                test.feltTempCold(),
                                                                               test.feltTempHot(),
                                                                               test.feltTempSuperHot())
    mock_temp = 14
    print("temp:{} -> feltTempCold:{} feltTempHot{} feltTempSuperHot:{}".format(mock_temp,
                                                                                test.feltTempCold(),
                                                                               test.feltTempHot(),
                                                                               test.feltTempSuperHot())
          

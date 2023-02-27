import math as m
class SitioLanzamiento():
  # Parametro de la Tierra
  Mass = 5.972 * 10 ** 24;
  Mu = 6.674 * 10 ** -11;
  a = 6378.136999995039 * 10 ** 3;
  b = 6356.75231420888 * 10 ** 3;
  f = 1 - b/ a;
  e = (2 * f - f ** 2) ** .5;
  omega = 2 * m.pi / (3600 * 24)
  VelSon = 300

  def __init__(self, lat, long, alt=0, nombre="Sin nombre"):
    self.lat=lat
    self.long=long
    self.alt=alt
    self.nombre=nombre
    self.Coor=[self.lat,self.long]

  def __str__(self):
    return "Sitio:{} Latitud:{} Longitud:{} Altitud: {}" .format(self.nombre, self.lat, self.long, self.alt)

  def MostrarParamTierra(self):
    print("Masa:", self.Mass, "\nMu: ", self.Mu, "\nSemi Eje Mayor: ", self.a, "\nSemi Eje Menor:",self.b)
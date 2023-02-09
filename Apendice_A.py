# -*- coding: utf-8 -*-
#ApendiceA_Final.ipynb


#from io import SEEK_SET
# esteprograma realiza el Apendice A del CFR 14
# El resultados son las graficas y las coordenadas de la zona de exlusion y corredor de vuelo
from SitioLanzamiento import SitioLanzamiento
import math as m
import math as math
import numpy as np
from Lanzamiento import Lanzamiento as Launch
import plotly.graph_objects  as go

class Apendice_A(Launch):

  def __init__(self, Launch):
    self.Corredor = [self.Launch.lat, self.Launch.long]
    super().__init__(self, Launch.Sitio, Launch.Tipo, Launch.Azimut, Launch.Payload, Launch.Apogeo)

  #Encontrar clase segun el peso para cohetes suborbitales
  def Analizar(self):

    
    if self.Tipo==2:
      Dmax=ListaDmax[4]
      Doez=ListaDoez[4]
      CF=ListaLineasSeg[0][4]
      DE=ListaLineasSeg[1][4]
      R=0.05*Apogeo

      if Apogeo <100*10**3:
        D=Apogeo*0.4

      else:
        D=Apogeo*0.7

      #defieniendo vectores de la zona de exclusion y utilizando la funcion previa
      FinZonaExcl = []
      FinZonaExcl=AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut,Doez)

      for i in range(PCirZnExcl):
        ZonaExcl.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut+(-270+10*i)*math.pi/180,Dmax))

      for i in range(PCirZnExcl+1,2*PCirZnExcl):
        ZonaExcl.append(AERtoLLH(FinZonaExcl[0], FinZonaExcl[1],Azimut+(-270+10*i)*math.pi/180,Dmax))

      ZonaExcl.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut+(-270)*math.pi/180,Dmax))

      #Ubicar punto de impacto y area
      ImpactPoint=[0,0]
      [ImpactPoint[0], ImpactPoint[1]]=AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut,D)
      ImpactArea = []

      for i in range(36):
        ImpactArea.append(AERtoLLH(ImpactPoint[0], ImpactPoint[1],Azimut+10*i*(math.pi/180),R))

      #definiendo y calculando vectores de las zonas
      ImpactArea.append(AERtoLLH(ImpactPoint[0], ImpactPoint[1],Azimut+10*0*(math.pi/180),R))
      Punto10 = [0,0]
      PuntoD = [[0,0]]

      self.Corredor = [[ BaseLanzamiento[0],BaseLanzamiento[1] ]]
      [Punto10[0], Punto10[1]]=AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut,Seg1)

      self.Corredor.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut-(180-20)*(math.pi/180),Dmax))
      self.Corredor.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut-(180+20)*(math.pi/180),Dmax))
      self.Corredor.append(AERtoLLH(Punto10[0], Punto10[1],Azimut+90*(math.pi/180),CF*0.5))

      if D>Seg2:
        i=1
        RangoSuborbital=0
        PuntoD.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut,Seg2))
        self.Corredor.append(AERtoLLH(PuntoD[1][0], PuntoD[1][1],Azimut+90*(math.pi/180),.5*DE))

        while RangoSuborbital<D-100000:
          RangoSuborbital=Seg2+i*100000
          PuntoD.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut,RangoSuborbital))
          i=i+1
          self.Corredor.append(AERtoLLH(PuntoD[i][0], PuntoD[i][1],Azimut+90*(math.pi/180),.5*(DE+(RangoSuborbital-Seg2)*(2*R-DE)/(D-Seg2))))

      self.Corredor.append(AERtoLLH(ImpactPoint[0], ImpactPoint[1],Azimut+90*(math.pi/180),R))
      self.Corredor.append(AERtoLLH(ImpactPoint[0], ImpactPoint[1],Azimut-90*(math.pi/180),R))

      if D>Seg2:
        while RangoSuborbital>Seg2+100000:
          RangoSuborbital=RangoSuborbital-100000
          self.Corredor.append(AERtoLLH(PuntoD[i][0], PuntoD[i][1],Azimut-90*(math.pi/180),.5*(DE+(RangoSuborbital-Seg2)*(2*R-DE)/(D-Seg2))))
          i=i-1;
        self.Corredor.append(AERtoLLH(PuntoD[1][0], PuntoD[1][1],Azimut-90*(math.pi/180),.5*DE))

      self.Corredor.append(AERtoLLH(Punto10[0], Punto10[1],Azimut-90*(math.pi/180),CF*0.5))
      self.Corredor.append([self.Corredor[1][0],self.Corredor[1][1]])


  #conviertiendo puntos a arrays
  Zonamatriz = np.array(ZonaExcl)
  Corredormatriz = np.array(self.Corredor)
  Impactmatriz = np.array(ImpactArea)
  
  #creando mapa y primer vector para graficar
  fig = go.Figure(go.Scattermapbox( 
                            
    mode = "markers+lines",
    lon = [BaseLanzamiento[1] * 180 / math.pi],
    lat = [BaseLanzamiento[0] * 180 / math.pi],
    marker = {'size': 5}))

  fig.add_trace(go.Scattermapbox(  
    mode = "markers+lines",
    lon = Corredormatriz[:,1] * 180 / math.pi,
    lat = Corredormatriz[:,0] * 180 / math.pi,
    marker = {'size': 5}))
  fig.add_trace(go.Scattermapbox(  
    mode = "markers+lines",
    lon = Zonamatriz[:,1] * 180 / math.pi,
    lat = Zonamatriz[:,0] * 180 / math.pi,
    marker = {'size': 5}))

  fig.add_trace(go.Scattermapbox(
    mode = "markers+lines",
    lon = Impactmatriz[:,1] * 180 / math.pi,
    lat = Impactmatriz[:,0] * 180 / math.pi,
    marker = {'size': 5}))
    
   
  fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': 50, 'lat': 70},
        'style': "stamen-terrain",
        'center': {'lon': -40, 'lat': -20},
        'zoom': 0.05})
  fig.show()

  #Zona Impacto
  print("\n")
  ImpactName="ZonaImpacto"+"_"+str(Lanzamiento.Tipo)+"_"+str((180/m.pi)*BaseLanzamiento[0])+"_" + str((180/m.pi)*BaseLanzamiento[1]) + "_" + str((180/m.pi)*Azimut)+".txt"
  print(ImpactName+"\n")
  ImpactCSV = open(ImpactName, "a")
  for i in range(len(Impactmatriz)):
    ss=str((180/m.pi)*Impactmatriz[i][0])+", "+str((180/m.pi)*Impactmatriz[i][1])
    print(ss)
    ImpactCSV.write(ss+"\n")
  ImpactCSV.close()

#aqui termina el primer tipo y comienza el segundo


#Encontra la clase segun la carga util e inclinacion

if Lanzamiento.Tipo==1:

  if Inclinacion<=28:
    Incl=0
    if PesoCarga<ClasePeso[Incl][0]:
      Clase=0

    if ClasePeso[Incl][0]<=PesoCarga and PesoCarga<ClasePeso[Incl][1]:
      Clase=1
    
    if ClasePeso[Incl][1]<=PesoCarga and PesoCarga<ClasePeso[Incl][2]:
      Clase=2
    
    if ClasePeso[Incl][2]<=PesoCarga: 
      Clase=3
  else:
    Incl=1
    if PesoCarga<ClasePeso[Incl][0]:
      Clase=0
      
    if ClasePeso[Incl][0]<=PesoCarga and PesoCarga<ClasePeso[Incl][1]:
      Clase=1
  
    if ClasePeso[Incl][1]<=PesoCarga and PesoCarga<ClasePeso[Incl][2]:
      Clase=2
  
    if ClasePeso[Incl][2]<=PesoCarga: 
      Clase=3

  #Calcular parametros de la zona de exclusion y corredor
  Dmax=ListaDmax[Clase]
  Doez=ListaDoez[Clase]
  CF=ListaLineasSeg[0][Clase]
  DE=ListaLineasSeg[1][Clase]
  HI=ListaLineasSeg[2][Clase]
  # Puntos de la zona de exclusion
  FinZonaExcl = []
  FinZonaExcl=AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut,Doez)

  for i in range(PCirZnExcl):
    ZonaExcl.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut+(-270+10*i)*math.pi/180,Dmax))

  for i in range(PCirZnExcl+1,2*PCirZnExcl):
    ZonaExcl.append(AERtoLLH(FinZonaExcl[0], FinZonaExcl[1],Azimut+(-270+10*i)*math.pi/180,Dmax))

  ZonaExcl.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut+(-270)*math.pi/180,Dmax))

  #Ubicar final del corredor
  Punto10 = []
  Punto100 = []
  Punto5000 = []
  self.Corredor = [[ BaseLanzamiento[0],BaseLanzamiento[1] ]]


  n=50
  Punto10.append(AERtoLLH(BaseLanzamiento[0],BaseLanzamiento[1],Azimut,Seg1))
  Punto100.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut,Seg2))
  self.Corredor.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut-(180-30)*(math.pi/180),Dmax))
  self.Corredor.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut-(180+30)*(math.pi/180),Dmax))
  self.Corredor.append(AERtoLLH(Punto10[0][0], Punto10[0][1],Azimut+90*(math.pi/180),CF*0.5))
  self.Corredor.append(AERtoLLH(Punto100[0][0], Punto100[0][1],Azimut+90*(math.pi/180),DE*0.5))
  [Az, Range, Az2]=LLHtoAER(Punto10[0][0], Punto10[0][1] ,Punto100[0][0], Punto100[0][1] )
  Punto5000.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut,Seg2+1*(RangoOrbital-Seg2)/n))
  n=50

  for i in range(1,n+1):
    Punto5000.append(AERtoLLH(BaseLanzamiento[0], BaseLanzamiento[1],Azimut,Seg2+(i+1)*(RangoOrbital-Seg2)/(n+1)))
    [Az, Range, Az2]=LLHtoAER(Punto5000[i-1][0],Punto5000[i-1][1] ,Punto5000[i][0],Punto5000[i][1] )
    #print(Punto5000[i-1][0],Punto5000[i-1][1] ,Punto5000[i][0],Punto5000[i][1])
    #print('[Az, Range, Az2]',[Az, Range, Az2])
    Az=Az*m.pi/180
    Az2=Az2*m.pi/180
    self.Corredor.append(AERtoLLH(Punto5000[i-1][0],Punto5000[i-1][1], Az+90, 0.5*(DE+i*(HI-DE)/n)))
 
  self.Corredor.append(AERtoLLH(Punto5000[i][0],Punto5000[i][1], Az+90, 0.5*HI))
  self.Corredor.append(AERtoLLH(Punto5000[i][0],Punto5000[i][1], Az-90, 0.5*HI))

  for i in range(n,0,-1):
    [Az, Range, Az2]=LLHtoAER(Punto5000[i-1][0],Punto5000[i-1][1] ,Punto5000[i][0],Punto5000[i][1] )
    Az=Az*m.pi/180
    Az2=Az2*m.pi/180
    self.Corredor.append(AERtoLLH(Punto5000[i][0],Punto5000[i][1], Az-90, 0.5*(DE+i*(HI-DE)/n)))
  
  self.Corredor.append(AERtoLLH(Punto100[0][0], Punto100[0][1],Azimut-90*(math.pi/180),DE*0.5))
  self.Corredor.append(AERtoLLH(Punto10[0][0], Punto10[0][1],Azimut-90*(math.pi/180),CF*0.5))
  self.Corredor.append([self.Corredor[1][0],self.Corredor[1][1]])

  #convirtiendo puntor y vectores a matrices(Arrays) para poder graficarlos
  print('ZonaExcl',ZonaExcl)
  Zonamatriz = np.array(ZonaExcl)
  print("Corredormatriz",Zonamatriz)

  Corredormatriz = np.array(self.Corredor)
  
  Pathmatriz = np.array(Punto5000)
  #print('Pathmatriz', Pathmatriz)
  #graficando 
  fig = go.Figure(go.Scattermapbox( #zona path corredor
                            
    mode = "markers+lines",
    lon = Pathmatriz[:,1] * 180 / math.pi,
    lat = Pathmatriz[:,0] * 180 / math.pi,
    marker = {'size': 5}))

  fig.add_trace(go.Scattermapbox(  
    mode = "markers+lines",
    lon = Corredormatriz[1:,1] * 180 / math.pi,
    lat = Corredormatriz[1:,0] * 180 / math.pi,
    marker = {'size': 5}))
  fig.add_trace(go.Scattermapbox(  
    mode = "markers+lines",
    lon = Zonamatriz[:,1] * 180 / math.pi,
    lat = Zonamatriz[:,0] * 180 / math.pi,
    marker = {'size': 5}))  
   
  fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': 50, 'lat': 70},
        'style': "stamen-terrain",
        'center': {'lon': -40, 'lat': -20},
        'zoom': 0.05})
  fig.show()



#Zon Exclusion
print("\n")
ZonaName="ZonaExclusion"+"_"+str(Lanzamiento.Tipo)+"_"+str((180/m.pi)*BaseLanzamiento[0])+"_" + str((180/m.pi)*BaseLanzamiento[1]) + "_" + str((180/m.pi)*Azimut)+".txt"
print(ZonaName+"\n")
ZonaExclCSV = open(ZonaName, "a")
for i in range(len(Zonamatriz)):
  ss=str((180/m.pi)*Zonamatriz[i][0])+", "+str((180/m.pi)*Zonamatriz[i][1])
  print(ss)
  ZonaExclCSV.write(ss+"\n")
ZonaExclCSV.close()

#CorredorCSV
print("\n")

CorredorName="Corredor"+"_"+str(Lanzamiento.Tipo)+"_"+str((180/m.pi)*BaseLanzamiento[0])+"_" + str((180/m.pi)*BaseLanzamiento[1]) + "_" + str((180/m.pi)*Azimut)+".txt"
print(CorredorName+"\n")
CorredorCSV = open(CorredorName, "a")
for i in range(len(Corredormatriz)):
  ss=str((180/m.pi)*Corredormatriz[i][0])+", "+str((180/m.pi)*Corredormatriz[i][1])
  print(ss)
  CorredorCSV.write(ss+"\n")
CorredorCSV.close()
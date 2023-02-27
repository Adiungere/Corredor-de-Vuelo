# -*- coding: utf-8 -*-
#ApendiceA_Final.ipynb


#from io import SEEK_SET
# esteprograma realiza el Apendice A del CFR 14
# El resultados son las graficas y las coordenadas de la zona de exlusion y corredor de vuelo
from SitioLanzamiento import SitioLanzamiento
import math as m
import math as math
import numpy as np
from Lanzamiento import Lanzamiento as Lanz
import plotly.graph_objects  as go

class Apendice_A(Lanz):

  def __init__(self, Vuelo):
    super().__init__(Vuelo.Sitio, Vuelo.Cohete, Vuelo.Azimut, Vuelo.Apogeo)
    self.Vuelo=Vuelo
    self.Corredor=[Vuelo.Sitio.Coor]
    self.ZonaExcl=[Vuelo.Sitio.Coor]
    self.ImpactArea = []

  #Encontrar clase segun el peso para cohetes suborbitales
  def Analizar(self):
    PCirZnExcl = 18
    ClasePeso = [[1995.8, 5034.8, 8391.4], [1496.8, 3810.1,
                                            6803.8]]  # Datos de del apendice A en Clasiifcacion de lso cohete por su masa de carga util a 185.2 km
    ListaDmax = [2222, 2833, 3222, 3963, 2444]  # Radio de la Zona de exclusion
    ListaDoez = [6111, 6426, 7889, 23816,
                 5889]  # Rango donde termina la zona de exclusion Small Medium Med-Large Large Sub-Guided

    ListaLineasSeg = [[73100, 75500, 77100, 80000, 73900],
                      [218300, 219500, 220300, 221800, 218700],
                      [3265576, 3265576, 3265576, 3265576, 0]]
    Seg1 = 18520
    Seg2 = 185200
    RangoOrbital = 9260000

    if self.Tipo==2:
      Dmax=ListaDmax[4]
      Doez=ListaDoez[4]
      CF=ListaLineasSeg[0][4]
      DE=ListaLineasSeg[1][4]
      R=0.05*self.Apogeo

      if self.Apogeo < 100*10**3:
        D=self.Apogeo*0.4

      else:
        D=self.Apogeo*0.7

      #defieniendo vectores de la zona de exclusion y utilizando la funcion previa
      FinZonaExcl = []
      FinZonaExcl=self.AERtoLLH(self.lat, self.long, self.Azimut,Doez)
      self.ZonaExcl[0]=self.AERtoLLH(self.lat, self.long,self.Azimut-270,Dmax)
      for i in range(1,PCirZnExcl):
        self.ZonaExcl.append(self.AERtoLLH(self.lat, self.long,self.Azimut+(-270+10*i),Dmax))

      for i in range(PCirZnExcl+1,2*PCirZnExcl):
        self.ZonaExcl.append(self.AERtoLLH(FinZonaExcl[0], FinZonaExcl[1],self.Azimut+(-270+10*i),Dmax))

      self.ZonaExcl.append(self.AERtoLLH(self.lat, self.long,self.Azimut+(-270),Dmax))

      #Ubicar punto de impacto y area
      ImpactPoint=[0,0]
      [ImpactPoint[0], ImpactPoint[1]]=self.AERtoLLH(self.lat, self.long,self.Azimut,D)

      for i in range(36):
        self.ImpactArea.append(self.AERtoLLH(ImpactPoint[0], ImpactPoint[1],self.Azimut+10*i,R))

      #definiendo y calculando vectores de las zonas
      self.ImpactArea.append(self.AERtoLLH(ImpactPoint[0], ImpactPoint[1],self.Azimut+10*0,R))
      Punto10 = [0,0]
      PuntoD = [[0,0]]

      [Punto10[0], Punto10[1]]=self.AERtoLLH(self.lat, self.long,self.Azimut,Seg1)

      self.Corredor[0]=self.AERtoLLH(self.lat, self.long,self.Azimut-(180+20),Dmax)
      self.Corredor.append(self.AERtoLLH(Punto10[0], Punto10[1],self.Azimut+90,CF*0.5))

      if D>Seg2:
        i=1
        RangoSuborbital=0
        PuntoD.append(self.AERtoLLH(self.lat, self.long,self.Azimut,Seg2))
        self.Corredor.append(self.AERtoLLH(PuntoD[1][0], PuntoD[1][1],self.Azimut+90,.5*DE))

        while RangoSuborbital<D-100000:
          RangoSuborbital=Seg2+i*100000
          PuntoD.append(self.AERtoLLH(self.lat, self.long,self.Azimut,RangoSuborbital))
          i=i+1
          self.Corredor.append(self.AERtoLLH(PuntoD[i][0], PuntoD[i][1],self.Azimut+90,.5*(DE+(RangoSuborbital-Seg2)*(2*R-DE)/(D-Seg2))))

      self.Corredor.append(self.AERtoLLH(ImpactPoint[0], ImpactPoint[1],self.Azimut+90,R))
      self.Corredor.append(self.AERtoLLH(ImpactPoint[0], ImpactPoint[1],self.Azimut-90,R))

      if D>Seg2:
        while RangoSuborbital>Seg2+100000:
          RangoSuborbital=RangoSuborbital-100000
          self.Corredor.append(self.AERtoLLH(PuntoD[i][0], PuntoD[i][1],self.Azimut-90,.5*(DE+(RangoSuborbital-Seg2)*(2*R-DE)/(D-Seg2))))
          i=i-1;
        self.Corredor.append(self.AERtoLLH(PuntoD[1][0], PuntoD[1][1],self.Azimut-90,.5*DE))

      self.Corredor.append(self.AERtoLLH(Punto10[0], Punto10[1],self.Azimut-90,CF*0.5))
      self.Corredor.append(self.AERtoLLH(self.lat, self.long,self.Azimut-(180-20),Dmax))
      self.Corredor.append(self.AERtoLLH(self.lat, self.long,self.Azimut-180,Dmax))
      self.Corredor.append([self.Corredor[0][0], self.Corredor[0][1]])

      self.Impactmatriz = np.array(self.ImpactArea)


    if self.Tipo == 1:
      if self.Inclinacion <= 28:
        Incl = 0
        if self.MasaCarga < ClasePeso[Incl][0]:
          Clase = 0

        if ClasePeso[Incl][0] <= self.MasaCarga and self.MasaCarga < ClasePeso[Incl][1]:
          Clase = 1

        if ClasePeso[Incl][1] <= self.MasaCarga and self.MasaCarga < ClasePeso[Incl][2]:
          Clase = 2

        if ClasePeso[Incl][2] <= self.MasaCarga:
          Clase = 3

      else:
        Incl = 1
        if self.MasaCarga < ClasePeso[Incl][0]:
          Clase = 0

        if ClasePeso[Incl][0] <= self.MasaCarga and self.MasaCarga < ClasePeso[Incl][1]:
          Clase = 1

        if ClasePeso[Incl][1] <= self.MasaCarga and self.MasaCarga < ClasePeso[Incl][2]:
          Clase = 2

        if ClasePeso[Incl][2] <= self.MasaCarga:
          Clase = 3

      # Calcular parametros de la zona de exclusion y corredor
      Dmax = ListaDmax[Clase]
      Doez = ListaDoez[Clase]
      CF = ListaLineasSeg[0][Clase]
      DE = ListaLineasSeg[1][Clase]
      HI = ListaLineasSeg[2][Clase]
      # Puntos de la zona de exclusion
      FinZonaExcl = []
      FinZonaExcl = self.AERtoLLH(self.lat, self.long, self.Azimut, Doez)

      self.ZonaExcl[0] = self.AERtoLLH(self.lat, self.long, self.Azimut - 270, Dmax)
      for i in range(1, PCirZnExcl):
        self.ZonaExcl.append(self.AERtoLLH(self.lat, self.long, self.Azimut + (-270 + 10 * i) , Dmax))

      for i in range(PCirZnExcl + 1, 2 * PCirZnExcl):
        self.ZonaExcl.append(
          self.AERtoLLH(FinZonaExcl[0], FinZonaExcl[1], self.Azimut + (-270 + 10 * i) , Dmax))

      self.ZonaExcl.append(self.AERtoLLH(self.lat, self.long, self.Azimut + (-270) , Dmax))

      # Ubicar final del corredor
      Punto10 = []
      Punto100 = []
      Punto5000 = []

      n = 50
      Punto10.append(self.AERtoLLH(self.lat, self.long, self.Azimut, Seg1))
      Punto100.append(self.AERtoLLH(self.lat, self.long, self.Azimut, Seg2))
      self.Corredor.append(self.AERtoLLH(self.lat, self.long, self.Azimut - (180 - 30) , Dmax))
      self.Corredor.append(self.AERtoLLH(self.lat, self.long, self.Azimut - (180 + 30) , Dmax))
      self.Corredor.append(self.AERtoLLH(Punto10[0][0], Punto10[0][1], self.Azimut + 90, CF * 0.5))
      self.Corredor.append(self.AERtoLLH(Punto100[0][0], Punto100[0][1], self.Azimut + 90 , DE * 0.5))
      [Az, Range, Az2] = self.LLHtoAER(Punto10[0][0], Punto10[0][1], Punto100[0][0], Punto100[0][1])
      Punto5000.append(self.AERtoLLH(self.lat, self.long, self.Azimut, Seg2 + 1 * (RangoOrbital - Seg2) / n))
      n = 50

      for i in range(1, n + 1):
        Punto5000.append(self.AERtoLLH(self.lat, self.long, self.Azimut, Seg2 + (i + 1) * (RangoOrbital - Seg2) / (n + 1)))
        [Az, Range, Az2] = self.LLHtoAER(Punto5000[i - 1][0], Punto5000[i - 1][1], Punto5000[i][0], Punto5000[i][1])
        self.Corredor.append(self.AERtoLLH(Punto5000[i - 1][0], Punto5000[i - 1][1], Az + 90, 0.5 * (DE + i * (HI - DE) / n)))

      self.Corredor.append(self.AERtoLLH(Punto5000[i][0], Punto5000[i][1], Az + 90, 0.5 * HI))
      self.Corredor.append(self.AERtoLLH(Punto5000[i][0], Punto5000[i][1], Az - 90, 0.5 * HI))

      for i in range(n, 0, -1):
        [Az, Range, Az2] = self.LLHtoAER(Punto5000[i - 1][0], Punto5000[i - 1][1], Punto5000[i][0], Punto5000[i][1])
        self.Corredor.append(self.AERtoLLH(Punto5000[i][0], Punto5000[i][1], Az - 90, 0.5 * (DE + i * (HI - DE) / n)))

      self.Corredor.append(self.AERtoLLH(Punto100[0][0], Punto100[0][1], self.Azimut - 90 , DE * 0.5))
      self.Corredor.append(self.AERtoLLH(Punto10[0][0], Punto10[0][1], self.Azimut - 90 , CF * 0.5))
      self.Corredor.append([self.Corredor[1][0], self.Corredor[1][1]])
      self.Pathmatriz = np.array(Punto5000)

    #convirtiendo puntor y vectores a matrices(Arrays) para poder graficarlos
    self.Zonamatriz = np.array(self.ZonaExcl)
    self.Corredormatriz = np.array(self.Corredor)

    return [self.Corredor, self.ZonaExcl]


  def MostrarMapa(self):
    if self.Tipo == 2:
      #conviertiendo puntos a arrays
      #creando mapa y primer vector para graficar
      fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = [self.long ],
        lat = [self.lat],
        marker = {'size': 5}))

      fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = self.Corredormatriz[:,1],
        lat = self.Corredormatriz[:,0],
        marker = {'size': 5}))

      fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = self.Zonamatriz[:,1],
        lat = self.Zonamatriz[:,0],
        marker = {'size': 5}))

      fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = self.Impactmatriz[:,1],
        lat = self.Impactmatriz[:,0],
        marker = {'size': 5}))

      fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': 50, 'lat': 70},
            'style': "stamen-terrain",
            'center': {'lon': -40, 'lat': -20},
            'zoom': 0.05})
      fig.show()

    if self.Tipo == 1:
      fig = go.Figure(go.Scattermapbox(  # zona path corredor
        mode="markers+lines",
        lon=self.Pathmatriz[:, 1],
        lat=self.Pathmatriz[:, 0],
        marker={'size': 5}))

      fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        lon=self.Corredormatriz[1:, 1],
        lat=self.Corredormatriz[1:, 0],
        marker={'size': 5}))

      fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        lon=self.Zonamatriz[:, 1],
        lat=self.Zonamatriz[:, 0],
        marker={'size': 5}))

      fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
          'center': {'lon': 50, 'lat': 70},
          'style': "stamen-terrain",
          'center': {'lon': -40, 'lat': -20},
          'zoom': 0.05})
      fig.show()


  def CrearArchivo(self):
    if self.Tipo==2:
      #Zona Impacto
      ImpactName="ResultadosApendiceA\ZonaImpacto"+"_"+str(self.Tipo)+"_"+str(self.lat)+"_" + str(self.long) + "_" + str(self.Azimut)+".txt"
      ImpactCSV = open(ImpactName, "a")
      for i in range(len(self.Impactmatriz)):
        ss=str(self.Impactmatriz[i][0])+", "+str(self.Impactmatriz[i][1])
        ImpactCSV.write(ss+"\n")
      ImpactCSV.close()

    #Zona Exclusion
    ZonaName="ResultadosApendiceA\ZonaExclusion"+"_"+str(self.Tipo)+"_"+str(self.lat)+"_" + str(self.long) + "_" + str(self.Azimut)+".txt"
    ZonaExclCSV = open(ZonaName, "a")
    for i in range(len(self.Zonamatriz)):
      ss=str(self.Zonamatriz[i][0])+", "+str(self.Zonamatriz[i][1])
      ZonaExclCSV.write(ss+"\n")
    ZonaExclCSV.close()

    #CorredorCSV
    CorredorName="ResultadosApendiceA\Corredor"+"_"+str(self.Tipo)+"_"+str(self.lat)+"_" + str(self.long) + "_" + str(self.Azimut)+".txt"
    CorredorCSV = open(CorredorName, "a")
    for i in range(len(self.Corredormatriz)):
      ss=str(self.Corredormatriz[i][0])+", "+str(self.Corredormatriz[i][1])
      CorredorCSV.write(ss+"\n")
    CorredorCSV.close()
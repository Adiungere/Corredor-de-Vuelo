from SitioLanzamiento import SitioLanzamiento
from Vehiculo import Vehiculo
from Lanzamiento import Lanzamiento
from Apendice_A import Apendice_A
import math

import math as m
Cancun=SitioLanzamiento(20.762896, -87.197700, 0, "Cancun")
BJC=SitioLanzamiento(24.5, -111.5, 0, "Baja California Sur")
Merida= SitioLanzamiento(18.219890, -87.852486, 0, "Merida")
BoChica=SitioLanzamiento(25.997059, -97.155805, 0, "Boca Chica")

# Parametros de Cohete
Diametro = 1.2  # Diametro de la seccion transversal cohete
MasaCarga = 225  # Masa de la carga util
M2Seca_P = 250 + MasaCarga  # Masa seca de la segunda etapa mas carga util
M2F = 2300 + M2Seca_P  # Masa total de la segunda etapa: seca, combustible, payload
M2F_1Seca = 950 + M2F  # Masa seca de la primera mas la total de la segunda
M_Rocket_o = M2F_1Seca + 10 * 10 ** 3  # Masa de despuegue, Liftoff mass del cohete
Cd_Min = 0.4

# Lso sigueintes datso pueden substituirse por una tabla con la curva de
# motor
MaxThrust1 = 162 * 10 ** 3
MinThrust1 = 50 * 10 ** 3
ThrustSecond = 23 * 10 ** 3
t_MECO = 155  # Tiempo que duran prendidos los motores de la primera etapa Main Engine Cutt Off
t_2Stage = 157  # Tiempo que duran prendidos los motores de la segunda etapa
t_SECO = t_2Stage + t_MECO  # Isntante en que se apagan los motores de la Segunda Etapa. Second Engien Cut Off
VJet1 = 3030  # Velocidad de los gases de escape de la primera etapa
VJet2 = 3400  # Velocidad de los gases de escape de la primera etapa
Electron=Vehiculo(2, 250)

#Espeficiar apogeo, solo importa para suborbitales, para orbitales no importa el valor

Azimut = 180 # Grados
Apogeo = 1000*10**3

t_pitchOver = 9  # Instante apartir del liftoff en que inicia el Gravity turn
Gimbal = 10 * math.pi / 180
PitchOverDuration = 2.1

Vuelo1=Lanzamiento(BoChica,Electron,  Azimut, Apogeo)

Analisis1=Apendice_A(Vuelo1)
[Corredor, ZonaExcl]=Analisis1.Analizar()
Analisis1.MostrarMapa()
Analisis1.CrearArchivo()
from SitioLanzamiento import SitioLanzamiento
import math as m
Cancun=SitioLanzamiento(20.762896, -87.197700)
BJC=SitioLanzamiento(24.5, -111.5)
Merida= SitioLanzamiento(18.219890, -87.852486)
BoChica=SitioLanzamiento(25.997059, -97.155805)

BoChica.MostrarParamTierra()
Tipo = 2                                                                # Orbital=1 , SubOrbital=2
Azimut = 230*m.pi/180
Payload = 9000                                           #Especificar Peso de la carga util kg
Apogeo = 200*10**3                                       #Espeficiar apogeo, solo importa para suborbitales, para orbitales no importa el valor

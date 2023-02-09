from SitioLanzamiento import SitioLanzamiento as SL
import math

from Vehiculo import Vehiculo

class Lanzamiento(SL):
    def __init__(self, Sitio, Tipo, Azimut, Payload, Apogeo):
        super().__init__(Sitio.lat, Sitio.long)
        self.Sitio=Sitio
        self.Tipo = Tipo           # Orbital=1 , SubOrbital=2
        self.Azimut = Azimut*math.pi/180
        self.Payload = Payload     #Especificar Peso de la carga util kg
        self.Apogeo = Apogeo       #Espeficiar apogeo, solo importa para suborbitales, para orbitales no importa el valor
        self.Inclinacion = (180/math.pi)*math.acos(math.sin(self.Azimut)*math.cos(Sitio.lat))

    def __str__(self):
        return "Tipo:{}, Azimut:{}°, Payload:{}kg, Apogeo:{}km".format(self.Tipo, self.Azimut*180/math.pi, self.Payload, self.Apogeo/1000)

    #creando función AERtoLLH para usar después
    def AERtoLLH(self, Lat1, Long1, azimut, Rango):
        ecc_sec=(SL.a**2-SL.b**2)**.5/SL.b
        theta=Rango/SL.b
        B1=math.atan2(SL.b*math.sin(Lat1),( SL.a*math.cos(Lat1)))
        g=math.cos(B1)*math.cos(azimut)
        h=math.cos(B1)*math.sin(azimut)
        m=0.5*(1+0.5*(ecc_sec*math.sin(B1))**2)*(1-h**2)
        n=0.5*(1+0.5*(ecc_sec*math.sin(B1))**2)*( (math.sin(B1)**2)*math.cos(theta)+g*math.sin(B1)*math.sin(theta))
        L=h*( -SL.f*theta + 3*(SL.f**2)*n*math.sin(theta) + 0.5*3*(SL.f**2)*m*(theta-math.sin(theta)*math.cos(theta)) )
        M=m*ecc_sec**2
        N=n*ecc_sec**2
        A1=N*math.sin(theta)
        A2=(.5*M)*(math.sin(theta)*math.cos(theta)-theta)
        A3=(5/2)*(N**2)*math.sin(theta)*math.cos(theta)
        A4=(M**2/16)*(11*theta-13*math.sin(theta)-8*theta*math.cos(theta)**2+10*math.sin(theta)*math.cos(theta)**3)
        A5=(M*N/2)*(3*math.sin(theta)+2*theta*math.cos(theta)-5*math.sin(theta)*math.cos(theta)**2)
        delta2=theta-A1+A2+A3+A4+A5
        B2_1=math.asin(math.sin(B1)*math.cos(delta2)+g*math.sin(delta2))
        B2_2=math.acos( ( h**2+(g*math.cos(delta2)-math.sin(B1)*math.sin(delta2))**2)**.5 )
        Lat2=math.atan2(SL.a*math.sin(B2_1),SL.b*math.cos(B2_1))
        Long2=(Long1 + L + math.atan2(math.sin(delta2)*math.sin(azimut),(math.cos(B1)*math.cos(delta2)-math.sin(B1)*math.sin(delta2)*math.cos(azimut))))
        return [Lat2, Long2]

    def LLHtoAER(self, Lat1, Long1, Lat2, Long2):
        if(Lat1 != Lat2 and Long2 != Long1):
          L=Long2-Long1;                      # Diferencia de Longitudes
          B1=math.atan2(SL.b*math.sin(Lat1),(SL.a*math.cos(Lat1)))
          B2=math.atan2(SL.b*math.sin(Lat2),(SL.a*math.cos(Lat2)))

          A=math.sin(B1)*math.sin(B2)
          B=math.cos(B1)*math.cos(B2)

          delta=math.acos(A+B*math.cos(L))
          n=(SL.a-SL.b)/(SL.a+SL.b)
          B12= Lat2-Lat1 + 2*( A*(n+n**2+n**3) - B*(n-n**2+n**3) )*math.sin(Lat1-Lat2)

          #DELTA=math.asin( ( (math.sin(L)*math.cos(B2))**2 + (math.sin(B2-B1) + 2*math.cos(B2)*math.sin(B1)*(math.sin(L/2)**2)))**.5 )
          c=B*math.sin(L)/math.sin(delta)
          m=1-c**2

          Range=SL.b*(delta*(1+SL.f+SL.f**2) + A*( (SL.f+SL.f**2)*math.sin(delta) - (SL.f*delta)**2/(2*math.sin(delta)) )
             -(m/2)*( (SL.f+SL.f**2)*(delta+math.sin(delta)*math.cos(delta)) - (SL.f*delta)**2/math.tan(delta) )
             -((A*SL.f)**2)*math.sin(delta)*math.cos(delta)
             +((SL.f*m/4)**2)*( delta + math.sin(delta)*math.cos(delta) - 2*math.sin(delta)*math.cos(delta)**3 - 8*delta**2/math.tan(delta) )
             +( ((A*SL.f)**2)*m/2 )*( math.sin(delta)*math.cos(delta)**2 + delta + delta**2/math.sin(delta) )
             +delta*(SL.f+SL.f**2) - ((A*SL.f**2)/2)*(math.sin(delta) + 2*delta**2/math.sin(delta)) )

          LAMBDA= L + c*( 0.25*m*(SL.f**2)*(math.sin(delta)*math.cos(delta) - 5*delta + 4*(delta**2)/math.tan(delta) ))
          Az=(180/math.pi)*math.atan2( math.cos(B2)*math.sin(LAMBDA),( 2*math.cos(B2)*math.sin(B1)*math.sin(LAMBDA/2)**2 + math.sin(B2-B1)  ))
          alfa21=(180/math.pi)*math.atan2(-math.cos(B1)*math.sin(LAMBDA),( 2*math.cos(B1)*math.sin(B2)*math.sin(LAMBDA/2)**2 - math.sin(B2-B1)  ))
          Az2=alfa21
        else:
          Az=0
          Range=0
          Az2=0

        vector = [Az, Range, Az2]
        return vector
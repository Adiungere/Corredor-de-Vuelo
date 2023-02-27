from SitioLanzamiento import SitioLanzamiento as SL
from Vehiculo import Vehiculo
import math


class Lanzamiento(SL, Vehiculo):
    def __init__(self, Sitio, Cohete, Azimut, Apogeo=100000, t_pitchOver=9, Gimbal=10 * math.pi / 180, PitchOverDuration=2.1):
        SL.__init__(self, Sitio.lat, Sitio.long, Sitio.alt)
        Vehiculo.__init__(self, Cohete.Tipo, Cohete.MasaCarga)
        self.Sitio=Sitio
        self.Cohete=Cohete
        self.Azimut = Azimut
        self.Apogeo = Apogeo       #Espeficiar apogeo, solo importa para suborbitales, para orbitales no importa el valor
        self.t_pitchOver = t_pitchOver  # Instante apartir del liftoff en que inicia el Gravity turn
        self.Gimbal = Gimbal
        self.PitchOverDuration = PitchOverDuration
        self.Inclinacion = math.acos(math.sin(self.Azimut)*math.cos(Sitio.lat))

    def __str__(self):
        return "Tipo:{}, Azimut:{}°, Payload:{}kg, Apogeo:{}km".format(self.Cohete.Tipo, self.Azimut*180/math.pi, self.Cohete.MasaCarga, self.Apogeo/1000)

    #creando función AERtoLLH para usar después
    def AERtoLLH(self, Lat1, Long1, azimut, Rango):
        Lat1=Lat1*math.pi/180
        Long1=Long1*math.pi/180
        azimut=azimut*math.pi/180

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
        return [Lat2*180/math.pi, Long2*180/math.pi]

    def LLHtoAER(self, Lat1, Long1, Lat2, Long2):
        Lat1=Lat1*math.pi/180
        Long1=Long1*math.pi/180
        Lat2=Lat2*math.pi/180
        Long2=Long2*math.pi/180

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
          Az=math.atan2( math.cos(B2)*math.sin(LAMBDA),( 2*math.cos(B2)*math.sin(B1)*math.sin(LAMBDA/2)**2 + math.sin(B2-B1)  ))
          alfa21=math.atan2(-math.cos(B1)*math.sin(LAMBDA),( 2*math.cos(B1)*math.sin(B2)*math.sin(LAMBDA/2)**2 - math.sin(B2-B1)  ))
          Az2=alfa21
        else:
          Az=0
          Range=0
          Az2=0
        return [Az*180/math.pi, Range, Az2*180/math.pi]

    def ECEFtoLLH(E, F, G):
        e = (2 * f - f ** 2) ** .5  # Eccentricidad
        # Calculas las coordenadas geodetic apartir de las ECEF, estos
        # valores son los que no son exactos y requeriran iteraciones
        longg = m.atan2(F, E)  # Primera aproximacion de la longitud
        latg = m.atan2(G * ((1 - f) ** -2), ((E ** 2 + F ** 2) ** .5))  # Primera aproxmacion de la latitud
        hg = (E ** 2 + F ** 2 + G ** 2) ** .5 - a_axis * ((1 - e ** 2) / (1 - (
                    e * m.cos(m.atan(G / ((E ** 2 + F ** 2) ** .5)))) ** 2)) ** .5  # Primera aproximacion de la altura

        # Prime radius of curvature. Radio de curvatura longitudinal
        Ng = a_axis / (1 - (e * m.sin(latg)) ** 2) ** .5
        # Meridian radius of curvture. Radio de curvatura latitud
        Mg = a_axis * (1 - e ** 2) * (1 - (e * m.sin(latg)) ** 2) ** -1.5

        # Imprimimos la primera aproximacion LLH. Esto solo sirve si se alguein
        # tiene interes en conocer el valor, para debuggear el programa

        LLH1 = np.array([longg, latg, hg])
        np.transpose(LLH1)
        LLH = LLH1
        # con las coordenadas LLH no exacta calcumos de nuevo las ECEF,
        # estas ECEFg tendran un error con las ECEF, esto nos servira para
        # medir el error de las LLH

        Eg = (Ng + hg) * m.cos(longg) * m.cos(latg)
        Fg = (Ng + hg) * m.sin(longg) * m.cos(latg)
        Gg = (Ng * (1 - e ** 2) + hg) * m.sin(latg)

        Error = np.array([Eg, Fg, Gg]) - np.array([E, F, G])

        # Haremos esta itereacion hasta que el error sea menor a una cantidad
        while (Error[0] ** 2 + Error[1] ** 2 + Error[2] ** 2) ** .5 > 1:
            # Matriz de transformacion
            dECEFtodENU = [[-m.sin(longg), m.cos(longg), 0],
                           [-m.cos(longg) * m.sin(latg), -m.sin(longg) * m.sin(latg), m.cos(latg)],
                           [m.cos(longg) * m.cos(latg), m.sin(longg) * m.cos(latg), m.sin(latg)]]
            dECEFtodENU = np.array(dECEFtodENU)

            # Matriz de transforacion diferencial o Tensor metrico
            dENUtodLLA = [[1 / (m.cos(latg) * (Ng + hg)), 0, 0],
                          [0, 1 / (Mg + hg), 0],
                          [0, 0, 1]]
            dENUtodLLA = np.array(dENUtodLLA)

            dECEFtodLLA = dENUtodLLA @ dECEFtodENU
            LLH = LLH - dECEFtodLLA @ Error

            longg = LLH[0]
            latg = LLH[1]
            hg = LLH[2]

            Eg = (Ng + hg) * m.cos(longg) * m.cos(latg)
            Fg = (Ng + hg) * m.sin(longg) * m.cos(latg)
            Gg = (Ng * (1 - e ** 2) + hg) * m.sin(latg)
            Ng = a_axis / (1 - (e * m.sin(latg)) ** 2) ** .5
            Mg = a_axis * (1 - e ** 2) * (1 - (e * m.sin(latg)) ** 2) ** -1.5
            Error = np.transpose([Eg, Fg, Gg]) - np.transpose([E, F, G])

        Long = (longg) * 180 / m.pi
        Lat = (latg) * 180 / m.pi
        High = hg
        return [Lat, Long, High]
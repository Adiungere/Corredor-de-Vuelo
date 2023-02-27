class Vehiculo:
    def __init__(self, Tipo, MasaCarga, Diametro = 1.2, M2Seca_P=475,M2F=2875, M2F_1Seca=3725, M_Rocket_o=13725, Cd_Min = 0.4, MaxThrust1 = 162 * 10 ** 3, MinThrust1 = 50 * 10 ** 3, ThrustSecond = 23 * 10 ** 3, t_MECO = 155, t_2Stage = 157, VJet1 = 3030, VJet2 = 3400 ):
        self.MasaCarga=MasaCarga
        self.Tipo=Tipo
        self.Diametro = Diametro  # Diametro de la seccion transversal cohete
        self.M2Seca_P = M2Seca_P  # Masa seca de la segunda etapa mas carga util
        self.M2F = M2F  # Masa total de la segunda etapa: seca, combustible, payload
        self.M2F_1Seca = M2F_1Seca  # Masa seca de la primera mas la total de la segunda
        self.M_Rocket_o = M_Rocket_o  # Masa de despuegue, Liftoff mass del cohete
        self.Cd_Min = Cd_Min
        self.Area = 3.14 * .25 * self.Diametro ** 2  # Area de la seccion transeversal

        # Lso sigueintes datso pueden substituirse por una tabla con la curva motor
        self.MaxThrust1 = MaxThrust1
        self.MinThrust1 = MinThrust1
        self.ThrustSecond = ThrustSecond
        self.t_MECO = t_MECO  # Tiempo que duran prendidos los motores de la primera etapa Main Engine Cutt Off
        self.t_2Stage = t_2Stage  # Tiempo que duran prendidos los motores de la segunda etapa
        self.t_SECO = self.t_2Stage + self.t_MECO  # Isntante en que se apagan los motores de la Segunda Etapa. Second Engien Cut Off
        self.VJet1 = VJet1  # Velocidad de los gases de escape de la primera etapa
        self.VJet2 = VJet2  # Velocidad de los gases de escape de la primera etapa
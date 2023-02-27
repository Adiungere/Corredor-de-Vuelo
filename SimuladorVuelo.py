# -*- coding: utf-8 -*-
"""SimuladorVuelo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UniX2ps1vvhTd4oy2ejQ5j0xZrSvqV1m
"""

# Commented out IPython magic to ensure Python compatibility.
# Este programa sirve para generar traectorias nominal es de proyectiles.
# Lanzamiento de cohetes desde cualquier punto de la tierra con culaquier
# velocidad inicial(Incluyendo lanzamientos desde aviones)

#Este programa un entrega txt con la posicion de las 2 etapas de un cohete
# en diferentes sistemas de referencia, incluyendo la velocidad en ENU 

# 1) Colocar una coordenada Geodetica oringen del sitio de lanzamiento
# 2) Pasar esa coordenada a ECEF y de ahi pasarla ENU el cual sera nuestro
# origen ENUo
# 3) Colocar parametros del cohete
# 4) Especificar instante en que se ejecuta el pitchover manuever, azimuth 
# y zenith. Estos parametros dependeran de la orbita a la que se desee llegar

# 5)Simular la Dinamica del cohete en sitema cartesiano apartir
# del ENUo, para consderar rotacion de la tierra pasar de ENU a ECEF y de
# ahi a ECI
# 6) Con los datos en ENU generar todas los demas: ECEF/ECI, Geodetic, AER
# 7) Al acabar la simulacion del cohete, lo datos de posicion y velocidad se
# guarda en un archivo ".txt", puede cambiarse el nombre
# 8) Se grafican trayectorias y proyecciones de interes

# ya que las ecuaciones para pasar de ECEF a LLH no son muy precisas se
# implemto un metodo de Newton Rapson de 3 dimesiones con ayuda de las
# matrices de transfomracion de lso diferentes sistemas de coordenadas
# "Tensor metrico"

#              [dLong] [-m.cos(latg)*m.sin(longg)*(Ng+hg), m.cos(latg)*m.cos(longg)*(Ng+hg),                 0][dE]
# dECEFtodLLH=  [dLat]=[-m.cos(longg)*m.sin(latg)*(Mg+hg),-m.sin(latg)*m.sin(longg)*(Mg+hg), m.cos(latg)*(Mg+hg)][dF]
#                [dH]  [           m.cos(latg)*m.cos(longg),       m.cos(latg)*m.sin(longg),         m.sin(latg)][dG]

# ENU, East North Up o local, plano tangente al 
# ECEF o EFG, Earth Centered Earth fixed, un sistema cartesiano
# Geodetic o LLH, Elipsoide WGS84, no es lo mismo que geocentrico, aqui
# solo se ocupa geodesico geodetic
# AER, Azimuth Elevation Range

# ------------------------
#      MEJORAS
#   Se utilza una velocidad del sonido constante SpeedSound. Esta en realidad no 
#   es constante, ya que la Temperatura cambia mucho con la altura. Agreguenlo
#   
#   No Considera el Efecto de la Rotacion de la Tierra, Sistema ECI. Importante Agregarlo
#
#   Considerar Armonicos Gravitacionales. Afectan considerablemente la trayectoria, sobretodo
#   Influyen en el angulo incial de la Gravity Turn
#
#   Graficar Trayectoria en 3D como si se puede en Matlab
#
#   Hacer un programa Anterior a este para analizar, con otras ecuaciones, o metodo analiticos 
#   Lso parametros orbitales deseados y tunearlos/optimizarlos/calibrarlos aqui
#
#   Usar este algoritmo como programa central en una rutina superior de optimizacion por
#   Fuerza bruta
#
#   Se modela como una Masa Puntual, Asi esta bien, no veo necesario modelarlo como
#   Como Cuerpo Rigido. No aqui. Pueden copiar este codigo para utilzarlo para ahcer 
#   en un programa especial para control de cohete y efectos de actuadores rotacionales
#

#---------------------------

import math as m
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

#Parametro de la Tierra

Geodetic1=[np.array([0,0,0])]
Geodetic2=[np.array([0,0,0])]
ECEF1=[np.array([0, 0, 0])]
ECEF2=ECEF1

AER1=[np.array([0,0,0])]
AER2=[np.array([0,0,0])]
ENU1=[np.array([0,0,0])]
ENU2=[np.array([0,0,0])]
Direccion1=[np.array([0,0,0])]
Direccion2=[np.array([0,0,0])]
DireccionG1=[np.array([0,0,0])]
DireccionG2=[np.array([0,0,0])]
Vel_ENU1=[np.array([0,0,0])]
Vel_ENU2=[np.array([0,0,0])]
M_Rocket1=[0]
M_Rocket2=[0]
Gravity1=[np.array([0,0,0])]
Gravity2=[np.array([0,0,0])]
Drag1=[np.array([0,0,0])]
Drag2=[np.array([0,0,0])]

DRAG1=[0]
Empuje1=[0]
DRAG2=[0]
Empuje2=[0]
Speed1=[0]
Speed2=[0]
Weigth1=[0]
Weigth2=[0]

Drag2=[np.array([0,0,0])]
Thrust1=[np.array([0,0,0])]
Thrust2=[np.array([0,0,0])]

Acc_ENU1=[np.array([0,0,0])]
Acc_ENU2=[np.array([0,0,0])]

#----------------------------------

# Parametrso del lanzamiento
file=open('ResultadosSimulador/BajaCaliforniaPolar', 'wt')     # Abrir el Archivo donde se guardaran los datos de la trayectoria nominal


latitud_o=(pi/180)*(origin[0])
longitud_o=(pi/180)*(origin[1])
ho=origin[2];
LLH=[latitud_o, longitud_o, ho]
Geodetic1[0]=[origin[0], origin[1], origin[2]*10**-3]
Geodetic2[0]=[origin[0], origin[1], origin[2]*10**-3]

# Origen en EFG o ECEF
No=a_axis/( 1-(e*m.sin(latitud_o))**2 )**.5;
Eo=(No+ho)*m.cos(longitud_o)*m.cos(latitud_o);
Fo=(No+ho)*m.sin(longitud_o)*m.cos(latitud_o);
Go=(No*(1-e**2)+ho)*m.sin(latitud_o);
ECEF1[0]=[Eo, Fo, Go]


# ECEF to ENU
ENUtoECEF=[  [-m.sin(longitud_o), -m.cos(longitud_o)*m.sin(latitud_o),   m.cos(longitud_o)*m.cos(latitud_o)],
             [ m.cos(longitud_o), -m.sin(longitud_o)*m.sin(latitud_o),   m.sin(longitud_o)*m.cos(latitud_o)],
             [                 0,                    m.cos(latitud_o),                     m.sin(latitud_o)]]
ENUtoECEF=np.array(ENUtoECEF)

ECEFtoENU=[[                 -m.sin(longitud_o),                    m.cos(longitud_o),                0 ],
           [-m.cos(longitud_o)*m.sin(latitud_o),  -m.sin(longitud_o)*m.sin(latitud_o),  m.cos(latitud_o)],
           [ m.cos(longitud_o)*m.cos(latitud_o),   m.sin(longitud_o)*m.cos(latitud_o),  m.sin(latitud_o)]]
ECEFtoENU=np.array(ECEFtoENU)


ENU1[0]=[0, 0, 0];
ENU2[0]=ENU1[0];


# Direccion a que apunta el cohete durante la pitch over manuever.
# Realmente esto es un proceso de dincamica del cuerpo rigido pero por
# simplesa lo ejecuto con un cambio en la direccion del vector de
# propulsion


# Esta direccion esta en ENU, osea que emepzamo apuntando hacia arriba
Direccion1[0]=np.array([0, 0, 1])  

Vel_ENU1[0]=.1*Direccion1[0];
Vel_ENU2[0]=Vel_ENU1[0];
M_Rocket1[0]=M_Rocket_o
M_Rocket2[0]=M2F

t=[0];
dt=.2;
##  Se generara una trayectoria en ENU
# j sera nuestro indice

for j in range(0,3000):
#----------------------------
  Geodetic1.append(np.array( Geodetic1[j] ))
  Geodetic2.append(np.array( Geodetic2[j] ))
  ECEF1.append(np.array([0,0,0]))
  ECEF2.append(np.array([0,0,0]))
  AER1.append(np.array([0,0,0]))
  AER2.append(np.array([0,0,0]))
  ENU1.append(np.array([0,0,0]))
  ENU2.append(np.array([0,0,0]))
  Direccion1.append(np.array([0,0,0]))
  Direccion2.append(np.array([0,0,0]))
  DireccionG1.append(np.array([0,0,0]))
  DireccionG2.append(np.array([0,0,0]))
  Vel_ENU1.append(np.array([0,0,0]))
  Vel_ENU2.append(np.array([0,0,0]))
  M_Rocket1.append(0)
  M_Rocket2.append(0)
  Gravity1.append(np.array([0,0,0]))
  Gravity2.append(np.array([0,0,0]))
  Drag1.append(np.array([0,0,0]))
  Drag2.append(np.array([0,0,0]))

  DRAG1.append(0)
  Empuje1.append(0)
  DRAG2.append(0)
  Empuje2.append(0)
  Speed1.append(0)
  Speed2.append(0)
  Weigth1.append(0)
  Weigth2.append(0)

  Drag2.append(np.array([0,0,0]))
  Thrust1.append(np.array([0,0,0]))
  Thrust2.append(np.array([0,0,0]))

  Acc_ENU1.append(np.array([0,0,0]))
  Acc_ENU2.append(np.array([0,0,0]))
  t.append(t[j])

# -----------------------
  #M_Rocket1.append(0)
  #M_Rocket2.append(0)
  #Vel_ENU1.append(np.array([0,0,0]))
  #Vel_ENU2.append(np.array([0,0,0]))
  #ENU1.append(np.array([0,0,0]))
  #ENU2.append(np.array([0,0,0]))
  #ECEF1.append(np.array([0,0,0]))
  #ECEF2.append(np.array([0,0,0]))
  #Geodetic1.append(np.array([0,0,0]))
  ##Geodetic2.append(np.array([0,0,0]))
  #AER1.append(np.array([0,0,0]))
  #AER2.append(np.array([0,0,0]))
#----------------------
  # Calcular a dinamica de vuelo de la primera etapa miestras se encuentre
  # en el aire, por encima del suelo
  if Geodetic1[j][2]>=0:
    # Calculo Dinamico dle Cohete
    #Gravedad
    R1=(ECEF1[j][0]**2+ECEF1[j][1]**2+ECEF1[j][2]**2)**.5;     # Dstancia al Centro de la Tierra   
    Gravity1[j]=-ECEFtoENU@ECEF1[j]*Mu*EarthMass/(R1**3);  # Vector de Gravedad
    Weigth1[j]=M_Rocket1[j]*(Gravity1[j][0]**2+Gravity1[j][1]**2+Gravity1[j][2]**2)**.5;
    DireccionG1[j]=Gravity1[j]/(Gravity1[j][0]**2+Gravity1[j][1]**2+Gravity1[j][2]**2)**.5; # Direccion de Gravedad
    
    # Drag
    rho1=1.3*m.exp(-Geodetic1[j][2]/7000);          # Densidad Standard de la atmosfera
    Speed1[j]=(Vel_ENU1[j][0]**2+Vel_ENU1[j][1]**2+Vel_ENU1[j][2]**2)**.5;    # Magnitud de la velocidad
    Mach1=Speed1[j]/SpeedSound;                                            #Numero de Mach

    #Parametros para calcular el cofiente de arrastre Supersonico
    p1 = 0.6387;p2 =-2.569;p3 = 4.717;p4 =-1.924;p5 =-3.301;p6 = 2.513;
    q1 =-4.526;q2 = 8.368;q3 =-5.147;q4 =-1.908;q5 = 2.27;
    Cd1 = Cd_Min*(p1*Mach1**5 + p2*Mach1**4 + p3*Mach1**3 + p4*Mach1**2 + p5*Mach1 + p6) / (Mach1**5 + q1*Mach1**4 + q2*Mach1**3 + q3*Mach1**2 + q4*Mach1 + q5); # coefientie de arrastre

    Drag1[j]=-Cd1*A_Rocket*(.5*rho1*Vel_ENU1[j]*Speed1[j]); #vector de Feurrza de arrastre
    DRAG1[j]=-Cd1*A_Rocket*.5*rho1*Speed1[j]**2;
    # Propulsion del motor. La direcion al inicio es paralela a la gravedad
    # despues se ejecuta la pitchover manuever para dirigir el cohete a la
    # orbita deseada. La fuerza acaba cuando el la masa del la de la etapa igual a su masa seca

    if  M_Rocket1[j]>M2F_1dry:
      T1=MaxThrust1 + MinThrust1*(M_Rocket1[j]/M2F_1dry)**.3;         #Magnitud de empuje
      Empuje1[j]=T1;
      t_MECO=t[j];

      #Ascenso vertical
      if t[j]<t_pitchOver:
        Thrust1[j]=-DireccionG1[j]*T1;     #Vector de Empuje 
        M_flow1=T1/VJet1;      #Flujo de masa del Motor
      
      # Pitchover manuever
      if  t_pitchOver<=t[j] and t[j]<=t_pitchOver+PitchOverDuration:
        Zenith=m.atan2(Vel_ENU1[j][2], (Vel_ENU1[j][0]**2+Vel_ENU1[j][1]**2)**.5)
        Direccion1[j]=np.array([m.cos(Zenith-Gimbal)*m.sin(Azimuth), m.cos(Zenith-Gimbal)*m.cos(Azimuth), m.sin(Zenith-Gimbal) ]);
        Thrust1[j]=Direccion1[j]*T1;
      
      
      # Gravity turn manuever
      if  t_pitchOver+PitchOverDuration<t[j]:
        Direccion1[j]=Vel_ENU1[j]/Speed1[j];
        Thrust1[j]=Direccion1[j]*T1;
      

    else:
      # Registrar instante del MECO
      if t[j]<t_MECO+2*dt:
        iMeco=j;
      
      # Coasting fligth
      Direccion1[j]=Vel_ENU1[j]/Speed1[j];
      Thrust1[j]=Direccion1[j]*0;
      M_flow1=0; 
      Empuje1[j]=0;
    

    M_Rocket1[j+1]=M_Rocket1[j] - M_flow1*dt;  #Actualizar Masa del cohete
    
    # Vector accelaracion en cordenadas Locales, ENU
    Acc_ENU1[j]=Gravity1[j] + (Drag1[j]+Thrust1[j])/M_Rocket1[j]; 
    
    # Vector velocidad en coordenadas Locales, ENU
    Vel_ENU1[j+1]=Vel_ENU1[j]+Acc_ENU1[j]*dt;

    # Vector de posicion en coordenadas ENU, ENU
    ENU1[j+1]=ENU1[j]+Vel_ENU1[j]*dt;

    #ENU to ECEF, obtenems la ubiciacion del cohete el coordenadas ECEF
    ECEF1[j+1]=ECEF1[0]+ENUtoECEF@ENU1[j+1];

    #ECEF to Geocentric, se hara un calculo que requiere varias iteracion
    #por punto fijo. Pasar de ECEF a Gecentric no es exacta requeire varias
    #iteraciones, los valores con "g" estaran cambiando con cada iteracion    
    # El objetivo de esto era calcualr el cambio de las coordenaradas
    # geocetricas y ECEF apartir del movienito del cohete en las coordenadas
    # ENU por lo que guadamos el dato de las nuevas geocentricas
    Geodetic1[j+1]= ECEFtoLLH(ECEF1[j+1][0], ECEF1[j+1][1], ECEF1[j+1][2]);#   [LLH[0] LLH[1] LLH[2]*10**-3];

    # Azimuth-elevation-range AER from ENU
    [Az, Range, Az2]=LLHtoAER(latitud_o, longitud_o, (pi/180)*(Geodetic1[j][0]), (pi/180)*(Geodetic1[j][1]));
    AER1[j+1]=[Az, m.atan2(ENU1[j][2],(ENU1[j][1]**2+ENU1[j][0]**2)**.5),Range]

    # ECI
#   theta=omega*t[j]
#   ECEFtoECI=[ m.cos(theta) -m.sin(theta) 0;
#               m.sin(theta)  m.cos(theta) 0;
#                          0           0  1];
#   ECI1[j+1]=ECEFtoECI*ECEF1[j]
    
    # Registrar la ultima ubicacion de la dinamica del cohete. Esto
    # para conocer el Immpacto Point IP
    jIP=j

  

  # Si la altura es menos que la del suelo, significa que el la primera 
  # etapa ya impacto con el suelo, por lo que conservara su ultima
  # posicion y tendra velocidad 0
  if Geodetic1[j][2]<0:
    Vel_ENU1[j+1]=[0, 0, 0];
    ENU1[j+1]=ENU1[j]
    ECEF1[j+1]=ECEF1[j]
    Geodetic1[j+1]=Geodetic1[j]
    AER1[j+1]=AER1[j]
    M_Rocket1[j+1]=M_Rocket1[j]
    Weigth1[j+1]=0;
    DRAG1[j+1]=0;
    Empuje1[j+1]=0;
    Speed1[j+1]=0;

  # ---------------------------------------------------------
  # Trayectoia de la segunda etapa
  # ---------------------------------------------------------

  #Gravedad    
  R2=(ECEF2[j][0]**2+ECEF2[j][1]**2+ECEF2[j][2]**2)**.5;     # Dstancia al Centro de la Tierra   
  Gravity2[j]=-ECEFtoENU@ECEF2[j]*Mu*EarthMass/(R2**3);  # Vector de Gravedad
  Weigth2[j]=M_Rocket2[j]*(Gravity2[j][0]**2+Gravity2[j][1]**2+Gravity2[j][2]**2)**.5;
  DireccionG2[j]=Gravity2[j]/(Gravity2[j][0]**2+Gravity2[j][1]**2+Gravity2[j][2]**2)**.5; # Direccion de Gravedad
  
  # Drag
  rho2=1.3*m.exp(-Geodetic2[j][2]/7000);          # Densidad Standard de la atmosfera
  Speed2[j]=(Vel_ENU2[j][0]**2+Vel_ENU2[j][1]**2+Vel_ENU2[j][2]**2)**.5;    # Magnitud de la velocidad
  Mach2=Speed2[j]/SpeedSound;                                             #Numero de Mach

  #Parametros para calcular el cofiente de arrastre Supersonico
  Cd2 = Cd_Min*(p1*Mach2**5 + p2*Mach2**4 + p3*Mach2**3 + p4*Mach2**2 + p5*Mach2 + p6) /(Mach2**5 + q1*Mach2**4 + q2*Mach2**3 + q3*Mach2**2 + q4*Mach2 + q5); # coefientie de arrastre

  Drag2[j]=-Cd2*A_Rocket*(.5*rho2*Vel_ENU2[j]*Speed2[j]); #vector de Feurrza de arrastre
  DRAG2[j]=-Cd2*A_Rocket*.5*rho2*Speed2[j]**2;
  # Propulsion del motor. La direcion al inicio es paralela a la gravedad
  # despues se ejecuta la pitchover manuever para dirigir el cohete a la
  # orbita deseada. La fuerza acaba cuando la masa iguala al masa seca de
  # la segunda etapa

  Direccion2[j]=Vel_ENU2[j]/Speed2[j];
  if M_Rocket1[j]<=M2F_1dry: 
    if M_Rocket2[j]>M2dry_P:
      T2=(ThrustSecond);         #Magnitud de empuje
      Empuje2[j]=T2;
      Thrust2[j]=Direccion2[j]*T2;
      M_flow2=T2/VJet2;
      t_SECO=t[j];
    else:
      if t[j]<t_SECO+2*dt:
          iSeco=j;
      
      # Coasting fligth
      Thrust2[j]=Direccion2[j]*0;
      M_flow2=0; 
      Empuje2[j]=0;
    

    if t[j]<t_MECO+2*dt:
      iMeco=j;
      
  else:
    M_flow2=0;
    Thrust2[j]=Thrust1[j];


  M_Rocket2[j+1]=M_Rocket2[j] - M_flow2*dt;  #Actualizar Masa del cohete
  
  # Vector accelaracion en cordenadas Locales, ENU
  if t_MECO<t[j]:
    Acc_ENU2[j]=Gravity2[j] + (Drag2[j]+Thrust2[j])/M_Rocket2[j]; 
  else:
    Acc_ENU2[j]=Acc_ENU1[j];
  
  
  # Vector velocidad en coordenadas Locales, ENU
  Vel_ENU2[j+1]=Vel_ENU2[j]+Acc_ENU2[j]*dt;

  # Vector de posicion en coordenadas ENU, ENU
  ENU2[j+1]=ENU2[j]+Vel_ENU2[j]*dt;

  #ENU to ECEF, obtenems la ubiciacion del cohete el coordenadas ECEF
  ECEF2[j+1]=ECEF2[0]+ENUtoECEF@ENU2[j+1];

  #ECEF to Geocentric, se hara un calculo que requiere varias iteracion
  #por punto fijo. Pasar de ECEF a Gecentric no es exacta requeire varias
  #iteraciones, los valores con "g" estaran cambiando con cada iteracion    
  # El objetivo de esto era calcualr el cambio de las coordenaradas
  # geocetricas y ECEF apartir del movienito del cohete en las coordenadas
  # ENU por lo que guadamos el dato de las nuevas geocentricas
  Geodetic2[j+1]= ECEFtoLLH(ECEF2[j+1][0], ECEF2[j+1][1], ECEF2[j+1][2]);#   [LLH[0] LLH[1] LLH[2]*10**-3];

  # Azimuth-elevation-range AER from ENU
  [Az, Range, Az2]=LLHtoAER(latitud_o, longitud_o, (pi/180)*(Geodetic2[j][0]), (pi/180)*(Geodetic2[j][1]));
  AER2[j+1]=[Az, m.atan2(ENU2[j][2],(ENU2[j][1]**2+ENU2[j][0]**2)**.5),Range]


  t[j+1]=t[j]+dt;


## Graficar
# Geodetic1
# ENU1
# ECEF1
# AER1

# Plot your track
Geodetic1=np.array(Geodetic1)
AER1=np.array(AER1)
Geodetic2=np.array(Geodetic2)
AER2=np.array(AER2)
M_Rocket1=np.array(M_Rocket1)
M_Rocket2=np.array(M_Rocket2)
ENU1=np.array(ENU1)
ENU2=np.array(ENU2)

#
fig1 = plt.figure(1)
plt.plot(t[:-1], Geodetic1[:-1,2]/1000, t[:-1], Geodetic2[:-1,2]/1000)
plt.LineWith=4
plt.title("Altitud[km] vs Tiempo[s]")
plt.ylabel("km")
plt.xlabel("s")
plt.legend(['Etapa 1','Etapa 2'])
#
fig2 = plt.figure(2)
plt.plot(AER1[:-1,2]/1000, Geodetic1[:-1,2]/1000, AER2[:-1,2]/1000, Geodetic2[:-1,2]/1000)
plt.title("Altitud[km] vs Rango[km]")
plt.ylabel("km")
plt.xlabel("km")
plt.legend(['Etapa 1','Etapa 2'])

fig3 = plt.figure(3)
plt.plot(t, M_Rocket1, t, M_Rocket2)
plt.title("Masa Vehiculo[kg] vs Tiempo[s]")
plt.ylabel("kg")
plt.xlabel("s")
plt.legend(['Etapa 1','Etapa 2'])

fig4 = plt.figure(4)
plt.plot(t[:-1], Speed1[:-1], t[:-1], Speed2[:-1])
plt.title("Velocidad[m/s] vs Tiempo[s]")
plt.ylabel("m/s")
plt.xlabel("s")
plt.legend(['Etapa 1','Etapa 2'])

fig5 = plt.figure(5)
plt.plot(t, Empuje1, t, Empuje2, t, DRAG1, t, DRAG2, t, Weigth1, t, Weigth2)
plt.title("Fuerzas[N] vs Tiempo[s]")
plt.ylabel("kN")
plt.xlabel("s")
plt.legend(['Empuje1',' Empuje2', 'Arrastre1', 'Arrastre2', 'Peso1', 'Peso2'])

#
fig7 = plt.figure(7)
ax = plt.axes(projection='3d')
plt.title("Este, Norte, Arriba")
ENU1=np.array(ENU1)
ax.scatter3D(ENU1[:,0], ENU1[:,1], ENU1[:,2],  cmap='Greens');
ax.scatter3D(ENU2[:,0], ENU2[:,1], ENU2[:,2],  cmap='Greens');

#
  #creando mapa y primer vector para graficar
fig = go.Figure(data=go.Scattergeo( lat=[latitud_o * 180 / m.pi], lon=[longitud_o * 180 / m.pi], mode='markers'))
fig.add_trace        (go.Scattergeo(lat= Geodetic1[0:iMeco,0],    lon= Geodetic1[0:iMeco,1],     mode='lines'))
fig.add_trace(       go.Scattergeo( lat=[Geodetic1[iMeco][0]],     lon=[Geodetic1[iMeco][1]],      mode='markers'))
fig.add_trace(       go.Scattergeo( lat= Geodetic2[iMeco:,0] ,    lon= Geodetic2[iMeco:,1],      mode='lines'))
fig.add_trace(       go.Scattergeo( lat=[Geodetic1[iSeco,0]],     lon=[Geodetic1[iSeco,1]],      mode='markers'))
fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True, fitbounds="locations")
fig.show()

plt.show()

#TrayectoriaCSV
TrayectoriaName="Trayectoria"+"_"+str((180/m.pi)*latitud_o)+"_" + str((180/m.pi)*longitud_o) + "_" + str((180/m.pi)*Azimuth)+".txt"

encabezado='Tiempo, VelENU1_E, VelENU1_N, VelENU1_U, ENU1_E, ENU1_N, ENU1_U, ECEF1_E, ECEF1_F, ECEF1_G, LLH1_Lat, LLH1_Long, LLH1_High, AER1_Az, AER1_El, AER1_R, VelENU2_E, VelENU2_N, VelENU2_U, ENU2_E, ENU2_N, ENU2_U, ECEF2_E, ECEF2_F, ECEF2_G, LLH2_Lat, LLH2_Long, LLH2_High, AER2_Az, AER2_El, AER2_R'
TrayectoriaCSV = open(TrayectoriaName, "a")
TrayectoriaCSV.write(encabezado + "\n")

for i in range(0,iSeco,5):
  ss1=   str(m.floor(t[i]))            + ","+ str(m.ceil(Vel_ENU1[i][0]))  + ","+ str(m.ceil(Vel_ENU1[i][1]))  + ","+ str(m.ceil(Vel_ENU1[i][2]))  + ","
  ss2=   str(m.ceil(ENU1[i][0]))       + ","+ str(m.ceil(ENU1[i][1]))      + ","+ str(m.ceil(ENU1[i][2]))      + "," 
  ss3=   str(m.floor(ECEF1[i][0]))     + ","+ str(m.floor(ECEF1[i][1]))    + ","+ str(m.floor(ECEF1[i][2]))    + "," 
  ss4=   str(Geodetic1[i][0])          + ","+ str(Geodetic1[i][1])         + ","+ str(Geodetic1[i][2])         + "," 
  ss5=   str(AER1[i][0])               + ","+ str(AER1[i][1])              + ","+ str(AER1[i][2])              + "," 
  ss6=   str(m.ceil( Vel_ENU2[i][0]))  + ","+ str(m.ceil(Vel_ENU2[i][1]))  + ","+ str(m.ceil(Vel_ENU2[i][2]))  + ","
  ss7=   str(m.ceil(ENU2[i][0]))       + ","+ str(m.ceil(ENU2[i][1]))      + ","+ str(m.ceil(ENU2[i][2]))      + "," 
  ss8=   str(m.floor(ECEF2[i][0]))     + ","+ str(m.floor(ECEF2[i][1]))    + ","+ str(m.floor(ECEF2[i][2]))    + "," 
  ss9=   str(Geodetic2[i][0])          + ","+ str(Geodetic2[i][1])         + ","+ str(Geodetic2[i][2])         + "," 
  ss10=  str(AER2[i][0])               + ","+ str(AER2[i][1])              + ","+ str(AER2[i][2])
  SS=ss1+ss2+ss3+ss4+ss5+ss6+ss7+ss8+ss9+ss10
  print(SS)
  TrayectoriaCSV.write(SS+"\n")
TrayectoriaCSV.close()
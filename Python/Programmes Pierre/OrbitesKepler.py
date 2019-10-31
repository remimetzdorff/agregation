# -*- coding: utf-8 -*-

#Nom du programme : OrbitesKepler

#Auteurs : François Lévrier, Arnaud Raoux et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.10

#Liste des modifications
#v 1.00 : 2016-05-15 Première version complète
#v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor

#Version de Python
# 3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


#Description : 
#Ce programme permet d'illustrer les orbites de deux astres, dont les masses peut être changées. Ces masses sont mesurées soit en masses solaires, soit en masses terrestres. En rouge et bleu sont tracées les trajectoires des deux astres. L'excentricité e, le demi-grand axe a et l'angle initial theta_0 peuvent être changés.


# =============================================================================
# --- Importation de modules Python--------------------------------------------
# =============================================================================


import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons



# =============================================================================
# --- Constantes--------------------------------------------
# =============================================================================

G=6.67408e-11 # Constante de la gravitation en m3.kg-1.s-2
Msun=1.988e30 # Masse du Soleil en kg
Mearth=5.9722e24 # Masse de la Terre en kg
UA=1.495978707e11 # Unite astronomique en m
an=365.0*86400. # annee en s
liste_unite_de_masse=('Masse solaire', 'Masse terrestre')


# =============================================================================
# --- Création de la figure --------------------------------------------
# =============================================================================

fig=plt.figure()
plt.subplots_adjust(left=0., bottom=0.3)
ax = fig.add_subplot(111, aspect='equal')

# Creation de l'axe des abscisses, ici les angles de 0 a 2pi
theta=np.linspace(0.000001,2.0*math.pi-0.000001,num=10000)

# Parametres de la fonction, avec des valeurs par defaut
init_theta0 = 0.0 # Angle du periastre, en degres
init_M1_val = 1.0 # Masse de l'astre 1, unite definie par M1_unit
init_M1_unit= 'Masse solaire' # Unite de la masse de l'astre 1, peut etre 'Masse solaire' pour une masse solaire, ou 'Masse terrestre' pour une masse terrestre 
init_M2_val = 1.0 # Masse de l'astre 2, unite definie par M2_unit
init_M2_unit= 'Masse terrestre' # Unite de la masse de l'astre 2, peut etre 'Masse solaire' pour une masse solaire, ou 'Masse terrestre' pour une masse terrestre 
init_a_UA = 4.0 # demi grand axe exprime en UA
init_e=0.0 # Excentricite
M1_unit=init_M1_unit
M2_unit=init_M2_unit

# Fonction retournant la masse en kg
def mass(M_val,M_unit):
    if (M_unit=="Masse solaire"):M=M_val*Msun
    if (M_unit=="Masse terrestre"):M=M_val*Mearth    
    return(M)

# Creation de la fonction a tracer 
def trace(theta0,M1_val,M1_unit,M2_val,M2_unit,a_UA,e):
    M1=mass(M1_val,M1_unit)
    M2=mass(M2_val,M2_unit)
    a=a_UA*UA
    # Masse reduite
    mu=M1*M2/(M1+M2)
    # Facteur K de la force centrale F=-K/r2
    K=G*M1*M2
    L=math.sqrt(K*mu*a*(1.0-math.pow(e,2.0)))
    theta0_rad=(math.pi/180.)*theta0
    p=math.pow(L,2.0)/(K*mu)
    # Mouvement de la particule fictive
    r=p/(1+e*np.cos(theta-theta0_rad))
    # Projection de ce mouvement, converti en UA
    x=r*np.cos(theta)/UA
    y=r*np.sin(theta)/UA
    # Mouvement de l'objet M1
    x1=-(M2/(M1+M2))*x
    y1=-(M2/(M1+M2))*y
    # Mouvement de l'objet M2
    x2=(M1/(M1+M2))*x
    y2=(M1/(M1+M2))*y
    return(x,y,x1,y1,x2,y2)

x,y,x1,y1,x2,y2=trace(init_theta0,init_M1_val,init_M1_unit,init_M2_val,init_M2_unit,init_a_UA,init_e)

# Creation de la trace de la fonction s en fonction de t. C'est un objet qui est sauvegarde dans 'l'
l,=plt.plot(x,y,'k-',lw=2)
l1,=plt.plot(x1,y1,'r-',lw=2)
l2,=plt.plot(x2,y2,'b-',lw=2)

# Specification des limites des axes (xmin,xmax,ymin,ymax)
plt.axis([-10.0, 10.0, -10.0, 10.0])

# Creation des barres de modification amplitude et frequence
axcolor = 'lightgoldenrodyellow'
axtheta0 = plt.axes([0.07, 0.07, 0.85, 0.03], facecolor=axcolor)
axM1 = plt.axes([0.07, 0.19, 0.85, 0.03], facecolor=axcolor)
axM2 = plt.axes([0.07, 0.16, 0.85, 0.03], facecolor=axcolor)
axa = plt.axes([0.07, 0.1, 0.85, 0.03], facecolor=axcolor)
axe = plt.axes([0.07, 0.13, 0.85, 0.03], facecolor=axcolor)
stheta0 = Slider(axtheta0, r'$\theta_0$', 0.0, 180.0, valinit=init_theta0) # Remarquer la valeur initiale init_theta0
sM1 = Slider(axM1, r'$M_1$', 0.1, 10.0, valinit=init_M1_val) # Remarquer la valeur initiale init_theta0
sM2 = Slider(axM2, r'$M_2$', 0.1, 10.0, valinit=init_M2_val) # Remarquer la valeur initiale init_theta0
sa = Slider(axa, r'$a$', 0.1, 10.0, valinit=init_a_UA) # Remarquer la valeur initiale init_theta0
se = Slider(axe, r'$e$', 0.0, 0.9999999, valinit=init_e) # Remarquer la valeur initiale init_theta0
# Creation des menus de changement des unites des masses
rax_M1_unit = plt.axes([0.7, 0.6, 0.22, 0.15], facecolor=axcolor,title=r'$M_1$'+' '+'[Unit]')
radio_M1_unit = RadioButtons(rax_M1_unit, liste_unite_de_masse, active=0) # La valeur par defaut est la numero 0 (Masse solaire)
rax_M2_unit = plt.axes([0.7, 0.3, 0.22, 0.15], facecolor=axcolor,title=r'$M_2$'+' '+'[Unit]')
radio_M2_unit = RadioButtons(rax_M2_unit, liste_unite_de_masse, active=1) # La valeur par defaut est la numero 1 (Masse terrestre)

# Fonction pour recuperer la valeur d'un bouton radio
def activated_radio_button(x,list):     
    for i in np.arange(len(x.circles)):
                if x.circles[i].get_facecolor()[0]<.5:
                    return list[i]

# Fonction de mise a jour du graphique
def update(val):    
    a_UA=sa.val # Mise a jour du demi-grand axe
    e=se.val # Mise a jour de l'excentricite
    M1_val=sM1.val # Mise a jour de la masse de l'astre 1
    M2_val=sM2.val # Mise a jour de la masse de l'astre 2
    M1_unit = activated_radio_button(radio_M1_unit,liste_unite_de_masse) # Mise a jour de l'unite de la masse de l'astre 1
    M2_unit = activated_radio_button(radio_M2_unit,liste_unite_de_masse) # Mise a jour de l'unite de la masse de l'astre 2
    theta0=stheta0.val # Mise a jour de l'angle du periastre
    x,y,x1,y1,x2,y2=trace(theta0,M1_val,M1_unit,M2_val,M2_unit,a_UA,e) # Calcul des traces 
    # Mise a jour des traces
    l.set_xdata(x)
    l.set_ydata(y)
    l1.set_xdata(x1)
    l1.set_ydata(y1)
    l2.set_xdata(x2)
    l2.set_ydata(y2)
    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut

# lorsqu'une barre ou un bouton radio est modifie, on applique la fonction update
sa.on_changed(update)
se.on_changed(update)
stheta0.on_changed(update)
sM1.on_changed(update)
sM2.on_changed(update)
radio_M1_unit.on_clicked(update)
radio_M2_unit.on_clicked(update)

plt.show() # On provoque l'affichage a l'ecran

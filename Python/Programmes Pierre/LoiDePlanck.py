#Nom du programme : LoiDePlanck

#Auteurs : François Lévrier, Emmanuel Baudin, Arnaud Raoux et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.20

#Liste des modifications
#v 1.00 : 2016-03-01 Première version complète
#v 1.10 : 2016-05-02 Mise à jour de la mise en page - baudin@lpa.ens.fr
#v 1.20 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor


#Version de Python
#3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#AVERTISSEMENT
#Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

#Description : 
#Ce programme représente la loi de Wien du corps noir en fonction de la fréquence du rayonnement électromagnétique. Il est possible de modifier la température du corps noir pour observer les effets. 
#Les lois de Rayleigh-Jeans et de Planck ont aussi été implémentées pour comparaison.

#import des bibliothèques python
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

#Definition des constantes physiques
def constant(symbol):
    if (symbol=="c"): return(299792.458) # Speed of light, in km/s
    elif (symbol=="h"): return(6.6260693e-34) # Planck constant in J.s
    elif (symbol=="k"): return(1.3806505e-23) # Boltzmann constant in J/K
    elif (symbol=="e"): return(1.60217653e-19) # Elementary electrical charge
    elif (symbol=="me"): return(9.1093826e-31) # Electron mass in kg
    elif (symbol=="mp"): return(1.67262171e-27) # Proton mass in kg
    elif (symbol=="G"): return(6.6742e-11) # Gravitational constant
    elif (symbol=="Na"): return(6.0221415e23) # Avogadro's number
    elif (symbol=="mu0"): return(12.566370614e-7) # Magnetic permeability
    elif (symbol=="epsilon0"): return(8.854187817e-12) # Electric permittivity
    elif (symbol=="amu"): return(1.66053886e-27)  # Atomic mass unit
    elif (symbol=="nu0_HI"): return(1420.405751) # Rest frequency of the HI line, in MHz
    elif (symbol=="nu0_CO"): return(115271.203) # Rest frequency of the CO(1->0) line, in MHz
    elif (symbol=="H0"): return(72) # Hubble constant, in km/s/Mpc
    else:
        print("Unknown symbol")
        return(0)

def Bnu(T,nu): # Fonction de Planck B_nu avec T en K en nu en Hz
    return((2.0*constant("h")*np.power(nu,3.0))/(math.pow(constant("c"),2.0)*1e6*(np.exp((constant("h")*nu)/(constant("k")*T))-1.0)))

def Bnu_RJ(T,nu): # Fonction de Planck B_nu dans l'approximation de Rayleigh-Jeans avec T en K en nu en Hz
    return((2.0*constant("k")*T*np.power(nu,2.0))/(math.pow(constant("c"),2.0)*1e6))

def Bnu_Wien(T,nu): # Fonction de Planck B_nu dans l'approximation de Wien avec T en K en nu en Hz
    return(((2.0*constant("h")*np.power(nu,3.0))/(math.pow(constant("c"),2.0)*1e6))*(np.exp(-(constant("h")*nu)/(constant("k")*T))))

def Blam(T,lam): # Fonction de Planck B_lambda avec T en K en lam (longueur d'onde) en m
    return(((2.0*constant("h")*math.pow(constant("c")*1e3,2.0))/np.power(lam,5.0))*(1.0/(np.exp((constant("h")*constant("c")*1e3)/(constant("k")*T*lam))-1.0)))

def Blam_RJ(T,lam): # Fonction de Planck B_lambda dans l'approximation de Rayleigh-Jeans avec T en K en lam (longueur d'onde) en m
    return((2.0*constant("c")*1e3*constant("k")*T)/np.power(lam,4.0))

def Blam_Wien(T,lam): # Fonction de Planck B_lambda dans l'approximation de Wien avec T en K en lam (longueur d'onde) en m
    return(((2.0*constant("h")*math.pow(constant("c")*1e3,2.0))/np.power(lam,5.0))*np.exp(-(constant("h")*constant("c")*1e3)/(constant("k")*T*lam)))

# Creation de la figure
fig, ax = plt.subplots(figsize=(15,10))
plt.subplots_adjust(left=0.25, bottom=0.25)

# Nombre de points
npoints=10000

# Limites
nu_min=1e4
nu_max=2e15
T_min=0.1
T_max=10000.0

# Creation de l'axe des abscisses
nu = np.logspace(np.log10(nu_min),np.log10(nu_max),num=npoints)

# Parametres de la fonction, avec des valeurs par defaut
T0 = 5800 # Temperature en K


#Ajout des lignes de reperes
plt.plot(6.7E14+np.zeros(100),np.linspace(0,10,100),'k', lw=2, color='purple') #violet
plt.plot(5.7E14+np.zeros(100),np.linspace(0,10,100),'k', lw=2, color='green') # vert
plt.plot(4.6E14+np.zeros(100),np.linspace(0,10,100),'k', lw=2, color='red') # rouge

# Creation de la fonction a tracer 
bnu=Bnu(T0,nu)
bnuRJ=Bnu_RJ(T0,nu)
bnuW=Bnu_Wien(T0,nu)

# Creation de la trace de la fonction de Planck en fonction de nu. C'est un objet qui est sauvegarde dans 'l'
l, = plt.plot(nu,bnu, lw=2, color='blue',visible=True)
# Idem pour la fonction de Wien
lW, = plt.plot(nu,bnuW, lw=2,color='black', visible=False)
# Idem pour la fonction de Rayleigh-Jeans
lRJ, = plt.plot(nu,bnuRJ, lw=2, color='red',visible=False)


#Titre de la figure
plt.title('Loi de Planck du rayonnement du corps noir')

#Commentaires affichés
plt.text(-7e14, 2e-8, "rouge :  633 nm", color='red')
plt.text(-7e14, 1.8e-8, "vert : 525 nm", color='green')
plt.text(-7e14, 1.6e-8, "violet : 425 nm", color='purple')

# Specification des limites des axes (xmin,xmax,ymin,ymax)
plt.ylim(0.0,1.1*np.max(bnu))
plt.xlim(nu_min,nu_max)
plt.xlabel(r"$\nu$ [$\mathrm{Hz}$]",fontsize=20)
plt.ylabel(r"$B_\nu$ [$\mathrm{W.m^{-2}.Hz^{-1}.sr^{-1}}$]"+"\n",fontsize=20)
for tick in ax.xaxis.get_major_ticks():tick.label.set_fontsize(15) 
for tick in ax.yaxis.get_major_ticks():tick.label.set_fontsize(15) 
#plt.legend(["Planck","Wien","Rayleigh-Jeans"])

# Creation des barres de modification de la temperature
axcolor = 'lightgoldenrodyellow'
axT = plt.axes([0.18, 0.07, 0.65, 0.03], facecolor=axcolor)
sT = Slider(axT, 'Temperature (K)', T_min, T_max, valinit=T0) # Remarquer la valeur initiale T0


# Fonction de mise a jour du graphique
def update(val):
    T = sT.val # On recupere la valeur de la barre sT comme temperature
    l.set_ydata(Bnu(T,nu)) # On met a jour l'objet 'l' avec ces nouvelles valeurs 
    lW.set_ydata(Bnu_Wien(T,nu)) # On met a jour l'objet 'lW' avec ces nouvelles valeurs 
    lRJ.set_ydata(Bnu_RJ(T,nu)) # On met a jour l'objet 'lRJ' avec ces nouvelles valeurs 
    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
sT.on_changed(update) # lorsque la barre sT est modifiee, on applique la fonction update

# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    sT.reset() # La methode .reset() appliquee a la barre sfreq lui redonne sa valeur valinit, soit T0
button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus

# Creation du menu de selection des traces a afficher
cax = plt.axes([0.015, 0.7, 0.15, 0.15], facecolor=axcolor)
check = CheckButtons(cax, ('Planck', 'Rayleigh-Jeans', 'Wien'), (True, False, False))

# Definition de la fonction qui passe un affichage de visible a invisible
def chooseplot(label):
    if label == 'Planck': l.set_visible(not l.get_visible()) # Si on clique sur le bouton "Planck", la trace 'll passe visible si elle ne l'etait pas, et vice versa
    elif label == 'Wien': lW.set_visible(not lW.get_visible()) # Si on clique sur le bouton "Wien", la trace 'lW' passe visible si elle ne l'etait pas, et vice versa
    elif label == 'Rayleigh-Jeans': lRJ.set_visible(not lRJ.get_visible()) # Si on clique sur le bouton "Rayleigh-Jeans", la trace 'lRJ' passe visible si elle ne l'etait pas, et vice versa
    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
check.on_clicked(chooseplot) # Lorsqu'on coche un de ces boutons, on applique la fonction chooseplot

plt.show() # On provoque l'affichage a l'ecran

'''
#Nom du programme : PropagationSon

#Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.10

#Liste des modifications
#v 1.00 : 2016-05-02 Première version complète - baudin@lpa.ens.fr
#v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor

#Version de Python
#3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#AVERTISSEMENT
#Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

#Description : 
#Ce programme représente les positions d'un ensemble de poussières soumises à une onde sonore à 2KHz et d'amplitude choisie. 
#Le choix de représenter des poussières plutôt que des particule du gaz permet de supprimer le problème de la représentation des vitesses thermiques. 
#Les zones de compression et dilatation peuvent être directement observées. Une poussière rouge est singularisée pour être suivie individuellement. Deux graphiques inférieurs représentent le champ de pression et le champ de vitesse respectivement. 
#Il est possible de faire varier l'amplitude de l'onde sonore et sa fréquence pour en constater directement l'effet. 
#ATTENTION : Le niveau sonore de 190 dB SPL correspond à une surpression de l'ordre de la pression atmosphèrique! L'hypothèse de perturbation pour obtenir l'équation de propagation du son n'est donc pas valide. Par ailleurs à ces niveaux la vitesse maximale de la particule fluide dépasse la vitesse du son ce qui n'est pas possible. Il faut donc prendre cette représentation avec prudence : ces niveaux extrêmes sont nécessaires pour pouvoir observer le phénomène dans une classe, mais ils ne correspondent pas à une situation réaliste. Au delà de 185 dB SPL, les champs de vitesse et de pression prédits par la théorie et représentés ne correspondent plus à la distribution représentée. 
'''

#import des bibliothèques python
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
from numpy.random import rand

# Creation de la figure, il y a 3 sous-figures correspondants aux 3 graphiques
f, axarr = plt.subplots(3, sharex=True)
plt.subplots_adjust(left=0.1, bottom=0.30)


# Creation de l'axe des abscisses, ici la distance x
x = np.arange(0., 1., 0.001) #Zone observee : 0-1 m

# Parametres de la fonction, avec des valeurs par defaut
cs = 340. #Vitesse du son en m/s
Pr = 2E-5 #Pression de référence (Pa) pour le calcul du niveau sonore en dB SPL
P0 = 1.01325E5 #Pression atmospherique moyenne (Pa)
rho0 = 1.184 #Masse volumique de l'air moyenne a 25°C (kg/m**3)
f0 = 2000. #Frequence de l'onde sonore en Hz
pi = 3.1415927
lambda0 = cs/f0 #Longueur d'onde de l'onde sonore (m)
L0 = 180 #Niveau sonore initial (en SPL)
AP0 = (10.**(L0/20.))*np.sqrt(2)*Pr #Amplitude de pression sonore. 
A0 = AP0/P0*lambda0/2./pi #Amplitude du déplacement sonore.
Av0 = AP0/rho0/cs #Amplitude de la vitesse des particules de poussiere
t0 = 0. #Temps initial




# Creation des ondes 1 et 2
def OndePression (ux, Ain,  tin):
	return (Ain*np.sin(2.*pi/lambda0*(ux-cs*tin)))

def OndeVitesse (ux, Ain,  tin):
	return (Ain*np.cos(2.*pi/lambda0*(ux-cs*tin)))

def Poussieres (ux, uy, Ain,  tin):
	return ((ux + Ain*np.cos(2.*pi/lambda0*(ux-cs*tin)))), (uy-0.5)*2



#Initialisation
s0 = OndePression (x, AP0, 0)
s1 = OndeVitesse (x, Av0, 0)

#On créé n particules à des positions aléatoires sur la fenêtre observée et on les répartie selon la loi de position lorsqu'une onde sonore est présente. 
n=500
ux,uy = rand(2, n)
scale = 30.
ux2, uy2 = Poussieres (ux, uy, A0, 0)

# Creation de la trace de la fonction s en fonction de t. C'est un objet qui est sauvegarde dans 'l'
# Three subplots, the axes array is 1-d



#Titre de la figure
axarr[0].set_title('Poussieres dans une onde sonore')
#Creation des donnees pour les figures
line0 = axarr[0].scatter(ux2, uy2, c='blue', s=scale, alpha=0.3, edgecolors='none')
line0 = axarr[0].scatter((0.5 + A0*(np.cos(2.*pi/lambda0*(0.5-cs*t0)))), 0., c='red', s=50., alpha=0.8, edgecolors='none') #Point rouge qui sera suivi
line1, = axarr[1].plot(x, s0, lw=2, color='red')
line2, = axarr[2].plot(x, s1, lw=2, color='black')

#Guides pour l'oeil
axarr[1].plot(np.linspace(-1000,1000,1000),np.zeros(1000),'k')
axarr[2].plot(np.linspace(-1000,1000,1000),np.zeros(1000),'k')

#Guides pour l'oeil
axarr[1].plot(np.zeros(1000),np.linspace(-10,10,1000),'k')
axarr[2].plot(np.zeros(1000),np.linspace(-10,10,1000),'k')



# Specification des limites des axes (xmin,xmax,ymin,ymax)
axarr[0].axis([0, 1, -1, 1])
axarr[1].axis([0, 1, -1E5, 1E5])
axarr[2].axis([0, 1, -1E2, 1E2])
plt.xlabel('Position (m)')
axarr[0].axes.get_xaxis().set_visible(False)
axarr[0].axes.get_yaxis().set_visible(False)
axarr[1].set_ylabel('Surpression (Pa)')
axarr[2].set_ylabel('Vitesse (m/s)')



#Commentaires affichés
#plt.text(-1900, 2.4, r'$\phi$ ')
#plt.text(-1900, 1.8, r"$\lambda$ longueur d'onde")


# Creation des barres de modification amplitude et frequence
axcolor = 'lightgoldenrodyellow'
axL = plt.axes([0.3, 0.07, 0.6, 0.03], facecolor=axcolor)
axT = plt.axes([0.3, 0.1, 0.6, 0.03], facecolor=axcolor)

sL = Slider(axL, 'Amplitude sonore (dB SPL)', 160, 190, valinit=L0) # Remarquer la valeur initiale a 190 dB SPL
sT = Slider(axT, 'Temps t (ms)', 0., 1., valinit=t0) # Remarquer la valeur initiale à 0


# Fonction de mise a jour du graphique
def update(val):
    L = sL.val  # On recupere la valeur de la barre sL comme niveau sonore
    AP = (10.**(L/20.))*np.sqrt(2)*Pr #Amplitude de pression sonore. 
    A = AP/P0*lambda0/2./pi #Amplitude du déplacement sonore.
    Av = AP/rho0/cs #Amplitude de la vitesse des particules de poussiere
    T = sT.val/1000. #Valeur recuperee en mm. On recupere la valeur de la barre sa comme distance entre les fentes

    ux2, uy2 = Poussieres (ux, uy, A, T)

    axarr[0].cla()
	# Specification des limites des axes (xmin,xmax,ymin,ymax)
    axarr[0].axis([0, 1, -1, 1])
    axarr[1].axis([0, 1, -1E5, 1E5])
    axarr[2].axis([0, 1, -1E2, 1E2])
    line0 = axarr[0].scatter(ux2, uy2, c='blue', s=scale, alpha=0.3, edgecolors='none') # On met a jour l'objet 'line0' avec ces nouvelles valeurs 
    line0 = axarr[0].scatter((0.5 + A*(np.cos(2.*pi/lambda0*(0.5-cs*T)))), 0., c='red', s=50., alpha=0.8, edgecolors='none') # On met a jour l'objet 'line0' avec ces nouvelles valeurs 
    axarr[0].set_title('Poussieres dans une onde sonore')
    line1.set_ydata(OndePression (x, AP, T)) # On met a jour l'objet 'line1' avec ces nouvelles valeurs 
    line2.set_ydata(OndeVitesse (x, Av, T)) # On met a jour l'objet 'line2' avec ces nouvelles valeurs 


    f.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
sL.on_changed(update) # lorsque la barre sL est modifiee, on applique la fonction update
sT.on_changed(update) # lorsque la barre sT est modifiee, on applique la fonction update


# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    sL.reset() # La methode .reset() appliquee a la barre sL lui redonne sa valeur valinit, soit L0
    sT.reset() # La methode .reset() appliquee a la barre sT lui redonne sa valeur valinit, soit 0
button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus



plt.show() # On provoque l'affichage a l'ecran


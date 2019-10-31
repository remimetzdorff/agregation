#Nom du programme : InterferenceElementaire

#Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.00

#Liste des modifications
#v 1.00 : 2016-05-02 Première version complète - baudin@lpa.ens.fr
#v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor

#Version Python
#3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#Description : 
#Ce programme permet d'illustrer le principe élémentaire de l'interférence de deux ondes harmoniques monochromatiques. Attention : les deux ondes sont supposées planes, scalaires et l'interférence intervient le long de leur propagation comme dans un interféromètre de Michelson, mais pas comme dans un dispositif de Fente d'Young. Il est possible de modifier la longueur d'onde et le déphasage de l'onde 2 par rapport à l'onde 1 de référence. La somme des deux ondes est représentée sur la fenêtre du bas. 


#import des bibliothèques python
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

# Creation de la figure
fig, axarr = plt.subplots(3, sharex=True) #Création de 3 sous-figures pour représenter la référence, l'onde déphasée et l'onde somme. 
plt.subplots_adjust(left=0.1, bottom=0.30)


# Creation de l'axe des abscisses, ici la distance x
x = np.arange(-1., 1., 0.001)*1000. #Zone observee : +/- 1 µm

# Parametres de la fonction, avec des valeurs par defaut
k0 = 2.*np.pi/(633./10.**9) # Vecteur d'onde
lambda0 = 633. # Longueur d'onde
phi0 = 0. # Déphasage (en radian)




# Creation des ondes 1 et 2
def Onde (lambdain, phiin, xin):
	return np.cos(xin*(2.*3.14159/lambdain)+phiin)
#Creation de l'interference
def Interference (lambdain, phiin, xin):
	return Onde (lambdain, 0, xin)+ Onde (lambdain, phiin, xin)



#Initialisation
s0 = Onde (lambda0, 0, x)
s1 = Onde (lambda0, phi0, x)
s2 = Interference (lambda0, phi0, x)

# Creation de la trace de la fonction s en fonction de t. C'est un objet qui est sauvegarde dans 'l'
# Three subplots, the axes array is 1-d


#Titre de la figure
axarr[0].set_title('Interference de deux ondes harmoniques')
line0, = axarr[0].plot(x, s0, lw=2, color='blue')
line1, = axarr[1].plot(x, s1, lw=2, color='red')
line2, = axarr[2].plot(x, s2, lw=2, color='black')

axarr[0].plot(np.linspace(-1000,1000,1000),np.zeros(1000),'k')
axarr[1].plot(np.linspace(-1000,1000,1000),np.zeros(1000),'k')
axarr[2].plot(np.linspace(-1000,1000,1000),np.zeros(1000),'k')

axarr[0].plot(np.zeros(1000),np.linspace(-10,10,1000),'k')
axarr[1].plot(np.zeros(1000),np.linspace(-10,10,1000),'k')
axarr[2].plot(np.zeros(1000),np.linspace(-10,10,1000),'k')



# Specification des limites des axes (xmin,xmax,ymin,ymax)
axarr[0].axis([-1000, 1000, -1, 1])
axarr[1].axis([-1000, 1000, -1, 1])
axarr[2].axis([-1000, 1000, -2, 2])
plt.xlabel('Position (nm)')
axarr[1].set_ylabel('Amplitude du champ electrique (u.a.)')



#Commentaires affichés
#plt.text(-1900, 2.4, r'$\phi$ ')
#plt.text(-1900, 1.8, r"$\lambda$ longueur d'onde")


# Creation des barres de modification amplitude et frequence
axcolor = 'lightgoldenrodyellow'
axlambda = plt.axes([0.3, 0.07, 0.6, 0.03], facecolor=axcolor)
axphi = plt.axes([0.3, 0.1, 0.6, 0.03], facecolor=axcolor)

slambda = Slider(axlambda, 'Longueur d\'onde $\lambda$ (nm)', 400., 800., valinit=633.) # Remarquer la valeur initiale 633 nm
sphi = Slider(axphi, 'Dephasage $\phi$ (rad)', 0., 2*3.14159, valinit=phi0) # Remarquer la valeur initiale phi0=0


# Fonction de mise a jour du graphique
def update(val):
    lambda1 = slambda.val  # On recupere la valeur de la barre slambda comme longueur d'onde (en nm)
    phi = sphi.val # On recupere la valeur de la barre sphi comme déphasage entre les deux ondes.

    line0.set_ydata(Onde (lambda1, 0, x)) # On met a jour l'objet 'line0' avec ces nouvelles valeurs 
    line1.set_ydata(Onde (lambda1, phi, x)) # On met a jour l'objet 'line1' avec ces nouvelles valeurs 
    line2.set_ydata(Interference (lambda1, phi, x)) # On met a jour l'objet 'line2' avec ces nouvelles valeurs 


    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
slambda.on_changed(update) # lorsque la barre slambda est modifiee, on applique la fonction update
sphi.on_changed(update) # lorsque la barre sphi est modifiee, on applique la fonction update


# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    slambda.reset() # La methode .reset() appliquee a la barre slambda lui redonne sa valeur valinit, soit 633 nm
    sphi.reset() # La methode .reset() appliquee a la barre sphi lui redonne sa valeur valinit, soit 0
button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus



plt.show() # On provoque l'affichage a l'ecran


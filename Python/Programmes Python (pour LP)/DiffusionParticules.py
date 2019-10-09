#Nom du programme : DiffusionParticules

#Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.Fr
#
#Année de création : 2016 
#Version : 1.10

#Liste des modifications
#v 1.00 : 2016-05-02 Première version complète - baudin@lpa.ens.fr
#v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#Description : 
#Ce programme représente l'évolution de la distribution spatiale de densité de particules lors d'une diffusion 1D. Il est possible de faire varier le temps, le nombre de particules initialement considérées (le problème est conservatif), le coeffcient de diffusion. 

#import des bibliothèques python
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

# Creation de la figure
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

#Nom des axes
plt.xlabel('Position (m)')
plt.ylabel('Densite de particules (#$.m^{-1}$)')

#Titre de la figure
plt.title('Diffusion de particules')

#Commentaires affichés
plt.text(-17., 1300, r'$D$ coeff. de diffusion')

# Creation de l'axe des abscisses, ici le temps
x = np.arange(-10.0, 10.0, 0.001)

# Parametres de la fonction, avec des valeurs par defaut
N0 = 500 # Nombre de particules initialement presentes
t0 = 0 # Temps 
x0 = 0.1 # Position de depart 
D0 = 1 # Coefficient de diffusion


#Creation de la fonction diffusion
def maxi(x0in, tin, Din):
    return np.sqrt(x0in**2 + Din*tin)
    
def diffusion(tin, ain, x0in, xin, Din):
    return ain*np.exp(-1/2*(xin/maxi(x0in, tin, Din))**2)/(np.sqrt(2*math.pi*maxi(x0in,tin,Din)))

#Initialisation
s = diffusion(t0, N0, x0, x, D0)

# Creation de la trace de la fonction s en fonction de t. C'est un objet qui est sauvegarde dans 'l'
l, = plt.plot(x, s, lw=2, color='red')

# Specification des limites des axes (xmin,xmax,ymin,ymax)
plt.axis([-10, 10, 0, 1500])

# Creation des barres de modification amplitude et frequence
axcolor = 'lightgoldenrodyellow'
axtemps = plt.axes([0.25, 0.13, 0.65, 0.03], facecolor=axcolor)
axamp  = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axdiff  = plt.axes([0.25, 0.07, 0.65, 0.03], facecolor=axcolor)
stemps = Slider(axtemps, 'Temps (s)', 0., 100.0, valinit=t0) # Remarquer la valeur initiale t0
samp = Slider(axamp, 'Nb part ', 0.1, 1000.0, valinit=N0) # Remarquer la valeur initiale N0
sdiff = Slider(axdiff, '$D$ (m^2.s^-1)', 0., 5.0, valinit=D0) # Remarquer la valeur initiale D0

# Fonction de mise a jour du graphique
def update(val):
    amp = samp.val # On recupere la valeur de la barre samp comme le nombre de particules initialement presentes
    temps = stemps.val # On recupere la valeur de la barre stemps comme le temps
    diff = sdiff.val # On recupere la valeur de la barre sdiff comme coeffcient diffusion
    l.set_ydata(diffusion (temps, amp, x0, x, diff)) # On met a jour l'objet 'l' avec ces nouvelles valeurs 
    fig.canvas.draw_idle()# On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
stemps.on_changed(update) # lorsque la barre stemps est modifiee, on applique la fonction update
samp.on_changed(update) # lorsque la barre samp est modifiee, on applique la fonction update
sdiff.on_changed(update) # lorsque la barre sdiff est modifiee, on applique la fonction update

# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    stemps.reset() # La methode .reset() appliquee a la barre stemps lui redonne sa valeur valinit, soit t0
    samp.reset() # La methode .reset() appliquee a la barre samp lui redonne sa valeur valinit, soit N0
    sdiff.reset() # La methode .reset() appliquee a la barre sdiff lui redonne sa valeur valinit, soit D0
button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus

plt.show() # On provoque l'affichage a l'ecran


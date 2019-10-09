'''
#Nom du programme : PropagationOnde

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

#Version Python
#3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#Description : 
#Ce programme représente l'effet d'une barrière d'amplitude du coefficient de reflexion r sur une onde sonore plane harmonique propagative. La réflexion est représentée spatialement, le temps pouvant être varié indépendamment. Il est possible de modifier l'amplitude de l'onde, le coefficient de réflexion de la barrière, ainsi que la fréquence de l'onde incidente. 
'''

#import des bibliothèques python
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
j = complex(0,1)

# Creation de la figure
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3, bottom=0.3)

# Creation de l'axe des abscisses, ici le temps
x = np.arange(-1., 1., 0.001)

plt.xlabel('Position (m)')
plt.ylabel('Amplitude (u.a.)')

#Titre de la figure
plt.title('Reflexion des ondes sonores planes harmoniques propagatives')


#Commentaires affichés
plt.text(-1.9, 9, r'$t$ temps')
plt.text(-1.9, 8, r"$f$ frequence de l'onde")
plt.text(-1.9, 7, r"$A$ amplitude de l'onde")
plt.text(-1.9, 6, r'$r$ coefficient de reflexion')

#Ajout des lignes de reperes
plt.plot(np.linspace(-3,3,1000),np.zeros(1000),'k')
plt.plot(np.zeros(1000),np.linspace(-10,10,1000),'k')

# Parametres de la fonction, avec des valeurs par defaut
t0 = 0. # Temps
a0 = 5 # Amplitude
f0 = 1000 # Frequence
ra0 = 0.5 # amplitude coeff reflectivite
rp0 = 0. # phase  coeff reflectivite, NON UTILISE
p0 = 0.

c = 340 # Vitesse du son en m/s

# Creation de la fonction a tracer 
def OscillationScalaire (tin, xin, ain, fin, rain, rpin):
    if xin<0 : return np.real(ain*np.exp(j*2*np.pi*fin*(tin-xin/c))+ain*rain*np.exp(j*rpin)*np.exp(j*2*np.pi*fin*(tin+xin/c)))
    else : return np.real(ain*(1.+rain*np.exp(j*rpin))*np.exp(j*2*np.pi*fin*(tin-xin/c)))

Oscillation = np.vectorize(OscillationScalaire) #En raison de la condition if, la fonction OscillationScalaire ne peut pas etre appliquee au vecteur temps, pour resoudre ce probleme il faut la 'vectoriser', d'ou la presence de cette ligne.

    
#Initialisation
s = Oscillation (t0, x, a0, f0, ra0, rp0)

# Creation de la trace de la fonction s en fonction de x. C'est un objet qui est sauvegarde dans 'l'
l, = plt.plot(x,s, lw=2, color='red')

# Specification des limites des axes (xmin,xmax,ymin,ymax)
plt.axis([-1, 1, -10, 10])

# Creation des barres de modification amplitude et frequence
axcolor = 'lightgoldenrodyellow'
axtemps = plt.axes([0.25, 0.16, 0.65, 0.03], facecolor=axcolor)
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axamp  = plt.axes([0.25, 0.13, 0.65, 0.03], facecolor=axcolor)
axrefl  = plt.axes([0.25, 0.07, 0.65, 0.03], facecolor=axcolor)

stemps = Slider(axtemps, '$t$ (ms)', 0, 2., valinit=t0*10**3)  # Remarquer la valeur initiale t0*10**3
sfreq = Slider(axfreq, '$f$ (Hz)', 500, 1500.0, valinit=f0) # Remarquer la valeur initiale f0
samp = Slider(axamp, '$A$ (V)', 0.0, 10.0, valinit=a0) # Remarquer la valeur initiale a0
srefl = Slider(axrefl, '$r$ (s.d.)', -1., 1., valinit=ra0) # Remarquer la valeur initiale ra0

# Fonction de mise a jour du graphique
def update(val):
    amp = samp.val # On recupere la valeur de la barre samp comme amplitude
    freq = sfreq.val # On recupere la valeur de la barre sfreq comme frequence
    t = stemps.val/10**3 # On recupere la valeur de la barre stemps comme un temps (en ms)
    refl = srefl.val # On recupere la valeur de la barre srefl comme un coefficient de reflexion
    l.set_ydata(Oscillation (t, x, amp, freq, refl, rp0)) # On met a jour l'objet 'l' avec ces nouvelles valeurs 
    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
sfreq.on_changed(update) # lorsque la barre sfreq est modifiee, on applique la fonction update
samp.on_changed(update) # lorsque la barre samp est modifiee, on applique la fonction update
stemps.on_changed(update) # lorsque la barre stemps est modifiee, on applique la fonction update
srefl.on_changed(update) # lorsque la barre srefl est modifiee, on applique la fonction update

# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    sfreq.reset() # La methode .reset() appliquee a la barre sfreq lui redonne sa valeur valinit, soit f0
    samp.reset() # La methode .reset() appliquee a la barre samp lui redonne sa valeur valinit, soit a0
    stemps.reset() # La methode .reset() appliquee a la barre stemps lui redonne sa valeur valinit, soit t0
    srefl.reset() # La methode .reset() appliquee a la barre srefl lui redonne sa valeur valinit, soit ra0
button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus

## Creation du menu de changement des couleurs
#rax = plt.axes([0.015, 0.5, 0.15, 0.15], facecolor=axcolor)
#radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0) # La valeur par defaut est la numero 0 (red). Si on met active=1, c'est bleu, et active=2 c'est vert...
## Definition de la fonction de changement des couleurs
#def colorfunc(label):
#    l.set_color(label) # On change la couleur en appliquant celle qui est contenue dans "label", a savoir "red", "blue" ou "green"
#    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
#radio.on_clicked(colorfunc) # Quand on clique sur un choix, le "label" associe a ce choix est passe a la fonction colorfunc

plt.show() # On provoque l'affichage a l'ecran


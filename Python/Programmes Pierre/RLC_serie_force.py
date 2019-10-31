'''
#Nom du programme : RLC_serie_force

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


#Description : 
#Ce programme représente la réponse fréquencielle d'un oscillateur RLC série à un forçage sinusoidal en tension de 1 Vpp. Il est possible de faire varier les valeurs de la résistance, la capacité et l'inductance du circuit. La fenêtre de gauche permet de choisir aux bornes de quel composant on observe la tension. A noter qu'un choisissant la résistance R, on observe à un facteur près la réponse en courant du circuit. 
'''

#import des bibliothèques python
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

# Creation de la figure
f, axarr = plt.subplots()
plt.subplots_adjust(left=0.3, bottom=0.30)



# Parametres de la fonction, avec des valeurs par defaut
fmin = 1. # NE PAS METTRE ZERO SINON IL Y A DIVISION PAR ZERO.
fmax = 10000.
pi = 3.1415927

L0 = 1E-3 # Inductance initiale
R0 = 10.  # Resistance initiale
C0 = 1E-5 # Capacité initiale

#Commentaires affichés
plt.text(-4500, 4, r'Forcage sin. 1Vp-p')


# Creation de l'axe des abscisses, ici la distance x
x = np.arange(fmin, fmax, 1.) #Zone observee

# Resonance en tension sur la résistance : attention, valeur complexe
def ResonanceR (Rin, Lin, Cin, fin):
	xin = fin*2*pi
	return Rin/(1j*Lin*xin+Rin+1/(1j*Cin*xin))

# Resonance en tension sur le condensateur : attention, valeur complexe
def ResonanceC (Rin, Lin, Cin, fin):
	xin = fin*2*pi
	return 1/(1j*Cin*xin)/(1j*Lin*xin+Rin+1/(1j*Cin*xin))

# Resonance en tension sur la bobine : attention, valeur complexe
def ResonanceL (Rin, Lin, Cin, fin):
	xin = fin*2*pi
	return 1j*Lin*xin/(1j*Lin*xin+Rin+1/(1j*Cin*xin))



#Initialisation
s0R = ResonanceR (R0, L0, C0, x)
s0L = ResonanceL (R0, L0, C0, x)
s0C = ResonanceC (R0, L0, C0, x)



#Titre de la figure
axarr.set_title("Resonance en tension d'un circuit RLC serie")

# Creation de la trace de la norme de la fonction s en fonction de x (qui correspond à la fréquence de forçage). C'est un objet qui est sauvegarde dans 'line0X'
line0R, = axarr.plot(x, np.absolute(s0R), lw=2, color='red', visible=False)
line0L, = axarr.plot(x, np.absolute(s0L), lw=2, color='blue', visible=False)
line0C, = axarr.plot(x, np.absolute(s0C), lw=2, color='green')
axarr.plot(np.linspace(fmin,fmax,1000),np.zeros(1000),'k')

# Creation de la trace de la phase de la fonction s en fonction de x (qui correspond à la fréquence de forçage). C'est un objet qui est sauvegarde dans 'line0PX'
ax2 = axarr.twinx()
line0PR, = ax2.plot(x, np.angle(s0R, deg=True), '--', color='red', visible=False)
line0PL, = ax2.plot(x, np.angle(s0L, deg=True), '--', color='blue', visible=False)
line0PC, = ax2.plot(x, np.angle(s0C, deg=True), '--', color='green', visible=False)
linePrepere, = ax2.plot(np.linspace(fmin,fmax,1000),np.zeros(1000),'--', color='black', visible=False)




# Specification des amplitudes minimales et maximales
AmpMin = 0.
AmpMax = 5.
axarr.axis([fmin, fmax, AmpMin, AmpMax])

# Titre des axes
axarr.set_ylabel('Amplitude pp du champ electrique (V)')
ax2.set_ylabel('Dephasage ($\degree$)')
axarr.set_xlabel('Frequence (Hz)')


# Creation des barres de modification amplitude et frequence
axcolor = 'lightgoldenrodyellow'
axR = plt.axes([0.3, 0.07, 0.6, 0.03], facecolor=axcolor)
axL = plt.axes([0.3, 0.1, 0.6, 0.03], facecolor=axcolor)
axC = plt.axes([0.3, 0.13, 0.6, 0.03], facecolor=axcolor)

sR = Slider(axR, 'Resistance ($\Omega$)', 1., 30., valinit=10.) # Remarquer la valeur initiale 10 Ohms
sL = Slider(axL, 'Inductance ($mH$)', 0.01, 3., valinit=1.) # Remarquer la valeur initiale 1 milliHenry
sC = Slider(axC, 'Capacite ($\mu F$)', 0.1, 30., valinit=10.) # Remarquer la valeur initiale 10 microFarads



# Fonction de mise a jour du graphique
def update(val):
    R = sR.val       # On recupere la valeur de la barre sR comme resistance du circuit RLC
    L = sL.val*1E-3  # On recupere la valeur de la barre sL comme inductance du circuit RLC
    C = sC.val*1E-6  # On recupere la valeur de la barre sC comme capacite du circuit RLC

    line0R.set_ydata(np.absolute(ResonanceR (R, L, C, x)))
    line0L.set_ydata(np.absolute(ResonanceL (R, L, C, x)))
    line0C.set_ydata(np.absolute(ResonanceC (R, L, C, x)))

    line0PR.set_ydata(np.angle(ResonanceR (R, L, C, x), deg=True))
    line0PL.set_ydata(np.angle(ResonanceL (R, L, C, x), deg=True))
    line0PC.set_ydata(np.angle(ResonanceC (R, L, C, x), deg=True))

    f.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
sR.on_changed(update) # lorsque la barre sR est modifiee, on applique la fonction update
sL.on_changed(update) # lorsque la barre sL est modifiee, on applique la fonction update
sC.on_changed(update) # lorsque la barre sC est modifiee, on applique la fonction update

# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    sR.reset() # La methode .reset() appliquee a la barre sR lui redonne sa valeur valinit, soit R0
    sL.reset() # La methode .reset() appliquee a la barre sL lui redonne sa valeur valinit, soit L0
    sC.reset() # La methode .reset() appliquee a la barre sC lui redonne sa valeur valinit, soit CO
button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus



# Creation du menu de selection des traces a afficher
cax = plt.axes([0.015, 0.3, 0.2, 0.15], facecolor=axcolor)
check = CheckButtons(cax, ('R $\equiv$ I', 'L', 'C', 'phases'), (False, False, True, False))
# Definition de la fonction qui passe un affichage de visible a invisible
def chooseplot(label):
    if label == 'R $\equiv$ I': line0R.set_visible(not line0R.get_visible()) # Si on clique sur le bouton "R $\equiv$ I", la trace 'R' passe visible si elle ne l'etait pas, et vice versa

    elif label == 'L': 	line0L.set_visible(not line0L.get_visible()) # Si on clique sur le bouton "L", la trace 'L' passe visible si elle ne l'etait pas, et vice versa

    elif label == 'C': 	line0C.set_visible(not line0C.get_visible()) # Si on clique sur le bouton "C", la trace 'C' passe visible si elle ne l'etait pas, et vice versa

    elif label == 'phases': linePrepere.set_visible(not linePrepere.get_visible()) # Si on clique sur le bouton "phases", les traces de phases correspondant aux canaux choisis passent visibles si elles ne l'etaient pas, et vice versa

#Le code de logique un peu complexe ci-dessous est destiné à choisir correctement quelles traces doivent être affichées en fonction des bouttons radio cochés.
    if linePrepere.get_visible() == True:
        line0PR.set_visible(line0R.get_visible())
        line0PL.set_visible(line0L.get_visible())
        line0PC.set_visible(line0C.get_visible())
    if linePrepere.get_visible() == False:
         line0PR.set_visible(False)
         line0PL.set_visible(False)
         line0PC.set_visible(False)
    f.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut

check.on_clicked(chooseplot) # Lorsqu'on coche un de ces boutons, on applique la fonction chooseplot

plt.show() # On provoque l'affichage a l'ecran


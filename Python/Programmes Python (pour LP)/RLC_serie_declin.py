'''
#Nom du programme : RLC_Serie_declin

#Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : baudin@lpa.ens.fr
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
#Ce programme représente la réponse temporelle d'un oscillateur RLC série à un forçage en échelon de tension à l'instant t=0. Il est possible de faire varier les valeurs de la résistance, la capacité et l'inductance du circuit. La fenêtre de gauche permet de choisir aux bornes de quel composant on observe la tension. A noter qu'un choisissant la résistance R, on observe à un facteur près la réponse en courant du circuit. 
'''

#import des bibliothèques python
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

# Creation de la figure
fig, axarr = plt.subplots()
plt.subplots_adjust(left=0.3, bottom=0.3)

# Creation de l'axe des abscisses, ici le temps (de 0 à 1 µs)
t = np.arange(0., 1.0, 0.001)

plt.xlabel('temps ($\mu$s)')
plt.ylabel('Amplitude (V)')

#Titre de la figure
plt.title("Reponse a un echelon de tension d'un circuit RLC serie")

#Commentaires affichés
plt.text(-0.45, 7, r'Ouverture DC 1V a t=0')


#Tracé d'une ligne horizontal pour repère
plt.plot(np.linspace(0,10,1000),np.zeros(1000),'k')

# Parametres de la fonction, avec des valeurs par defaut
tmin = 0.
tmax = 1.
pi = 3.1415927

L0 = 1E-3 # Inductance initiale
R0 = 10.  # Resistance initiale
C0 = 1E-5 # Capacité initiale

# Resonance en tension sur la résistance : attention, valeur complexe
def ResonanceR (Rin, Lin, Cin, tin):
	tin2 = 1E-3*tin
	w0 = 1/np.sqrt(Lin*Cin)
	a = Rin/(2*Lin*w0)
	delta = a**2-1

	if delta > 0 : 
		r1 = (-a+np.sqrt(delta))*w0
		r2 = (-a-np.sqrt(delta))*w0
	else :
		r1 = (-a+1j*np.sqrt((-1)*delta))*w0
		r2 = (-a-1j*np.sqrt((-1)*delta))*w0
	return np.real(Rin*Cin*r1*r2/(r2-r1)*(np.exp(r1*tin2)-np.exp(r2*tin2)))

# Resonance en tension sur le condensateur : attention, valeur complexe
def ResonanceC (Rin, Lin, Cin, tin):
	tin2 = 1E-3*tin
	w0 = 1/np.sqrt(Lin*Cin)
	a = Rin/(2*Lin*w0)
	delta = a**2-1
        
	if delta > 0 : 
		r1 = (-a+np.sqrt(delta))*w0
		r2 = (-a-np.sqrt(delta))*w0
	else :
		r1 = (-a+1j*np.sqrt((-1)*delta))*w0
		r2 = (-a-1j*np.sqrt((-1)*delta))*w0
	return np.real(1/(r2-r1)*(r2*np.exp(r1*tin2)-r1*np.exp(r2*tin2)))

# Resonance en tension sur la bobine : attention, valeur complexe
def ResonanceL (Rin, Lin, Cin, tin):
	return -ResonanceR(Rin, Lin, Cin, tin)-ResonanceC(Rin, Lin, Cin, tin)

#Initialisation
s0R = ResonanceR (R0, L0, C0, t)
s0L = ResonanceL (R0, L0, C0, t)
s0C = ResonanceC (R0, L0, C0, t)

# Creation de la trace de la fonction s en fonction de t. C'est un objet qui est sauvegarde dans 'line0X'
line0R, = axarr.plot(t, s0R, lw=2, color='red', visible=False)
line0L, = axarr.plot(t, s0L, lw=2, color='blue', visible=False)
line0C, = axarr.plot(t, s0C, lw=2, color='green')

# Specification des limites des axes (xmin,xmax,ymin,ymax)
plt.axis([0, 1, -1, 1])


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
    R = sR.val  # On recupere la valeur de la barre sR comme resistance du circuit RLC
    L = sL.val*1E-3  # On recupere la valeur de la barre sL comme inductance du circuit RLC
    C = sC.val*1E-6  # On recupere la valeur de la barre sC comme capacite du circuit RLC

    #On met à jour les donner à représenter
    line0R.set_ydata(ResonanceR (R, L, C, t))
    line0L.set_ydata(ResonanceL (R, L, C, t))
    line0C.set_ydata(ResonanceC (R, L, C, t))

    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
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
check = CheckButtons(cax, ('R $\equiv$ I', 'L', 'C'), (False, False, True))
# Definition de la fonction qui passe un affichage de visible a invisible
def chooseplot(label):
    if label == 'R $\equiv$ I': line0R.set_visible(not line0R.get_visible()) # Si on clique sur le bouton "Function", la trace 'l' passe visible si elle ne l'etait pas, et vice versa

    elif label == 'L': 	line0L.set_visible(not line0L.get_visible()) # Si on clique sur le bouton "Upper envelope", la trace 'lenvplus' passe visible si elle ne l'etait pas, et vice versa

    elif label == 'C': 	line0C.set_visible(not line0C.get_visible()) # Si on clique sur le bouton "Lower envelope", la trace 'lenvminus' passe visible si elle ne l'etait pas, et vice versa


    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut

check.on_clicked(chooseplot) # Lorsqu'on coche un de ces boutons, on applique la fonction chooseplot

plt.show() # On provoque l'affichage a l'ecran


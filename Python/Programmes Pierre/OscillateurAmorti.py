'''
Nom du programme : OscillateurAmorti

Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier et la prépa agreg de Montrouge
Adresse : Departement de physique de l'Ecole Normale Superieure
		24 rue Lhomond
		75005 Paris
Contact : baudin@lpa.ens.fr

Année de création : 2016 
Version : 1.10

#Liste des modifications
#v 0.10 : 2015-10-01 Première version complète
#v 1.00 : 2016-05-02 
#v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor

#Version de Python
# 3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#AVERTISSEMENT
#Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

#Description : 
#Ce programme représente la réponse temporelle d'un oscillateur amorti générique à un forçage en échelon à l'instant t=0. Il est possible de faire varier l'amplitude de l'échelon, la fréquence centrale de l'oscillateur amorti, sont temps de décroissance caractéristique ainsi que la phase de sa réponse. 
'''

#import des bibliothèques python
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

# Creation de la figure
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3, bottom=0.3)

# Creation de l'axe des abscisses, ici le temps
t = np.arange(0.0, 1.0, 0.001)

plt.xlabel('temps (s)')
plt.ylabel('Amplitude (V)')

#Titre de la figure
plt.title('Oscillateur amorti')

#Commentaires affichés
plt.text(-0.45, 9, r'$f$ frequence propre')
plt.text(-0.45, 8, r"$A$ Amplitude de l'echelon")
plt.text(-0.45, 7, r"tau temps de declin caracteristique")
plt.text(-0.45, 6, r'$\phi$ phase de la reponse')

#Tracé d'une ligne horizontal pour repère
plt.plot(np.linspace(0,10,1000),np.zeros(1000),'k')

# Parametres de la fonction, avec des valeurs par defaut
a0 = 5 # Amplitude
f0 = 3 # Frequence
t0 = 1 # temps de decroissance
p0 = 0 # Phase a l'origine

# Creation de la fonction a tracer 
def Oscillation (tin, ain, fin, pin, tdecin):
	return ain*np.sin(2*np.pi*fin*tin+pin)*np.exp(-(tin/tdecin))
# Et on fait aussi les enveloppes
def Envplus (tin, ain, fin, pin, tdecin):
	return ain*np.exp(-t/tdecin)

def Envminus (tin, ain, fin, pin, tdecin):
	return -ain*np.exp(-t/tdecin)

#Initialisation
s = Oscillation (t, a0, f0, p0, t0)
senvplus = Envplus (t, a0, f0, p0, t0)
senvminus = Envminus (t, a0, f0, p0, t0)

# Creation de la trace de la fonction s en fonction de t. C'est un objet qui est sauvegarde dans 'l'
l, = plt.plot(t,s, lw=2, color='red')
lenvplus, = plt.plot(t,senvplus, lw=1, ls='--',color='red', visible=False)
lenvminus, = plt.plot(t,senvminus, lw=1, ls='--',color='red',visible=False)

# Specification des limites des axes (xmin,xmax,ymin,ymax)
plt.axis([0, 1, -10, 10])

# Creation des barres de modification amplitude et frequence
axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.07, 0.65, 0.03], facecolor=axcolor)
axamp  = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axdec  = plt.axes([0.25, 0.13, 0.65, 0.03], facecolor=axcolor)
axphase  = plt.axes([0.25, 0.16, 0.65, 0.03], facecolor=axcolor)
sfreq = Slider(axfreq, '$f$ (Hz)', 0.1, 30.0, valinit=f0) # Remarquer la valeur initiale f0
samp = Slider(axamp, '$A$ (V)', 0.1, 10.0, valinit=a0) # Remarquer la valeur initiale a0
sdec = Slider(axdec, "tau (s)", 0.1, 2.0, valinit=t0) # Remarquer la valeur initiale t0
sphase = Slider(axphase, '$\phi$ (rad)', 0, 2.0*math.pi, valinit=p0) # Remarquer la valeur initiale p0

# Fonction de mise a jour du graphique
def update(val):
    amp = samp.val # On recupere la valeur de la barre samp comme amplitude
    freq = sfreq.val # On recupere la valeur de la barre sfreq comme frequence
    dec = sdec.val # On recupere la valeur de la barre sdec comme temps de decroissance
    p = sphase.val # On recupere la valeur de la barre sphase comme phase a l'origine
    l.set_ydata(Oscillation (t, amp, freq, p, dec)) # On met a jour l'objet 'l' avec ces nouvelles valeurs 
    lenvplus.set_ydata(Envplus (t, amp, freq, p, dec)) # On met a jour l'objet 'lenvplus' avec ces nouvelles valeurs 
    lenvminus.set_ydata(Envminus (t, amp, freq, p, dec)) # On met a jour l'objet 'lenvminus' avec ces nouvelles valeurs 
    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
sfreq.on_changed(update) # lorsque la barre sfreq est modifiee, on applique la fonction update
samp.on_changed(update) # lorsque la barre sfreq est modifiee, on applique la fonction update
sdec.on_changed(update) # lorsque la barre sdec est modifiee, on applique la fonction update
sphase.on_changed(update) # lorsque la barre sphase est modifiee, on applique la fonction update

# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    sfreq.reset() # La methode .reset() appliquee a la barre sfreq lui redonne sa valeur valinit, soit f0
    samp.reset() # La methode .reset() appliquee a la barre samp lui redonne sa valeur valinit, soit a0
    sdec.reset() # La methode .reset() appliquee a la barre sdec lui redonne sa valeur valinit, soit t0
    sphase.reset() # La methode .reset() appliquee a la barre sphase lui redonne sa valeur valinit, soit p0
button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus

# Creation du menu de changement des couleurs
#rax = plt.axes([0.015, 0.5, 0.15, 0.15], facecolor=axcolor)
#radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0) # La valeur par defaut est la numero 0 (red). Si on met active=1, c'est bleu, et active=2 c'est vert...
## Definition de la fonction de changement des couleurs
#def colorfunc(label):
#    l.set_color(label) # On change la couleur en appliquant celle qui est contenue dans "label", a savoir "red", "blue" ou "green"
#    lenvplus.set_color(label) # On change la couleur en appliquant celle qui est contenue dans "label", a savoir "red", "blue" ou "green"
#    lenvminus.set_color(label) # On change la couleur en appliquant celle qui est contenue dans "label", a savoir "red", "blue" ou "green"
#    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
#radio.on_clicked(colorfunc) # Quand on clique sur un choix, le "label" associe a ce choix est passe a la fonction colorfunc

# Creation du menu de selection des traces a afficher
cax = plt.axes([0.015, 0.3, 0.2, 0.15], facecolor=axcolor)
check = CheckButtons(cax, ('Fonction', 'Env. sup.', 'Env. inf.'), (True, False, False))
# Definition de la fonction qui passe un affichage de visible a invisible
def chooseplot(label):
    if label == 'Fonction': l.set_visible(not l.get_visible()) # Si on clique sur le bouton "Function", la trace 'l' passe visible si elle ne l'etait pas, et vice versa
    elif label == 'Env. sup.': lenvplus.set_visible(not lenvplus.get_visible()) # Si on clique sur le bouton "Upper envelope", la trace 'lenvplus' passe visible si elle ne l'etait pas, et vice versa
    elif label == 'Env. inf.': lenvminus.set_visible(not lenvminus.get_visible()) # Si on clique sur le bouton "Lower envelope", la trace 'lenvminus' passe visible si elle ne l'etait pas, et vice versa
    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
check.on_clicked(chooseplot) # Lorsqu'on coche un de ces boutons, on applique la fonction chooseplot

plt.show() # On provoque l'affichage a l'ecran


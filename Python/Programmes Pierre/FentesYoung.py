#Nom du programme : FentesYoung

#Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.10

#Liste des modifications
#v 1.00 : 2016-05-02 Première version complète 
#v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor

#Version de Python
# 3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#AVERTISSEMENT
#Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

#Description : 
#Ce programme représente la figure d'interférence obtenue lorsqu'une onde plane monochromatique de longueur d'onde lambda traverse un dispositif de fentes d'Young éloignées d'une distance a (centre-centre) et de largeur w. L'écran est positionné à une distance L des fentes. 
#Le résultat présenté est l'intensité lumineuse en fonction de la position sur l'écran.
#Les paramètres peuvent être variés indépendamment pour observer leur effet sur la figure d'interférence. Il est aussi possible de tracer l'enveloppe de diffraction correspondant à la diffraction par une fente de largeur w seule. 


#import des bibliothèques python
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

# Creation de la figure
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.30, bottom=0.30)

# Creation de l'axe des abscisses, ici la distance x
x = np.arange(-1., 1., 0.001)/100. #Zone observee : +/- 10 cm

# Parametres de la fonction, avec des valeurs par defaut
k0 = 2.*np.pi/(633./10.**9) # Vecteur d'onde
L0 = 1. # Distance ecran-fentes
a0 = 1./10**3 # Distance fentes
w0 = 100./10**6 # Largeur fente

# Creation de la fonction a tracer 
def Oscillation (kin, Lin, ain, win, xin):
	return np.cos(kin*ain*xin/(2*Lin))*np.cos(kin*ain*xin/(2*Lin))*np.sinc(kin*win*xin/(2*Lin))*np.sinc(kin*win*xin/(2*Lin))
# Et on fait aussi l'enveloppe
def EnvDiffraction (kin, Lin, ain, win, xin):
	return np.sinc(kin*win*xin/(2*Lin))**2



#Initialisation
s = Oscillation (k0, L0, a0, w0, x)
senvdiff = EnvDiffraction (k0, L0, a0, w0, x)

# Creation de la trace de la fonction s en fonction de x. C'est un objet qui est sauvegarde dans 'l'
l, = plt.plot(x, s, lw=2, color='red')
lenvdiff, = plt.plot(x, senvdiff, lw=1, ls='--',color='red', visible=True)



# Specification des limites des axes (xmin,xmax,ymin,ymax)
plt.axis([-0.01, 0.01, 0, 1])

#Nom des axes
plt.xlabel('Position sur l\'ecran (m)')
plt.ylabel('Intensite lumineuse (u.a.)')

#Titre de la figure
plt.title('Interference par des fentes d\'Young')

#Commentaires affichés
plt.text(-0.019, 0.9, r'$a$ distance entre fentes')
plt.text(-0.019, 0.85, r"$\lambda$ longueur d'onde")
plt.text(-0.019, 0.8, r"$w$ Largeur d'une fente")
plt.text(-0.019, 0.75, r'$L$ Distance fentes-ecran')


# Creation des barres de modification amplitude et frequence
axcolor = 'lightgoldenrodyellow'
axk = plt.axes([0.25, 0.07, 0.65, 0.03], facecolor=axcolor)
axa = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axw = plt.axes([0.25, 0.13, 0.65, 0.03], facecolor=axcolor)
axL = plt.axes([0.25, 0.16, 0.65, 0.03], facecolor=axcolor)
sk = Slider(axk, '$\lambda$ (nm)', 400., 800., valinit=633.) # Remarquer la valeur initiale 633 nm
sa = Slider(axa, '$a$ (mm)', 0.5, 3.0, valinit=a0*10**3) # Remarquer la valeur initiale a0*10**3
sw = Slider(axw, '$w$ ($\mu$m)', 10., 300., valinit=w0*10**6) # Remarquer la valeur initiale w0
sL = Slider(axL, '$L$ (m)', 0.3, 2.0, valinit=L0) # Remarquer la valeur initiale L0

# Fonction de mise a jour du graphique
def update(val):
    k = 2.*np.pi/(sk.val/10**9)  # On recupere la valeur de la barre sk comme vecteur d'onde
    a = sa.val/10**3 #Valeur recuperee en mm. On recupere la valeur de la barre sa comme distance entre les fentes
    w = sw.val/10**6 #Valeur récupérée en µm On recupere la valeur de la barre sw comme largeur d'une fente
    L = sL.val # On recupere la valeur de la barre sL comme distance a l'ecran
    l.set_ydata(Oscillation (k, L, a, w, x)) # On met a jour l'objet 'l' avec ces nouvelles valeurs 
    lenvdiff.set_ydata(EnvDiffraction (k, L, a, w, x)) # On met a jour l'objet 'lenvdiff' avec ces nouvelles valeurs 
    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
sa.on_changed(update) # lorsque la barre sa est modifiee, on applique la fonction update
sk.on_changed(update) # lorsque la barre sk est modifiee, on applique la fonction update
sL.on_changed(update) # lorsque la barre sL est modifiee, on applique la fonction update
sw.on_changed(update) # lorsque la barre sw est modifiee, on applique la fonction update

# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    sL.reset() # La methode .reset() appliquee a la barre sfreq lui redonne sa valeur valinit, soit L0
    sk.reset() # La methode .reset() appliquee a la barre samp lui redonne sa valeur valinit, soit 633 nm (attention, en longueur d'onde ici)
    sa.reset() # La methode .reset() appliquee a la barre sdec lui redonne sa valeur valinit, soit sa
    sw.reset() # La methode .reset() appliquee a la barre sphase lui redonne sa valeur valinit, soit sw
button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus
#
## Creation du menu de changement des couleurs
#rax = plt.axes([0.015, 0.5, 0.15, 0.15], facecolor=axcolor)
#radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0) # La valeur par defaut est la numero 0 (red). Si on met active=1, c'est bleu, et active=2 c'est vert...
## Definition de la fonction de changement des couleurs
#def colorfunc(label):
#    l.set_color(label) # On change la couleur en appliquant celle qui est contenue dans "label", a savoir "red", "blue" ou "green"
#    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
#radio.on_clicked(colorfunc) # Quand on clique sur un choix, le "label" associe a ce choix est passe a la fonction colorfunc

# Creation du menu de selection des traces a afficher
cax = plt.axes([0.015, 0.3, 0.2, 0.15], facecolor=axcolor)
check = CheckButtons(cax, ('Fonction', 'Env. diff.'), (True, True))
# Definition de la fonction qui passe un affichage de visible a invisible
def chooseplot(label):
    if label == 'Fonction': l.set_visible(not l.get_visible()) # Si on clique sur le bouton "Function", la trace 'l' passe visible si elle ne l'etait pas, et vice versa
    elif label == 'Env. diff.': lenvdiff.set_visible(not lenvdiff.get_visible()) # Si on clique sur le bouton "Env. diff.", la trace 'lenvdiff' passe visible si elle ne l'etait pas, et vice versa
    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
check.on_clicked(chooseplot) # Lorsqu'on coche un de ces boutons, on applique la fonction chooseplot



#plt.show() # On provoque l'affichage a l'ecran


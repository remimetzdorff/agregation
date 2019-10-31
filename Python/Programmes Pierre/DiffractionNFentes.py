'''
#Nom du programme : DiffractionNFentes

#Auteurs : Arnaud Raoux, Emmanuel Baudin, François Lévrier et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.20

#Liste des modifications
#v 1.00 : 2016-03-01 Première version complète
#v 1.10 : 2016-05-02 Mise à jour de la mise en page
#v 1.20 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor

#Version de Python
#3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#AVERTISSEMENT
#Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

#Description : 
#Ce programme représente la figure d'interférence obtenue lorsqu'une onde plane monochromatique de longueur d'onde lambda traverse un dispositif de N fentes régulièrement espacées d'une distance a (centre-centre) et de largeur b chacunes. L'écran est positionné à une distance D des fentes. 
# Le résultat présenté est l'intensité lumineuse normalisée en fonction de la position réduite sur l'écran pour permettre une comparaison des différentes situations.
#Les paramètres peuvent être variés indépendamment pour observer leur effet sur la figure d'interférence. Il est aussi possible de tracer l'enveloppe de diffraction correspondant à la diffraction par une fente de largeur w seule. 
'''

#import des bibliothèques python
from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons

# =============================================================================
# --- Defaults values ---------------------------------------------------------
# =============================================================================

N0 = 2  # Nombre de fentes
a0 = 2  # Pas du reseau (distance entre fentes en µm)
b0 = 1  # taille d'une fente (en µm)
lamb0 = 0.633  # Longueur d'onde dans le vide (en µm)


# =============================================================================
# --- Utility functions -------------------------------------------------------
# =============================================================================

def forme(abscisses, b):
    """
    Calcule le facteur de forme du reseau.
    """
    return (np.sinc(b*abscisses))**2


def structure(abscisses, lamb, a, N):
    """
    Calcule le facteur de structure du reseau.
    """
    return (np.sin(N*np.pi*a*abscisses/lamb) /
            (N*np.sin(np.pi*a*abscisses/lamb)))**2


def signal(abscisses, b, lamb, a, N):
    """
    Le signal est le produit du facteur de forme et du facteur de structure.
    """
    return forme(abscisses, b)*structure(abscisses, lamb, a, N)

# =============================================================================
# --- Creation de la figure ---------------------------------------------------
# =============================================================================

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

# Creation de l'axe des abscisses, ici sin(theta) où theta est l'angle de sortie du faisceau. sin(theta)=x/D

abscisses = np.arange(-2.0, 2.0, 0.001)

#La ligne qui quit indique l'équation utilisé pour obtenir la courbe.
# plt.text(0, 1.2, r'$\frac{I}{I_0} = \mathrm{sinc}^2\left(\frac{\pi bx}{\lambda_0D}\right)\times\frac{\sin^2(N\pi a x/\lambda_0D)}{N^2\sin^2(\pi ax/\lambda_0D)}$',        horizontalalignment='center', fontsize='22')

#Commentaires utiles affichés
plt.text(-3.4, 1., r'$a$ pas du reseau')
plt.text(-3.4, 0.9, r"$\lambda_0$ longueur d'onde")
plt.text(-3.4, 0.8, r'$b$ Taille de la fente')
plt.text(-3.4, 0.7, r'$N$ Nombre de fentes')
plt.text(-3.4, 0.6, r'$D$ Distance reseau-ecran (1 m)')

#Titre de la figure
plt.title('Figure de diffraction par N fentes')

#Nom des axes
plt.xlabel(r'Position reduite sur l ecran ($\frac{\pi bx}{\lambda_0D}$)')
plt.ylabel('Intensite lumineuse normalisee')


# Limites des axes (xmin,xmax,ymin,ymax)
plt.axis([abscisses[0], abscisses[-1], -0.1, 1.4])

# Creation de la trace de la fonction s en fonction de abscisses.
# C'est un objet qui est sauvegarde dans 'l'
PLOTS = {}
PLOTS['Fonction'] = plt.plot(abscisses, signal(abscisses, b0, lamb0, a0, N0),
                             lw=2, color='red')[0]
PLOTS['Facteur de forme'] = plt.plot(abscisses, forme(abscisses, b0), lw=1.5,
                                     ls='--', color='blue', visible=False)[0]
PLOTS['Facteur de structure'] = plt.plot(abscisses,
                                         structure(abscisses, lamb0, a0, N0),
                                         lw=1.5, ls='--', color='green',
                                         visible=False)[0]


# Positionnement des barres de modification
axcolor = 'lightgoldenrodyellow'  # Choix de la couleur
ax_N = plt.axes([0.25, 0.07, 0.65, 0.03], facecolor=axcolor)
ax_a = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_b = plt.axes([0.25, 0.13, 0.65, 0.03], facecolor=axcolor)
ax_lamb = plt.axes([0.25, 0.16, 0.65, 0.03], facecolor=axcolor)

# Noter les valeurs initiales
s_N = Slider(ax_N, 'N', 2, 30.0, valinit=N0)
s_a = Slider(ax_a, 'a (µm)', 0.1, 10.0, valinit=a0)
s_b = Slider(ax_b, 'b (µm)', 0.1, 2.0, valinit=b0)
s_lamb = Slider(ax_lamb, r"$\lambda_0$ (µm)", 0.1, 3., valinit=lamb0)


def update(val):
    """
    Met a jour le graph a partir des valeurs des sliders.
    """
    N = s_N.val  # On recupere la valeur de la barre s_N
    a = s_a.val  # On recupere la valeur de la barre s_a
    b = s_b.val  # On recupere la valeur de la barre s_b
    lamb = s_lamb.val  # On recupere la valeur de la barre s_lamb

    f = forme(abscisses, b)
    s = structure(abscisses, lamb, a, N)

    PLOTS['Fonction'].set_ydata(f*s)  # On met a jour le signal
    PLOTS['Facteur de forme'].set_ydata(f)  # On met a jour la forme
    PLOTS['Facteur de structure'].set_ydata(s)  # On met a jour la structure

    if (N-int(N) != 0):
        s_N.set_val(int(s_N.val))

    # On provoque la mise a jour du graphique (pas automatique par defaut)
    fig.canvas.draw_idle()

# Chaque fois qu'un slider est modifie, on appelle la fonction update
for s in (s_N, s_a, s_b, s_lamb):
    s.on_changed(update)


# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    """
    On rend leurs valeurs initiales a tous les sliders.
    """
    for s in (s_N, s_a, s_b, s_lamb):
        s.reset()

# Lorsqu'on clique sur "reset", on appelle la fonction reset
button.on_clicked(reset)

# Creation du menu de selection des traces a afficher
cax = plt.axes([0.015, 0.3, 0.2, 0.15], facecolor=axcolor)
check = CheckButtons(cax,
                     ('Fonction', 'Facteur de forme', 'Facteur de structure'),
                     (True, False, False))


# Definition de la fonction qui passe un affichage de visible a invisible
def chooseplot(label):
    """
    Choose which plot to diplay.
    """
    graph = PLOTS[label]
    graph.set_visible(not graph.get_visible())
    fig.canvas.draw_idle()  # On provoque la mise a jour du graphique

# Lorsqu'on coche un de ces boutons, on appelle la fonction chooseplot
check.on_clicked(chooseplot)

plt.show()  # On provoque l'affichage a l'ecran

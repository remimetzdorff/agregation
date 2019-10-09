'''
Nom du programme : PropagationAvecDispersion

Auteurs : Vincent Lusset, Arnaud Raoux et la prépa agreg de Montrouge
Adresse : Departement de physique de l'Ecole Normale Superieure
		24 rue Lhomond
		75005 Paris
Contact : arnaud.raoux@ens.fr

Année de création : 2018
Version : 1.1

Liste des modifications
v 1.00 : 2018-03-01 Première version complète
v 1.10 : 2019-03-12 Amélioration, simplification et nettoyage du code

Version de Python
3.6

LICENCE
Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

AVERTISSEMENT
Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

Description : 
Ce programme permet d'observer l'effet de la dispersion sur la propagation d'une onde, et en particulier de faire la différence entre vitesse de phase et vitesse de groupe.
'''
#import des bibliothèques/fonctions python
from matplotlib import pyplot, animation
from numpy import *

# =============================================================================
# --- Définitions ------------------------------------------------
# =============================================================================

Xmin = -2
Xmax = 10.0 #échelle max selon l'axe de propagation
Tmax = 10.0 #échelle max selon le temps

NbEchantillons=3000 # Échantillonage spatial
NbEchantillonsT=100 # Échantillonage temporel

x = linspace(Xmin,Xmax,NbEchantillons) # x est ici un array en ligne
t = linspace(0,Tmax,NbEchantillonsT).reshape((NbEchantillonsT,1)) # t un array en colonne

T=0.25 #période de l'onde

#définition des vitesses de phase et de groupe (à optimiser, avec vphi > vg)
c=1
vphi=1.1*c # Pas de dispersion si vphi=vg
vg=c**2/vphi

tau = 15 # Temps d'amortissement de l'onde. À comparer à Tmax

# =============================================================================
# --- Creation de la figure ------------------------------------------
# =============================================================================
fig = pyplot.figure()
ax = pyplot.axes(xlim=(Xmin, Xmax), ylim=(-1.5, 1.5))

ax.set_xlabel(r'x')
ax.set_ylabel(r'$\psi$')
ax.set_title('Propatation d\'un paquet d\'onde\n avec dispersion')

ax.axhline(y=1,xmin=Xmin,xmax=Xmax,linestyle=':',color='grey') 
ax.axhline(y=-1,xmin=Xmin,xmax=Xmax,linestyle=':',color='grey') 

# =============================================================================
# --- Matrices de données ------------------------------------------
# =============================================================================

# On construit des matrices où chaque ligne correspond à un instant t donné.
att = 1+(t/tau)**2

mescourbes=exp(-(t-x/vg)**2/att)*cos(2*pi/T*(t-x/vphi))/att
monenveloppe_p=exp(-(t-x/vg)**2/att)/att
monenveloppe_m=-exp(-(t-x/vg)**2/att)/att

max_enveloppe = (vg*t,1/att)

# =============================================================================
# --- Initialisation ------------------------------------------
# =============================================================================

courbe, = ax.plot(x,mescourbes[0,:],'c-')
enveloppes_p, = ax.plot(x,monenveloppe_p[0,:], 'r--')
enveloppes_m, = ax.plot(x,monenveloppe_m[0,:], 'r--')

points_vg, = pyplot.plot([], [], 'ro')  # point rouge avançant à vg
points_vphi, = pyplot.plot([], [], 'bo') # point bleu avançant à vphi

# =============================================================================
# --- Incrémentation ------------------------------------------
# =============================================================================

def incrementemps(i):
   courbe.set_ydata(mescourbes[i,:])
   enveloppes_p.set_ydata(monenveloppe_p[i,:])
   enveloppes_m.set_ydata(monenveloppe_m[i,:])
   points_vg.set_data(max_enveloppe[0][i],max_enveloppe[1][i])

   x_vphi = t[i]*vphi # position du point à l'instant t[i]
   indice_x = where(x>x_vphi)[0][0] # on recherche l'indice qui correspond le mieux à x[indice]=x_vphi
   points_vphi.set_data(x_vphi,mescourbes[i,indice_x])

   return courbe,

# =============================================================================
# --- Animation  --------------------------------------------------------------
# =============================================================================

line_ani = animation.FuncAnimation(fig, incrementemps, 100, interval=50, blit=False)

pyplot.show()
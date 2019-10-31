'''
#Nom du programme : PortraitdePhase

#Auteurs : Arnaud Raoux, François Lévrier, Emmanuel Baudin et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.00

#Liste des modifications
#v 1.00 : 2016-05-02 Première version complète

#Version Python
#3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#AVERTISSEMENT
#Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

#Description : 
#Ce programme permet de représenter partiellement le portrait de phase d'une solution de l'équation d'un pendule simple. Seules les trajectoires commençant à theta=0 (avec une grande gamme de vitesses initiales) sont tracées, d'où un portrait de phase non rempli.
'''

#import des bibliothèques python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint # Pour la resolution d'equations differentielles

# =============================================================================
# --- Définitions ------------------------------------------------
# =============================================================================

om0=4 # Pulsation propre en U.A.

N=100 # le nombre de pas
t=np.linspace(0,5,N) # le temps en U.A.

# Etats initiaux
Ninit=20 # nbr de conditions initiales
theta0=0*np.ones(Ninit) # angle initial fixé à 0
dtheta0=np.linspace(-50,50,Ninit)


# =============================================================================
# --- Fonction intermediaire ------------------------------------------------
# =============================================================================

def eq_diff(etat_courant,t):
    """
    Fonction qui encode l equation differentielle
    """  
    return np.array([etat_courant[1],-om0**2*np.sin(etat_courant[0])])


# =============================================================================
# --- Creation de la figure ------------------------------------------
# =============================================================================
fa, ax = plt.subplots(1, sharex=True)

ax.set_title(r"Portrait de phase d'un pendule simple")
ax.set_ylim(-15,15)
ax.set_ylabel(r'$\dot \theta$')
ax.set_xlim(-8,8)
ax.set_xlabel(r'$\theta$')

# =============================================================================
# --- Résolution de l'equation differentielle pour chaque condition intiale ---
# =============================================================================

for i in np.arange(Ninit):
  etat0=np.array([theta0[i],dtheta0[i]/om0])
  solution = odeint(eq_diff, etat0, t)
    
  ax.plot(solution[:,0],solution[:,1],color='red',linewidth=1)
  ax.plot(-solution[:,0],solution[:,1],color='red',linewidth=1) # la fonction dtheta(theta) etant paire
#ax.axis('equal')
 
plt.show()



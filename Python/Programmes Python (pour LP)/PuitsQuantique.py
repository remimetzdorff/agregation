'''
#Nom du programme : PuitsQuantique

#Auteurs : Arnaud Raoux, François Lévrier, Emmanuel Baudin et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.0

#Liste des modifications
#v 1.00 : 2016-03-01 Première version complète

#Version de Python
#3.6

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#Description : 
#Ce programme permet de représenter les niveaux d'énergie dans un puits quantique, ainsi que les fonctions d'onde correspondantes. Il est inspiré d'un programme détaillé dans les références.
'''

#import des bibliothèques python
from pylab import *
from scipy.integrate import odeint # Pour la resolution d'equations differentielles
from scipy.optimize import brentq # Pour trouver les zeros d'une fonction

# =============================================================================
# --- References ------------------------------------------------
# =============================================================================

## Griffiths, Introduction to Quantum Mechanics, 1st edition, page 62.
## https://helentronica.wordpress.com/2014/09/04/quantum-mechanics-with-the-python/

# =============================================================================
# --- Definitions ------------------------------------------------
# =============================================================================


N = 1000                  # Discretisation du puits
psi = np.zeros([N,2])     # Vecteur contenant [psi, psi']
psi0 = array([0,1])       # Condition initiale pour psi0
Vo = 30                   # Hauteur du puits quantique
E = 0.0                   # Variable globale amenee a changer
b = 2                     # Point en dehors du puits pour verifier si la fonction diverge
x = linspace(-b, b, N)    # abscisses
L=1                       # largeur du puits

# =============================================================================
# --- Fonctions intermediaires ------------------------------------------------
# =============================================================================

def V(x):
    """
    Potentiel du puits quantique. L est la largeur du puits, et Vo la hauteur
    """
    if abs(x) < L:
        return 0
    else:
        return Vo

def SE(psi, x):
    """
    Fonction qui renvoie le vecteur (psi',psi'') grace a l'equation de Schrodinger
    """
    state0 = psi[1]
    state1 = 2.0*(V(x) - E)*psi[0]
    return array([state0, state1])
 
def Wave_function(energy):
    """
    Calcule la fonction d'onde solution de l'equation de Schrodinger, et renvoie sa valeur en b
    """
    global psi,E
    
    E = energy
    psi = odeint(SE, psi0, x)
    return psi[-1,0]
 
def find_all_zeroes(x,y):
    """
    Donne tous les zeros de y = Psi(x)
    """
    all_zeroes = []
    s = sign(y)
    for i in range(len(y)-1):
        if s[i]+s[i+1] == 0:
            zero = brentq(Wave_function, x[i], x[i+1])
            all_zeroes.append(zero)
    return all_zeroes

def find_analytic_energies(en):
    """
    Calcule les energies du puits carre. cf. Griffiths, Introduction to Quantum Mechanics, 1st edition, page 62.
    """
    z = sqrt(2*en)
    z0 = sqrt(2*Vo)
    z_zeroes = []
    f_sym = lambda z: tan(z)-sqrt((z0/z)**2-1)      # Equation implicite pour les valeurs symetriques
    f_asym = lambda z: -1/tan(z)-sqrt((z0/z)**2-1)  # Equation implicite pour les valeurs antisymetriques
 
    # Pour les fonctions d'onde symetriques
    s = sign(f_sym(z))
    for i in range(len(s)-1):
       if s[i]+s[i+1] == 0:
           zero = brentq(f_sym, z[i], z[i+1])
           z_zeroes.append(zero)
    
    # Pour les fonctions d'onde antisymetriques
    z_zeroes = []
    s = sign(f_asym(z))
    for i in range(len(s)-1):   # find zeroes of this crazy function
       if s[i]+s[i+1] == 0:
           zero = brentq(f_asym, z[i], z[i+1])
           z_zeroes.append(zero)

# =============================================================================
# --- Fonction principal (main loop) ------------------------------------------
# =============================================================================

def main():
    """
    L'idee est de scanner toutes les energies entre 0 et 100Vo, et de chercher celles dont la fonction d'onde vaut 0 loin a l'interieur du puits (en x=b).
    """        
    
    en = linspace(0.1, Vo, 100)   # Energies que l'on va investiger pour trouver les etats propres
    psi_b = []      # Vecteur contenant les valeurs en x=b
 
    for e1 in en:
        psi_b.append(Wave_function(e1))     
    E_zeroes = find_all_zeroes(en, psi_b) # On ne selectionne que les energies telles que la fonction d'onde vaut 0 en x=b
 
    # =============================================================================
    # --- Creation de la figure ------------------------------------------
    # =============================================================================
    f, ax = subplots(2, sharex=True) # La figure sera composee de deux sous-figures
 
    ## Energies
    
    ax[1].set_title(r'Energies propres')
    ax[1].set_ylim(-0.2,1.5)
    ax[1].set_ylabel('$E/V_0$')
    ax[1].set_xlim(-2,2)
    ax[1].set_xlabel('$x/L$')
    
    for E in E_zeroes[0:4]:
        ax[1].plot(linspace(-1,1,50), E*ones(50)/Vo, label="E = %.2f"%E)
    
    #Dessin du puits
    l1=ax[1].plot(linspace(-2,-1,50),ones(50),-1*ones(50),linspace(0,1,50),linspace(-1,1,50),0*ones(50)/Vo,1*ones(50),linspace(0,1,50),linspace(1,2,50),ones(50))
    plt.setp(l1, linewidth=2, color='k')
    
    #Pointilles
    l2=ax[1].plot(-1*ones(50),linspace(-0.5,1.5,50),1*ones(50),linspace(-0.5,1.5,50))
    plt.setp(l2, linewidth=0.5, color='k',linestyle='--')

    ## Fonctions d'onde
    
    for E in E_zeroes[0:4]:
        Wave_function(E)
        ax[0].plot(x, psi[:,0], label="E = %.2f"%E)

    ax[0].set_title("Fonctions d'onde propres")
    ax[0].set_ylim(-250,800)
    ax[0].set_ylabel('$\Psi(x)$', rotation='horizontal', fontsize = 15)
    
    # Pointilles
    l3=ax[0].plot(-1*ones(50),linspace(-300,300,50),1*ones(50),linspace(-300,300,50))
    plt.setp(l3, linewidth=0.5, color='k',linestyle='--')


main()
show()
#input()




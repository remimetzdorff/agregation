#Nom du programme : EffetTunnel

#Auteurs : Arnaud Raoux, François Lévrier et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.10

#Liste des modifications
#v 1.00 : 2016-05-15 Première version complète
#v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor


#Version de Python
# 3.4

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


#Description : 
#Ce programme permet de calculer la transmission d'une barrière de potentiel pour une onde de matière incidente d'énergie E variable. Il permet en particulier de mettre en évidence l'effet tunnel. La formule de la transmission est donnée sur la figure, et celle-ci est tracée en fonction de l'énergie de la particule incidente. Il est également possible de faire varier la largeur de la barrière d. Sont également représentées, l'équivalent classique de la transmission, et l'approximation de barrière large habituelle en mécanique quantique dans sa limite de validité.



# =============================================================================
# --- Importation de modules Python--------------------------------------------
# =============================================================================

import cmath, math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import scipy.integrate as integrate


# =============================================================================
# --- References--------------------------------------------
# =============================================================================

## https://fr.wikipedia.org/wiki/Effet_tunnel

# =============================================================================
# --- Definitions et normalisations--------------------------------------------
# =============================================================================

hbar = 1#.054e-34
m = 1#9.1093e-31
i=complex(0,1)

d0 = 2 # Épaisseur de la barriere
V0 = 1 # Hauteur de la barriere, c'est l'unite d'energie
Emax0=6 # Maximum de l'axe des abscisses, en unite de V0
approx = 1.3 # Valeur minimale acceptable pour K*d afin que l'approximation de barriere large soit verifiee
# Creation de l'axe des abscisses ici l'energie
nbr_points=1000 # Nombre de points du trace


# =============================================================================
# --- Creation de la figure ---------------------------------------------------
# =============================================================================

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25) # On ajuste la taille de la figure (rectangle blanc)
ax.set_title(r'Transmission a travers une barriere de potentiel $V_0$') # Cela fixe le titre

# Parametres de la fonction, avec des valeurs par defaut

def abscisses(xmin,xmax,nbr): return np.linspace(xmin, xmax, nbr) # fonction qui permettra de modifier l'axe horizontal
absci0 = abscisses(0,Emax0, nbr_points) # Axe initial
plt.axis([absci0[0], absci0[-1], 0, 1.2]) # Limites des axes (xmin,xmax,ymin,ymax)

# Texte explicatif
plt.text(1,0.7,r'$T = \frac{4K^2k^2}{(K^2+k^2)\mathrm{sh}^2(Kd)+4K^2k^2}$',horizontalalignment='right',fontsize='xx-large',transform=ax.transAxes)
plt.text(1,0.55,r'$K = \sqrt{2m(V_0-E)}/\hbar$',horizontalalignment='right',fontsize='medium',transform=ax.transAxes)
plt.text(1,0.48,r'$k = \sqrt{2mE}/\hbar$',horizontalalignment='right',fontsize='large',transform=ax.transAxes)
plt.text(1,0.4,r'$d$ Épaisseur, $V_0$ hauteur',transform=ax.transAxes,horizontalalignment='right')


# Creation de la fonction a tracer
def transmission(E,V,d,forme):
  if (forme == 'carre'): # Laisse la possibilite d'une barriere non carree, pas encore implementee
    k=np.sqrt(2*m*E)/hbar # Vecteur d'onde a l'exterieur de la barriere
    K=np.sqrt(2*m*(V-E)+0*i)/hbar # Vecteur d'onde a l'interieur de la barriere
    #t=2*i*k*K*np.exp(-i*k*d)*1/ ( (K**2+k**2)*np.sinh(K*d) + 2*i*K*k*np.cosh(K*d) ) # coefficient de transmission en amplitude
    T=np.real(4*K**2*k**2 / ( (K**2+k**2)**2*np.sinh(K*d)**2 + 4*K**2*k**2 ) ) # coefficient de transmission en probabilite
    return T

def transmission_classique(E,V,d,forme): # Cas classique
  T = (E-V > 0) # Si E>V, la particule passe, sinon elle est reflechie
  return T

def limite_large_barriere(E,V,d,forme): # Cas d'effet tunnel pour une barriere epaisse, ou la formule se simplifie
  k=np.sqrt(2*m*E)/hbar # Vecteur d'onde a l'exterieur de la barriere
  K=np.sqrt(2*m*(V-E)+0*i)/hbar # Vecteur d'onde a l'interieur de la barriere
  T=np.real(16*K**2*k**2 / (K**2+k**2)**2 *np.exp(-2*K*d))
  return T

s = transmission(absci0,V0,d0,'carre')
s_cla=transmission_classique(absci0,V0,d0,'carre')

absci_red0=absci0[np.where(absci0<V0)] # On se limite a l'effet tunnel : E<V0
absci_red0=absci_red0[np.where(np.sqrt(2*m*(V0-absci_red0)/hbar*d0)>approx)] # On limite le trace au cas de validite de l'approximation : Kd>approx avec "approx" defini dans les parametres
s_lim=limite_large_barriere(absci_red0,V0,d0,'carre')

## Creation de la trace de la fonction s en fonction de abscisses. C'est un objet qui est sauvegarde dans 'l'
l, = plt.plot(absci0,s, lw=2, color='red', label='Quantique')
l_cla, =plt.plot(absci0,s_cla, lw=2, ls='--', color='blue', label='Classique')
l_lim, =plt.plot(absci_red0,s_lim, lw=3, ls='--', color='green', label='barriere large: Kd>'+str(approx))

plt.xlabel('Énergie (en unite de $V_0$)') # Label de l'axe des abscisses
plt.ylabel('Transmission') # Label de l'axe des ordonnees

# Positionnement des barres de modification
axcolor = 'lightgoldenrodyellow'  # Choix de la couleur
ax_d = plt.axes([0.1, 0.1, 0.75, 0.03], facecolor=axcolor)
ax_Emax  = plt.axes([0.1, 0.07, 0.75, 0.03], facecolor=axcolor)

s_d = Slider(ax_d, r'$d$', 0, 5.0, valinit=d0) # Remarquer la valeur initiale d0
s_Emax = Slider(ax_Emax, r'$E_\mathrm{max}$', 1, 10.0, valinit=Emax0) # Remarquer la valeur initiale Emax0

# Fonction de mise a jour du graphique
def update(val):
  d = s_d.val # On recupere la valeur de la barre s_d
  Emax = s_Emax.val # On recupere la valeur de la barre s_Emax
  absci = abscisses(0,Emax,nbr_points) # absci est le nouvel axe des abscisses
  ax.set_xlim(0,Emax) # On fixe les limites de l'axe des abscisses sur la figure

  l.set_xdata(absci) # On met a jour l'abscisse de l'objet 'l'
  l.set_ydata(transmission(absci,V0,d,'carre')) # On met a jour l'ordonnee de l'objet 'l'
  l_cla.set_xdata(absci) # On met a jour l'abscisse de l'objet 'l'
  l_cla.set_ydata(transmission_classique(absci,V0,d,'carre')) # On met a jour l'ordonnee de l'objet 'l'
  
  absci_red=absci[np.where(absci<V0)] # On se limite a l'effet tunnel : E<V0
  absci_red=absci_red[np.where(np.sqrt(2*m*(V0-absci_red)/hbar*d)>approx)] # On limite le trace au cas de validite de l'approximation : Kd>approx avec "approx" defini dans les parametres
  l_lim.set_xdata(absci_red) # On met a jour l'abscisse de l'objet 'l'
  l_lim.set_ydata(limite_large_barriere(absci_red,V0,d,'carre')) # On met a jour l'ordonnee de l'objet 'l'
  fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
    
s_d.on_changed(update) # lorsque la barre s_d est modifiee, on applique la fonction update
s_Emax.on_changed(update) # lorsque la barre s_Emax est modifiee, on applique la fonction update

leg=ax.legend(loc=4) # On affiche la legende. La position 4 correspond a 'lower right'

# Creation du bouton de "reset"
resetax = plt.axes([0.8, 0.015, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# Definition de la fonction de "reset" (valeurs par defaut)
def reset(event):
    s_d.reset() # La methode .reset() appliquee a la barre s_N lui redonne sa valeur valinit, soit f0
    s_Emax.reset() # La methode .reset() appliquee a la barre s_a lui redonne sa valeur valinit, soit a0
        
button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus

plt.show() # On provoque l'affichage a l'ecran

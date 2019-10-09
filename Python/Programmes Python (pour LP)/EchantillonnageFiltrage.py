#Nom du programme : EchantillionageFiltrage

#Auteurs : David Delgove, Arnaud Raoux et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 20167
#Version : 1.00

#Liste des modifications
#v 1.00 : 2017-06-09 Première version complète
#v 1.10 : 2018-05-08 Ajout d'un slider pour la fréquence d'échantillonage
#v 1.20 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor


#Version de Python
#3.5

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#AVERTISSEMENT
#Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

#Description : 
#Ce programme a pour objectif de mettre en évidence l'effet d'échantionnage, ainsi que l'effet de filtrage sur un signal analogique.

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

# =============================================================================
# --- Définitions des paramètres sur lesquels on peut agir --------------------
# =============================================================================

### Signal analogique ###
Forme_signal = 0 # 0 cosinus / 1 : rectangulaire # forme du signal échantillongé
fe = 10 # fréquence du signal
Amplitude = 1.0 # Amplitude du signal

### Signal numérique d'entrée ###
Tacquisition = 1 # durée d'acquisition
fechantillonnage0 = 35 # fréquence d'échantillonnage

### Signal numérique post-filtre passe-bas ###
Plot_Action_filtre = False # Tracer ou non l'action du filtre passe-bas
fc = 0.5 # fréquence de coupure du filtre
    
# =============================================================================
# --- Fonction intermediaire qui échantillone le signal -----------------------
# =============================================================================

def TableSignalEntree(fe,fech,Tacq,A) : 
    '''
    fe : fréquence du signal
    fech : fréquence d'échantillonage
    Tacq : Temps d'acquisition
    A : amplitude du signal
    '''

    Npoint = int(fech*Tacq+1)
    temps=np.linspace(1,Npoint,Npoint)/fech
    
    if (Forme_signal): # Cas où le signal est rectangulaire
        test=round(2*temps*fe,0) %2
        signal=A*(2*test-1)
        
    else: # Cas où le signal est sinusoidal
        signal=A*np.cos(2*np.pi*fe*temps)
    
    return temps,signal
  
# =============================================================================
# --- Fonction qui applique le filtre passe-bas sur le signal -----------------
# =============================================================================
    
def PasseBas(fcoupure,fech,Entree) : 
    '''
    fcoupure : fréquence de coupure du filtre
    fech : fréquence d'échantillonnage du signal d'entrée
    Entree : table contenant le signal d'entrée
    '''

    Sortie = [0]
    for i in range(0,len(Entree)-1) :
        Sortie.append(Sortie[i]+2*math.pi*fcoupure/fech*(Entree[i]-Sortie[i]))
    return Sortie

    
# =============================================================================
# --- Code principal-----------------------------------------------------------
# =============================================================================

#Table du signal analogique (en fait échantilloné avec une très grande fréquence : aucun problème de repliement de spectre)
Table_vrai_signalx, Table_vrai_signaly = TableSignalEntree(fe,200*fe,Tacquisition,Amplitude)
    
#Table du signal échantilloné initial
Tablex,Tabley = TableSignalEntree(fe,fechantillonnage0,Tacquisition,Amplitude)

## Calcul l'action du filtre 
#if Plot_Action_filtre :
    #sortie = PasseBas(fc,fechantillonnage,Tabley)

fig, ax = plt.subplots(1, sharex=True)
plt.subplots_adjust(left=0.12, bottom=0.2)

if Plot_Action_filtre :
    ax.set_title(r'Filtre Passe-bas (fech='+str(fechantillonnage0)+' Hz, fana='+str(fe)+' Hz, fc='+str(fc)+' Hz)')
    Msize = 0; Mtype = '.'
else :
    ax.set_title(r'Echantillonnage ($f_\mathrm{analog}=$'+str(fe)+' Hz)')
    Msize = 10; Mtype = 'x'

    
#Titres et dimensions des axes 
ax.set_ylim(-1.5*Amplitude,1.5*Amplitude)
ax.set_ylabel(r'U.A')
ax.set_xlim(0,Tacquisition)
ax.set_xlabel(r't(s)')
plt.grid(True)

#Trace le signal "analogique", le signal échantilloné et le signal filtré
ax.plot(Table_vrai_signalx,Table_vrai_signaly,color='blue',linewidth=1,label="Analogique")
l, = ax.plot(Tablex,Tabley,color='red',marker=Mtype,markersize=Msize,linewidth=2,label="Numérique")

#if Plot_Action_filtre :
    #ax.plot(Tablex,sortie,color='black',marker=Mtype,markersize=Msize,linewidth=2,label="Sortie du filtre")

plt.legend(loc="upper left", bbox_to_anchor=[0, 1],ncol=3, shadow=True,fancybox=True)

# =============================================================================
# --- Slider fréquence --------------------------------------------------------
# =============================================================================

# Creation des barres de modification amplitude et frequence
axcolor = 'lightgoldenrodyellow'
axf = plt.axes([0.25, 0.07, 0.65, 0.03], facecolor=axcolor)
sf = Slider(axf, '$f_\mathrm{echantillonnage}$ (Hz)', 5., 60., valinit=fechantillonnage0) # Remarquer la valeur initiale 633 nm

# Fonction de mise a jour du graphique
def update(val):
    fechantillonnage=sf.val  # On recupere la valeur de la barre sk comme vecteur d'onde
    new_x, new_y =  TableSignalEntree(fe,fechantillonnage,Tacquisition,Amplitude)
    l.set_ydata(new_y) # On met a jour l'objet 'l' avec ces nouvelles valeurs
    l.set_xdata(new_x) # On met a jour l'objet 'l' avec ces nouvelles valeurs 
    fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
sf.on_changed(update) # lorsque la barre sa est modifiee, on applique la fonction update


plt.show() # On provoque l'affichage a l'ecran

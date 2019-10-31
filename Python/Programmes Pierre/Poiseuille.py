'''
#Nom du programme : Poiseuille

#Auteurs : Arnaud Raoux, Emmanuel Baudin, François Lévrier et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 2016 
#Version : 1.10

#Liste des modifications
#v 1.00 : 2016-03-01 Première version complète
#v 1.10 : 2016-05-02 Mise à jour de la mise en page

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#Description : 
#Ce programme représente le champ de vitesse dans un ecoulement de Poiseuille (tube)
'''

#import des bibliothèques python
import matplotlib.pyplot as plt
import numpy as np

#Definition d'un maillage du plan dans lequel a lieu l'ecoulement
Y, X = np.mgrid[-1:1:25j, 0:3:6j]

#Calcul du champ de vitesse
U = 4*(1-(Y**2))
V = 0

#Epaisseur des vecteurs vitesse
widths = np.linspace(0, 2, X.size)

# Creation de la figure
plot2 = plt.figure()

#Creation des vecteurs vitesse
plt.quiver(X, Y, U, V, 
           color='Teal', 
           scale=25,
           headlength=10)

#Definition des axes
plt.axis([0,3,-1.5,1.5])

#Repere des limites superieure et inferieure de l'ecoulement
plt.plot(np.linspace(-3,3,1000),np.ones(1000),'k')
plt.plot(np.linspace(-3,3,1000),-np.ones(1000),'k')

#Titre du graphique
plt.title('Ecoulement de Poiseuille')

#Nom des axes
plt.xlabel('Position X (m)')
plt.ylabel('Position Z (m)')


plt.show(plot2) # On provoque l'affichage a l'ecran



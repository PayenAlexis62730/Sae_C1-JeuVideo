import math
import random

# Classe mère pour chaque ennemi
class Ennemi:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.vitesse = 0  # Initialisation de la vitesse à zéro

    def attaquer(self):
        pass

    def se_deplacer_vers_cible(self, joueur_le_plus_proche):
        direction_x = 0
        direction_y = 0

        if joueur_le_plus_proche.x < self.x:
            direction_x = -1
        elif joueur_le_plus_proche.x > self.x:
            direction_x = 1

        if joueur_le_plus_proche.y < self.y:
            direction_y = -1
        elif joueur_le_plus_proche.y > self.y:
            direction_y = 1

        # Appliquer la vitesse de l'ennemi
        self.x += direction_x * self.vitesse
        self.y += direction_y * self.vitesse

        # Assurance que l'ennemi reste dans les limites du plateau
        self.x = max(0, min(self.x, 15))
        self.y = max(0, min(self.y, 7))

class Barbare(Ennemi):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.PV = 22
        self.ATK = 8
        self.DEF = 2
        self.vitesse = 3

    def attaquer(self):
        attaque = self.ATK
        # Logique d'attaque pour le Barbare

class Chasseur_Drag(Ennemi):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.PV = 65
        self.ATK = 6
        self.DEF = 2
        self.vitesse = 4
        self.image_path = 'Sprite/ChasseurDrag.png'  # Chemin vers l'image du Chasseur_Drag

    def attaquer(self):
        attaque = self.ATK
        # Logique d'attaque pour le Chasseur_Drag

class Mage_noir(Ennemi):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.PV = 26
        self.ATK = 6
        self.DEF = 1
        self.vitesse = 3

    def attaquer(self):
        attaque = self.ATK
        # Logique d'attaque pour le Mage noir

    def attaquer_par_sort(self):
        sort = self.ATK * 2
        # Logique d'attaque par sort pour le Mage noir

class EvilArcher(Ennemi):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.PV = 32
        self.ATK = 8
        self.DEF = 1
        self.vitesse = 2

    def attaquer(self):
        attaque = self.ATK
        # Logique d'attaque pour l'EvilArcher

class Enchanteresse(Ennemi):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.PV = 60
        self.ATK = 6
        self.DEF = 0
        self.vitesse = 6  # Déplacement entre 1 et 6 cases

    def fuir_joueur(self, joueur_le_plus_proche):
        direction_x = 0
        direction_y = 0

        if joueur_le_plus_proche.x < self.x:
            direction_x = 1  # Inverser la direction pour fuir
        elif joueur_le_plus_proche.x > self.x:
            direction_x = -1

        if joueur_le_plus_proche.y < self.y:
            direction_y = 1  # Inverser la direction pour fuir
        elif joueur_le_plus_proche.y > self.y:
            direction_y = -1

        # Application la vitesse de l'ennemi
        self.x += direction_x * self.vitesse
        self.y += direction_y * self.vitesse

        # Assurance que l'ennemi reste dans les limites du plateau
        self.x = max(0, min(self.x, 15))
        self.y = max(0, min(self.y, 7))

    def attaquer(self):
        attaque = self.ATK
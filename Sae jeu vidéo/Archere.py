class Archere:
    def __init__(self, x=0, y=0):
        self.PV = 45
        self.ATK = 10
        self.DEF = 2
        self.vitesse = 3  # Déplacement entre 1 et 3 cases
        self.x = x
        self.y = y

    # Fonction qui permettra a attaquer les enemies proche du personnage
    def attaquer(self):
        degats = self.ATK


    def deplacer(self, direction_x, direction_y):
        self.x += direction_x * self.vitesse
        self.y += direction_y * self.vitesse

        # Assurez-vous que les coordonnées x et y restent dans les limites du plateau de jeu
        self.x = max(0, min(self.x, 15))
        self.y = max(0, min(self.y, 7))
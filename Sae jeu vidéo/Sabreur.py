class Sabreur:
    def __init__(self, x=0, y=0):
        self.PV = 52
        self.ATK = 15
        self.DEF = 1
        self.vitesse = 4  # Déplacement entre 1 et 4 cases
        self.x = x
        self.y = y

    #Fonction qui permettra a attaquer les enemies proche du personnage
    def attaquer(self):
        degats = self.ATK

    def deplacer(self, direction_x, direction_y):
            self.x += direction_x * self.vitesse
            self.y += direction_y * self.vitesse

            # Assurez-vous que les coordonnées x et y restent dans les limites du plateau de jeu
            self.x = max(0, min(self.x, 15))
            self.y = max(0, min(self.y, 7))


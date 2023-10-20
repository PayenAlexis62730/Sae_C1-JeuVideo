import pygame

class Inventaire:
    def __init__(self, fenetre, font):
        self.fenetre = fenetre
        self.font = font
        self.visible = False
        self.inventaire = [{'nom': 'Potion de guérison', 'image': pygame.image.load('Sprite/PopoSoin.png'), 'quantite': 1},
                           {'nom': 'Potion de coup critique', 'image': pygame.image.load('Sprite/PopoCrit.png'), 'quantite': 0}]
        self.rect = pygame.Rect(self.fenetre.get_width() - 350, 10, 300, 150)

    def afficher(self):
        if self.visible:
            pygame.draw.rect(self.fenetre, (200, 200, 200), self.rect)  # Afficher le rectangle d'inventaire
            y_offset = 20  # Décalage vertical pour afficher les objets (ajusté pour mieux s'adapter)
            for item in self.inventaire:
                self.fenetre.blit(item['image'], (self.fenetre.get_width() - 320, y_offset))  # Ajustez les coordonnées pour le coin en haut à droite
                text_quantite = self.font.render(f"Quantité: {item['quantite']}", True, (0, 0, 0))
                self.fenetre.blit(text_quantite, (self.fenetre.get_width() - 270, y_offset + 10))  # Ajustez les coordonnées
                y_offset += 50  # Augmentez le décalage vertical pour le prochain objet

    def toggle(self):
        self.visible = not self.visible

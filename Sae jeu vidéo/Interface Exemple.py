#importation des bibliothèque importante
import pygame
import sys

#/------------------------------------------------------------------------------------------------------#
#/ Ceci est un code d'exemple pour montrer un des nombreux exemples d'affichages du jeu                 #                                                     #
#/------------------------------------------------------------------------------------------------------#

#on initialise Pygame
pygame.init()

#dimensions de l'interface
largeur_fenetre = 16 * 80
hauteur_fenetre = 8 * 80

#création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

#création des couleurs et barre des cases 
VERT =(107,142,35)
NOIR = (0, 0, 0)

#fonction pour crée le plateau de jeu
def créer_plateau():
    #on définit la largeur du plateau
    for x in range(16):
        #on définit la hauteur du plateau
        for y in range(8):
            pygame.draw.rect(fenetre, NOIR, (x * 80, y * 80, 80, 80), 2)

    
    # Inclusion du chevalier
    cr_X = 6  # Coordonnée X du chevalier
    cr_Y = 1  # Coordonnée Y du chevalier
    cr_image = pygame.image.load('Sprite/chevalier.png')  # inclusion de l'image du chevalier
    fenetre.blit(cr_image, (cr_X * 80, cr_Y * 80))

    # Inclusion de  l'archère
    arc_X = 4   # Coordonnée X de l'archère
    arc_Y = 3   # Coordonnée Y de l'archère
    arc_image = pygame.image.load('Sprite/archere.png')  # inclusion de l'image de l'archère
    fenetre.blit(arc_image, (arc_X * 80, arc_Y * 80))

    # Inclusion du Sabreur
    Sb_X = 7   # Coordonnée X du Sabreur
    Sb_Y = 4   # Coordonnée Y du Sabreur
    Sb_image = pygame.image.load('Sprite/Sabreur.png')  # inclusion de l'image du Sabreur
    fenetre.blit(Sb_image, (Sb_X * 80, Sb_Y * 80))

    # Inclusion du Dragon
    Sb_X = 9   # Coordonnée X du Dragon
    Sb_Y = 7   # Coordonnée Y du Dragon
    Sb_image = pygame.image.load('Sprite/Monteur_Dragon.png')  # inclusion de l'image du Dragon 
    fenetre.blit(Sb_image, (Sb_X * 80, Sb_Y * 80))

    # Inclusion du Manoir
    Sb_X = 7   # Coordonnée X du Manoir
    Sb_Y = 5  # Coordonnée Y du Manoir
    Sb_image = pygame.image.load('Sprite/Manoir.png')  # inclusion de l'image du Manoir
    fenetre.blit(Sb_image, (Sb_X * 80, Sb_Y * 80))

    # Inclusion du Manoir
    Sb_X = 4   # Coordonnée X du Manoir
    Sb_Y = 2  # Coordonnée Y du Manoir
    Sb_image = pygame.image.load('Sprite/Manoir.png')  # inclusion de l'image du Manoir
    fenetre.blit(Sb_image, (Sb_X * 80, Sb_Y * 80))

   # Inclusion du Manoir
    Sb_X = 11   # Coordonnée X du Manoir
    Sb_Y = 0  # Coordonnée Y du Manoir
    Sb_image = pygame.image.load('Sprite/Manoir.png')  # inclusion de l'image du Manoir
    fenetre.blit(Sb_image, (Sb_X * 80, Sb_Y * 80))

    # Inclusion de la Taverne
    Sb_X = 7   # Coordonnée de la Taverne
    Sb_Y = 3  # Coordonnée Y de la Taverne
    Sb_image = pygame.image.load('Sprite/Taverne.png')  # inclusion de l'image de la Taverne
    fenetre.blit(Sb_image, (Sb_X * 80, Sb_Y * 80))


# Boucle du jeu 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #commande pour effacer l'écran
    fenetre.fill(VERT)

    #appel de la fonction pour crée le  plateau de jeu
    créer_plateau()

    #commande permettant de rafraichir l'interface de jeu 
    pygame.display.flip()

import pygame
import sys
import random

#/------------------------------------------------------------------------------------------------------#
#/ Ceci est un code d'exemple pour tester l'affichage du menu et s'il peut lancer le jeu après que tout #
#/ les joueurs ont choisis leur classes de jeu                                                          #
#/------------------------------------------------------------------------------------------------------#

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur_fenetre = 16 * 80
hauteur_fenetre = 8 * 80 + 60  # Augmenter la hauteur de la fenêtre pour le compteur de tours

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

# Couleurs en RGB
VERT = (107, 180, 35)
NOIR = (0, 0, 0)
BLEU = (51, 112, 59)
JAUNE = (255, 255, 0)
ROUGE = (255, 0, 0)
Orange = (255, 140, 0)
VIOLET = (148, 0, 211)

# Police d'écriture
font = pygame.font.Font(None, 36)

# Liste des emplacements occupés par chaque type de lieu (manoir, taverne, tour, fort)
emplacements_forts = set()
emplacements_manoirs = set()
emplacements_taverne = set()
emplacements_tours = set()

# Compteur de tours
nombre_de_tours = 0

# Fonction pour ajouter des forts aléatoirement sur le plateau de jeu
def ajouter_forts():
    emplacements = set()

    while len(emplacements) < 4:
        x = random.randint(0, 15)
        y = random.randint(0, 7)
        if (x, y) not in emplacements_forts and (x, y) not in [(0, 2), (0, 3), (0, 4), (0, 5)]:  # Empêche de poser les forts sur les positions des joueurs
            emplacements.add((x, y))
            emplacements_forts.add((x, y))

    for x, y in emplacements:
        pygame.draw.rect(fenetre, JAUNE, (x * 80 + 10, y * 80 + 10, 60, 60))

# Fonction pour ajouter des manoirs aléatoirement sur le plateau de jeu
def ajouter_manoirs():
    emplacements = set()

    while len(emplacements) < 3:
        x = random.randint(0, 15)
        y = random.randint(0, 7)
        if (x, y) not in emplacements_manoirs and (x, y) not in [(0, 2), (0, 3), (0, 4), (0, 5)]:  # Empêche de poser les manoirs sur les positions des joueurs
            emplacements.add((x, y))
            emplacements_manoirs.add((x, y))

    for x, y in emplacements:
        pygame.draw.rect(fenetre, BLEU, (x * 80 + 10, y * 80 + 10, 60, 60))

# Fonction pour ajouter une taverne aléatoirement sur le plateau de jeu
def ajouter_taverne():
    x = random.randint(0, 15)
    y = random.randint(0, 7)
    if (x, y) not in emplacements_taverne and (x, y) not in [(0, 2), (0, 3), (0, 4), (0, 5)]:  # Empêche de poser la taverne sur les positions des joueurs
        pygame.draw.rect(fenetre, Orange, (x * 80 + 10, y * 80 + 10, 60, 60))
        emplacements_taverne.add((x, y))

# Fonction pour ajouter des tours aléatoirement sur le plateau de jeu
def ajouter_tours():
    emplacements = set()

    while len(emplacements) < 4:
        x = random.randint(0, 15)
        y = random.randint(0, 7)
        if (x, y) not in emplacements_tours and (x, y) not in [(0, 2), (0, 3), (0, 4), (0, 5)]:  # Empêche de poser les tours sur les positions des joueurs
            emplacements.add((x, y))
            emplacements_tours.add((x, y))

    for x, y in emplacements:
        pygame.draw.rect(fenetre, ROUGE, (x * 80 + 10, y * 80 + 10, 60, 60))

# Fonction pour créer le plateau de jeu
def creer_plateau():
    for x in range(16):
        for y in range(8):
            pygame.draw.rect(fenetre, NOIR, (x * 80, y * 80, 80, 80), 2)

# Fonction pour afficher le menu de sélection de classe
def afficher_menu():
    fenetre.fill(BLEU)

    # Affichage du titre du menu
    text_titre = font.render("Sélectionnez votre classe", True, NOIR)
    fenetre.blit(text_titre, (50, 50))

    # Affichage des options possibles de classe (Chevalier, Archère, Sabreur, Dragon)
    text_chevalier = font.render("Chevalier", True, NOIR)
    fenetre.blit(text_chevalier, (50, 200))

    text_archere = font.render("Archère", True, NOIR)
    fenetre.blit(text_archere, (50, 300))

    text_sabreur = font.render("Sabreur", True, NOIR)
    fenetre.blit(text_sabreur, (50, 400))

    text_dragon = font.render("Dragon", True, NOIR)
    fenetre.blit(text_dragon, (50, 500))

    pygame.display.flip()

    # Boucle en attente de la sélection des classes
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 50 <= x <= 200 and 200 <= y <= 236:
                    return "Chevalier"
                elif 50 <= x <= 200 and 300 <= y <= 336:
                    return "Archère"
                elif 50 <= x <= 200 and 400 <= y <= 436:
                    return "Sabreur"
                elif 50 <= x <= 200 and 500 <= y <= 536:
                    return "Dragon"

# Fonction pour afficher le plateau de jeu en fonction du nombre de joueurs et des classes sélectionnées
def afficher_plateau(num_joueurs, classes):
    fenetre.fill(VERT)

    ajouter_manoirs()
    ajouter_forts()
    ajouter_taverne()
    ajouter_tours()

    pygame.display.flip()

    # Coordonnées de départ pour chaque joueur [Joueur1, joueur2, joueur3 joueur4]
    coordonnees_joueurs = [(0, 2), (0, 3), (0, 4), (0, 5)]

    # Boucle du jeu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        creer_plateau()

        for i in range(num_joueurs):
            classe = classes[i]
            x, y = coordonnees_joueurs[i]

            if classe == "Chevalier":
                cr_image = pygame.image.load('Sprite/chevalier.png')
                fenetre.blit(cr_image, (x * 80, y * 80))
            elif classe == "Archère":
                arc_image = pygame.image.load('Sprite/archere.png')
                fenetre.blit(arc_image, (x * 80, y * 80))
            elif classe == "Sabreur":
                sabreur_image = pygame.image.load('Sprite/Sabreur.png')
                fenetre.blit(sabreur_image, (x * 80, y * 80))
            elif classe == "Dragon":
                dragon_image = pygame.image.load('Sprite/Monteur_Dragon.png')
                fenetre.blit(dragon_image, (x * 80, y * 80))

        # Afficher le nombre de tours
        text_tours = font.render(f"Tours: {nombre_de_tours}", True, NOIR)
        fenetre.blit(text_tours, (10, hauteur_fenetre - 50))

        pygame.display.flip()

# Fonction principale du lancement
def main():
    global nombre_de_tours  # Déclarer nombre_de_tours comme variable globale

    # Permet de demander le nombre de joueurs
    num_joueurs = int(input("Nombre de joueurs (1 à 4) : "))
    if num_joueurs < 1 or num_joueurs > 4:
        # Permet de ne pas avoir de partie sans joueur ou avec plus de 4 joueurs
        print("Nombre de joueurs invalide.")
        return

    classes = []
    for i in range(num_joueurs):
        classe = afficher_menu()
        classes.append(classe)

    while True:
        # Appeler la fonction afficher_plateau avec le nombre de joueurs et les classes
        afficher_plateau(num_joueurs, classes)
        nombre_de_tours += 1  # Incrémenter le compteur de tours

if __name__ == "__main__":
    main()

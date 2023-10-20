#############################################################
#Partie pour essayer de corriger la listes des bugs restants#
#############################################################

#Liste de Bug Restant:
# -Erreur cannot-unpack quand un joueur meurt au lieu d'afficher la condition de defaite 
# -Inventaire pas correctement cacher

import pygame
import sys
import random
import pygame.mixer
from Chevalier import Chevalier
from Archere import Archere
from Sabreur import Sabreur
from Dragon import Dragon
from Enemie import *
from inventaire import *

################################################################################
#---------------------------ATTRIBUTS DU PROGRAMME-----------------------------#
################################################################################

# Initialisation de Pygame
pygame.init()

# Initialisatiion de la Bibliothèque
pygame.mixer.init()

# Initialisation de Pygame Mixer pour la musique du menu
pygame.mixer.music.load('Musique/MenuSong.mp3')

# Jouez la musique du menu en boucle
pygame.mixer.music.play(-1)

# Dimensions de la fenêtre
largeur_fenetre = 16 * 80
hauteur_fenetre = 8 * 80 + 60  # Augmenter la hauteur de la fenêtre pour le compteur de tours

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

# Couleurs en RGB
VERT = (107, 180, 35)
NOIR = (0, 0, 0)
BLEU = (51, 112, 59)
JAUNE = (200,185,52)
ROUGE = (255, 0, 0)
ORANGE = (255, 140, 0)
VERT_FONCEE = (0, 100, 0)
BLANC = (255,255,255)

# Police d'écriture global
font = pygame.font.Font(None, 36)

# Police d'écriture pour les PV
font_pv = pygame.font.Font(None, 25)

# Liste des emplacements occupés par chaque type de lieu (manoir, taverne, tour, fort)
emplacements_forts = set()
emplacements_manoirs = set()
emplacements_taverne = set()
emplacements_forge = set()

# Coordonnées de départ pour chaque joueur [Joueur1, joueur2, joueur3 joueur4]
coordonnees_joueurs = [(0, 2), (0, 3), (0, 4), (0, 5)]
classes = []  # Liste des classes des joueurs

# Points de vie initiaux pour chaque joueur sous forme de liste
pv_joueurs = []

# Attaque initiale pour chaque joueur sous forme de liste
atk_joueurs = []

# Ajout pour initialiser la liste des joueurs en jeu
joueurs_en_jeu = []

# initialisation de x_old et y_old pour chaque joueur
x_old, y_old = [x for x, _ in coordonnees_joueurs], [y for _, y in coordonnees_joueurs]

nombre_max_mouvements_par_classe = {
    "Chevalier": 2,
    "Archere": 3,
    "Sabreur": 4,
    "Dragon": 5
}

# Compteur de tours
nombre_de_tours = 0  # Déclarez la variable ici

# En dehors de toutes les fonctions
font_pv_atk = pygame.font.Font(None, 25)

# Ajout de la Difiiculté comme variable
difficulte = 0

# Créez une structure de données pour suivre l'état des manoirs
manoirs_etat = {} 

# Variables  pour les boosts unique 
forge_boost_applique = False
fort_boost_applique = False

# dictionnaires pour suivre les boosts récupérés par chaque joueur
forge_boosts_recuperes = {}
fort_boosts_recuperes = {}

################################################################################
#--------------------PARTIE DES LIEUX SPECIAUX --------------------------------#
################################################################################

# Fonction pour ajouter des manoirs aléatoirement sur le plateau de jeu
def ajouter_manoirs():
    emplacements = set()

    while len(emplacements) < 3:
        x = random.randint(0, 15)
        y = random.randint(0, 7)
        
        # Vérification si l'emplacement est déjà occupé
        if (x, y) not in emplacements_manoirs and (x, y) not in coordonnees_joueurs:
            emplacements.add((x, y))
            emplacements_manoirs.add((x, y))

    for x, y in emplacements:
        manoir_image = pygame.image.load('Sprite/Manoir.png')
        fenetre.blit(manoir_image, (x * 80 + 5, y * 80 + 5))

    return emplacements

# Fonction pour ajouter des forts aléatoirement sur le plateau de jeu
def ajouter_forts():
    emplacements = set()

    while len(emplacements) < 4:
        x = random.randint(0, 15)
        y = random.randint(0, 7)
        
        # Vérification si l'emplacement est déjà occupé
        if (x, y) not in emplacements_forts and (x, y) not in coordonnees_joueurs and (x,y) not in emplacements_manoirs:
            emplacements.add((x, y))
            emplacements_forts.add((x, y))

    for x, y in emplacements:
        fort_image = pygame.image.load('Sprite/fort.png')
        fenetre.blit(fort_image, (x * 80 + 5, y * 80 + 10))

# Fonction pour ajouter une taverne aléatoirement sur le plateau de jeu
def ajouter_taverne():
    emplacements = set()

    while len(emplacements) < 1:
        x = random.randint(0, 15)
        y = random.randint(0, 7)
        
        # Vérification si l'emplacement est déjà occupé
        if (x, y) not in emplacements_taverne and (x, y) not in coordonnees_joueurs and (x, y) not in emplacements_manoirs and (x, y) not in emplacements_forts :
            emplacements.add((x, y))
            emplacements_taverne.add((x, y))

    for x, y in emplacements:
        taverne_image = pygame.image.load('Sprite/Taverne.png')
        fenetre.blit(taverne_image, (x * 80 + 10, y * 80 + 5))

# Fonction pour ajouter des forges aléatoirement sur le plateau de jeu
def ajouter_forge():
    emplacements = set()

    while len(emplacements) < 4:
        x = random.randint(0, 15)
        y = random.randint(0, 7)
        
        # Vérification si l'emplacement est déjà occupé
        if (x, y) not in emplacements_forge and (x, y) not in emplacements_taverne and (x, y) not in coordonnees_joueurs and (x, y) not in emplacements_manoirs and (x, y) not in emplacements_forts :
            emplacements.add((x, y))
            emplacements_forge.add((x, y))

    for x, y in emplacements:
        forge_image = pygame.image.load('Sprite/forge.png')
        fenetre.blit(forge_image, (x * 80 + 10, y * 80 + 5))

# Fonction pour créer le plateau de jeu
def creer_plateau():
    for x in range(16):
        for y in range(8):
            pygame.draw.rect(fenetre, VERT_FONCEE, (x * 80, y * 80, 80, 80), 2)

    for x, y in emplacements_manoirs:
        manoir_image = pygame.image.load('Sprite/Manoir.png')
        fenetre.blit(manoir_image, (x * 80 + 5, y * 80 + 5))

    for x, y in emplacements_forts:
        fort_image = pygame.image.load('Sprite/fort.png')
        fenetre.blit(fort_image, (x * 80 + 5, y * 80 + 10))

    for x, y in emplacements_taverne:
        taverne_image = pygame.image.load('Sprite/Taverne.png')
        fenetre.blit(taverne_image, (x * 80 + 10, y * 80 + 5))

    for x, y in emplacements_forge:
        forge_image = pygame.image.load('Sprite/forge.png')
        fenetre.blit(forge_image, (x * 80 + 10, y * 80 + 5))

# Fonction pour réinitialiser les boosts au début de chaque tour
def reinitialiser_boosts(num_joueurs):
    global forge_boost_applique
    global fort_boost_applique

    forge_boost_applique = False
    fort_boost_applique = False

    # Réinitialisez les dictionnaires de boosts pour chaque joueur
    forge_boosts_recuperes.clear()
    fort_boosts_recuperes.clear()
    # Initialisez les dictionnaires de boosts pour chaque joueur
    for i in range(num_joueurs):
        forge_boosts_recuperes[i] = set()
        fort_boosts_recuperes[i] = set()

    return forge_boosts_recuperes, fort_boosts_recuperes

# Modifiez la fonction pour appliquer les boosts sur les emplacements spécifiques
def appliquer_boosts_sur_emplacements(x, y, classe, pv_joueurs, atk_joueurs, num_joueurs, joueur_actuel):
    global forge_boost_applique
    global fort_boost_applique

    if (x, y) in emplacements_forge and not forge_boost_applique:
        if (x, y) not in forge_boosts_recuperes[joueur_actuel]:
            for i in range(num_joueurs):
                if classe == "Sabreur":
                    atk_joueurs[i] += 2
            forge_boost_applique = True
            forge_boosts_recuperes[joueur_actuel].add((x, y))

    if (x, y) in emplacements_forts and not fort_boost_applique:
        if (x, y) not in fort_boosts_recuperes[joueur_actuel]:
            for i in range(num_joueurs):
                if classe == "Chevalier":
                    pv_joueurs[i] += 1
            fort_boost_applique = True
            fort_boosts_recuperes[joueur_actuel].add((x, y))

################################################################################
#--------------------PARTIE DES Interfaces du Jeu------------------------------#
################################################################################

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Heroes of Nazuma")

# Charger les images d'arrière-plan pour chaque fonction
arriere_plan_menu = pygame.image.load("Image/Menu.jpeg").convert()
arriere_plan_menu = pygame.transform.scale(arriere_plan_menu, (largeur_fenetre, hauteur_fenetre))

arriere_plan_nb_joueurs = pygame.image.load("Image/joueur.jpg").convert()
arriere_plan_nb_joueurs = pygame.transform.scale(arriere_plan_nb_joueurs, (largeur_fenetre, hauteur_fenetre))

arriere_plan_difficulte = pygame.image.load("Image/Difficulté.jpg").convert()
arriere_plan_difficulte = pygame.transform.scale(arriere_plan_difficulte, (largeur_fenetre, hauteur_fenetre))

arriere_plan_classe = pygame.image.load("Image/personnages.jpg").convert()
arriere_plan_classe = pygame.transform.scale(arriere_plan_classe, (largeur_fenetre, hauteur_fenetre))

arriere_plan_tuto = pygame.image.load("Image/tuto.jpg").convert()
arriere_plan_tuto = pygame.transform.scale(arriere_plan_tuto, (largeur_fenetre, hauteur_fenetre))

# Fonction pour initialiser le menu principal du jeu
def afficher_Lancement():
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if bouton_jouer_rect.collidepoint(x, y):
                    menu = False  # Quittez la boucle du menu et démarrez le jeu
                elif bouton_quitter_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

        # arrière-plan
        fenetre.blit(arriere_plan_menu, (0, 0))

        titre_font = pygame.font.Font(None, 72)
        text_titre = titre_font.render("Heroes of Nazuma", True, ORANGE)
        titre_rect = text_titre.get_rect(center=(largeur_fenetre // 2, 100))
        fenetre.blit(text_titre, titre_rect)

        bouton_font = pygame.font.Font(None, 36)
        espace_boutons = 20  # Espace  entre les boutons

        # Bouton "Jouer"
        bouton_jouer_rect = pygame.Rect(0, 0, 200, 50)
        bouton_jouer_rect.center = (largeur_fenetre // 2, hauteur_fenetre // 2 - bouton_jouer_rect.height - espace_boutons // 2)
        pygame.draw.rect(fenetre, VERT, bouton_jouer_rect)
        text_jouer = bouton_font.render("Jouer", True, NOIR)
        text_jouer_rect = text_jouer.get_rect(center=bouton_jouer_rect.center)
        fenetre.blit(text_jouer, text_jouer_rect)
        
        # Bouton "Quitter"
        bouton_quitter_rect = pygame.Rect(0, 0, 200, 50)
        bouton_quitter_rect.center = (largeur_fenetre // 2, hauteur_fenetre // 2 + bouton_quitter_rect.height + espace_boutons // 2)
        pygame.draw.rect(fenetre, ROUGE, bouton_quitter_rect)
        text_quitter = bouton_font.render("Quitter", True, NOIR)
        text_quitter_rect = text_quitter.get_rect(center=bouton_quitter_rect.center)
        fenetre.blit(text_quitter, text_quitter_rect)

        pygame.display.flip()


# Nouvelle fonction pour afficher le menu de sélection du nombre de joueurs
def afficher_menu_nb_joueurs():

    # arrière-plan
    fenetre.blit(arriere_plan_nb_joueurs, (0, 0))
    
    # Affichage du titre du menu
    titre_font = pygame.font.Font(None, 72)
    text_titre = titre_font.render("Selectionnez le nombre de joueurs :", True, ORANGE) 
    titre_rect = text_titre.get_rect(center=(largeur_fenetre // 2, 50))
    fenetre.blit(text_titre, titre_rect)

    # Affichage des options possibles de nombre de joueurs
    options = ["1 joueur", "2 joueurs", "3 joueurs", "4 joueurs"]
    for i, option in enumerate(options):
        text_option = font.render(option, True, NOIR)
        fenetre.blit(text_option, (50, 200 + i * 100))
    
    pygame.display.flip()
    
    # Boucle en attente de la sélection du nombre de joueurs
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                for i in range(len(options)):
                    if 50 <= x <= 250 and 200 + i * 100 <= y <= 236 + i * 100:
                        return i + 1  # Retourne le nombre de joueurs sélectionné (1-indexed)
                    
# Fonction pour l'interface de choix de  difficulté
def afficher_menu_difficulte():
    # arrière-plan
    fenetre.blit(arriere_plan_difficulte, (0,0))

    # Affichage du titre du menu
    titre_font = pygame.font.Font(None, 72)
    text_titre = titre_font.render("Selectionné la difficultés", True, (255, 165, 0))  # Titre avec une teinte orange
    titre_rect = text_titre.get_rect(center=(largeur_fenetre // 2, 100))
    fenetre.blit(text_titre, titre_rect)

    # Affichage des options de difficulté
    options = ["Facile : Pour les amateurs de Tactical RPG ( Joueur recommandé : 1 )", "Modérée : Pour les vétérants du jeu (Joueur recommandé : 2/3) )", "Apocalypse : Découvrez l'enfer de ce monde (Joueur recommandé : 4)"]
    for i, option in enumerate(options):
        text_option = font.render(option, True, NOIR)
        fenetre.blit(text_option, (50, 200 + i * 100))

    pygame.display.flip()

    # Boucle en attente de la sélection de la difficulté
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                for i in range(len(options)):
                    if 50 <= x <= 250 and 200 + i * 100 <= y <= 236 + i * 100:
                        # Retourne le nombre d'ennemis en fonction de la difficulté
                        if i == 0:  # Difficulté Facile
                            return 3
                        elif i == 1:  # Difficulté Modérée
                            return 5
                        else:  # Difficulté Apocalypse
                            return 7
    
# Fonction pour afficher le menu de sélection de classe
def afficher_classe():
    # arrière plan
    fenetre.blit(arriere_plan_classe, (0,0))

    # Affichage du titre du menu
    titre_font = pygame.font.Font(None, 72)
    text_titre = titre_font.render("Selectionnez votre classe", True, (255, 165, 0))  # Titre avec une teinte orange
    titre_rect = text_titre.get_rect(center=(largeur_fenetre // 2, 100))
    fenetre.blit(text_titre, titre_rect)

    # Chargement des images des personnages
    chevalier_image = pygame.image.load('Sprite/chevalier.png')
    archere_image = pygame.image.load('Sprite/archere.png')
    sabreur_image = pygame.image.load('Sprite/Sabreur.png')
    dragon_image = pygame.image.load('Sprite/Monteur_Dragon.png')

    # Affichage des options possibles de classe avec les sprites à côté
    options = [
        ("Chevalier", chevalier_image),
        ("Archere", archere_image),
        ("Sabreur", sabreur_image),
        ("Dragon", dragon_image)
    ]

    y_position = 200
    for option, sprite in options:
        text_option = font.render(option, True, NOIR)
        fenetre.blit(text_option, (50, y_position))

        # Afficher le sprite à côté du nom de la classe
        fenetre.blit(sprite, (250, y_position))

        y_position += 100

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
                    return "Archere"
                elif 50 <= x <= 200 and 400 <= y <= 436:
                    return "Sabreur"
                elif 50 <= x <= 200 and 500 <= y <= 536:
                    return "Dragon"

# Fonction pour l'interface de tuto
def afficher_tuto():
    # arrière-plan
    fenetre.blit(arriere_plan_tuto, (0,0))
    
    # Affichage du titre du menu
    titre_font = pygame.font.Font(None, 55)
    text_titre = titre_font.render("Tutoriel :", True, (255, 165, 0))  # Titre avec une teinte orange
    titre_rect = text_titre.get_rect(center=(largeur_fenetre // 2, 50))
    fenetre.blit(text_titre, titre_rect)

    # Affiche les instructions de déplacement
    text_deplacement = font.render("Utilisez les touches fléchées pour vous déplacer.", True, JAUNE)
    fenetre.blit(text_deplacement, (50, 70))
    
    # Affiche les instructions pour passer le tour
    text_espace = font.render("Appuyez sur la touche ESPACE pour passer votre tour.", True, JAUNE)
    fenetre.blit(text_espace, (50, 110))
    
    # Affiche les instructions pour les batiments
    text_batiments = font.render("N'hésitez pas à finir votre tour sur des bâtiments pour devenir plus fort ! ", True, JAUNE)
    fenetre.blit(text_batiments, (50, 150))

    # Affiche les instructions pour lattaque
    text_attaque = font.render("Appuyer sur A près d'un ennemi pour l'attaquer", True, JAUNE)
    fenetre.blit(text_attaque, (50, 190))

    # Affiche les instructions pour l'inventaire
    text_attaque = font.render("Appuyer sur I pour utiliser votre inventaire", True, JAUNE)
    fenetre.blit(text_attaque, (50, 230))

    # Affiche les instructions pour la condition de VICTOIRE
    text_Victoire = font.render("Les ennemies apparaîtront dès le tour 1, Tuer les tous pour gagner le jeu (^_^) ", True, JAUNE)
    fenetre.blit(text_Victoire, (50, 270))

    # Affiche les instructions pour la condition de DEFAITE
    text_Defaite = font.render("Si l'un des joueurs meurt, c'est Game Over (;-;) ", True, JAUNE)
    fenetre.blit(text_Defaite, (50, 310))

    # Affiche les instructions pour la condition de stratégie
    text_conseil1 = font.render("TIPS: Les potions utiliser affecte tout les alliées !", True, JAUNE)
    fenetre.blit(text_conseil1, (50, 350))

    # Affiche les instructions pour la condition de stratégie
    text_conseil2 = font.render("TIPS: L'attaque de votre personnages retire un point de déplacement", True, JAUNE)
    fenetre.blit(text_conseil2, (50, 390))

    # Affiche les instructions pour les Boost
    text_lieux = font.render("Chaque joueurs ne peut récupérer qu'un seul boost d'ATK et de PV", True, JAUNE)
    fenetre.blit(text_lieux, (50, 430))

    # Affiche les instructions pour les potions
    text_manoirs = font.render("Besoin de potion ? allez sur les cases manoirs ou taverne pour en récupérés", True, JAUNE)
    fenetre.blit(text_manoirs, (50, 470))
    
    # Affiche le texte pour skipper la page
    text_skip = font.render("appuyez sur Entrée pour passer cette page", True, JAUNE)
    fenetre.blit(text_skip, (770, 650))
    
    pygame.display.flip()
    
    attente_touche = True
    while attente_touche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Touche Entrée pour passer
                    attente_touche = False

################################################################################
#--------------------PARTIE DES FONCTIONS ENEMIES------------------------------#
################################################################################

# Fonction pour charger les images d'enemie dans le but d'optimiser un minimum le code
def charger_image_ennemi(ennemi):
    if isinstance(ennemi, Chasseur_Drag):
        return pygame.image.load('Sprite/ChasseurDrag.png')
    elif isinstance(ennemi, Barbare):
        return pygame.image.load('Sprite/barbare.png')
    elif isinstance(ennemi, EvilArcher):
        return pygame.image.load('Sprite/EvilArch.png')
    elif isinstance(ennemi, Enchanteresse):
        return pygame.image.load('Sprite/healeuse.png')
    elif isinstance(ennemi, Mage_noir):
        return pygame.image.load('Sprite/mage.png')

# Fonction pour générée les enemies sur le plateau
def ajouter_enemies(difficulte):
    ennemis = []  # Liste pour stocker les ennemis générés aléatoirement
    classes_limites = {
        Chasseur_Drag: 1,
        Enchanteresse: 1,
        EvilArcher: 2,
        Mage_noir: 2,
        Barbare: 3
    }

    # Compteurs pour le nombre d'ennemis de chaque classe
    ennemis_par_classe = {classe: 0 for classe in classes_limites.keys()}

    # Générer le nombre d'ennemis en fonction de la difficulté choisie
    while len(ennemis) < difficulte:
        x = random.randint(12, 15)  # Colonnes x entre 12 et 15
        y = random.randint(0, 7)    # Lignes y entre 0 et 7

        # Vérifier si la case est déjà occupée par un joueur ou un ennemi
        case_occupee = False
        for joueur in coordonnees_joueurs:
            if joueur == (x, y):
                case_occupee = True
                break
        for ennemi in ennemis:
            if ennemi.x == x and ennemi.y == y:
                case_occupee = True
                break

        if not case_occupee:
            # Sélectionner une classe d'ennemi aléatoire
            classe_ennemi = random.choice([classe for classe in classes_limites.keys() if ennemis_par_classe[classe] < classes_limites[classe]])
            ennemi = classe_ennemi(x, y)
            ennemis.append(ennemi)
            ennemis_par_classe[classe_ennemi] += 1

    return ennemis  # Retourner la liste d'ennemis générés

# Fonction pour générer les ennemis sur le plateau
def ajouter_enemies(difficulte):
    ennemis = []  # Liste pour stocker les ennemis générés aléatoirement
    classes_limites = {
        Chasseur_Drag: 1,
        Enchanteresse: 1,
        EvilArcher: 2,
        Mage_noir: 2,
        Barbare: 3
    }

    # Compteurs pour le nombre d'ennemis de chaque classe
    ennemis_par_classe = {classe: 0 for classe in classes_limites.keys()}

    # Générer le nombre d'ennemis en fonction de la difficulté choisie
    while len(ennemis) < difficulte:
        x = random.randint(12, 15)  # Colonnes x entre 12 et 15
        y = random.randint(0, 7)    # Lignes y entre 0 et 7

        # Vérifier si la case est déjà occupée par un joueur ou un ennemi
        case_occupee = False
        for joueur in coordonnees_joueurs:
            if joueur == (x, y):
                case_occupee = True
                break
        for ennemi in ennemis:
            if ennemi.x == x and ennemi.y == y:
                case_occupee = True
                break

        if not case_occupee:
            # Sélectionner une classe d'ennemi aléatoire
            classe_ennemi = random.choice([classe for classe in classes_limites.keys() if ennemis_par_classe[classe] < classes_limites[classe]])
            ennemi = classe_ennemi(x, y)
            ennemis.append(ennemi)
            ennemis_par_classe[classe_ennemi] += 1
 
    return ennemis  # Retourner la liste d'ennemis générés

def deplacer_ennemis(ennemis, coordonnees_joueurs, pv_joueurs, classes):
    # Filtrer les coordonnées des joueurs pour exclure les valeurs None
    coordonnees_joueurs = [coord for coord in coordonnees_joueurs if coord is not None]
    
    # Création du dictionnaire pour stocker les PV des ennemis
    pv_ennemis = {} 
    #Variable pour les conditions enemies
    atk_augmente = False

    # Déterminer s'il y a une Enchanteresse sur le plateau
    enchanteresse_presente = any(isinstance(ennemi, Enchanteresse) for ennemi in ennemis)

    for ennemi in ennemis:
        x_ennemi, y_ennemi = ennemi.x, ennemi.y
        joueur_le_plus_proche = None
        distance_minimale = float('inf')

        # Trouver le joueur le plus proche
        for joueur_x, joueur_y in coordonnees_joueurs:
            if joueur_x is not None and joueur_y is not None:
                distance = abs(joueur_x - x_ennemi) + abs(joueur_y - y_ennemi)
                if distance < distance_minimale:
                    distance_minimale = distance
                    joueur_le_plus_proche = (joueur_x, joueur_y)

        # Vérifier si l'ennemi est adjacent à un joueur
        for joueur_coord in coordonnees_joueurs:
            if joueur_coord is not None:
                joueur_x, joueur_y = joueur_coord
                if (
                    (joueur_x == x_ennemi + 1 and joueur_y == y_ennemi) or
                    (joueur_x == x_ennemi - 1 and joueur_y == y_ennemi) or
                    (joueur_x == x_ennemi and joueur_y == y_ennemi + 1) or
                    (joueur_x == x_ennemi and joueur_y == y_ennemi - 1)
                ):
                    joueur_index = coordonnees_joueurs.index(joueur_coord)
                    joueur_pv = pv_joueurs[joueur_index]
                    joueur_classe = classes[joueur_index]

                    # Obtenir la valeur de défense du joueur en fonction de sa classe
                    if joueur_classe == "Chevalier":
                        joueur_defense = 5  # Remplacez 5 par la valeur de défense du Chevalier
                    elif joueur_classe == 'Archere':
                        joueur_defense = 2
                    elif joueur_classe == 'Sabreur':
                        joueur_defense = 1
                    elif joueur_classe == 'Dragon':
                        joueur_defense = 3

                    ennemi_degats = ennemi.ATK
                    degats_infliges = max(0, ennemi_degats - joueur_defense)
                    pv_joueurs[joueur_index] -= degats_infliges

                    # Si les PV du joueur tombent à 0 ou moins, retirez-le du jeu
                    if pv_joueurs[joueur_index] <= 0:
                        # Retirez le joueur du jeu en le remplaçant par None
                        coordonnees_joueurs[joueur_index] = None

        # Vérifier si l'ennemi est un Mage et si un joueur est un Chevalier
        if isinstance(ennemi, Mage_noir) and "Chevalier" in classes:
            ennemi.ATK += 0.5

        # Vérifier si l'ennemi est un Chasseur de Dragon et si un joueur est un Dragon
        if isinstance(ennemi, Chasseur_Drag) and "Dragon" in classes:
               ennemi.PV += 2
                
        # Vérifier si l'ennemi est un Archer Demoniaque et si un joueur est un Archer
        if isinstance(ennemi, EvilArcher) and "Archere" in classes:
            ennemi.PV += 0.25
            ennemi.ATK += 0.5

        # Effacer l'ancienne image de l'ennemi en dessinant un rectangle vert
        pygame.draw.rect(fenetre, VERT, (x_ennemi * 80, y_ennemi * 80, 80, 80))

        # Déplacer l'ennemi vers le joueur le plus proche
        if joueur_le_plus_proche:
            x_joueur, y_joueur = joueur_le_plus_proche
            if x_joueur > x_ennemi:
                x_ennemi += 1
            elif x_joueur < x_ennemi:
                x_ennemi -= 1
            if y_joueur > y_ennemi:
                y_ennemi += 1
            elif y_joueur < y_ennemi:
                y_ennemi -= 1

        # Vérifier les collisions entre ennemis
        for autre_ennemi in ennemis:
            if autre_ennemi != ennemi and autre_ennemi.x == x_ennemi and autre_ennemi.y == y_ennemi:
                # Si une collision est détectée, ne déplacez pas l'ennemi
                break
        else:
            # Vérifier les collisions avec les joueurs
            joueur_present = False
            for joueur_x, joueur_y in coordonnees_joueurs:
                if joueur_x == x_ennemi and joueur_y == y_ennemi:
                    joueur_present = True
                    break

            # Si la case est déjà occupée par un joueur ou un autre ennemi, ne déplacez pas l'ennemi
            if not joueur_present:
                ennemi.x, ennemi.y = x_ennemi, y_ennemi

        # Dessiner l'image de l'ennemi à sa nouvelle position
        ennemi_image = charger_image_ennemi(ennemi)
        fenetre.blit(ennemi_image, (ennemi.x * 80, ennemi.y * 80))

        # Si l'ennemi traverse un lieu, redessinez ce lieu
        if (x_ennemi, y_ennemi) in emplacements_manoirs:
            manoir_image = pygame.image.load('Sprite/Manoir.png')
            fenetre.blit(manoir_image, (x_ennemi * 80 + 5, y_ennemi * 80 + 5))
        elif (x_ennemi, y_ennemi) in emplacements_forts:
            fort_image = pygame.image.load('Sprite/fort.png')
            fenetre.blit(fort_image, (x_ennemi * 80 + 5, y_ennemi * 80 + 10))
        elif (x_ennemi, y_ennemi) in emplacements_taverne:
            taverne_image = pygame.image.load('Sprite/Taverne.png')
            fenetre.blit(taverne_image, (x_ennemi * 80 + 10, y_ennemi * 80 + 5))
        elif (x_ennemi, y_ennemi) in emplacements_forge:
            forge_image = pygame.image.load('Sprite/forge.png')
            fenetre.blit(forge_image, (x_ennemi * 80 + 10, y_ennemi * 80 + 5))

    # Augmenter les PV de tous les ennemis de 1 si une Enchanteresse est présente
    if enchanteresse_presente:
        for ennemi in ennemis:
            ennemi.PV += 2

    pygame.display.update()

################################################################################
#----------------FONCTION DE BOUCLE PRINCIPAL DU JEU---------------------------#
################################################################################

# Fonction pour afficher le plateau de jeu en fonction du nombre de joueurs, des classes, des PV et des ATK
def afficher_plateau(num_joueurs, classes, pv_joueurs, atk_joueurs, mouvements_restants, nombre_de_tours):
    fenetre.fill(VERT)
    global font_pv_atk
    global difficulte

    ajouter_manoirs()
    ajouter_forts()
    ajouter_taverne()
    ajouter_forge()
    ennemis = ajouter_enemies(difficulte)
    pygame.display.flip()

    tour_termine = [False] * num_joueurs
    font_pv_atk = pygame.font.Font(None, 25)
    joueur_actuel = 0
    # Déclarez la liste des joueurs morts au début du jeu
    joueurs_morts = []
    joueurs_vivants = num_joueurs

    # Initialisation des anciennes positions des joueurs
    x_old = [0] * num_joueurs
    y_old = [0] * num_joueurs
    
    # Initialiser les boost par joueur au début de chaque tour
    tour_termine = [False] * num_joueurs
    boost_utilise_par_joueur = [False] * num_joueurs

    # Initaliser le nombre de boost PV et ATK utiliser par les joueurs
    boosts_forge_utilises = 0
    boosts_fort_utilises = 0
    boosts_manoir_utilises = 0
    boosts_taverne_utilises = 0
    boost_forge_utilise_par_joueur = [False] * num_joueurs
    boost_fort_utilise_par_joueur = [False] * num_joueurs
    cases_forts_utilisees = [False] * num_joueurs
    cases_forge_utilisees = [False] * num_joueurs
    boost_manoir_utilise_par_joueur = [False] * num_joueurs
    boost_taverne_utilise_par_joueur = [False] * num_joueurs
    cases_manoir_utilisees = [False] * num_joueurs
    cases_taverne_utilisees = [False] * num_joueurs

    # Calculer la liste des coordonnées des joueurs en fonction du nombre de joueurs
    coordonnees_joueurs = [(0, i + 2) for i in range(num_joueurs)]
    # Filtrer les coordonnées des joueurs pour exclure les valeurs None
    coordonnees_joueurs = [coord for coord in coordonnees_joueurs if coord is not None]

    # Définir une liste de booléens pour suivre si chaque joueur a déjà attaqué
    a_attaque = [False] * num_joueurs
    
    # Créez une instance d'Inventaire
    inventaire = Inventaire(fenetre, font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        creer_plateau()
        # Dessinez l'inventaire au-dessus de la grille de jeu
        inventaire.afficher()
        afficher_inventaire = False  # Variable pour suivre si l'inventaire doit être affiché

        for i in range(num_joueurs):
            if not tour_termine[i]:
                classe = classes[i]
                x, y = coordonnees_joueurs[i]
                pv = pv_joueurs[i]
                atk = atk_joueurs[i]

                for j in range(num_joueurs):
                    if j != i and coordonnees_joueurs[j] == (x, y):
                        x, y = x_old[i], y_old[i]
                        coordonnees_joueurs[i] = (x, y)

                pygame.draw.rect(fenetre, VERT, (x_old[i] * 80, y_old[i] * 80, 80, 80))

                if classe == "Chevalier":
                    cr_image = pygame.image.load('Sprite/chevalier.png')
                    fenetre.blit(cr_image, (x * 80, y * 80))
                elif classe == "Archere":
                    arc_image = pygame.image.load('Sprite/archere.png')
                    fenetre.blit(arc_image, (x * 80, y * 80))
                elif classe == "Sabreur":
                    sabreur_image = pygame.image.load('Sprite/Sabreur.png')
                    fenetre.blit(sabreur_image, (x * 80, y * 80))
                elif classe == "Dragon":
                    dragon_image = pygame.image.load('Sprite/Monteur_Dragon.png')
                    fenetre.blit(dragon_image, (x * 80, y * 80))

                text_pv = font_pv_atk.render(f"PV: {pv}", True, NOIR)
                text_pv_rect = text_pv.get_rect()
                text_pv_rect.center = (x * 80 + 40, y * 80 + 40 + 32)
                fenetre.blit(text_pv, text_pv_rect)

                text_atk = font_pv_atk.render(f"ATK: {atk}", True, NOIR)
                text_atk_rect = text_atk.get_rect()
                text_atk_rect.center = (x * 80 + 40, y * 80 + 40 - 32)
                fenetre.blit(text_atk, text_atk_rect)

                if (x_old[i], y_old[i]) in emplacements_forts:
                    fort_image = pygame.image.load('Sprite/fort.png')
                    fenetre.blit(fort_image, (x_old[i] * 80 + 5, y_old[i] * 80 + 10))
                elif (x_old[i], y_old[i]) in emplacements_manoirs:
                    manoir_image = pygame.image.load('Sprite/Manoir.png')
                    fenetre.blit(manoir_image, (x_old[i] * 80 + 5, y_old[i] * 80 + 5))
                elif (x_old[i], y_old[i]) in emplacements_taverne:
                    taverne_image = pygame.image.load('Sprite/Taverne.png')
                    fenetre.blit(taverne_image, (x_old[i] * 80 + 10, y_old[i] * 80 + 5))
                elif (x_old[i], y_old[i]) in emplacements_forge:
                    forge_image = pygame.image.load('Sprite/forge.png')
                    fenetre.blit(forge_image, (x_old[i] * 80 + 10, y_old[i] * 80 + 5))

                if (x_old[i], y_old[i]) in emplacements_forts and not cases_forts_utilisees[i]:
                    if not boost_utilise_par_joueur[i] and boosts_fort_utilises < 4:
                        fort_image = pygame.image.load('Sprite/fort.png')
                        fenetre.blit(fort_image, (x_old[i] * 80 + 5, y_old[i] * 80 + 10))
                        pv += 5  # Augmenter les PV de +5
                        pv_joueurs[i] = pv  # Mettre à jour les PV du joueur
                        boosts_fort_utilises += 1
                        cases_forts_utilisees[i] = True
                        boost_fort_utilise_par_joueur[i] = True
                elif (x_old[i], y_old[i]) in emplacements_forge and not cases_forge_utilisees[i]:
                    if not boost_utilise_par_joueur[i] and boosts_forge_utilises < 4:
                        forge_image = pygame.image.load('Sprite/forge.png')
                        fenetre.blit(forge_image, (x_old[i] * 80 + 10, y_old[i] * 80 + 5))
                        atk += 4  # Augmenter l'ATK de +4
                        atk_joueurs[i] = atk  # Mettre à jour l'ATK du joueur
                        boosts_forge_utilises += 1
                        cases_forge_utilisees[i] = True
                        boost_forge_utilise_par_joueur[i] = True

                elif (x_old[i], y_old[i]) in emplacements_manoirs and not cases_manoir_utilisees[i]:
                    if not boost_utilise_par_joueur[i] and boosts_manoir_utilises < 4:
                        manoir_image = pygame.image.load('Sprite/Manoir.png')
                        fenetre.blit(manoir_image, (x_old[i] * 80 + 5, y_old[i] * 80 + 10))
                        pv += 10  # Augmenter les PV de +5
                        pv_joueurs[i] = pv  # Mettre à jour les PV du joueur
                        boosts_manoir_utilises += 1
                        cases_manoir_utilisees[i] = True
                        boost_manoir_utilise_par_joueur[i] = True
                elif (x_old[i], y_old[i]) in emplacements_taverne and not cases_taverne_utilisees[i]:
                    if not boost_utilise_par_joueur[i] and boosts_forge_utilises < 4:
                        taverne_image = pygame.image.load('Sprite/Taverne.png')
                        fenetre.blit(taverne_image, (x_old[i] * 80 + 10, y_old[i] * 80 + 5))
                        atk += 8  # Augmenter l'ATK de +8
                        atk_joueurs[i] = atk  # Mettre à jour l'ATK du joueur
                        boosts_taverne_utilises += 1
                        cases_taverne_utilisees[i] = True
                        boost_taverne_utilise_par_joueur[i] = True

                x_old[i], y_old[i] = x, y
                new_x, new_y = x, y  # Initialisation de new_x et new_y ici pour les coordonnées

                # Vérifiez si le joueur a des points de vie inférieurs ou égaux à 0
                if pv_joueurs[i] <= 0:
                    joueurs_morts.append(i)  # Ajoutez le joueur à la liste des joueurs morts

        pygame.draw.rect(fenetre, VERT, (10, hauteur_fenetre - 50, 120, 40))
        text_tours = font.render(f"Tours: {nombre_de_tours}", True, NOIR)
        fenetre.blit(text_tours, (10, hauteur_fenetre - 50))
        pygame.display.flip()


        for i in range(num_joueurs):
            if not tour_termine[i]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        x, y = coordonnees_joueurs[i]
                        if event.key == pygame.K_LEFT and x > 0 and mouvements_restants[i] > 0:
                            new_x, new_y = x - 1, y
                        elif event.key == pygame.K_RIGHT and x < 15 and mouvements_restants[i] > 0:
                            new_x, new_y = x + 1, y
                        elif event.key == pygame.K_UP and y > 0 and mouvements_restants[i] > 0:
                            new_x, new_y = x, y - 1
                        elif event.key == pygame.K_DOWN and y < 7 and mouvements_restants[i] > 0:
                            new_x, new_y = x, y + 1
                        elif event.key == pygame.K_a and not a_attaque[i]:
                            # Vérifiez s'il y a un ennemi adjacent et infligez des dégâts en conséquence
                            for ennemi in ennemis:
                                if (
                                    (ennemi.x == x + 1 and ennemi.y == y) or (ennemi.x == x - 1 and ennemi.y == y) or
                                    (ennemi.x == x and ennemi.y == y + 1) or (ennemi.x == x and ennemi.y == y - 1)
                                ):
                                    degats_infliges = max(0, atk_joueurs[i] - ennemi.DEF)
                                    ennemi.PV -= degats_infliges

                                    if ennemi.PV < 0:
                                        ennemis.remove(ennemi)

                            # Mettez à jour l'affichage des points de vie des ennemis ici
                            for ennemi in ennemis:
                                # Effacez l'ancien affichage en dessinant un rectangle de la couleur du fond
                                pygame.draw.rect(fenetre, VERT, (ennemi.x * 80, ennemi.y * 80 + 40 - 32, 80, 50))

                                ennemi_image = charger_image_ennemi(ennemi)
                                fenetre.blit(ennemi_image, (ennemi.x * 80, ennemi.y * 80))
                                text_pv_ennemi = font_pv_atk.render(f"PV: {ennemi.PV}", True, NOIR)
                                text_pv_ennemi_rect = text_pv_ennemi.get_rect()
                                text_pv_ennemi_rect.center = (ennemi.x * 80 + 40, ennemi.y * 80 + 40 + 32)
                                fenetre.blit(text_pv_ennemi, text_pv_ennemi_rect)

                            a_attaque[i] = True  # Marquez que le joueur a attaqué
                        elif event.key == pygame.K_i:
                                inventaire.toggle()  # Affichez ou masquez l'inventaire lorsque le joueur appuie sur "i"
                        elif event.key == pygame.K_SPACE:
                            tour_termine[i] = True
                            a_attaque[i] = False  # Permet de réinitilaliser la variable d'attaque lorsque le tour est terminé
                        else:
                            new_x, new_y = x, y

                            if (x, y) != (x_old[i], y_old[i]):  # Vérifiez si le joueur a bougé
                                appliquer_boosts_sur_emplacements(x, y, classe, pv_joueurs, atk_joueurs, num_joueurs)

                        ennemi_present = False
                        for ennemi in ennemis:
                            if ennemi.x == new_x and ennemi.y == new_y:
                                ennemi_present = True
                                break

                        if not ennemi_present:
                            joueur_present = False
                            for j in range(num_joueurs):
                                if j != i and coordonnees_joueurs[j] == (new_x, new_y):
                                    joueur_present = True
                                    break

                            ennemi_sur_case = False
                            for ennemi in ennemis:
                                if ennemi.x == new_x and ennemi.y == new_y:
                                    ennemi_sur_case = True
                                    break

                            if not joueur_present and not ennemi_sur_case:
                                coordonnees_joueurs[i] = (new_x, new_y)
                                mouvements_restants[i] -= 1

        # Ajout de la condition de VICTOIRE
        if not ennemis:
            pygame.draw.rect(fenetre, NOIR, (largeur_fenetre // 2 - 200, hauteur_fenetre // 2 - 50, 400, 100))
            text_VICTOIRE = font.render("VICTOIRE !", True, ORANGE)
            text_VICTOIRE_rect = text_VICTOIRE.get_rect()
            text_VICTOIRE_rect.center = (largeur_fenetre // 2, hauteur_fenetre // 2)
            fenetre.blit(text_VICTOIRE, text_VICTOIRE_rect)
            pygame.display.flip()
            pygame.time.delay(5000)  # Attendre 5 secondes avant de lancer la fin du jeu
            # Afficher l'interface de conclusion et de remerciement du joueur
            fenetre.fill(NOIR)  # Effacer l'écran
            text_conclusion = font.render("Félicitation, grâce à vos efforts vous avez su triompher des plus grands guerriers du royaume de ", True, BLANC)
            fenetre.blit(text_conclusion, (50, 50))  # Position du texte de conclusion
            text_conclusion2 = font.render("Shurixtal tout en protégeant la capitale de Midascius et votre roi, c'est grâce à tous ses", True, BLANC)
            fenetre.blit(text_conclusion2, (50, 100))  # Position du texte de conclusion
            text_conclusion3 = font.render("efforts que quelques années plus tard vous réussissez à faire chuter le royaume de Shurixtal et ", True, BLANC)
            fenetre.blit(text_conclusion3, (50, 150))  # Position du texte de conclusion
            text_conclusion4 = font.render("à instaurer enfin votre monde de paix tant espérer, vous êtes devenues les légendes de ce monde", True, BLANC)
            fenetre.blit(text_conclusion4, (50, 200))  # Position du texte de conclusion
            text_conclusion5 = font.render("et les gens se souviendront de vous de votre courage, de votre force et de votre sagesse ", True, BLANC)
            fenetre.blit(text_conclusion5, (50, 250))  # Position du texte de conclusion
            text_conclusion5 = font.render("vous pouvez être fière de vous Héros vous avez mérité votre repos éternel, toutes mes félicitations.", True, BLANC)
            fenetre.blit(text_conclusion5, (50, 300))  # Position du texte de conclusion
            text_remerciement = font.render("Merci d'avoir joué !", True, BLANC)
            text_remerciement_rect = text_remerciement.get_rect()
            text_remerciement_rect.center = (largeur_fenetre // 2, hauteur_fenetre - 150)  # Position du message de remerciement
            fenetre.blit(text_remerciement, text_remerciement_rect)
            text_developpeur = font.render("Jeu crée par Alexis Payen !", True, BLANC)
            fenetre.blit(text_developpeur, (largeur_fenetre - 350, hauteur_fenetre - 40))  # Position du nom du développeur
            pygame.display.flip()

            # Attendre que le joueur appuie sur la touche Entrée
            attente_entree = True
            while attente_entree:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        attente_entree = False

            # Fermer le jeu
            pygame.quit()
            sys.exit()

        # Condition de DEFAITE
        if len(joueurs_morts) == num_joueurs:
            pygame.draw.rect(fenetre, NOIR, (largeur_fenetre // 2 - 200, hauteur_fenetre // 2 - 50, 400, 100))
            text_DEFAITE = font.render("DEFAITE !", True, ROUGE)
            text_DEFAITE_rect = text_DEFAITE.get_rect()
            text_DEFAITE_rect.center = (largeur_fenetre // 2, hauteur_fenetre // 2)
            fenetre.blit(text_DEFAITE, text_DEFAITE_rect)
            pygame.display.flip()
            pygame.time.delay(5000)  # Attendre 5 secondes avant de lancer la fin du jeu
            # Afficher l'interface de conclusion et de remerciement du joueur
            fenetre.fill(NOIR)  # Effacer l'écran
            text_conclusion = font.render("Malheureusement pour vous,l'armée d'élite de Shurixtal aure eu raison de vous et a réussi à", True, BLANC)
            fenetre.blit(text_conclusion, (50, 50))  # Position du texte de conclusion
            text_conclusion2 = font.render("envahir Midascius et à détruire la capitale malgré tous vos efforts", True, BLANC)
            fenetre.blit(text_conclusion2, (50, 100))  # Position du texte de conclusion
            text_conclusion3 = font.render("Le royaume de Shurixtal règne désormais en maître et votre roi est tombé,", True, BLANC)
            fenetre.blit(text_conclusion3, (50, 150))  # Position du texte de conclusion
            text_conclusion4 = font.render("vôtre légende prend fin ici...", True, BLANC)
            fenetre.blit(text_conclusion4, (50, 200))  # Position du texte de conclusion
            text_conclusion5 = font.render("Merci d'avoir joué !", True, BLANC)
            text_conclusion5_rect = text_conclusion5.get_rect()
            text_conclusion5_rect.center = (largeur_fenetre // 2, hauteur_fenetre - 150)  # Position du message de remerciement
            fenetre.blit(text_conclusion5, text_conclusion5_rect)
            text_developpeur = font.render("Jeu crée par Alexis Payen !", True, BLANC)
            fenetre.blit(text_developpeur, (largeur_fenetre - 350, hauteur_fenetre - 40))  # Position du nom du développeur
            pygame.display.flip()

            # Attendre que le joueur appuie sur la touche Entrée
            attente_entree = True
            while attente_entree:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        attente_entree = False

            # Fermer le jeu
            pygame.quit()
            sys.exit()
        
        if all(tour_termine):
            forge_boost = False
            fort_boost = False
            mouvements_restants = [nombre_max_mouvements_par_classe[classe] for classe in classes]
            nombre_de_tours += 1
            tour_termine = [False] * num_joueurs
            deplacer_ennemis(ennemis, coordonnees_joueurs, pv_joueurs, classes)
            creer_plateau()
            for ennemi in ennemis:
                # Mettez à jour les points de vie des ennemis ici
                ennemi_image = charger_image_ennemi(ennemi)
                fenetre.blit(ennemi_image, (ennemi.x * 80, ennemi.y * 80))
                text_pv_ennemi = font_pv_atk.render(f"PV: {ennemi.PV}", True, NOIR)
                text_pv_ennemi_rect = text_pv_ennemi.get_rect()
                text_pv_ennemi_rect.center = (ennemi.x * 80 + 40, ennemi.y * 80 + 40 + 32)
                fenetre.blit(text_pv_ennemi, text_pv_ennemi_rect)
                text_atk_ennemi = font_pv_atk.render(f"ATK: {ennemi.ATK}", True, NOIR)
                text_atk_ennemi_rect = text_atk_ennemi.get_rect()
                text_atk_ennemi_rect.center = (ennemi.x * 80 + 40, ennemi.y * 80 + 40 - 32)
                fenetre.blit(text_atk_ennemi, text_atk_ennemi_rect)

        pygame.display.flip()

def main():
    afficher_Lancement()  # Affichez le menu principal du jeu
    num_joueurs = afficher_menu_nb_joueurs()  # Sélection du nombre de joueurs ici

    # Ensuite, demandez la difficulté une seule fois
    global difficulte  # Utilisez la variable globale
    difficulte = afficher_menu_difficulte()

    classes = []  # Liste des classes possibles pour les joueurs
    pv_joueurs = []  # Liste pour stocker les points de vie des joueurs selon la classe
    atk_joueurs = []  # Liste pour stocker les attaques des joueurs selon la classe

    for i in range(num_joueurs):
        classe = afficher_classe()
        classes.append(classe)

        # initialisations des points de vie et de l'attaque du joueur en fonction de la classe choisie
        if classe == "Chevalier":
            pv_joueurs.append(Chevalier().PV)
            atk_joueurs.append(Chevalier().ATK)
        elif classe == "Archere":
            pv_joueurs.append(Archere().PV)
            atk_joueurs.append(Archere().ATK)
        elif classe == "Sabreur":
            pv_joueurs.append(Sabreur().PV)
            atk_joueurs.append(Sabreur().ATK)
        elif classe == "Dragon":
            pv_joueurs.append(Dragon().PV)
            atk_joueurs.append(Dragon().ATK)
            
    afficher_tuto()  # Afficher le tuto après avoir choisi les héros
    
    # Arrêtez la musique du menu lorsque le plateau est affiché
    pygame.mixer.music.stop()

    # Initialisation de Pygame Mixer pour la musique de fond du jeu
    pygame.mixer.music.load('Musique/GameSong.mp3')

    # Initialisation de mouvements_restants en fonction de la classe choisie pour chaque joueur
    mouvements_restants = [nombre_max_mouvements_par_classe[classe] for classe in classes]

    ennemis = ajouter_enemies(difficulte)  # Génération des ennemis

    while True:
        # Afficher les ennemis et leurs sprites
        creer_plateau()
        for ennemi in ennemis:
            ennemi_image = charger_image_ennemi(ennemi)
            fenetre.blit(ennemi_image, (ennemi.x * 80, ennemi.y * 80))
            text_pv_ennemi = font_pv_atk.render(f"PV: {ennemi.PV}", True, NOIR)
            text_pv_ennemi_rect = text_pv_ennemi.get_rect()
            text_pv_ennemi_rect.center = (ennemi.x * 80 + 40, ennemi.y * 80 + 40 + 32)
            fenetre.blit(text_pv_ennemi, text_pv_ennemi_rect)
            text_atk_ennemi = font_pv_atk.render(f"ATK: {ennemi.ATK}", True, NOIR)
            text_atk_ennemi_rect = text_atk_ennemi.get_rect()
            text_atk_ennemi_rect.center = (ennemi.x * 80 + 40, ennemi.y * 80 + 40 - 32)
            fenetre.blit(text_atk_ennemi, text_atk_ennemi_rect)
        pygame.display.flip()
        
        # Commencez la musique de fond du jeu lorsque le plateau est affiché
        pygame.mixer.music.play(-1)  # Jouer la musique du jeu en boucle

        afficher_plateau(num_joueurs, classes, pv_joueurs, atk_joueurs, mouvements_restants, nombre_de_tours)
        
if __name__ == "__main__":
    main()
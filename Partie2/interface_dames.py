# Auteurs: À compléter

from tkinter import Tk, Label, NSEW, Button
from Partie2.canvas_damier import CanvasDamier
from Partie1.partie import Partie
from Partie1.position import Position
from Partie1.damier import Damier
from sys import platform


class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme

        TODO: AJOUTER VOS PROPRES ATTRIBUTS ICI!

    """

    def __init__(self):
        """Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre.
        """

        # Appel du constructeur de la classe de base (Tk)
        super().__init__()

        # La partie
        self.position_source = None
        self.position_cible = None
        self.validite = False
        self.partie = Partie()

        # On va chercher le système d'exploitation pour le clique droit
        self.systeme_exploitation = platform

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)
        if self.systeme_exploitation == "darwin":  # Si on est en Mac
            self.canvas_damier.bind('<Button-2>', self.deplacer)
        else:  # Si on est sur Windows
            self.canvas_damier.bind('<Button-3>', self.deplacer)


        # Enregistrer la position de la pièce sélectionnée
        self.piece_selectionnee = self.selectionner

        # Faire passer le deplacement
        self.piece_deplacer = self.deplacer

        # Convertir les inputs de demander_position_deplacement en clics de souris
        #self.partie.demander_positions_deplacement = self.selectionner

        # Création des boutons pour la partie
        self.button_start = Button(self, text="Commencer la partie", command=self.jouer_interface)
        self.button_start.grid()

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        position = Position(ligne, colonne)

        # On récupère l'information sur la pièce à l'endroit choisi.
        piece = self.partie.damier.recuperer_piece_a_position(position)

        if piece is None:
            self.messages['foreground'] = 'red'
            self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
        else:
            self.messages['foreground'] = 'black'
            self.messages['text'] = (
                'Pièce sélectionnée à la position {}.'.format(position), '.Clic droit sur une case pour déplacer')

        # On vérifie si la position est valide
        if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
            self.partie.doit_prendre = True
        print(self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant))
        if self.partie.position_source_valide(position)[0]:
            self.position_source = position
            self.partie.position_source_selectionnee = position
            self.validite = True
            print(self.partie.position_source_valide(position))
            return

        print(self.partie.position_source_valide(position))
        self.validite = False
        return




    def deplacer(self, event):
        """Méthode utilisant le clic droit pour déplacer la dernière pièce sélectionnée

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # On stocke la position_cible dans le clic droit et initialise le tour
        if self.validite is not False:
           ligne = event.y // self.canvas_damier.n_pixels_par_case
           colonne = event.x // self.canvas_damier.n_pixels_par_case
           position = Position(ligne, colonne)
           piece = self.partie.damier.recuperer_piece_a_position(position)
           if piece is None:
               self.position_cible = position
               self.jouer_suite_au_clic(self.position_source, self.position_cible)

        return

    def jouer_interface(self):
        self.button_start.destroy()

    def jouer_suite_au_clic(self, position_source, position_cible):

        # On valide les positions
        try:
            self.partie.position_source_valide(position_source)
            self.partie.position_cible_valide(position_cible)
        except:
            print("non")

        # On fait le déplacement
        self.partie.damier.deplacer(position_source, position_cible)
        self.canvas_damier.damier.deplacer(position_source, position_cible)
        self.canvas_damier.actualiser()
        self.messages['foreground'] = 'black'
        self.messages['text'] = 'Clic droit.'

        # Mettre à jour les attributs de la classe
        if self.partie.damier.piece_de_couleur_peut_faire_une_prise(
                self.partie.couleur_joueur_courant) and self.partie.double_prise_possible == True:
            return

        if self.partie.couleur_joueur_courant == "blanc":
            self.partie.couleur_joueur_courant = "noir"
        else:
            self.partie.couleur_joueur_courant = "blanc"

        self.partie.doit_prendre = False
        self.partie.double_prise_possible = False



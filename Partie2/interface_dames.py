# Auteurs: À compléter

from tkinter import Tk, Label, NSEW, Button
from Partie2.canvas_damier import CanvasDamier
from Partie1.partie import Partie
from Partie1.position import Position
from Partie1.damier import Damier



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
        self.partie = Partie()

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)
        self.canvas_damier.bind('<Button-3>', self.deplacer)

        # Enregistrer la position de la pièce sélectionnée
        self.piece_selectionnee = self.selectionner

        # Convertir les inputs de demander_position_deplacement en clics de souris
        self.partie.demander_positions_deplacement = self.selectionner

        # Création des boutons pour la partie
        self.button_start = Button(self, text="Commencer la partie", command=self.jouer)
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

        self.position_source = position


    def deplacer(self, event):
        """Méthode utilisant le clic droit pour déplacer la dernière pièce sélectionnée

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """
        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        position = Position(ligne, colonne)
        self.canvas_damier.damier.deplacer(self.position_source, position)
        self.canvas_damier.actualiser()



        # TODO: À continuer....
        #self.canvas_damier.bind('<Button-1>', self.selectionner)
        self.canvas_damier.actualiser()
        #self.canvas_damier.bind('<Button-1>', self.deplacer(event))

    def jouer(self):
        """Méthode permettant de proprement lancer la partie grâce à un bouton
        """

        self.button_start.destroy()
        #self.canvas_damier.actualiser()
        self.partie.jouer()



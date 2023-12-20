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



        # Création des boutons pour la partie
        self.quitter_partie = Button(self, text="Quitter la partie", command=self.quitter_la_partie)
        self.quitter_partie.grid()
        self.messages = Label(self)
        self.messages.grid()
        self.button_start = Button(self, text="Commencer une nouvelle partie", command=self.jouer_interface,)
        self.button_start.grid()


        # Ajout du joueur courant
        self.joueur_courant = Label(self, bg="white",)
        self.joueur_courant['foreground'] = 'black'
        self.joueur_courant['text'] = 'Au tour du joueur {}.'.format(self.partie.couleur_joueur_courant)
        self.joueur_courant.place(relx=0.72,rely=0.87)

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
        elif self.partie.position_source_valide(position)[0]:
            self.messages['foreground'] = 'black'
            self.messages['text'] = (
                'Pièce sélectionnée à la position {}.'.format(position), 'Clic droit sur une case pour déplacer')
        elif not self.partie.position_source_valide(position)[0]:
            self.messages['foreground'] = 'black'
            self.messages['text'] = self.partie.position_source_valide(position)[1]

        # On vérifie si la position est valide
        if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
            self.partie.doit_prendre = True
        if self.partie.position_source_valide(position)[0]:
            self.position_source = position
            self.partie.position_source_selectionnee = position
            self.validite = True
            return

        # Message de rétroaction
        if self.partie.position_source_valide(position)[1] == 'Une autre pièce peut faire une prise, fais attention!':
            self.messages['foreground'] = 'black'
            self.messages['text'] = self.partie.position_source_valide(position)[1]

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
        """Cette méthode permet de lancer une nouvelle partie en appuyant le bouton :
           Commencer une nouvelle partie
           """

        self.destroy()
        fenetre = FenetrePartie()
        fenetre.mainloop()


    def jouer_suite_au_clic(self, position_source, position_cible):
        """Cette méthode est appelé suite au relâchement du clic droit et permet d'effectuer le tour du joueur.
            Elle met ensuite à jour les attributs de joueur courant et affiche les messages nécessaire à la rétroaction.
            Finalement, elle vérifie si une double prise et possible.

            Args : position_source (donner par le clic gauche de sélectionner() )
                   position_cible  (donner par le clic droit de déplacer() )
            """

        # On valide les positions
        try:
            self.partie.position_source_valide(position_source)
            self.partie.position_cible_valide(position_cible)
        except:
            print("non")

        # Messages de rétroaction
        if not self.partie.position_source_valide(position_source):
            self.messages['foreground'] = 'black'
            self.messages['text'] = self.partie.position_source_valide(position_source)[1]

        if not self.partie.position_cible_valide(position_cible)[0]:
            self.messages['foreground'] = 'black'
            self.messages['text'] = self.partie.position_cible_valide(position_cible)[1]
            return

        if self.partie.position_source_valide(position_source)[1] == 'Une autre pièce peut faire une prise, fais attention!':
            self.messages['foreground'] = 'black'
            self.messages['text'] = self.partie.position_source_valide(position_source)[1]

        # On fait le déplacement
        self.partie.damier.deplacer(position_source, position_cible)
        self.canvas_damier.damier.deplacer(position_source, position_cible)
        self.canvas_damier.actualiser()

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
        self.joueur_courant['foreground'] = 'black'
        self.joueur_courant['text'] = 'Au tour du joueur {}.'.format(self.partie.couleur_joueur_courant)



    def quitter_la_partie(self):
        self.destroy()

# Auteurs: Équipe IFT-1004

from tkinter import Tk, Canvas
from Partie1.position import Position


class CanvasDamier(Canvas):
    """Interface graphique de la partie de dames.

    Attributes:
        damier (Damier): L'objet qui contient les informations sur le damier à dessiner
        n_pixels_par_case (int): Nombre de pixels par case.

    """

    def __init__(self, parent, damier, n_pixels_par_case=60):
        """Constructeur de la classe CanvasDamier. Initialise les deux attributs de la classe.

        Args:
            parent (tkinter.Widget): Le «widget» parent sur lequel sera ajouté le nouveau CanvasDamier
            damier (Dnmier): L'objet qui contient les informations sur le damier à dessiner
            n_pixels_par_case (int): Nombre de pixels par case. Ceci peut varier selon la taille de l'affichage

        """
        self.damier = damier

        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case

        # Appel du constructeur de la classe de base (Canvas).
        largeur = self.damier.n_lignes * n_pixels_par_case
        hauteur = self.damier.n_colonnes * n_pixels_par_case
        super().__init__(parent, width=largeur, height=hauteur)

        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.bind('<Configure>', self.redimensionner)

    def dessiner_cases(self):
        """Méthode qui dessine les cases du damier sur le canvas (sans les pièces)
        """
        for i in range(self.damier.n_lignes):
            for j in range(self.damier.n_colonnes):
                debut_ligne = i * self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case
                debut_colonne = j * self.n_pixels_par_case
                fin_colonne = debut_colonne + self.n_pixels_par_case

                # On détermine la couleur.
                if (i + j) % 2 == 0:
                    couleur = '#FF6464'
                else:
                    couleur = '#DDDDFF'

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments
                # par la suite.
                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')

    def dessiner_pieces(self):
        """Méthode qui dessine les pièces sur le canvas"""

        # Pour tout paire position, pièce:
        for position, piece in self.damier.cases.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = position.ligne * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = position.colonne * self.n_pixels_par_case + self.n_pixels_par_case // 2

            # On utilise des caractères unicodes représentant des pièces
            if piece.est_blanche() and piece.est_pion():
                icone = "\u26C0"
            elif piece.est_blanche() and piece.est_dame():
                icone = "\u26C1"
            elif piece.est_noire() and piece.est_pion():
                icone = "\u26C2"
            else:
                icone = "\u26C3"

            police_de_caractere = ('Deja Vu', self.n_pixels_par_case//2)
            self.create_text(coordonnee_x, coordonnee_y, text=icone, font=police_de_caractere, tags='piece')

    def redimensionner(self, event):
        """Méthode qui est est appellé automatiquement lorsque le canvas est redimensionné.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.damier.n_lignes

        self.actualiser()

    def actualiser(self):
        """Méthode qui redésinne le canvas (mets à jour l'affichage du damier).
        """
        # On supprime les anciennes cases et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_cases()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_pieces()

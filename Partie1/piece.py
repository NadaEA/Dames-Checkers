# Auteurs: Équipe IFT-1004


class Piece:
    """Une pièce d'un jeu de dames.

    Attributes:
        couleur (str): La couleur de la pièce. Les deux valeurs possibles sont 'blanc' et 'noir'.
        type_de_piece (str): Le type de pièce. Les deux valeurs possibles sont 'pion' et 'dame'.

    """
    def __init__(self, couleur, type_de_piece):
        """Constructeur de la classe Piece. Initialise les deux attributs de la classe.

        Args:
            couleur (str): La couleur de la pièce ('blanc' ou 'noir').
            type_de_piece (str) : Le type de pièce ('pion' ou 'dame').

        """
        self.couleur = couleur
        self.type_de_piece = type_de_piece

    def est_pion(self):
        """Détermine si la pièce est un pion.

        Returns:
            (bool) : True si la pièce est un pion, False autrement.

        """
        return self.type_de_piece == "pion"

    def est_dame(self):
        """Détermine si la pièce est une dame.

        Returns:
            (bool) : True si la pièce est une dame, False autrement.

        """
        return self.type_de_piece == "dame"

    def est_blanche(self):
        """Détermine si la pièce est de couleur blanche.

        Returns:
            (bool) : True si la pièce est blanche, False autrement.

        """
        return self.couleur == "blanc"

    def est_noire(self):
        """Détermine si la pièce est de couleur noire.

        Returns:
            (bool) : True si la pièce est noire, False autrement.

        """
        return self.couleur == "noir"

    def promouvoir(self):
        """Cette méthode permet de promouvoir une pièce, c'est à dire la transformer en dame.

        """
        self.type_de_piece = "dame"
	
    def __eq__(self, other):
        """Méthode spéciale indiquant à Python comment vérifier si deux pièces sont égales. On compare simplement
        la couleur et le type de l'objet actuel (self) et de l'autre objet (other).

        """
        return self.couleur == other.couleur and self.type_de_piece == other.type_de_piece

    def __repr__(self):
        """Méthode spéciale indiquant à Python comment représenter une instance de Piece sous la forme d'une chaîne
        de caractères. Permet notamment d'afficher une pièce à l'écran.

        """
        if self.est_blanche() and self.est_pion():
            return "o"
        elif self.est_blanche() and self.est_dame():
            return "O"
        elif self.est_noire() and self.est_pion():
            return "x"
        else:
            return "X"


if __name__ == '__main__':
    print('Test unitaires de la classe "Piece"...')

    une_piece = Piece('blanc', 'pion')
    assert une_piece.est_pion()
    assert not une_piece.est_dame()
    assert une_piece.est_blanche()
    assert not une_piece.est_noire()

    une_piece.promouvoir()
    assert not une_piece.est_pion()
    assert une_piece.est_dame()
    assert une_piece.est_blanche()
    assert not une_piece.est_noire()

    print('Test unitaires passés avec succès!')
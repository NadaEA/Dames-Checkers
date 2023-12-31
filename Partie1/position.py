# Auteurs: À compléter


class Position:
    """Une position à deux coordonnées: ligne et colonne. La convention utilisée est celle de la notation matricielle :
    le coin supérieur gauche d'une matrice est dénoté (0, 0) (ligne 0 et colonne 0). On additionne une unité de colonne
    lorsqu'on se déplace vers la droite, et une unité de ligne lorsqu'on se déplace vers le bas.

    +-------+-------+-------+-------+
    | (0,0) | (0,1) | (0,2) |  ...  |
    | (1,0) | (1,1) | (1,2) |  ...  |
    | (2,0) | (2,1) | (2,2) |  ...  |
    |  ...  |  ...  |  ...  |  ...  |
    +-------+-------+-------+-------+

    Attributes:
        ligne (int): La ligne associée à la position.
        colonne (int): La colonne associée à la position

    """
    def __init__(self, ligne, colonne):
        """Constructeur de la classe Position. Initialise les deux attributs de la classe.

        Args:
            ligne (int): La ligne à considérer dans l'instance de Position.
            colonne (int): La colonne à considérer dans l'instance de Position.

        """
        self.ligne = ligne
        self.colonne = colonne

    def positions_diagonales_bas(self):
        """Retourne une liste contenant les deux positions diagonales bas à partir de la position actuelle.
        Args:
            None
        Returns:
            list: La liste des deux positions.

        """
        return [Position(self.ligne + 1, self.colonne - 1), Position(self.ligne + 1, self.colonne + 1)]

############################################# Jérémie ##################################################
    def positions_diagonales_haut(self):
        """Retourne une liste contenant les deux positions diagonales haut à partir de la position actuelle.

        Returns:
            list: La liste des deux positions.

        """
        return [Position(self.ligne - 1, self.colonne - 1), Position(self.ligne -1 , self.colonne + 1)]



    def quatre_positions_diagonales(self):
        """Retourne une liste contenant les quatre positions diagonales à partir de la position actuelle.

        Returns:
            list: La liste des quatre positions.

        """
        return [Position(self.ligne - 1, self.colonne - 1), Position(self.ligne -1 , self.colonne + 1)
               ,Position(self.ligne + 1, self.colonne - 1), Position(self.ligne + 1, self.colonne + 1)]




    def quatre_positions_sauts(self):
        """Retourne une liste contenant les quatre "sauts" diagonaux à partir de la position actuelle. Les positions
        retournées sont donc en diagonale avec la position actuelle, mais a une distance de 2.

        Returns:
            list: La liste des quatre positions.

        """
        return [Position(self.ligne - 2, self.colonne - 2), Position(self.ligne -2 , self.colonne + 2)
               ,Position(self.ligne + 2, self.colonne - 2), Position(self.ligne + 2, self.colonne + 2)]


    def __eq__(self, other):
        """Méthode spéciale indiquant à Python comment vérifier si deux positions sont égales. On compare simplement
        la ligne et la colonne de l'objet actuel et de l'autre objet.

        """
        return self.ligne == other.ligne and self.colonne == other.colonne

    def __repr__(self):
        """Méthode spéciale indiquant à Python comment représenter une instance de Position par une chaîne de
        caractères. Notamment utilisé pour imprimer une position à l'écran.

        """
        return '({}, {})'.format(self.ligne, self.colonne)

    def __hash__(self):
        """Méthode spéciale indiquant à Python comment "hasher" une Position. Cette méthode est nécessaire si on veut
        utiliser une classe que nous avons définie nous mêmes comme clé d'un dictionnaire.
        Les étudiants(es) curieux(ses) peuvent consulter wikipédia pour en savoir plus:
            https://fr.wikipedia.org/wiki/Fonction_de_hachage

        """
        return hash(str(self))



if __name__ == '__main__':
    print('Test unitaires de la classe "Position"...')
    # TODO: À compléter

    #test_unitaire de positions_diagonales_bas
    position_1 = Position(0,1)
    assert Position(1,0).positions_diagonales_bas() == [Position(2,-1), Position(2,1)]
    assert Position(1, 1).positions_diagonales_bas() == [Position(2, 0), Position(2, 2)]



    #test_unitaire de positions_diagonales_haut
    position_1 = Position(0, 1)
    liste_positions_des_diagonales_hautes = position_1.positions_diagonales_haut()
    assert liste_positions_des_diagonales_hautes[0].ligne == -1 and liste_positions_des_diagonales_hautes[0].colonne == 0
    assert liste_positions_des_diagonales_hautes[1].ligne == -1 and liste_positions_des_diagonales_hautes[1].colonne == 2

    # test_unitaire de quatre_positions_diagonales
    position_1 = Position(0, 1)
    liste_positions_des_quatres_diagonales = position_1.quatre_positions_diagonales()
    assert liste_positions_des_quatres_diagonales[2].ligne == 1 and liste_positions_des_quatres_diagonales[2].colonne == 0
    assert liste_positions_des_quatres_diagonales[3].ligne == 1 and liste_positions_des_quatres_diagonales[3].colonne == 2

    # test_unitaire de quatre_positions_sauts
    assert Position(2,2).quatre_positions_sauts()[1] == Position(0,4)
    assert Position(2, 2).quatre_positions_sauts()[0] == Position(0,0)





    print('Test unitaires passés avec succès!')
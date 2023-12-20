# Auteurs: À compléter

from Partie1.piece import Piece
from Partie1.position import Position


class Damier:
    """Plateau de jeu d'un jeu de dames. Contient un ensemble de pièces positionnées à une certaine position
    sur le plateau.

    Attributes:
        cases (dict): Dictionnaire dont une clé représente une Position, et une valeur correspond à la Piece
            positionnée à cet endroit sur le plateau. Notez bien qu'une case vide (sans pièce blanche ou noire)
            correspond à l'absence de clé la position de cette case dans le dictionnaire.

        n_lignes (int): Le nombre de lignes du plateau. La valeur est 8 (constante).
        n_colonnes (int): Le nombre de colonnes du plateau. La valeur est 8 (constante).

    """

    def __init__(self):
        """Constructeur du Damier. Initialise un damier initial de 8 lignes par 8 colonnes.

        """
        self.n_lignes = 8
        self.n_colonnes = 8

        self.cases = {
            Position(7, 0): Piece("blanc", "pion"),
            Position(7, 2): Piece("blanc", "pion"),
            Position(7, 4): Piece("blanc", "pion"),
            Position(7, 6): Piece("blanc", "pion"),
            Position(6, 1): Piece("blanc", "pion"),
            Position(6, 3): Piece("blanc", "pion"),
            Position(6, 5): Piece("blanc", "pion"),
            Position(6, 7): Piece("blanc", "pion"),
            Position(5, 0): Piece("blanc", "pion"),
            Position(5, 2): Piece("blanc", "pion"),
            Position(5, 4): Piece("blanc", "pion"),
            Position(5, 6): Piece("blanc", "pion"),
            Position(2, 1): Piece("noir", "pion"),
            Position(2, 3): Piece("noir", "pion"),
            Position(2, 5): Piece("noir", "pion"),
            Position(2, 7): Piece("noir", "pion"),
            Position(1, 0): Piece("noir", "pion"),
            Position(1, 2): Piece("noir", "pion"),
            Position(1, 4): Piece("noir", "pion"),
            Position(1, 6): Piece("noir", "pion"),
            Position(0, 1): Piece("noir", "pion"),
            Position(0, 3): Piece("noir", "pion"),
            Position(0, 5): Piece("noir", "pion"),
            Position(0, 7): Piece("noir", "pion"),
        }

    def recuperer_piece_a_position(self, position):
        """Retourne la pièce à une certaine position sur le damier. Si aucune pièce n'est à cette position, retourne
        None.

        Args
            position (Position): La position à vérifier.

        Returns:
            Piece: La pièce à la position reçue, ou None si aucune pièce n'est à cette position.
        """
        if position not in self.cases:
            return None

        return self.cases[position]

    def position_est_dans_damier(self, position):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """
        dans_bornes = False
        if (position.ligne >= 0 and position.ligne < 8) and (position.colonne >= 0 and position.colonne < 8):
            dans_bornes = True
        return dans_bornes

    def piece_peut_se_deplacer_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut se déplacer à une certaine position cible.
        On parle ici d'un déplacement standard (et non une prise).

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce de type pion ne peut qu'avancer en diagonale (vers le haut pour une pièce blanche, vers le bas pour
        une pièce noire). Une pièce de type dame peut avancer sur n'importe quelle diagonale, peu importe sa couleur.
        Une pièce ne peut pas se déplacer sur une case déjà occupée par une autre pièce. Une pièce ne peut pas se
        déplacer à l'extérieur du damier.

        Args:
            position_piece (Position): La position de la pièce source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            bool: True si la pièce peut se déplacer à la position cible, False autrement.

        """
        piece = self.recuperer_piece_a_position(position_piece)

        # D'abord on vérifie que la position en question est occuppée par une pièce:
        if piece is None:
            return False
        # Ensuite on vérifie que la position cible est bien dans le damier:
        if not self.position_est_dans_damier(position_cible):
            return False
        # Ensuite on s'assure que la position cible n'est pas déjà occuppée
        piece_2 = self.recuperer_piece_a_position(position_cible)
        if piece_2 is not None:
            return False

        # Maintenant on considère les différentes pièces possibles

        # Cas où la pièce est un pion
        if piece.type_de_piece == "pion":
            if piece.couleur == "noir":
                # Ici on s'assure que la position cible est un move légal
                if position_cible not in position_piece.positions_diagonales_bas():
                    return False
            # Ici on considère le cas où la pièce est un pion de couleur blanche
            else:
                if position_cible not in position_piece.positions_diagonales_haut():
                    return False
        # Dans l'autre cas nous avons une dame
        else:
            if position_cible not in position_piece.quatre_positions_diagonales():
                return False

        # Si on a toujours pas retourné False, alors le move est légal
        return True

    def piece_peut_sauter_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut sauter vers une certaine position cible.
        On parle ici d'un déplacement qui "mange" une pièce adverse.

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce ne peut que sauter de deux cases en diagonale. N'importe quel type de pièce (pion ou dame) peut sauter
        vers l'avant ou vers l'arrière. Une pièce ne peut pas sauter vers une case qui est déjà occupée par une autre
        pièce. Une pièce ne peut faire un saut que si elle saute par dessus une pièce de couleur adverse.

        Args:
            position_piece (Position): La position de la pièce source du saut.
            position_cible (Position): La position cible du saut.

        Returns:
            bool: True si la pièce peut sauter vers la position cible, False autrement.

        """
        piece = self.recuperer_piece_a_position(position_piece)

        # D'abord on vérifie que la position en question est occupée par une pièce:
        if piece is None:
            return False

        # Ensuite on vérifie que la position cible est bien dans le damier:
        if not self.position_est_dans_damier(position_cible):
            return False

        # Ensuite on s'assure que la position cible est bien un saut possible
        if position_cible not in position_piece.quatre_positions_sauts():
            return False

        # Maintenant on peut déterminer la position de la pièce enemie (sur laquelle on saute)
        ligne_position_piece = position_piece.ligne
        ligne_position_cible = position_cible.ligne

        colonne_position_piece = position_piece.colonne
        colonne_position_cible = position_cible.colonne

        if ligne_position_piece - ligne_position_cible > 0:
            ligne_position_enemie = ligne_position_cible + 1
        else:
            ligne_position_enemie = ligne_position_piece + 1

        if colonne_position_piece - colonne_position_cible > 0:
            colonne_position_enemie = colonne_position_cible + 1
        else:
            colonne_position_enemie = colonne_position_piece + 1

        # Donc la position de la piece enemie est:
        position_piece_enemie = Position(ligne_position_enemie, colonne_position_enemie)

        # Maintenant on peut vérifier que la position enemie est occupée
        piece_enemie = self.recuperer_piece_a_position(position_piece_enemie)
        if piece_enemie is None:
            return False
        # Finalement on s'assure que la piece enemie est bien une piece adverse
        if (piece.couleur == "noir" and piece_enemie.couleur == "noir") or (
                piece.couleur == "blanc" and piece_enemie.couleur == "blanc"):
            return False
        # Si on a pas return False by now, on peut return True
        return True, position_piece_enemie

    def piece_peut_se_deplacer(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de se déplacer (sans faire de saut).

        ATTENTION: N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
        les positions des quatre déplacements possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut se déplacer, False autrement.

        """
        #piece = self.recuperer_piece_a_position(position_piece)

        # Déterminons les 4 positions possibles pour la piece:
        liste_positions_possibles = position_piece.quatre_positions_diagonales()
        peut_se_deplacer = False
        # Si une des positions possibles est disponible on return True
        for elem in liste_positions_possibles:
            if self.piece_peut_se_deplacer_vers(position_piece, elem):
                print(peut_se_deplacer)
                peut_se_deplacer = True

        return peut_se_deplacer

    def piece_peut_faire_une_prise(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de faire une prise.

        Warning:
            N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
            les positions des quatre sauts possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut faire une prise. False autrement.

        """
        #piece = self.recuperer_piece_a_position(position_piece)

        # Déterminons les 4 positions possibles pour la piece:
        liste_positions_possibles = position_piece.quatre_positions_sauts()
        peut_faire_une_prise = False
        # Si une des positions possibles est disponible on return True
        for element in liste_positions_possibles:
            if self.piece_peut_sauter_vers(position_piece, element) and self.recuperer_piece_a_position(element) is None:
                peut_faire_une_prise = True
        return peut_faire_une_prise

    def piece_de_couleur_peut_se_deplacer(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de se déplacer
        vers une case adjacente (sans saut).

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un déplacement standard, False autrement.
        """

        for position in self.cases:
            piece = self.recuperer_piece_a_position(position)
            if piece.couleur == couleur:
                if self.piece_peut_se_deplacer(position):
                    return True
        return False

    def piece_de_couleur_peut_faire_une_prise(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de faire un
        saut, c'est à dire vérifie s'il existe une pièce d'une certaine couleur qui a la possibilité de prendre une
        pièce adverse.

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un saut (une prise), False autrement.
        """

        for position in self.cases:
            piece = self.recuperer_piece_a_position(position)
            if piece.couleur == couleur:
                if self.piece_peut_faire_une_prise(position):
                    return True

        return False

    def deplacer(self, position_source, position_cible):
        """Effectue le déplacement sur le damier. Si le déplacement est valide, on doit mettre à jour le dictionnaire
        self.cases, en déplaçant la pièce à sa nouvelle position (et possiblement en supprimant une pièce adverse qui a
        été prise).

        Cette méthode doit également:
        - Promouvoir un pion en dame si celui-ci atteint l'autre extrémité du plateau.
        - Retourner un message indiquant "ok", "prise" ou "erreur".

        ATTENTION: Si le déplacement est effectué, cette méthode doit retourner "ok" si aucune prise n'a été faite,
            et "prise" si une pièce a été prise.
        ATTENTION: Ne dupliquez pas de code! Vous avez déjà programmé (ou allez programmer) des méthodes permettant
            de valider si une pièce peut se déplacer vers un certain endroit ou non.

        Args:
            position_source (Position): La position source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            str: "ok" si le déplacement a été effectué sans prise, "prise" si une pièce adverse a été prise, et
                "erreur" autrement.

        """
        piece_position_source = self.recuperer_piece_a_position(position_source)

        # On vérifie que la position source est bien occupée
        if self.recuperer_piece_a_position(position_source) is not None:

            # On vérifie que la position cible est bien dans le damier
            if self.position_est_dans_damier(position_cible):

                # On vérifie que la position cible est bien vide
                if self.recuperer_piece_a_position(position_cible) is None:

                    # On vérifie que le déplacement est une prise
                    verification = self.piece_peut_sauter_vers(position_source, position_cible)
                    if verification:
                        position_enemie = self.determiner_position_enemie(position_source, position_cible)
                        if piece_position_source.est_blanche() and position_cible.ligne == 0:
                            self.cases[position_source].promouvoir()
                        elif piece_position_source.est_noire() and position_cible.ligne == 7:
                            self.cases[position_source].promouvoir()
                        del self.cases[position_enemie]
                        self.cases[position_cible] = self.cases[position_source]
                        #print(self.cases[position_cible].type_de_piece)
                        del self.cases[position_source]
                        return "prise"
                    else:
                        # Si ce n'est pas une prise, mais juste un déplacement
                        if self.piece_peut_se_deplacer_vers(position_source, position_cible):
                            if piece_position_source.est_blanche() and position_cible.ligne == 0:
                                self.cases[position_source].promouvoir()
                            elif piece_position_source.est_noire() and position_cible.ligne == 7:
                                self.cases[position_source].promouvoir()
                            self.cases[position_cible] = self.cases[position_source]
                            #print(self.cases[position_cible].type_de_piece)
                            del self.cases[position_source]
                            return "ok"

        return "erreur"

    def determiner_position_enemie(self, position_source, position_cible):
        """
        Cette méthode détermine la position de la pièce enemie qui est prise lors d'un saut.
        Args:
            position_source (Position): La position source du saut.
            position_cible (Position): La position cible du saut.

        Returns:
            Position: La position de la pièce enemie qui est prise lors d'un saut.
        """

        ligne_position_piece = position_source.ligne
        ligne_position_cible = position_cible.ligne

        colonne_position_piece = position_source.colonne
        colonne_position_cible = position_cible.colonne

        if ligne_position_piece - ligne_position_cible > 0:
            ligne_position_enemie = ligne_position_cible + 1
        else:
            ligne_position_enemie = ligne_position_piece + 1

        if colonne_position_piece - colonne_position_cible > 0:
            colonne_position_enemie = colonne_position_cible + 1
        else:
            colonne_position_enemie = colonne_position_piece + 1

        # Donc la position de la piece enemie est:
        position_piece_enemie = Position(ligne_position_enemie, colonne_position_enemie)
        return position_piece_enemie
    def __repr__(self):
        """Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Damier pour
        l'affichage. Faire un print(un_damier) affichera le damier à l'écran.

        """
        s = " +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, 8):
            s += str(i) + "| "
            for j in range(0, 8):
                if Position(i, j) in self.cases:
                    s += str(self.cases[Position(i, j)]) + " | "
                else:
                    s += "  | "
            s += "\n +---+---+---+---+---+---+---+---+\n"

        return s


if __name__ == "__main__":
    print('Test unitaires de la classe "Damier"...')

    un_damier = Damier()

    # TODO: À compléter

    # tests unitaires de position_est_dans_damier
    position_1 = Position(-2, -3)
    assert un_damier.position_est_dans_damier(position_1) == False

    position_2 = Position(0, 8)
    assert un_damier.position_est_dans_damier(position_2) == False

    position_3 = Position(0, 7)
    assert un_damier.position_est_dans_damier(position_3) == True

    # tests unitaires de piece_peut_se_deplacer_vers
    # S'il n'y a pas de piece a la position_piece
    position_1 = Position(1, 1)
    position_2 = Position(2, 2)
    valeur_bool = un_damier.piece_peut_se_deplacer_vers(position_1, position_2)
    assert valeur_bool == False

    # Si la position_cible n'est pas dans le damier
    position_1 = Position(2, 1)
    position_2 = Position(0, 8)
    assert un_damier.piece_peut_se_deplacer_vers(position_1, position_2) == False

    # Si la position cible est déjà occupée
    position_1 = Position(2, 1)
    position_2 = Position(5, 4)
    assert un_damier.piece_peut_se_deplacer_vers(position_1, position_2) == False

    # Si on essaie de se déplacer dans une position qui est trop loin (pas dans les diagonales immédiates
    position_1 = Position(5, 2)
    position_2 = Position(3, 4)
    assert un_damier.piece_peut_se_deplacer_vers(position_1, position_2) == False

    # Finalement faut quand même que ça passe si c'est correct
    position_1 = Position(2, 1)
    position_2 = Position(3, 2)
    position_3 = Position(3, 0)
    assert un_damier.piece_peut_se_deplacer_vers(position_1, position_2) == True
    assert un_damier.piece_peut_se_deplacer_vers(position_1, position_3) == True

    # Tests unitaire de piece_peut_sauter_vers
    # Si notre position est pas occupée
    position_1 = Position(1, 1)
    position_2 = Position(3, 3)
    assert un_damier.piece_peut_sauter_vers(position_1, position_2) == False

    # Si c'est pas un saut possible
    position_1 = Position(2, 1)
    position_2 = Position(5, 4)
    assert un_damier.piece_peut_sauter_vers(position_1, position_2) == False

    # Si c'est pas une pièce adverse
    position_1 = Position(0, 1)
    position_2 = Position(3, 2)
    assert un_damier.piece_peut_sauter_vers(position_1, position_2) == False
    ####Probablement faire d'autres tests quand on pourra bouger!#########

    # Tests unitaires de piece_peut_se_deplacer
    position_1 = Position(0, 1)
    assert un_damier.piece_peut_se_deplacer(position_1) == False

    position_1 = Position(2, 3)
    assert un_damier.piece_peut_se_deplacer(position_1) == True

    position_1 = Position(6, 5)
    assert un_damier.piece_peut_se_deplacer(position_1) == False

    position_1 = Position(5, 6)
    assert un_damier.piece_peut_se_deplacer(position_1) == True

    # Tests unitaires de piece_peut_faire_une_prise
    position_1 = Position(0, 1)
    assert un_damier.piece_peut_faire_une_prise(position_1) == False

    position_1 = Position(2, 3)
    assert un_damier.piece_peut_faire_une_prise(position_1) == False

    position_1 = Position(6, 5)
    assert not un_damier.piece_peut_faire_une_prise(position_1) == True


    # Tests unitaires de piece_de_couleur_peut_se_deplacer
    assert un_damier.piece_de_couleur_peut_se_deplacer("blanc") == True
    assert un_damier.piece_de_couleur_peut_se_deplacer("noir") == True
    assert not un_damier.piece_de_couleur_peut_se_deplacer("blanc") == False

    # Tests unitaires de piece_de_couleur_peut_faire_une_prise
    assert un_damier.piece_de_couleur_peut_faire_une_prise("blanc") == False
    assert un_damier.piece_de_couleur_peut_faire_une_prise("noir") == False
    assert not un_damier.piece_de_couleur_peut_faire_une_prise("blanc") == True


    # Tests unitaires de deplacer
    # Si la position source est vide
    position_1 = Position(1, 1)
    position_2 = Position(2, 2)
    assert un_damier.deplacer(position_1, position_2) == "erreur"

    # Si la position cible est pas dans le damier
    position_1 = Position(2, 1)
    position_2 = Position(0, 8)
    assert un_damier.deplacer(position_1, position_2) == "erreur"

    # Si la position cible est déjà occupée
    position_1 = Position(2, 1)
    position_2 = Position(5, 4)
    assert un_damier.deplacer(position_1, position_2) == "erreur"

    # Si le déplacement est une prise
    position_1 = Position(2, 1)
    position_2 = Position(4, 3)
    assert not un_damier.deplacer(position_1, position_2) == "prise"


    #Si le déplacement est  sans prise
    position_1 = Position(2, 1)
    position_2 = Position(3, 2)
    assert un_damier.deplacer(position_1, position_2) == "ok"

    #tests unitaires recuperer_piece_a_position
    position_1 = Position(2, 1)
    assert un_damier.recuperer_piece_a_position(position_1) == None

    position_1 = Position(0, 1)
    assert un_damier.recuperer_piece_a_position(position_1) == Piece("noir", "pion")

    assert un_damier.recuperer_piece_a_position(Position(7, 0)) == Piece("blanc", "pion")

    #tests unitaires determiner_position_enemie
    position_1 = Position(2, 1)
    position_2 = Position(4, 3)
    assert un_damier.determiner_position_enemie(position_1, position_2) == Position(3, 2)

    position_1 = Position(2, 1)
    position_2 = Position(5, 4)
    assert un_damier.determiner_position_enemie(position_1, position_2) == Position(3, 2)



    print('Test unitaires passés avec succès !')



    # NOTEZ BIEN: Pour vous aider lors du développement, affichez le damier!
    print(un_damier)

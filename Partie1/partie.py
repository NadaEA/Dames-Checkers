# Auteurs: À compléter

from Partie1.damier import Damier
from Partie1.position import Position
from Partie1.piece import Piece


class Partie:
    """Gestionnaire de partie de dames.

    Attributes:
        damier (Damier): Le damier de la partie, contenant notamment les pièces.
        couleur_joueur_courant (str): Le joueur à qui c'est le tour de jouer.
        doit_prendre (bool): Un booléen représentant si le joueur actif doit absolument effectuer une prise
            de pièce. Sera utile pour valider les mouvements et pour gérer les prises multiples.
        position_source_selectionnee (Position): La position source qui a été sélectionnée. Utile pour sauvegarder
            cette information avant de poursuivre. Contient None si aucune pièce n'est sélectionnée.
        position_source_forcee (Position): Une position avec laquelle le joueur actif doit absolument jouer. Le
            seul moment où cette position est utilisée est après une prise: si le joueur peut encore prendre
            d'autres pièces adverses, il doit absolument le faire. Ce membre contient None si aucune position n'est
            forcée.

    """
    def __init__(self):
        """Constructeur de la classe Partie. Initialise les attributs à leur valeur par défaut. Le damier est construit
        avec les pièces à leur valeur initiales, le joueur actif est le joueur blanc, et celui-ci n'est pas forcé
        de prendre une pièce adverse. Aucune position source n'est sélectionnée, et aucune position source n'est forcée.

        """
        self.damier = Damier()
        self.couleur_joueur_courant = "blanc"
        self.doit_prendre = False
        self.position_source_selectionnee = None
        self.position_source_forcee = None

    def position_source_valide(self, position_source):
        """Vérifie la validité de la position source, notamment:
            - Est-ce que la position contient une pièce?
            - Est-ce que cette pièce est de la couleur du joueur actif?
            - Si le joueur doit absolument continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
              bonne pièce?

        Cette méthode retourne deux valeurs. La première valeur est Booléenne (True ou False), et la seconde valeur est
        un message d'erreur indiquant la raison pourquoi la position n'est pas valide (ou une chaîne vide s'il n'y a pas
        d'erreur).

        ATTENTION: Utilisez les attributs de la classe pour connaître les informations sur le jeu! (le damier, le joueur
            actif, si une position source est forcée, etc.

        ATTENTION: Vous avez accès ici à un attribut de type Damier. vous avez accès à plusieurs méthodes pratiques
            dans le damier qui vous simplifieront la tâche ici :)

        Args:
            position_source (Position): La position source à valider.

        Returns:
            bool, str: Un couple où le premier élément représente la validité de la position (True ou False), et le
                 deuxième élément est un message d'erreur (ou une chaîne vide s'il n'y a pas d'erreur).

        """
        # On vérifie que la position contient une pièce, et on stocke dans i l'index du dictionnaire si elle y est
        message_erreur = ""
        i = 0
        validite = True
        # for keys in Damier.cases:
        # On doit utiliser l'objet de la classe Damier qu'on instantie à l'intérieur de la classe Partie, sinon si tu essaie d'accéder à la classe Damier
        # à travers le nom de la classe et pas un objet de la classe damier, tu reçois une erreur comme quoi les attributs sont pas trouvables (parce qu'ils
        # ont pas été crées parce qu'on a pas d'instance de damier dans ce cas là
        for keys in self.damier.cases:
            if position_source == keys:
                validite = True
                message_erreur = ""
                break
            else:
                validite = False
                i += 1
                message_erreur = "La position ne contient aucune pièce!"

        if i == 24 and validite == False:
            return validite, "La position ne contient aucune pièce!"

        # On compare la couleur du joueur courant avec la couleur de la pièce pour déterminer la validité
        if self.damier.cases[position_source].couleur != self.couleur_joueur_courant:
            validite = False
            message_erreur = "Cette pièce ne t'appartient pas!"
            return validite, message_erreur

        # On vérifie que si le joueur est obligé de jouer une pièce, qu'il a sélectionné la bonne pièce
        if self.doit_prendre:
            if not self.damier.piece_peut_faire_une_prise(position_source):
                validite = False
                message_erreur = "Une autre pièce peut faire une prise, fais attention!"
                return validite, message_erreur

        return validite, message_erreur


        #TODO: À compléter

    def position_cible_valide(self, position_cible):
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).

        """

        # Il y a deux possibilités généralement: un déplacement sans prise ou un déplacement avec prise (un saut)
        # On vérifie d'abord que la contrainte de prise obligatoire est respectée (vérifie les sauts)
        # Ensuite si ce n'est pas un saut, on regarde si le déplacement est valide
        if self.damier.piece_peut_faire_une_prise(
                self.position_source_selectionnee):  # Est-ce que la pièce peut faire une prise?
            if self.damier.piece_peut_sauter_vers(self.position_source_selectionnee,
                                                  position_cible):  # La pièce peut faire une prise, est-ce que la position cible est une prise possible?
                return True, "La position cible est valide et c'est une prise"
            else:
                return False, "La pièce doit prendre une pièce mais la position cible n'est pas valide"
        elif self.damier.piece_peut_se_deplacer_vers(self.position_source_selectionnee,
                                                     position_cible):  # La pièce ne peut pas faire une prise, elle peut se déplacer?
            return True, "Le déplacement est valide"
        else:  # La pièce ne peut ni faire une prise, ni se déplacer vers la position cible
            return False, "La pièce ne peut pas se déplacer"

    def demander_positions_deplacement(self):
        """Demande à l'utilisateur les positions sources et cible, et valide ces positions. Cette méthode doit demander
        les positions à l'utilisateur tant que celles-ci sont invalides.Qu

        Cette méthode ne doit jamais planter, peu importe ce que l'utilisateur entre.

        Returns:
            Position, Position: Un couple de deux positions (source et cible).

        """

        def ligne_valide():
            error = False
            while error == False:
                try:
                    ligne_source = int(input("Entrez la ligne: "))
                    error = True
                except ValueError:
                    print("Entrez une valeur numérique entre 0 et 7 s'il vous plaît")
                    error = False
            return ligne_source


        def colonne_valide():
            error = False
            while error == False:
                try:
                    colonne_source = int(input("Entrez la colonne: "))
                    error = True
                except ValueError:
                    print("Entrez une valeur numérique entre 0 et 7 s'il vous plaît")
                    error = False
            return colonne_source

        # On demande la position source

        ligne_source = ligne_valide()
        colonne_source = colonne_valide()
        position_source = Position(ligne_source, colonne_source)
        self.position_source_selectionnee = position_source
        position_source_valide = self.position_source_valide(position_source)
        print(self.position_source_valide(position_source)[1])
        while not position_source_valide[0]:
            ligne_source = ligne_valide()
            colonne_source = colonne_valide()
            position_source = Position(ligne_source, colonne_source)
            self.position_source_selectionnee = position_source
            position_source_valide = self.position_source_valide(position_source)
            print(self.position_source_valide(position_source)[1])

        # On demande la position cible

        ligne_cible = ligne_valide()
        colonne_cible = colonne_valide()
        position_cible = Position(ligne_cible, colonne_cible)
        position_cible_valide = self.position_cible_valide(position_cible)
        print(self.position_cible_valide(position_cible)[1])
        while not position_cible_valide[0]:
            ligne_cible = ligne_valide()
            colonne_cible = colonne_valide()
            position_cible = Position(ligne_cible, colonne_cible)
            position_cible_valide = self.position_cible_valide(position_cible)
            print(self.position_cible_valide(position_cible)[1])

        #On retourne les deux positions
        return position_source, position_cible

    def tour(self):
        """Cette méthode effectue le tour d'un joueur, et doit effectuer les actions suivantes:
        - Assigne self.doit_prendre à True si le joueur courant a la possibilité de prendre une pièce adverse.
        - Affiche l'état du jeu
        - Demander les positions source et cible (utilisez self.demander_positions_deplacement!)
        - Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        - Si une pièce a été prise lors du déplacement, c'est encore au tour du même joueur si celui-ci peut encore
          prendre une pièce adverse en continuant son mouvement. Utilisez les membres self.doit_prendre et
          self.position_source_forcee pour forcer ce prochain tour!
        - Si aucune pièce n'a été prise ou qu'aucun coup supplémentaire peut être fait avec la même pièce, c'est le
          tour du joueur adverse. Mettez à jour les attributs de la classe en conséquence.

        """

        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.doit_prendre = True

        # Affiche l'état du jeu
        print(self.damier)
        print("")
        print("Tour du joueur", self.couleur_joueur_courant, end=".")
        if self.doit_prendre:
            if self.position_source_forcee is None:
                print(" Doit prendre une pièce.")
            else:
                print(" Doit prendre avec la pièce en position {}.".format(self.position_source_forcee))
        else:
            print("")

        # Demander les positions


        positions = self.demander_positions_deplacement()
        position_source = positions[0]
        position_cible = positions[1]



        # Effectuer le déplacement (à l'aide de la méthode du damier appropriée)

        self.damier.deplacer(position_source, position_cible)
        self.damier.deplacer(self.position_source_forcee, position_cible)



        # Mettre à jour les attributs de la classe

        if self.couleur_joueur_courant == "blanc":
            self.couleur_joueur_courant = "noir"
        else:
            self.couleur_joueur_courant = "blanc"

        # TODO: À compléter

    def jouer(self):
        """Démarre une partie. Tant que le joueur courant a des déplacements possibles (utilisez les méthodes
        appriopriées!), un nouveau tour est joué.

        Returns:
            str: La couleur du joueur gagnant.
        """

        while self.damier.piece_de_couleur_peut_se_deplacer(self.couleur_joueur_courant) or \
                self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.tour()

        if self.couleur_joueur_courant == "blanc":
            return "noir"
        else:
            return "blanc"


if __name__ == "__main__":
    une_partie = Partie()
    le_damier = une_partie.damier
    print(le_damier)

    # Tests unitaires
    position = Position(1, 0)
    assert une_partie.position_source_valide(position) == (False, "Cette pièce ne t'appartient pas!")

    position_2 = Position(0, 2)
    assert une_partie.position_source_valide(position_2) == (False, "La position ne contient aucune pièce!")
    une_partie.position_source_selectionnee = Position(1, 0)

    #Pour des tests
    # le_damier.deplacer(Position(5,0), Position(4,1))
    # print(le_damier)
    # le_damier.deplacer(Position(4, 1), Position(3, 2))
    # print(le_damier)
    # positions = une_partie.demander_positions_deplacement()   # Input 5, 0, 4, 1
    # assert positions == (Position(5,0), Position(4,1))

    print("Tests réussis!")

    une_partie.jouer()

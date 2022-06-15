import argparse
import os

# stocke l'alphabet dans une variable pour l'itérer plus tard
alphabetMin = "abcdefghijklmnopqrstuvwxyz"
alphabetMaj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# méthode pour créer les arguments pour le cmd
def creation_arguments():
    # gère le texte sur le cmd
    parser = argparse.ArgumentParser(
        description="Programme de chiffrage Vigenère")

    # ajoute des "arguments" qui seront les éléments demandés à l'utilisateur
    # si l'utilisateur oublie de donner un argument le script le lui demandera
    # (c'est pour ça qu'aucun argument n'est obligatoire)
    parser.add_argument('-fe', '--fichierEntree',  # nom de l'argument
                        type=str,  # type de l'argument
                        # description donnée quand l'utilisateur fait -h
                        help="Fichier dans lequel se trouve le message à chiffrer ou à déchiffrer",
                        metavar="")

    parser.add_argument('-c', '--clef',  # nom de l'argument
                        type=str,  # type de l'argument
                        help="Clef de chiffrage",  # description donnée quand l'utilisateur fait -h
                        metavar="")

    parser.add_argument('-fs', '--fichierSortie',  # nom de l'argument
                        type=str,  # type de l'argument
                        # description donnée quand l'utilisateur fait -h
                        help="Fichier dans lequel se trouvera le résultat (crée le fichier s'il n'existe pas)",
                        metavar="")

    # crée un groupe d'arguments (dans ce cas des bools) où seulement un seul des arguments peut être appelé
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-ch', '--chiffrement',  # nom de l'argument
                       action='store_true',  # si cet argument est appelé il devient vrai
                       help="Permet de specifier l'action de chiffrement")  # description donnée quand l'utilisateur
    # fait -h

    group.add_argument('-de', '--dechiffrement',  # nom de l'argument
                       action='store_true',  # si cet argument est appelé il devient vrai
                       help="Permet de spécifier l'action de déchiffrement")  # description donnée quand l'utilisateur
    # fait -h

    # assigne tous les arguments à une variable
    args = parser.parse_args()
    return args


# cette variable est utilisée dans les autres méthodes pour appeler les arguments du cmd
arguments = creation_arguments()


# vérifie que le fichier existe dans le directory du script, renvoie un bool
def fichier_existe_il(fichier):
    # vérifie si le lien du fichier mène à quelque chose
    if os.path.exists(fichier):

        # si c'est le cas renvoie vraie et la méthode s'arrête
        return True

    # si le lien du fichier ne mène à rien
    elif not os.path.exists(fichier):

        # renvoie un faux
        return False


# vérifie si le text contient un caractère spécial, renvoi un bool
def text_contient_il_caractere_special(text):
    for caractere in text:

        # ord() transforme le char en sa valeur ascii
        valeur_ascii_lettre = ord(caractere)

        # regarde si la valeur ascii est comprise dans les caractères non acceptés
        if 90 < valeur_ascii_lettre < 97:

            # si c'est le cas prévient l'utilisateur et renvoi un True
            print(f"{caractere} est un caractère invalide")
            return True

        # si le caractère n'est pas une lettre
        elif valeur_ascii_lettre < 65 or valeur_ascii_lettre > 122:

            # si c'est le cas prévient l'utilisateur et renvoi un True
            print(f"{caractere} est un caractère invalide")
            return True

    # si aucun caractère n'est spécial
    return False


# vérifie si l'utilisateur a oublié de donner un argument, si c'est le cas lui demande d'en rentrer un
def verifier_si_argument_est_null(argument, nom_argument):
    # si l'argument est null ça veut dire qu'il n'a pas été rentré
    if argument is None:

        # demande l'argument à l'utilisateur
        argument = str(input(f"Veuillez écrire {nom_argument} : "))

        # renvoi l'argument
        return argument

    # si l'argument n'est pas null ça veut dire qu'il a été rentré
    elif argument is not None:

        # renvoi l'argument
        return argument


# trouve l'index de l'objet dans la liste
def trouve_index(objet, liste):
    index = 0

    while index < len(liste):

        if liste[index] == objet:
            return index

        index += 1


# trouve si la lettre est une majuscule, une minuscule ou pas une lettre
def majuscule_minuscule_ou_autre(lettre):
    # pour savoir si une lettre est une majuscule ou minuscule on regarde sa valeur ascii
    # ord() transform le char en sa valeur ascii
    ascii_lettre = ord(lettre)

    if 65 <= ascii_lettre <= 90:
        genre = "Majuscule"
        return genre
    elif 97 <= ascii_lettre <= 122:
        genre = "Minuscule"
        return genre
    else:
        genre = "Autre"
        return genre


# méthode pour obtenir le message contenu dans le fichier d'entrée
def creation_message():
    # vérifie si l'utilisateur a rentré un fichier d'entrée
    # si oui l'assigne à la variable
    # si non lui demande un fichier d'entrée et l'assigne à la variable
    fichier_entree = verifier_si_argument_est_null(
        arguments.fichierEntree, "le fichier d'entrée")

    # vérifie si le fichier donné par l'utilisateur existe
    fichier_entree_existe = fichier_existe_il(fichier_entree)

    # si le fichier n'existe pas
    if not fichier_entree_existe:

        # tant que le fichier n'existe pas, redemande un nouveau fichier à l'utilisateur
        while not fichier_entree_existe:
            # précise le problème à l'utilisateur
            print(
                f"{fichier_entree} n'existe pas (Avez-vous précisé l'extension ? / Êtes-vous sûr que le fichier "
                f"existe dans ce dossier ?) ")

            fichier_entree = str(input("Écrivez le nom du fichier d'entrée : "))

            fichier_entree_existe = fichier_existe_il(fichier_entree)

    # copie le contenu du fichier d'entrée dans une variable
    text = ""
    f = open(fichier_entree, "r")
    for x in f:
        text += x
    f.close()

    return text


# méthode pour créer et vérifier la clef
def creation_clef():
    # vérifie si l'utilisateur a rentré une clef
    # si oui l'assigne à la variable
    # si non lui demande une clef et l'assigne à la variable
    clef = verifier_si_argument_est_null(arguments.clef, "la clé de chiffrement")

    # vérifie si la clé contient un caractère non autorisé
    text_contient_car_spec = text_contient_il_caractere_special(clef)

    # tant qu'il contient un caractère non autorisé, demande à l'utilisateur de rentrer une nouvelle clef
    while text_contient_car_spec:
        clef = str(input("Écrivez la clef de chiffrement : "))
        text_contient_car_spec = text_contient_il_caractere_special(clef)

    return clef


# méthode pour créer et vérifier le fichier de sortie
def creation_fichier_sortie():
    # vérifie si l'utilisateur a rentré un fichier de sortie
    # si oui l'assigne à la variable
    # si non lui demande un fichier de sortie et l'assigne à la variable
    fichier_sortie = verifier_si_argument_est_null(
        arguments.fichierSortie, "le fichier de sortie")

    # vérifie si le fichier de sortie existe déjà
    fichier_sortie_existe = fichier_existe_il(fichier_sortie)

    # s'il existe, prévient l'utilisateur qu'il serait écrasé
    while fichier_sortie_existe:

        print(f"{fichier_sortie} existe déjà et serait écrasé")

        # demande ensuite à l'utilisateur s'il est sûr
        confirmation = str(
            input("Êtes-vous sûr de vouloir le supprimer ? [oui | non] :"))

        # si il est sûr supprime le fichier
        if confirmation == "oui" \
                or confirmation == "Oui" \
                or confirmation == "" \
                or confirmation == "OUI" \
                or confirmation == "o" \
                or confirmation == "O":

            os.remove(fichier_sortie)

        # autrement demande un nouveau fichier de sortie
        else:
            fichier_sortie = str(
                input("Écrivez le nouveau nom du fichier de sortie : "))

        # vérifie si le nouveau fichier de sortie n'existe pas déjà
        # si oui reboucle
        fichier_sortie_existe = fichier_existe_il(fichier_sortie)

    return fichier_sortie


# méthode pour créer et vérifier si l'utilisateur veut chiffrer ou déchiffrer
def chiffrement_ou_dechiffrement():
    # contrairement aux autres arguments chiffrement et dechiffrement ont une valeur par défaut de False de plus
    # seulement un seul des deux arguments peut être appelés ainsi pour savoir si l'utilisateur n'a rentré aucun
    # argument nous devons regarder si chiffrement et dechiffrement sont False
    if not arguments.chiffrement and not arguments.dechiffrement:

        # si c'est le cas on demande à l'utilisateur s'il souhaite chiffrer ou déchiffrer
        type_operation = str(input("Voulez-vous chiffrer ou déchiffrer ? : "))

        # si l'utilisateur a rentré un message qui n'est pas "chiffrer" ou "déchiffrer"
        # on va lui redemander jusqu'a ce qu'il rentre une valeur valide
        while type_operation != "chiffrer" and type_operation != "déchiffrer":
            type_operation = str(
                input("Voulez-vous chiffrer ou dechiffrer ? : "))

        # enfin dépendant de sa réponse on change les valeurs des arguments
        if type_operation == "chiffrer":

            # l'utilisateur veut chiffrer
            arguments.chiffrement = True

        elif type_operation == "déchiffrer":

            # l'utilisateur veut déchiffrer
            arguments.dechiffrement = True


# chiffre
def chiffrement(message, clef, fichier_sortie):
    # pour "additionner" 2 lettres, il faut les transformer en valeur numérique d'une façon ou d'une autre.

    index_message = 0
    index_clef = 0
    message_chiffre = ""

    # parcourt toutes les lettres du message
    while index_message < len(message):

        # assigne la lettre du message selectionnée à une variable
        lettre_message = message[index_message]
        # assigne la lettre de la clef selectionnée à une variable
        lettre_clef = clef[index_clef]

        # regarde si la lettre actuelle est une majuscule, une minuscule ou un caractère spécial
        genre_lettre_message = majuscule_minuscule_ou_autre(lettre_message)
        # regarde si la lettre actuelle est une majuscule, une minuscule ou un caractère spécial
        genre_lettre_clef = majuscule_minuscule_ou_autre(lettre_clef)

        if genre_lettre_message == "Majuscule" and genre_lettre_clef == "Majuscule":

            # TrouveIndex trouve l'index de l'objet dans la liste
            # % 26 pour retourner au début de l'alphabet si on dépasse
            index_alphabetic = (trouve_index(
                lettre_message, alphabetMaj) + trouve_index(lettre_clef, alphabetMaj)) % 26

            # on ajoute maintenant la lettre de l'alphabet au message chiffré
            message_chiffre += alphabetMaj[index_alphabetic]

        elif genre_lettre_message == "Minuscule" and genre_lettre_clef == "Minuscule":

            # TrouveIndex trouve l'index de l'objet dans la liste
            # % 26 pour retourner au début de l'alphabet si on dépasse
            index_alphabetic = (trouve_index(
                lettre_message, alphabetMin) + trouve_index(lettre_clef, alphabetMin)) % 26

            # on ajoute maintenant la lettre de l'alphabet au message chiffré
            message_chiffre += alphabetMin[index_alphabetic]

        # si la lettre_message est majuscule et la lettre_clef est minuscule
        elif genre_lettre_message == "Majuscule" and genre_lettre_clef == "Minuscule":

            # TrouveIndex trouve l'index de l'objet dans la liste
            # % 26 pour retourner au début de l'alphabet si on dépasse
            index_alphabetic = (trouve_index(
                lettre_message, alphabetMaj) + trouve_index(lettre_clef, alphabetMin)) % 26

            # on ajoute maintenant la lettre de l'alphabet au message chiffré
            message_chiffre += alphabetMaj[index_alphabetic]

        # si la lettre_message est minuscule et la lettre_clef est majuscule
        elif genre_lettre_message == "Minuscule" and genre_lettre_clef == "Majuscule":

            # TrouveIndex trouve l'index de l'objet dans la liste
            # % 26 pour retourner au début de l'alphabet si on dépasse
            index_alphabetic = (trouve_index(
                lettre_message, alphabetMin) + trouve_index(lettre_clef, alphabetMaj)) % 26

            # on ajoute maintenant la lettre de l'alphabet au message chiffré
            message_chiffre += alphabetMin[index_alphabetic]

        # si la lettre est un caractère spécial celle-ci sera gardée dans le message codé
        elif genre_lettre_message == "Autre":
            message_chiffre += lettre_message

        index_message += 1
        index_clef += 1

        # si on atteint le bout de la clef avant d'avoir fini le message, on retourne au début de la clef
        if index_clef == len(clef):
            index_clef = 0

    # écrit le message chiffré dans le fichier de sortie
    f = open(fichier_sortie, "w")
    f.write(message_chiffre)
    f.close()

    print(f"Message chiffré avec succès dans {fichier_sortie}")


# déchiffre
def dechiffrement(message, clef, fichier_sortie):
    # pour déchiffrer il suffit de faire la même opération que pour le chiffrage, mais en faisant la différence des
    # indexés et non pas leur somme
    index_message_chiffre = 0
    index_clef = 0
    message_chiffre = message
    message_dechiffre = ""

    while index_message_chiffre < len(message_chiffre):

        # assigne la lettre du message chiffré selectionné à une variable
        lettre_message_chiffre = message_chiffre[index_message_chiffre]
        # assigne la lettre de la clef selectionnée à une variable
        lettre_clef = clef[index_clef]

        # assigne la lettre du message selectionnée à une variable
        genre_lettre_message_chiffre = majuscule_minuscule_ou_autre(lettre_message_chiffre)
        # assigne la lettre du message selectionnée à une variable
        genre_lettre_clef = majuscule_minuscule_ou_autre(lettre_clef)

        if genre_lettre_message_chiffre == "Majuscule" and genre_lettre_clef == "Majuscule":  # 2 maj

            # même chose que le chiffrage, mais fais une soustraction
            index_alphabetic = trouve_index(
                lettre_message_chiffre, alphabetMaj) - trouve_index(lettre_clef, alphabetMaj)

            # si on dépasse le début du tableau (la lettre "a" qui a un index de 0)
            if index_alphabetic < 0:
                # on ajoute 26 ce qui nous donnera le bon résultat
                # ex : index de "d" est 3, index de e est 4, 3-4 = -1  ainsi -1 + 26 = 25 = z
                index_alphabetic += 26

            message_dechiffre += alphabetMaj[index_alphabetic]

        # si les deux lettres sont minuscules
        elif genre_lettre_message_chiffre == "Minuscule" and genre_lettre_clef == "Minuscule":

            # même chose que le chiffrage, mais fait une soustraction
            index_alphabetic = trouve_index(
                lettre_message_chiffre, alphabetMin) - trouve_index(lettre_clef, alphabetMin)
            # si on dépasse le début du tableau (la lettre "a" qui a un index de 0)

            if index_alphabetic < 0:
                # on ajoute 26 ce qui nous donnera le bon résultat
                # ex : index de "d" est 3, index de e est 4, 3-4 = -1  ainsi -1 + 26 = 25 = z
                index_alphabetic += 26

            message_dechiffre += alphabetMin[index_alphabetic]

        # si lettre message est maj et lettre clef est min
        elif genre_lettre_message_chiffre == "Majuscule" and genre_lettre_clef == "Minuscule":

            # même chose que le chiffrage, mais fais une soustraction
            index_alphabetic = trouve_index(
                lettre_message_chiffre, alphabetMaj) - trouve_index(lettre_clef, alphabetMin)

            # si on dépasse le début du tableau (la lettre "a" qui a un index de 0)
            if index_alphabetic < 0:
                # on ajoute 26 ce qui nous donnera le bon résultat
                # ex : index de "d" est 3, index de e est 4, 3-4 = -1  ainsi -1 + 26 = 25 = z
                index_alphabetic += 26

            message_dechiffre += alphabetMaj[index_alphabetic]

        # si lettre message est min et lettre clef est maj
        elif genre_lettre_message_chiffre == "Minuscule" and genre_lettre_clef == "Majuscule":

            # même chose que le chiffrage, mais fais une soustraction
            index_alphabetic = trouve_index(
                lettre_message_chiffre, alphabetMin) - trouve_index(lettre_clef, alphabetMin)

            # si on dépasse le début du tableau (la lettre "a" qui a un index de 0)
            if index_alphabetic < 0:
                # on ajoute 26 ce qui nous donnera le bon résultat
                # ex : index de "d" est 3, index de e est 4, 3-4 = -1  ainsi -1 + 26 = 25 = z
                index_alphabetic += 26

            message_dechiffre += alphabetMin[index_alphabetic]

        # si la lettre est un caractère spécial celle-ci sera gardée dans le message codé
        elif genre_lettre_message_chiffre == "Autre":
            message_dechiffre += lettre_message_chiffre

        index_message_chiffre += 1
        index_clef += 1

        # si on atteint le bout de la clef avant d'avoir fini le message, on retourne au début de la clef
        if index_clef == len(clef):
            index_clef = 0

    # écrit le message chiffré dans le fichier de sortie
    f = open(fichier_sortie, "w")
    f.write(message_dechiffre)
    f.close()

    print(f"Message déchiffré avec succès dans {fichier_sortie}")


message = creation_message()
clef = creation_clef()
fichierSortie = creation_fichier_sortie()
chiffrement_ou_dechiffrement()

if arguments.chiffrement:
    chiffrement(message, clef, fichierSortie)
elif arguments.dechiffrement:
    dechiffrement(message, clef, fichierSortie)

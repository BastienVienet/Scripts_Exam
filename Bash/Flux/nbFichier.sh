#! /bin/bash

#On demande à l'utilisateur de saisir le nom du fichier à lire avec la commande Read
echo "Quel fichier aimerais-tu analyser ? : "
read file
#echo $blabla
#cat $blabla
wc < $file > fichierStat.txt



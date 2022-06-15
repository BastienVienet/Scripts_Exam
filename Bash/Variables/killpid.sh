#! /bin/bash
#Exercice pour kill un processus
# on affiche les processus en cours d'exécution
ps -aux
echo "Merci d'indiquer le pid a kill : "
read pid

# supprime le processus par son numéro PID
kill $pid



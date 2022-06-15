#! /bin/bash

echo Nom du fichier à analyser :
read fileName
wc $fileName > statFichier.txt
echo Le fichier à analyser a été mis dans 'statFichier.txt'

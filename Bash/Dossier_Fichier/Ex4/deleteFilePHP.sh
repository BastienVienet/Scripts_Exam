#! /bin/bash

#Parcourt tous les dossiers dans le dossier ou on se trouve
for directory in */ ; do
	#Rentre dans le dossier
	cd "$directory"
	#Boucle dans les éléments du dossier
	for file in *; do
		if [ -f $file ]
		then
			rm $file
			echo "Supression du fichier $file"
		fi
	done
	#Sortir du dossier pour rentrer dans le prochain lors de la prochaine ittération de boucle
	cd ..
done
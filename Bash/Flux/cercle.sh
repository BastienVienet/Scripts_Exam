#! /bin/bash

pi=$(echo "scale=3; 4*a(1)" | bc -l)

echo "Saisie d'un diamètre pour votre cercle : "
read diametre

perim=$(echo $pi*$diametre | bc)
aire=$(echo $diametre^2*$pi/4 | bc)
echo "Le perimètre de votre cercle fait : $perim cm"
echo "L'air du cercle fait $aire cm2"

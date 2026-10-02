---
output: beast-fr.html
title: La Bête &middot; Du ghee fait par une IA
description: Une perceuse sans fil, une planche à découper, une plaque chauffante et un Raspberry Pi. Ce que fait chaque pièce de la machine à ghee.
og_title: La Bête
og_description: Une perceuse sans fil, une planche à découper et un Raspberry Pi. Ce que fait chaque pièce de la machine à ghee.
og_image: images/beast.jpg
og_url: https://mindtensorml.github.io/ai-ghee/beast-fr.html
skip_text: Aller au contenu
lang: fr
stem: beast
locale: fr_FR
mark: La machine
nav_text: L'histoire
nav_href: index-fr.html
nav_side: left
kicker: La construction
headline: La Bête
standfirst: Tout ce qui est sur cet engin vient d'un magasin de bricolage ou d'un tiroir de cuisine. Voici ce que fait vraiment chaque pièce.
next_text: Retour à l'histoire
next_href: index-fr.html
next_blurb: Le yaourt, la baratte, la cassure, et une heure à regarder la couleur.
credit: Les photos viennent toutes d'une même session, en août 2026. La baratte, les pots finis et la deuxième fournée ont été photographiés plus tard.
contact_text: Des questions, des corrections, ou vous en avez construit un vous aussi.
---

## De quoi c'est fait

C'est une perceuse sans fil qui fait tourner. Elle est tenue par un serre-joint boulonné sur une planche à découper, et c'est la planche qui garde tout bien aligné au-dessus de la casserole. La tête de baratte, c'est du bois dur sur un axe en acier, vissé plutôt que collé, et c'est justement pour ça que je l'ai faite au lieu de l'acheter.

L'électronique habite dans une boîte alimentaire en plastique transparent, surtout pour que je puisse voir si quelque chose a pris feu. Un Raspberry Pi s'occupe des relevés. Le gros bouton jaune coupe l'alimentation du moteur, et aucun logiciel n'a le droit de passer outre.

![Perceuse, planche, boîte, bouton](images/beast-wide.jpg "Le montage sur un plan de travail de cuisine, avec la perceuse dans son serre-joint, la planche en bois, la boîte transparente d'électronique et un Raspberry Pi à la base.")

| Moteur | Perceuse sans fil, serrée dans un serre-joint, tournant bien en dessous de sa vitesse maximale |
| Baratte | Bois dur et inox, faite et non achetée |
| Chaleur | Plaque chauffante, allumée et coupée par un régulateur secteur |
| Châssis | Une planche à découper et une boîte alimentaire en plastique |
| Alimentation | Bloc à découpage 12 V, branché sur le secteur |
| Cerveau | Raspberry Pi, qui écrit dans un CSV |
| Sens | Courant et tension pendant le barattage, une sonde dans la casserole pendant la cuisson |
| Arrêt | Un gros bouton, câblé en dur |

## Comment c'est câblé

Quatre fils de signal et une grosse boucle. Le Pi calcule la force et le sens, le pont en H est ce qui pousse vraiment le courant, et les deux ne se rencontrent jamais. Rien de ce que touche le Pi ne transporte plus de quelques milliampères.

Le bouton est la partie qui vaut le coup d'œil. Il n'est pas relié au Pi du tout. Il est dans la boucle du moteur et il la coupe, donc aucun bug logiciel ne peut le convaincre de ne pas s'arrêter. Ce que le Pi peut faire, c'est s'en apercevoir. S'il demande trente pour cent et que le capteur lui renvoie moins de deux cents milliampères, il en déduit que la boucle est ouverte et il arrête de demander.

Le capteur est sur la même boucle, mais sa partie logique est alimentée par le Pi, et c'est pour ça qu'il répond encore quand l'alimentation est coupée. Toute l'astuce du test du bouton tient là.

![Schéma électrique](images/schematic-fr.svg "Un schéma électrique de la machine à ghee. Un Raspberry Pi pilote un pont en H BTS7960 par quatre fils de signal et lit un capteur de courant INA260 en I2C. Une alimentation douze volts, un fusible de quinze ampères, le bouton d'arrêt d'urgence et le capteur sont en série dans la boucle du moteur, que le Pi ne touche jamais.")

## Où ça s'installe

Au-dessus de l'évier. La casserole va dans la cuve, un couvercle plat se pose dessus avec un trou découpé pour l'axe, et tout ce qui s'échappe tombe à un endroit où ça n'a pas d'importance.

C'est la partie que personne ne met dans le rendu 3D. Construire quelque chose dans une cuisine, c'est pour moitié décider où les saletés ont le droit d'aller.

![En place, en pleine fournée](images/rig-sink.jpg "Le montage serré en place au-dessus de l'évier de cuisine, avec un ordinateur portable en dessous affichant des courbes en direct.")

## Ce qu'elle surveille

Pendant le barattage, le courant et la tension sur la ligne du moteur, relevés environ une fois par seconde et écrits directement dans un fichier. Pendant la cuisson, une sonde dans la casserole à la place, et le régulateur allume et coupe la plaque pour tenir le nombre.

Pas de micro et pas de caméra, et c'est la prochaine chose que je veux corriger. Le pari jusqu'ici, c'était que si la charge toute seule suffit à trouver la cassure, le reste peut attendre.

![La trace en direct pendant une fournée](images/laptop.jpg "L'écran d'un ordinateur portable affichant deux courbes en direct des relevés du moteur, au-dessus d'un terminal où défilent les logs.")

## Ce qu'elle décide

Deux choses. Si la charge est montée puis redescendue assez pour annoncer la cassure, et si la plaque doit être allumée ou coupée pour rester à 250 F.

Elle ne sait pas ce qu'est le yaourt. Elle ne sait pas ce qu'est le beurre. Elle sait qu'un nombre est monté un moment puis est retombé, et que cette forme veut dire que le travail est fini.

![À quoi sert cette forme](images/batch-big.jpg "Deux grands bocaux de ghee figé et pâle, couvercles vissés et étiquettes transparentes, posés sur une rambarde, avec des bocaux à clip plus petits et flous derrière.")

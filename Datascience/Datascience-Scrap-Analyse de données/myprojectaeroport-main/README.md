# AeroProject
Maxime Bouet et Paul Monsigny  



![This is an image](https://www.usinenouvelle.com/mediatheque/4/3/0/000271034_image_260x175.jpg)




## OUR MISSION

Notre projet porte sur les aéroports les plus visités au monde face au Covid-19, l'objectif de ce projet est de générer des graphiques nous permettant de voir quels sont les  aéroports accueillant le plus de passagers chaque année et de voir comment ces derniers sont répartis.  
Nous avons imaginé et créé plusieurs graphiques :
 - Une carte interactive avec environ 7000 aéroports dans le monde.  
 - Une seconde avec seulement les 50 plus grands du monde.  
 - Un graphique en bâton qui reprend les mêmes données.  
 - Un graphique camembert qui représente le nombre de voyageur par pays en 2021  
 - Une courbe afin de mesurer l'impact du covid sur les aéroports européens qui change en fonction de l’année sélectionnée en dessous.
Pour ce projet nous avons codé sur Visual studio et l'avons partager sur le gitlab de l’ESIEE.  
Les données ont été récupérées à l’aide de Scrapping en utilisant Beautifulsoup.  
Les données sont donc « scrappées » et stockées une première fois dans des Dataframes pour ensuite être transformées en fichier CSV (pour ne pas à avoir à compiler ce fichier à chaque fois).

## USER GUIDE
Veuillez d’abord vous assurez d’avoir le git d’installé sur votre machine.  
Ensuite, lancer un terminal et placez-vous dans le dossier désiré pour récupérer le projet avec la commande suivante :  
`git clone https://git.esiee.fr/bouetm/myprojectaeroport`  
Puis, vous pouvez installer tous les paquets requis pour le bon fonctionnement du programme avec la commande suivante :  
`python -m pip install -r requirements.txt`  
Enfin, si vous le désirez ou si les fichiers CSV ne sont pas présents dans le dossier « tab », vous pouvez compiler le fichier get_data.py avec la commande suivante :  
`python get_data.py`  
Pour finir, vous pouvez compiler le fichier principal main.py avec la commande suivante :  
`python main.py`  
En cliquant sur le liens affiché dans le terminal, vous aurez accès au Dashboard. Si le Dashboard ne s'affiche pas, veuillez exécuter la commande sur le terminal de Visual studio.  

## DEVELOPER GUIDE
Dans le dossier du projet, il y a trois fichiers python.  
Tout d’abord, pour récupérer les données, c’est get_data.py qui s’en occupe. Il y a 4 fonctions qui permettent de récupérer des données sur le web et les stocker dans des fichiers  CSV dans le répertoire « tab ». En dessous, il y a les liens utilisés et les appels aux fonctions.  
Le principal est main.py, tout ce qu’il fait, c’est générer trois Dataframes grâce aux fichiers CSV présents dans le répertoire « tab ».  
Le dernier est graph.py, il permet de générer le Dashboard. On créer donc plusieurs graphiques dans différents subplot pour ensuite organiser tout cela dans la partie HTML en   dessous.

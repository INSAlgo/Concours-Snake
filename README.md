# Tournoi de Snake d'INSAlgo

Bienvenue à la prestigieuse compétition de Snake d'INSAlgo ! 

Il s'agit d'un jeu **tour par tour** en 1 contre 1 dont le but est simple : faire en sorte que la tête du serpent adverse rencontre le corps du votre ou bien un mur.

Pour participer, il vous suffit de développer une petite IA capable jouer au jeu, dans le langage de votre choix.
À la fin, toutes les IA vont se rencontrer, et les meilleures remporteront des prix !

```plaintext
🟡🟡🟡🟡🟡🟡🟡🟡🔴🟡
🟡🟡🟡🟡🟡🟡🟡🟡🔴🟡
🟡🟡🟡🟡🟡🟡🟡🟡🔴🟡
🟡🟡🟡🟡🟡🟡🟡🟡🔴🟡
🟡🟡🟡🟡🟡🟡🔴🔴🔴🟡
🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡
🟡🔵🔵🔵🟡🟡🟡🟡🟡🟡
🟡🔵🟡🟡🟡🟡🟡🟡🟡🟡
🟡🔵🟡🟡🟡🟡🟡🟡🟡🟡
🟡🔵🔵🟡🟡🟡🟡🟡🟡🟡
```

# Programme

## Spécification

La communication avec votre programme est automatisée. Les entrées se présentent sous cette forme :

 Au début de la partie :
 - Sur une première ligne, 2 entiers séparés par un espace : `W` la largeur de la grille et `H` la hauteur de la grille.
 - Sur la deuxième ligne, un entier `M`, la vitesse de croissance des serpents: une case tout les `M` tours.
 - Sur la troisième ligne, 2 entiers séparés par un espace : `N` (2 <= `N` <= 4) le nombre de joueurs (pour le concours, on aura toujours `N` = 2, mais vous pouvez supporter des parties multijoueurs si ça vous amuse). Et `P` le tour auquel votre programme commence à jouer (1 <= `P` <= `N`).
 - Sur les `N` lignes suivantes, 2 entiers séparés par un espace : `X`<sub>`i`</sub> et `Y`<sub>`i`</sub> la position de départ du joueur `i`.

Votre programme doit ensuite supporter une boucle de jeu :

 - Lire le coup de votre adversaire : une chaine de charactères sous la forme `move P DIR` avec `P` le numéro du joueur et DIR la direction (parmi `up`, `down`, `left`, `right`) dans laquelle l'adversaire s'est déplacé d'une case.
 - Afficher son coup : la direction de déplacement (`up`, `down`, `left`, `right`).

 Si `P` = 1, votre programme doit jouer en premier, donc affiche son coup. Si `P` = 2, il doit d'abord lire le coup de l'adversaire.

Pour permettre le debug, les sorties commençant par `>` seront transmises à l'écran en étant ignorées par le jeu.

Un exemple d'IA très simple en Python est donné : [template.py](https://github.com/INSAlgo/Concours-Snake/blob/main/test-ai/template.py). Vous pouvez vous en servire de base pour votre IA.

## Tester un programme en local

Récupérez le script [snake.py](https://github.com/INSAlgo/Concours-Snake/blob/main/snake.py).
Ce script fournit un certain nombre d'outils pour tester et debugger votre programme :

`python snake.py [OPTIONS] [prog1, prog2, ..., progN]`

Exemples :
- partie entre deux joueurs, sans IA : `python snake.py`
- partie contre votre IA : `python snake.py prog1`
- partie entre 2 IA : `python snake.py prog1 prog2`
- partie de l'IA contre elle-même : `python snake.py prog1 prog1`

Les options sont :
  - `-s` : mode silencieux
  - `-g W H` (par défaut `W` = 10, `H` = 10) : la taille de la grille
  - `-p N` (par défaut, `N` = 2) : nombre de joueurs
  - `-G M` (par défaut, `M` = 5) : les serpents grandissent d'une case tous les M tours

Un exemple plus compliqué : partie à 4 joueurs dont 2 IA et 2 humains sur une grille 20x20 :

`python snake.py -g 20 20 -p 4 prog1 prog2`

Les programmes acceptés sont :
 - les scripts Python `.py`
 - les scripts JavaScript `.js`
 - les classes java compilées `.class`
 - Les exécutables compilés (C++, ...)

# Le concours

## Déroulement du concours

Pour être tenu au courant du déroulement du concours, venez sur le [Discord d'INSAlgo](https://discord.gg/68NE6tGMVk).
La phase de développement des IA, pendant laquelle les participants peuvent soumettre leur code, s'étent jusqu'au 11 mars.

A la fin, votre programme participera à un tournoi qui fera se rencontrer toutes les IA.
Chaque IA jouera 2 fois contre chacune des autres IA, une fois en jouant en premier, une fois en laissant l'adversaire commencer.
Une victoire rapporte un point, une défaite ou une égalité ne rapporte pas de point.
Un temps de réponse trop long ou un coup invalide fait perdre le match au programme.

## Participer au concours

Les soumissions sont faites par message privé au bot Dijkstra-Chan du serveur Discord.
Pour ce faire, envoyez la commande `!game submit snake` avec votre fichier attaché dans le même message.
Donnez comme nom à votre programme votre pseudo.

Votre dernière soumission vous représentera lors du tournoi final.
Pour le tournoi, transmettez votre code source et non un exécutable.
Les langages acceptés sont :
 - Python 3 `.py`
 - JavaScript `.js`
 - C++ `.cpp` (qui sera compilé avec g++ en O3)
 - Java `.java`
 - C# `.cs`
 - Rust `.rs`

Si vous souhaitez participer avec un autre langage, contactez un membre de bureau d'INSAlgo sur le serveur Discord.

## Règles du concours

Tous les étudiants de l'INSA Lyon peuvent participer. Il est autorisé de participer à plusieurs, danc ce cas, soumettez un seul programme pour le groupe.

Les soumissions se terminent le 11 mars 2025 à 18h.

Les soumissions doivent être ORIGINALES, c'est-à-dire ne pas implémenter une solution toute prête trouvée sur internet.
Les organisateurs vérifieront le code avant de valider les gagnants, alors soyez honnêtes !
Pour rendre cette tache plus facile, écrivez autant que possible du code lisible et commenté.

Les prix sont :
 - **64 €** pour le premier
 - **32 €** pour le deuxième
 - **16 €** pour le troisième

Les membres du bureau d'INSAlgo et ceux qui ont aidé à préparer le concours ne peuvent pas gagner les prix :'(

Si un groupe gagne, la récompense est par groupe et non par personnes.
Si des égalités se présentent, les personnes/groupes à égalité se partageront la somme des prix, par exemple :
  - 1er : Bob -> il gagne 64 €
  - 2e ex-aequo : Alice et Eve -> elles gagnent chacune (32+16)/2 = 24 €

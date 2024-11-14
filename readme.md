Guide d'Utilisation (Linux)

Ce guide explique comment installer Redis, configurer un environnement virtuel Python (venv), et exécuter les programmes de gestion de réservations sur Linux.
Prérequis

    Python 3.x : Assurez-vous d'avoir Python 3 installé.
    Redis : Le serveur Redis doit être installé et en cours d'exécution sur votre machine.

Étape 1 : Installation de Redis

    Mettez à jour vos paquets et installez Redis avec les commandes suivantes :

sudo apt update && sudo apt install redis-server

Vérifiez que le serveur Redis fonctionne correctement en le démarrant :

redis-server

Dans un autre terminal, lancez le client Redis pour vérifier la connexion :

    redis-cli ping

    Vous devriez obtenir PONG en réponse, ce qui indique que Redis fonctionne correctement.

Étape 2 : Création et Activation de l’Environnement Virtuel

    Créez un environnement virtuel en exécutant :

python3 -m venv venv

Activez l'environnement virtuel :

source venv/bin/activate

Installez les dépendances nécessaires à l'aide d'un fichier requirements.txt contenant les bibliothèques (redis, pandas, pybloom_live) avec la commande :

    pip install -r requirements.txt

Étape 3 : Exécution des Programmes

    Assurez-vous que le serveur Redis est en cours d'exécution. Si nécessaire, démarrez Redis avec la commande :

redis-server

Exécutez le script Python contenant vos programmes en vous assurant que l'environnement virtuel est activé :

    python <nom_du_script>.py

    Remplacez <nom_du_script> par le nom du fichier Python contenant votre code.

Fonctionnalités Principales des Programmes

    Compter le nombre de pilotes uniques : La fonction compter_pilotes_uniques parcourt les réservations et compte les pilotes uniques. Le résultat est stocké dans Redis sous la clé NB_Pilotes.

    Lister les villes d'arrivée : La fonction villes_arrivee_reservations extrait les villes d'arrivée des vols et retourne une liste unique de ces villes, stockée dans Redis sous la clé villes_arrivee.

    Classement des pilotes par nombre de vols : La fonction classement_pilotes génère un classement des pilotes basé sur le nombre de vols associés.

    Vérification de passagers avec Bloom Filter : Cette fonction utilise un filtre de Bloom pour vérifier rapidement si un passager est enregistré.

Note : Pour chaque nouvelle session, activez l'environnement virtuel avec source venv/bin/activate.
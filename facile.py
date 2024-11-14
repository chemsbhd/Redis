import redis
import json
import fonctions

r = redis.Redis(host='localhost', decode_responses=True, port="6379")


def compter_pilotes_uniques():
    # récupérer toutes les clés des réservations
    reservations_keys = r.keys('reservation:*')
    
    # créer un set pour stocker les pilotes uniques
    pilotes_uniques = set()
    
    # parcourir chaque réservation
    for reservation_key in reservations_keys:
        # récupérer les données de la réservation (au format JSON)
        reservation_data = json.loads(r.get(reservation_key))
        
        # extraire le pilote de la réservation
        pilote = reservation_data['reservation']['vol']['pilote']

        # ajouter le pilote au set (les doublons seront ignorés automatiquement)
        pilotes_uniques.add(pilote['nom'])
    
    # retourner le nombre de pilotes uniques
    return len(pilotes_uniques)

nombre_pilotes = compter_pilotes_uniques()
r.set("NB_Pilotes",nombre_pilotes)
fonctions.get_key(r, "NB_Pilotes")

def villes_arrivee_reservations():
    # récupérer toutes les clés des réservations
    keys = r.keys('reservation:*')
    
    villes_arrivee = set()  # utilisation d'un set pour éviter les doublons
    
    # parcourir chaque réservation pour extraire la ville d'arrivée
    for i in keys:
        # récupérer les données de la réservation (au format JSON)
        data = json.loads(r.get(i))
        
        # extraire la ville d'arrivée du vol associé à la réservation
        ville_arrivee = data['reservation']['vol']['villeArrivee']
        
        # ajouter la ville d'arrivée au set
        villes_arrivee.add(ville_arrivee)
    
    # retourner la liste des villes d'arrivée
    return list(villes_arrivee)

villes_arrivee = villes_arrivee_reservations()
r.set('villes_arrivee', json.dumps(villes_arrivee))
fonctions.get_key(r,'villes_arrivee')

def classement_pilotes():
    # récupérer toutes les clés des réservations
    reservations_keys = r.keys('reservation:*')

    # dictionnaire pour compter le nombre de vols par pilote
    compte_vols = {}

    # parcourir chaque réservation
    for reservation_key in reservations_keys:
        # récupérer les données de la réservation (au format JSON)
        reservation_data = json.loads(r.get(reservation_key))

        # extraire le pilote de la réservation
        pilote_nom = reservation_data['reservation']['vol']['pilote']['nom']

        # incrémenter le compteur pour ce pilote
        if pilote_nom in compte_vols:
            compte_vols[pilote_nom] += 1
        else:
            compte_vols[pilote_nom] = 1

    # trier les pilotes par nombre de vols (en ordre décroissant)
    classement = sorted(compte_vols.items(), key=lambda x: x[1], reverse=True)

    # retourner le classement
    return classement

# appeler la fonction et afficher le classement
classement = classement_pilotes()
print("Classement des pilotes par nombre de vols :")
for pilote, vols in classement:
    print(f"{pilote}: {vols} vols")


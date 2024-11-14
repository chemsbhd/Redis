import redis
import json

server = redis.Redis(host='localhost', decode_responses=True, port="6379")

# chargement des fichiers JSON
with open('reservations1.json') as file1, open('reservations2.json') as file2:
    reservations1 = json.load(file1)
    reservations2 = json.load(file2)

# fonction pour extraire la valeur d'un attribut imbriqué
def obtenir_valeur(data, chemin):
    # découper le chemin de l'attribut en segments
    attributs = chemin.split(".")
    valeur = data
    for attribut in attributs:
        valeur = valeur.get(attribut)
        if valeur is None:
            return None
    return valeur

# fonction de jointure basée sur un attribut, supportant les attributs imbriqués
def jointure(d1, d2, chemin_attribut):
    jointures = []  # Liste pour stocker les jointures
    
    # parcourir les éléments des deux dictionnaires
    for id1, data1 in d1.items():
        for id2, data2 in d2.items():
            # comparer l'attribut imbriqué entre les deux dictionnaires
            if obtenir_valeur(data1, chemin_attribut) == obtenir_valeur(data2, chemin_attribut):
                # créer une jointure contenant les infos des deux réservations
                jointure = {
                    "reservation1": data1,
                    "reservation2": data2
                }
                jointures.append(jointure)

    return jointures

# utilisation
resultat_jointure = jointure(reservations1, reservations2, "vol.pilote")

# affichage des jointures
print("Jointures trouvées pour cette attribut :")
for idx, jointure in enumerate(resultat_jointure, start=1):
    print(f"Jointure {idx}: \n")
    print("RESERVATION 1:", jointure["reservation1"], "\n")
    print("RESERVATION 2:", jointure["reservation2"])
    print("------------------------------------------------------------")

for idx, jointure in enumerate(resultat_jointure, start=1):
    # enregistrement de chaque jointure sous une clé Redis distincte
    server.set(f"jointure:{idx}", json.dumps(jointure))
    
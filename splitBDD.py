import redis
import json

# Connexion à Redis
r = redis.Redis(host='localhost', decode_responses=True, port="6379")

# Charger les données des pilotes
piloteFile = open("txt/PILOTES.txt", 'r', encoding='utf-8')
pilotes = {}
for line in piloteFile:
    line = line.split('\t')
    pilotes[line[0]] = {"nom": line[1], "naissance": line[2], "ville": line[3].rstrip()}
piloteFile.close()

# Charger les données des clients
clientFile = open("txt/CLIENTS.txt", 'r', encoding='utf-8')
clients = {}
for line in clientFile:
    line = line.split('\t')
    clients[line[0]] = {"nom": line[1], "numeroRue": line[2], "nomRue": line[3], "codePostal": line[4], "ville": line[5].rstrip()}
clientFile.close()

# Charger les classes de vols (première classe, classe économique, etc.)
classesFile = open('txt/DEFCLASSES.txt', 'r', encoding="utf-8")
classes = {}
for line in classesFile:
    line = line.split('\t')
    if line[0] not in classes:
        classes[line[0]] = {line[1]: int(line[2].rstrip())}
    else:
        classes[line[0]][line[1]] = int(line[2].rstrip())
classesFile.close()

# Charger les données des avions
avionsFile = open("txt/AVIONS.txt", 'r', encoding='utf-8')
avions = {}
for line in avionsFile:
    line = line.rstrip().split("\t")
    avions[line[0]] = {"nom": line[1], "capacite": line[2], "ville": line[3]}
avionsFile.close()

# Charger les données des vols
volsFile = open('txt/VOLS.txt', 'r', encoding="utf-8")
vols = {}
for line in volsFile:
    line = line.split("\t")
    vols[line[0]] = {"villeDepart": line[1], "villeArrivee": line[2], "dateDepart": line[3], "heureDepart": line[4], "dateArrivee": line[5], "heureArrivee": line[6], "pilote": pilotes[line[7]], "avion": avions[line[8].rstrip()]}
volsFile.close()

# Charger les données des réservations
reservationFile = open("txt/RESERVATIONS.txt", 'r', encoding='utf-8')
reservations = []
for line in reservationFile:
    line = line.split('\t')
    reservations.append({
        "client": clients[line[0]],
        "vol": vols[line[1]],
        "classe": {"nom": line[2], "coeffPrix": classes[line[1]][line[2]]},
        "places": int(line[3].rstrip())
    })
reservationFile.close()

# Formater chaque réservation dans le format "reservation n"
formatted_reservations = {f"reservation {i+1}": reservation for i, reservation in enumerate(reservations)}

# Créer un fichier JSON contenant toutes les réservations formatées
with open("all_reservations.json", "w", encoding="utf-8") as outfile:
    json.dump(formatted_reservations, outfile, ensure_ascii=False, indent=4)

# Diviser les réservations formatées en deux parties égales
half = len(formatted_reservations) // 2
reservations_part1 = {f"reservation {i+1}": reservation for i, (key, reservation) in enumerate(formatted_reservations.items()) if i < half}
reservations_part2 = {f"reservation {i+1}": reservation for i, (key, reservation) in enumerate(formatted_reservations.items()) if i >= half}

# Écrire deux fichiers JSON distincts pour les deux parties
with open("reservations1.json", "w", encoding="utf-8") as part1:
    json.dump(reservations_part1, part1, ensure_ascii=False, indent=4)

with open("reservations2.json", "w", encoding="utf-8") as part2:
    json.dump(reservations_part2, part2, ensure_ascii=False, indent=4)

# Stocker les réservations formatées dans Redis
for i, (key, reservation) in enumerate(formatted_reservations.items()):
    r.set(f"reservation:{i+1}", json.dumps({key: reservation}))

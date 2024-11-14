import redis

r = redis.Redis(host='localhost', decode_responses=True, port="6379")

def set_key(r, key, value):
    # définit une clé avec une valeur
    r.set(key, value)
    print(f"clé '{key}' définie avec la valeur '{value}'")

def get_key(r, key):
    # récupère la valeur d'une clé
    value = r.get(key)
    if value is not None:
        print(f"valeur pour '{key}': {value}")
    else:
        print(f"la clé '{key}' n'existe pas.")
    return value

def get_pattern(r, pattern="*"):
    # obtient toutes les clés qui correspondent à un motif
    keys = r.keys(pattern)
    print(f"clés correspondant au motif '{pattern}': {keys}")

def update_key(r, key, new_value):
    # met à jour la valeur d'une clé existante
    if r.exists(key):
        r.set(key, new_value)
        print(f"valeur de la clé '{key}' mise à jour à '{new_value}'")
    else:
        print(f"la clé '{key}' n'existe pas pour mise à jour.")

def delete_key(r, key):
    # supprime une clé de redis
    if r.delete(key):
        print(f"clé '{key}' supprimée.")
    else:
        print(f"la clé '{key}' n'existe pas.")

def increment_key(r, key):
    # incrémente la valeur d'une clé numérique
    if r.exists(key):
        new_value = r.incr(key)
        print(f"valeur de la clé '{key}' incrémentée à {new_value}")
        return new_value
    else:
        print(f"la clé '{key}' n'existe pas pour incrémentation.")
        return None

def get_all_keys(r):
    # affiche toutes les clés présentes dans la base redis
    keys = r.keys('*')  # récupère toutes les clés
    if keys:
        print("clés dans la base de données redis :")
        for key in keys:
            print(f"- {key}")
    else:
        print("aucune clé dans la base de données redis.")

def delete_all_keys(r):
    # supprime toutes les clés présentes dans la base redis
    keys = r.keys('*')  # récupère toutes les clés
    if keys:
        r.delete(*keys)  # supprime toutes les clés
        print("toutes les clés ont été supprimées de la base de données redis.")
    else:
        print("aucune clé à supprimer dans la base de données redis.")

# test d'une clé avec une récupération de valeur
get_key(r, "reservation:1")

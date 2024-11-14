import redis

def test_redis_connection(host='localhost', decode_responses=True, port="6379"):
    """
    Teste la connexion à Redis et retourne True si la connexion est réussie,
    False sinon.
    """
    try:
        r = redis.Redis(host=host, port=port)
        if r.ping():
            print(f"Connexion réussie à Redis sur le port {port}")
            return True
    except redis.ConnectionError:
        print(f"Connexion échouée à Redis sur le port {port}")
        return False

# Tests
def main():
    # Test avec le bon port
    print("Test avec le port correct (6379) :")
    test_redis_connection(port=6379)

    # Test avec un mauvais port
    print("\nTest avec un port incorrect (6380) :")
    test_redis_connection(port=6380)

if __name__ == '__main__':
    main()

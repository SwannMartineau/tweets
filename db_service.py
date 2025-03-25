import mysql.connector
from dotenv import load_dotenv
import os

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Fonction pour récupérer les 100 derniers tweets
def get_last_100_tweets():
    try:
        # Connexion à MySql
        connection = mysql.connector.connect(
            host = os.getenv('DB_URL'),
            port = os.getenv('DB_PORT'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_TABLE')
        )
        
        # Création d'un curseur pour effectuer des requêtes
        cursor = connection.cursor()
        
        # Sélectionner les 100 derniers tweets de la table
        query = "SELECT text, positive, negative FROM tweets ORDER BY id DESC LIMIT 100"
        cursor.execute(query)
        
        # Récupérer les résultats
        result = cursor.fetchall()
        
        # Fermer la connexion
        cursor.close()
        connection.close()
        
        return result
        
    except mysql.connector.Error as err:
        print(f"Erreur: {err}")
        return []
    
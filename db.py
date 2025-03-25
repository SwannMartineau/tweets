import mysql.connector
from dotenv import load_dotenv
import os
import csv

def init_db() :
    try:
        # Connexion à MySql
        connection = mysql.connector.connect(
            host = os.getenv('DB_URL'),
            port = os.getenv('DB_PORT'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD')
        )
                
        # Il va gérer les requêtes et résultats SQL
        cursor = connection.cursor()
        
        # Création de la table si elle n'existe pas
        cursor.execute("CREATE DATABASE IF NOT EXISTS tweets_db")
        print("Base de données créée avec succès")
        
        # Connexion à la db
        connection.database = "tweets_db"
        
        # Création de la table tweets
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text VARCHAR(280) NOT NULL,
            positive TINYINT(1) NOT NULL,
            negative TINYINT(1) NOT NULL
        )
        """)
        print("Table 'tweets' créée avec succès.")
        
    except mysql.connector.Error as err:
        print(f"Erreur: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_tweets_db(tweets_csv):
    try:
        # Connexion à MySql
        connection = mysql.connector.connect(
            host = os.getenv('DB_URL'),
            port = os.getenv('DB_PORT'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_TABLE')
        )
        
        # Il va gérer les requêtes et résultats SQL
        cursor = connection.cursor()
        
        # Lire le fichier CSV
        with open(tweets_csv, mode='r') as file:
            
            reader = csv.reader(file)
            
            # Passer la première ligne (le header avec les champs)
            next(reader)
            
            # Insérer les lignes dans la base de données
            for row in reader:
                # Si vous mettez des virgules dans vos textes on rentrera dans cette condition et votre texte sera ignorée pour l'insérer dans la db
                if len(row) != 3:
                    print(f"Ligne ignorée (format incorrect) : {row}")
                    continue
                
                text, positive, negative = row
                sqlQuery = "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)"
                cursor.execute(sqlQuery, (text, int(positive), int(negative)))
        
        connection.commit()
        print("Tweets insérés avec succès.")
        
    except mysql.connector.Error as err:
        print(f"Erreur: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Charger les variables d'environnement du fichier .env
load_dotenv()
# Appel la fonction pour init
init_db()
# INSERT tweets into database
insert_tweets_db('tweets.csv')

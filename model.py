import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import re
from db_service import get_last_100_tweets  # Importation de la fonction pour récupérer les 100 derniers tweets

# Télécharger les ressources nécessaires de nltk pour les stopwords inutiles pour analyser le texte
nltk.download('stopwords')

# Fonction de nettoyage
def clean_text(text):
    text = text.lower() # Mettre en minuscule
    text = re.sub(r'[^\w\s]', '', text) # Supprimer les caractères spéciaux
    return text

def train_model():
    # Récupérer les 100 derniers tweets de la base de données
    tweets_data = get_last_100_tweets()

    # Pour voir les problèmes potentiels avec la récupération des datas
    # print("Données récupérées:", tweets_data)

    if not tweets_data:
        print("Aucun tweet trouvé pour l'entraînement.")
        return None, None

    # Convertir en DataFrame
    df = pd.DataFrame(tweets_data, columns=['text', 'positive', 'negative'])
    
    # On peut utiliser la colonne 'positive' comme label (1 pour positif, 0 pour négatif) car si c'est pas positif c'est négatif
    df['sentiment'] = df['positive'].apply(lambda x: 1 if x == 1 else 0)
    
    # Appliquer le nettoyage
    df['text_clean'] = df['text'].apply(clean_text)
    
    # Vectorisation
    vectorizer = CountVectorizer(stop_words=nltk.corpus.stopwords.words('french'))

    # Préparation des données : diviser en X (tweets) et y (sentiment)
    X = vectorizer.fit_transform(df['text_clean'])
    y = df['sentiment']

    # Diviser les données en un ensemble d'entraînement et un ensemble de test en 20% 80%
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

    # Entraîner le modèle de régression logistique
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Évaluation du modèle (sur l'ensemble de test)
    y_pred = model.predict(X_test)

    # Générer et afficher la matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    print("\nMatrice de confusion :\n", cm)
    
    # Rapport de classification (Précision, Rappel, F1-score)
    report = classification_report(y_test, y_pred, target_names=['Négatif', 'Positif'])
    print("\n Rapport de classification :\n", report)

    # Retourner le modèle et le vectorizer pour pouvoir transformer les nouveaux tweets
    return model, vectorizer

def predict_feeling(model, vectorizer, tweet):
    tweet = clean_text(tweet)
    # Transformer le tweet en vecteur avec le même vectorizer
    tweet_vec = vectorizer.transform([tweet])
    # Prédire le sentiment du tweet avec le modèle
    feeling = model.predict(tweet_vec)[0]
    return feeling

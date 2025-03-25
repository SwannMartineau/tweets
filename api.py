from flask import Flask, request, jsonify # Importation de Flask pour créer l'API
from textblob import TextBlob # Pour analyser le sentiment des tweets
from model import train_model, predict_feeling

# Init de l'app Flask
app = Flask(__name__)

# Endpoint POST pour analyser les sentiments des tweets
@app.route('/analyze_feeling', methods=['POST'])

def analyze_feeling():
    try:
        # Entraîner le modèle avec les 100 derniers tweets
        model, vectorizer = train_model()
        
        if model is None or vectorizer is None:
            return jsonify({'error': 'Erreur lors de l\'entraînement du modèle'}), 500
        
        # Parse data as JSON et récupération des données JSON envoyées dans la requête
        data = request.get_json()

        if not data or 'tweets' not in data:
            return jsonify({'error': 'Veuillez fournir une liste de tweets avec le mot "tweets"'}), 400
        
        tweets = data['tweets']
        
        # On vérifie si c'est une liste
        if not isinstance(tweets,list):
            return jsonify({'error': 'Les tweets doivent être un tableau"'}), 400
        
        # On instancie le résultat
        results = {}
        
        for tweet in tweets:
            if not isinstance(tweet,str):
                results[tweet] = 'Invalid input (this is not a string)'
            else:
                # Ici on prédit le sentiment négatif ou non
                analysis = predict_feeling(model, vectorizer, tweet)
                # Insérer le score du tweet et le transformer en int (de base on a du int64)
                results[tweet] = int(analysis)
        
        # Renvoyer les résultats en JSON
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Lancer l'app
if __name__ == '__main__':
    app.run(debug=True)
# 📊 Analyse de Sentiments des Tweets avec Flask et Machine Learning

Ce projet implémente une API Flask permettant d'analyser le sentiment des tweets (positif ou négatif) à l'aide d'un modèle de machine learning.  
L'application utilise la régression logistique pour classer les tweets en **positifs** ou **négatifs** et propose des métriques d'évaluation pour suivre les performances du modèle.

---

## 🧰 Prérequis

Avant de commencer, assurez-vous d'avoir :

- **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** installé et lancé
- **Python 3.x** installé
- **Postman** ou tout autre outil similaire pour tester l’API

---

## ⚙️ Installation et Lancement

### 1. **Démarrer Docker**
- Lancez Docker Desktop.
- Vérifiez que Docker est en cours d'exécution.

---

### 2. **Lancer les Services**
- Dans un terminal, exécutez la commande suivante pour lancer les services définis dans `docker-compose.yml` :
```bash
docker-compose up -d
```

### 3. **Installer les libs**
- Installer les libs avec :
```bash
pip install Flask TextBlob mysql-connector-python python-dotenv scikit-learn nltk pandas
```

### 4. **Initialiser la Base de Données**
- Pour créer les tables et insérer les données initiales :
```bash
py .\db.py
```

### 5. **Lancer l'API Flask**
- Pour lancer l'API Flask faire :
```bash
py api.py
```

### 6. **Tester l’API avec Postman**
- Pour tester l'endpoint se mettre sur l'url depuis Postman ou un autre outil de votre choix :
```bash
http://127.0.0.1:5000/analyze_feeling
```

- Faire un POST sous la forme JSON (exemple) :
```bash
{
    "tweets": [
        "Je n'aime pas ce texte !",
        "Je ne veux plus voir ce film de ma vie",
        "Le film était nul !",
        "Je deteste",
        "J'aime ce texte",
    ]
}
```

## 🛠️ Résultat de l’Analyse
```bash
Examiner le retour :
    - 1 pour positif
    - 0 pour négatif
```
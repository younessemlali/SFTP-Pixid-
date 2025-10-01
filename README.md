# 📤 Pixid XML Uploader

Application Streamlit pour uploader des fichiers XML vers le serveur d'intégration Pixid via SSH/SFTP.

## 🎯 Fonctionnalités

- 🔐 **Authentification interactive** : Saisissez vos identifiants à chaque utilisation
- 🔌 **Test de connexion** : Vérifiez vos identifiants avant d'uploader
- ✅ Validation automatique des fichiers XML
- 🔒 Connexion SSH sécurisée
- 📤 Upload SFTP vers `inbox/`
- 👁️ Prévisualisation du contenu XML
- 📊 Statistiques d'upload
- 🎨 Interface conviviale
- 🚫 **Aucun stockage des identifiants**

## 🚀 Installation locale

### Prérequis

- Python 3.8+
- Git

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/VOTRE_USERNAME/pixid-xml-uploader.git
cd pixid-xml-uploader
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

**Note :** Vous saisirez vos identifiants SSH directement dans l'interface à chaque utilisation.

## ☁️ Déploiement sur Streamlit Cloud

### Étape 1 : Préparer le repository GitHub

1. Créez un nouveau repository sur GitHub
2. Poussez le code (sans le fichier `secrets.toml`) :

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/pixid-xml-uploader.git
git push -u origin main
```

### Étape 2 : Déployer sur Streamlit Cloud

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec votre compte GitHub
3. Cliquez sur "New app"
4. Sélectionnez votre repository `pixid-xml-uploader`
5. Branch : `main`
6. Main file path : `app.py`
7. Cliquez sur "Deploy"

🎉 Votre application sera accessible via une URL publique (ex: `https://pixid-xml-uploader.streamlit.app`)

**Note :** Aucune configuration de secrets n'est nécessaire ! Les utilisateurs saisissent leurs identifiants directement dans l'interface.

## 📖 Utilisation

1. **Saisir vos identifiants** : Entrez votre nom d'utilisateur et mot de passe SSH dans les champs en haut de la page
2. **Tester la connexion** : Cliquez sur "🔌 Tester la connexion" pour vérifier vos identifiants
3. **Uploader un fichier** : Une fois la connexion validée, cliquez sur "Browse files" ou glissez-déposez votre fichier XML
4. **Vérifier la validation** : L'application valide automatiquement la structure XML
5. **Personnaliser le nom** (optionnel) : Modifiez le nom du fichier si nécessaire
6. **Uploader** : Cliquez sur le bouton "📤 Uploader"

**Important :** 
- Vos identifiants ne sont pas stockés et doivent être saisis à chaque session
- Le test de connexion est **fortement recommandé** avant de charger un fichier

## 🔒 Sécurité

- ⚠️ Les identifiants sont saisis à chaque session et **ne sont jamais stockés**
- ✅ Connexion SSH/SFTP chiffrée (TLS)
- 🔐 Les mots de passe sont masqués dans l'interface
- 🚫 Aucune persistance des credentials
- ✅ Validation XML avant upload

## 🛠️ Technologies utilisées

- **Streamlit** : Framework web Python
- **Paramiko** : Bibliothèque SSH/SFTP
- **Python 3** : Langage de programmation

## 📝 Structure du projet

```
pixid-xml-uploader/
├── .streamlit/
│   └── secrets.toml.example    # Template (optionnel, pour référence)
├── app.py                       # Application principale
├── requirements.txt             # Dépendances Python
├── .gitignore                  # Fichiers à ignorer
└── README.md                   # Documentation
```

## 🐛 Troubleshooting

### Erreur de connexion SSH

- Vérifiez que vos identifiants sont corrects
- Vérifiez que le serveur est accessible (firewall, VPN)
- Testez manuellement la connexion : `ssh username@integrationprod.pixid-services.net`

### Identifiants non acceptés

- Assurez-vous d'avoir saisi le bon nom d'utilisateur (sensible à la casse)
- Vérifiez qu'il n'y a pas d'espaces avant/après les identifiants
- Utilisez le bouton "Tester la connexion" pour diagnostiquer le problème
- Contactez l'équipe technique pour vérifier vos accès

### Le bouton "Tester la connexion" ne répond pas

- Vérifiez votre connexion internet
- Assurez-vous que vous n'êtes pas derrière un proxy bloquant
- Vérifiez que le port 22 est accessible depuis votre réseau

### Erreur "Module not found"

```bash
pip install -r requirements.txt
```

### Le fichier ne s'upload pas

- Vérifiez que le répertoire `inbox/` existe sur le serveur
- Vérifiez les permissions d'écriture de votre compte SSH

## 📞 Support

Pour toute question ou problème, contactez l'équipe technique Pixid.

## 📄 Licence

Ce projet est à usage interne uniquement.

# 📤 Pixid XML Uploader

Application Streamlit pour uploader des fichiers XML vers le serveur d'intégration Pixid via SSH/SFTP.

## 🎯 Fonctionnalités

- ✅ Validation automatique des fichiers XML
- 🔒 Connexion SSH sécurisée
- 📤 Upload SFTP vers `inbox/`
- 👁️ Prévisualisation du contenu XML
- 📊 Statistiques d'upload
- 🎨 Interface conviviale

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

4. **Configurer les secrets**

Créez le dossier `.streamlit/` et le fichier `secrets.toml` :

```bash
mkdir .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Éditez `.streamlit/secrets.toml` avec vos vrais identifiants :

```toml
[ssh]
hostname = "integrationprod.pixid-services.net"
port = 22
username = "votre_identifiant"
password = "votre_mot_de_passe"
remote_path = "inbox"
```

5. **Lancer l'application**
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

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
7. Cliquez sur "Advanced settings"
8. Dans la section "Secrets", collez le contenu de votre `secrets.toml` :

```toml
[ssh]
hostname = "integrationprod.pixid-services.net"
port = 22
username = "votre_identifiant"
password = "votre_mot_de_passe"
remote_path = "inbox"
```

9. Cliquez sur "Deploy"

🎉 Votre application sera accessible via une URL publique (ex: `https://pixid-xml-uploader.streamlit.app`)

## 📖 Utilisation

1. **Uploader un fichier** : Cliquez sur "Browse files" ou glissez-déposez votre fichier XML
2. **Vérifier la validation** : L'application valide automatiquement la structure XML
3. **Personnaliser le nom** (optionnel) : Modifiez le nom du fichier si nécessaire
4. **Uploader** : Cliquez sur le bouton "📤 Uploader"

## 🔒 Sécurité

- ⚠️ **Ne jamais** commiter le fichier `.streamlit/secrets.toml` sur GitHub
- ✅ Les credentials sont stockés de manière sécurisée dans Streamlit Cloud
- 🔐 Connexion SSH/SFTP chiffrée

## 🛠️ Technologies utilisées

- **Streamlit** : Framework web Python
- **Paramiko** : Bibliothèque SSH/SFTP
- **Python 3** : Langage de programmation

## 📝 Structure du projet

```
pixid-xml-uploader/
├── .streamlit/
│   ├── secrets.toml.example    # Template de configuration
│   └── secrets.toml            # Configuration réelle (non versionné)
├── app.py                       # Application principale
├── requirements.txt             # Dépendances Python
├── .gitignore                  # Fichiers à ignorer
└── README.md                   # Documentation
```

## 🐛 Troubleshooting

### Erreur de connexion SSH

- Vérifiez que vos identifiants sont corrects dans `secrets.toml`
- Vérifiez que le serveur est accessible (firewall)
- Testez manuellement la connexion : `ssh username@integrationprod.pixid-services.net`

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

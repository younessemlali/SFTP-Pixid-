import streamlit as st
import paramiko
import io
from datetime import datetime
import xml.etree.ElementTree as ET

# Configuration de la page
st.set_page_config(
    page_title="Pixid XML Uploader",
    page_icon="📤",
    layout="wide"
)

# Initialisation de session_state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'upload_count' not in st.session_state:
    st.session_state.upload_count = 0

# Configuration du serveur (paramètres fixes)
HOSTNAME = "integrationprod.pixid-services.net"
PORT = 22
REMOTE_PATH = "inbox"

# Titre de l'application
st.title("📤 Pixid XML File Uploader")
st.markdown("Upload de fichiers XML vers integrationprod.pixid-services.net")
st.markdown("---")

# Fonction de validation XML
def validate_xml(file_content):
    """Valide la structure XML"""
    try:
        ET.fromstring(file_content)
        return True, "✅ Fichier XML valide"
    except ET.ParseError as e:
        return False, f"❌ Erreur XML : {str(e)}"

# Fonction de connexion SSH
def ssh_connect(hostname, port, username, password):
    """Établit une connexion SSH"""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            timeout=10
        )
        return client, True, "✅ Connexion établie avec succès"
    except paramiko.AuthenticationException:
        return None, False, "❌ Erreur d'authentification : identifiant ou mot de passe incorrect"
    except paramiko.SSHException as e:
        return None, False, f"❌ Erreur SSH : {str(e)}"
    except Exception as e:
        return None, False, f"❌ Erreur de connexion : {str(e)}"

# Fonction d'upload via SFTP
def upload_file_sftp(client, file_content, remote_path, filename):
    """Upload un fichier via SFTP"""
    try:
        sftp = client.open_sftp()
        
        # Vérifier si le répertoire existe, sinon le créer
        try:
            sftp.stat(remote_path)
        except FileNotFoundError:
            st.warning(f"Le répertoire {remote_path} n'existe pas. Tentative de création...")
            sftp.mkdir(remote_path)
        
        # Chemin complet du fichier distant
        remote_file = f"{remote_path}/{filename}"
        
        # Upload du fichier
        file_obj = io.BytesIO(file_content)
        sftp.putfo(file_obj, remote_file)
        
        sftp.close()
        return True, f"✅ Fichier uploadé avec succès : {remote_file}"
    except Exception as e:
        return False, f"❌ Erreur lors de l'upload : {str(e)}"

# Sidebar pour les informations et statistiques
with st.sidebar:
    st.header("ℹ️ Informations")
    st.info(f"""
    **Serveur :** {HOSTNAME}  
    **Port :** {PORT}  
    **Destination :** {REMOTE_PATH}/
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Statistiques")
    st.metric("Fichiers uploadés", st.session_state.upload_count)
    
    st.markdown("---")
    st.markdown("### 📖 Guide")
    st.markdown("""
    **Étapes :**
    1. Entrez vos identifiants
    2. Testez la connexion 🔌
    3. Chargez votre fichier XML
    4. Vérifiez la validation
    5. Cliquez sur Uploader
    
    **Sécurité :**
    - Connexion SSH chiffrée
    - Identifiants non stockés
    - Validation XML automatique
    - Test préalable recommandé
    """)

# Zone de connexion
st.header("🔐 Authentification SSH")

col_user, col_pass = st.columns(2)

with col_user:
    username = st.text_input(
        "Identifiant SSH",
        placeholder="votre_identifiant",
        help="Votre nom d'utilisateur pour la connexion SSH"
    )

with col_pass:
    password = st.text_input(
        "Mot de passe SSH",
        type="password",
        placeholder="votre_mot_de_passe",
        help="Votre mot de passe SSH (non stocké)"
    )

# Vérifier si les identifiants sont renseignés
credentials_provided = bool(username and password)

# Bouton de test de connexion
col_test, col_status = st.columns([1, 3])

with col_test:
    test_button = st.button("🔌 Tester la connexion", disabled=not credentials_provided, use_container_width=True)

with col_status:
    if not credentials_provided:
        st.warning("⚠️ Veuillez renseigner vos identifiants SSH pour tester la connexion")
    elif 'connection_tested' not in st.session_state:
        st.info("💡 Cliquez sur 'Tester la connexion' pour vérifier vos identifiants")

# Test de connexion
if test_button:
    with st.spinner('🔄 Test de connexion en cours...'):
        client, success, message = ssh_connect(HOSTNAME, PORT, username, password)
        
        if success:
            st.session_state.connection_tested = True
            st.session_state.connection_success = True
            client.close()
            st.success(f"✅ {message} - Vous pouvez maintenant uploader vos fichiers !")
        else:
            st.session_state.connection_tested = True
            st.session_state.connection_success = False
            st.error(message)
            st.warning("💡 Vérifiez vos identifiants et réessayez")

# Afficher le statut de la connexion si déjà testée
if 'connection_tested' in st.session_state and not test_button:
    if st.session_state.connection_success:
        with col_status:
            st.success("✅ Connexion vérifiée avec succès")
    else:
        with col_status:
            st.error("❌ La dernière tentative de connexion a échoué")

st.markdown("---")

# Interface principale - Upload de fichier
if credentials_provided:
    # Vérifier si la connexion a été testée avec succès
    connection_verified = st.session_state.get('connection_success', False)
    
    if not connection_verified:
        st.info("ℹ️ Pour uploader des fichiers, testez d'abord votre connexion SSH ci-dessus")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload de fichier XML")
        
        # Upload de fichier - désactivé si connexion non testée
        uploaded_file = st.file_uploader(
            "Choisissez un fichier XML",
            type=['xml'],
            help="Sélectionnez un fichier XML à uploader vers le serveur Pixid" if connection_verified else "Testez d'abord votre connexion SSH",
            disabled=not connection_verified
        )
        
        if uploaded_file is not None:
            # Lecture du contenu
            file_content = uploaded_file.read()
            file_size = len(file_content) / 1024  # Taille en KB
            
            st.success(f"📄 Fichier chargé : **{uploaded_file.name}** ({file_size:.2f} KB)")
            
            # Validation XML
            is_valid, validation_message = validate_xml(file_content)
            
            if is_valid:
                st.success(validation_message)
                
                # Prévisualisation
                with st.expander("👁️ Prévisualiser le contenu XML"):
                    try:
                        xml_str = file_content.decode('utf-8')
                        st.code(xml_str[:1000] + ("..." if len(xml_str) > 1000 else ""), language='xml')
                    except:
                        st.warning("Impossible d'afficher le contenu")
            else:
                st.error(validation_message)
            
            st.markdown("---")
            
            # Options d'upload
            st.subheader("🚀 Options d'upload")
            
            col_name, col_btn = st.columns([3, 1])
            
            with col_name:
                custom_filename = st.text_input(
                    "Nom du fichier (optionnel)",
                    value=uploaded_file.name,
                    help="Laissez vide pour utiliser le nom original"
                )
            
            with col_btn:
                st.write("")  # Espacement
                st.write("")  # Espacement
                upload_button = st.button("📤 Uploader", type="primary", use_container_width=True)
            
            # Processus d'upload
            if upload_button:
                if not is_valid:
                    st.error("⚠️ Impossible d'uploader un fichier XML invalide")
                else:
                    with st.spinner('🔄 Connexion au serveur...'):
                        # Connexion SSH
                        client, success, message = ssh_connect(HOSTNAME, PORT, username, password)
                        
                        if success:
                            st.success(message)
                            
                            with st.spinner('📤 Upload en cours...'):
                                # Upload du fichier
                                final_filename = custom_filename if custom_filename else uploaded_file.name
                                upload_success, upload_message = upload_file_sftp(
                                    client, 
                                    file_content, 
                                    REMOTE_PATH, 
                                    final_filename
                                )
                                
                                if upload_success:
                                    st.success(upload_message)
                                    st.balloons()
                                    st.session_state.upload_count += 1
                                    
                                    # Informations de l'upload
                                    st.info(f"""
                                    **Détails de l'upload :**
                                    - 📁 Fichier : {final_filename}
                                    - 📊 Taille : {file_size:.2f} KB
                                    - 🕒 Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                                    - 📍 Destination : {HOSTNAME}:{REMOTE_PATH}/
                                    - 👤 Utilisateur : {username}
                                    """)
                                else:
                                    st.error(upload_message)
                            
                            # Fermeture de la connexion
                            client.close()
                        else:
                            st.error(message)
                            st.warning("💡 Vérifiez vos identifiants et réessayez")
    
    with col2:
        st.header("✅ Checklist")
        
        st.markdown("""
        ### Avant l'upload :
        
        - ✅ Identifiants renseignés
        - ⬜ Connexion testée
        - ⬜ Fichier XML chargé
        - ⬜ Validation réussie
        - ⬜ Nom vérifié
        - ⬜ Prêt à uploader
        
        ### Après l'upload :
        
        - Vérifiez le message de confirmation
        - Notez la date et l'heure
        - Consultez les statistiques
        
        ### 🔒 Sécurité :
        
        Vos identifiants :
        - Ne sont **pas stockés**
        - Sont utilisés **uniquement** pour cette session
        - Sont transmis de manière **chiffrée**
        
        ### 💡 Astuce :
        
        Testez toujours votre connexion avant de charger un fichier !
        
        ### 📞 Support :
        
        En cas de problème :
        - Vérifiez vos identifiants
        - Testez la connexion réseau
        - Contactez l'équipe technique
        """)

else:
    # Message si pas d'identifiants
    st.info("👆 Renseignez vos identifiants SSH ci-dessus puis testez la connexion avant d'uploader des fichiers")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>Pixid XML Uploader v2.1 | Test de connexion | Développé avec Streamlit</small>
    </div>
    """,
    unsafe_allow_html=True
)

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

# Titre de l'application
st.title("📤 Pixid XML File Uploader")
st.markdown("Upload de fichiers XML vers integrationprod.pixid-services.net")
st.markdown("---")

# Sidebar pour la configuration
with st.sidebar:
    st.header("⚙️ Configuration SSH")
    
    # Récupération des credentials depuis secrets.toml
    try:
        hostname = st.secrets["ssh"]["hostname"]
        port = st.secrets["ssh"]["port"]
        username = st.secrets["ssh"]["username"]
        password = st.secrets["ssh"]["password"]
        remote_path = st.secrets["ssh"]["remote_path"]
        
        st.success("✅ Configuration chargée")
        st.info(f"**Serveur:** {hostname}:{port}")
        st.info(f"**Destination:** {remote_path}")
    except Exception as e:
        st.error("❌ Configuration manquante dans secrets.toml")
        st.stop()
    
    st.markdown("---")
    st.markdown("### 📊 Statistiques")
    if 'upload_count' not in st.session_state:
        st.session_state.upload_count = 0
    st.metric("Fichiers uploadés", st.session_state.upload_count)

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

# Interface principale
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📁 Upload de fichier XML")
    
    # Upload de fichier
    uploaded_file = st.file_uploader(
        "Choisissez un fichier XML",
        type=['xml'],
        help="Sélectionnez un fichier XML à uploader vers le serveur Pixid"
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
                    client, success, message = ssh_connect(hostname, port, username, password)
                    
                    if success:
                        st.success(message)
                        
                        with st.spinner('📤 Upload en cours...'):
                            # Upload du fichier
                            final_filename = custom_filename if custom_filename else uploaded_file.name
                            upload_success, upload_message = upload_file_sftp(
                                client, 
                                file_content, 
                                remote_path, 
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
                                - 📍 Destination : {hostname}:{remote_path}
                                """)
                            else:
                                st.error(upload_message)
                        
                        # Fermeture de la connexion
                        client.close()
                    else:
                        st.error(message)

with col2:
    st.header("📖 Guide d'utilisation")
    
    st.markdown("""
    ### Étapes :
    
    1. **Chargez** votre fichier XML
    2. **Vérifiez** la validation
    3. **Personnalisez** le nom (optionnel)
    4. **Cliquez** sur Uploader
    
    ### ✅ Prérequis :
    
    - Fichier au format XML valide
    - Connexion réseau active
    - Credentials configurés
    
    ### 🔒 Sécurité :
    
    - Connexion SSH sécurisée
    - Validation XML automatique
    - Credentials chiffrés
    
    ### ℹ️ Informations :
    
    - **Serveur :** integrationprod.pixid-services.net
    - **Port :** 22
    - **Protocole :** SFTP
    - **Destination :** inbox/
    """)
    
    st.markdown("---")
    st.info("💡 **Astuce :** Vérifiez toujours la validation XML avant l'upload")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>Pixid XML Uploader v1.0 | Développé avec Streamlit</small>
    </div>
    """,
    unsafe_allow_html=True
)

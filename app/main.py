"""
Application principale Tchad Langues AI
Interface gamifiée pour apprendre les langues du Tchad
"""

import streamlit as st
import yaml
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "config.yaml"

# Charger la configuration
@st.cache_data
def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Initialisation de la session
def init_session_state():
    """Initialise les variables de session"""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': '',
            'selected_language': None,
            'level': 1,
            'xp': 0,
            'streak': 0,
            'hearts': 5,
            'completed_lessons': []
        }
    
    if 'current_character' not in st.session_state:
        st.session_state.current_character = 'Neloumta'

# Styles CSS personnalisés
def load_custom_css():
    """Charge les styles CSS pour l'univers africain"""
    config = load_config()
    theme = config['app']['theme']
    
    st.markdown(f"""
    <style>
    .main {{
        background: linear-gradient(135deg, {theme['background_color']} 0%, #E8E8E8 100%);
    }}
    
    .app-header {{
        background: linear-gradient(135deg, {theme['primary_color']} 0%, {theme['accent_color']} 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }}
    
    .app-title {{
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .app-subtitle {{
        color: white;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }}
    
    .character-card {{
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid {theme['primary_color']};
    }}
    
    .stats-container {{
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    .stat-value {{
        font-size: 2rem;
        font-weight: bold;
        color: {theme['primary_color']};
    }}
    </style>
    """, unsafe_allow_html=True)

def display_header(config):
    """Affiche l'en-tête de l'application"""
    st.markdown(f"""
    <div class="app-header">
        <h1 class="app-title">{config['app']['title']}</h1>
        <p class="app-subtitle">{config['app']['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

def display_user_stats(profile):
    """Affiche les statistiques de l'utilisateur"""
    config = load_config()
    
    st.markdown(f"""
    <div class="stats-container">
        <div style="text-align: center;">
            <div class="stat-value">{profile['xp']} XP</div>
            <div style="color: #666; margin-top: 0.5rem;">Points d'expérience</div>
        </div>
        <div style="text-align: center;">
            <div class="stat-value">Niveau {profile['level']}</div>
            <div style="color: #666; margin-top: 0.5rem;">Ton niveau</div>
        </div>
        <div style="text-align: center;">
            <div class="stat-value">🔥 {profile['streak']}</div>
            <div style="color: #666; margin-top: 0.5rem;">Jours consécutifs</div>
        </div>
        <div style="text-align: center;">
            <div class="stat-value">❤️ {profile['hearts']}</div>
            <div style="color: #666; margin-top: 0.5rem;">Vies</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_character_greeting(character_name, characters):
    """Récupère le message de bienvenue d'un personnage"""
    for char in characters:
        if char['name'] == character_name:
            import random
            greetings = char.get('greetings', ['Bonjour !'])
            return random.choice(greetings)
    return "Bonjour !"

def display_character_message(character_name, message=None):
    """Affiche un message d'un personnage"""
    config = load_config()
    characters = config['characters']
    
    character = next((c for c in characters if c['name'] == character_name), None)
    if not character:
        return
    
    if message is None:
        message = get_character_greeting(character_name, characters)
    
    st.markdown(f"""
    <div style="background: white; border-radius: 15px; padding: 1.5rem; margin: 1.5rem 0; border-left: 5px solid {config['app']['theme']['accent_color']};">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-right: 1rem;">{character['avatar']}</div>
            <div>
                <div style="font-size: 1.3rem; font-weight: bold; color: {config['app']['theme']['primary_color']};">
                    {character['name']}
                </div>
                <div style="font-style: italic; color: #666;">
                    {character['description']}
                </div>
            </div>
        </div>
        <div style="font-size: 1.1rem; color: #333; line-height: 1.6;">{message}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Fonction principale"""
    st.set_page_config(
        page_title="Tchad Langues AI",
        page_icon="🇹🇩",
        layout="wide"
    )
    
    config = load_config()
    load_custom_css()
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🇹🇩 Tchad Langues AI")
        
        # Menu principal
        page = st.radio(
            "Navigation",
            ["🏠 Accueil", "📚 Apprendre", "👥 Personnages"]
        )
        
        st.markdown("---")
        
        # Profil utilisateur
        if not st.session_state.user_profile['name']:
            name = st.text_input("Entre ton prénom :")
            if name:
                st.session_state.user_profile['name'] = name
                st.rerun()
        else:
            st.success(f"👋 Bonjour {st.session_state.user_profile['name']} !")
            if st.button("Changer de nom"):
                st.session_state.user_profile['name'] = ''
                st.rerun()
        
        # Personnage actuel
        st.markdown("### Ton guide")
        character_names = [c['name'] for c in config['characters']]
        selected_char = st.selectbox(
            "Choisis ton personnage",
            character_names,
            index=character_names.index(st.session_state.current_character) if st.session_state.current_character in character_names else 0
        )
        st.session_state.current_character = selected_char
    
    # Contenu principal
    if page == "🏠 Accueil":
        display_header(config)
        
        if st.session_state.user_profile['name']:
            display_character_message(
                st.session_state.current_character,
                f"Bonjour {st.session_state.user_profile['name']} ! Bienvenue dans ton parcours d'apprentissage des langues du Tchad. Prêt(e) à commencer ?"
            )
        
        display_user_stats(st.session_state.user_profile)
        
        st.markdown("---")
        st.subheader("🎯 Choisis ta langue")
        
        languages = config['languages']
        cols = st.columns(2)
        
        for i, lang in enumerate(languages):
            with cols[i % 2]:
                if st.button(f"{lang['flag']} {lang['name']}", key=f"lang_{lang['code']}", use_container_width=True):
                    st.session_state.user_profile['selected_language'] = lang
                    st.rerun()
        
        if st.session_state.user_profile['selected_language']:
            lang = st.session_state.user_profile['selected_language']
            st.success(f"✅ Langue sélectionnée : {lang['name']} - {lang['description']}")
    
    elif page == "📚 Apprendre":
        display_header(config)
        
        if not st.session_state.user_profile['selected_language']:
            st.warning("⚠️ Sélectionne d'abord une langue dans l'Accueil !")
        else:
            lang = st.session_state.user_profile['selected_language']
            st.info(f"🌍 Tu apprends actuellement : **{lang['name']}** - {lang['description']}")
            
            st.subheader("📚 Tes leçons")
            lessons_structure = config['lessons']['structure']
            
            for level_info in lessons_structure:
                with st.expander(f"🌟 Niveau {level_info['level']}: {level_info['name']}"):
                    for lesson in level_info['lessons']:
                        is_completed = lesson in st.session_state.user_profile.get('completed_lessons', [])
                        if st.button(f"{'✅' if is_completed else '📖'} {lesson}", 
                                   key=f"lesson_{level_info['level']}_{lesson}"):
                            st.success(f"Leçon '{lesson}' sélectionnée ! (Les exercices seront disponibles bientôt)")
    
    elif page == "👥 Personnages":
        display_header(config)
        st.subheader("👥 Nos personnages")
        
        characters = config['characters']
        cols = st.columns(3)
        
        for i, char in enumerate(characters):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="character-card">
                    <div style="font-size: 4rem; text-align: center; margin-bottom: 1rem;">{char['avatar']}</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: {config['app']['theme']['primary_color']}; text-align: center; margin-bottom: 0.5rem;">
                        {char['name']}
                    </div>
                    <div style="text-align: center; color: #666; font-style: italic; margin-bottom: 1rem;">
                        {char['role'].replace('_', ' ').title()}
                    </div>
                    <div style="text-align: center; color: #333; font-size: 0.9rem;">
                        {char['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Afficher le message du personnage sélectionné
        selected_char_name = st.selectbox(
            "En savoir plus sur un personnage",
            [c['name'] for c in characters]
        )
        
        selected_char = next((c for c in characters if c['name'] == selected_char_name), None)
        if selected_char:
            display_character_message(
                selected_char['name'],
                get_character_greeting(selected_char['name'], characters)
            )

if __name__ == "__main__":
    main()


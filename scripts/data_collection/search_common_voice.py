"""
Script pour rechercher et télécharger des données depuis Mozilla Common Voice
"""

import requests
import json
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "common_voice"
CONFIG_FILE = BASE_DIR / "config.yaml"

def load_config():
    """Charge la configuration"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_data_dirs():
    """Crée les répertoires nécessaires"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def search_common_voice(language_code="sara"):
    """
    Recherche des données sur Common Voice
    
    Note: Common Voice utilise des codes de langue ISO 639-3
    Pour Sara, le code pourrait être 'sre' ou autre
    """
    print("Recherche de donnees sur Mozilla Common Voice...")
    print("URL: https://commonvoice.mozilla.org/")
    
    # Common Voice API (si disponible)
    # Note: L'API peut ne pas être publique, il faut vérifier
    
    languages_to_check = [
        "sara",  # Sara
        "sre",   # Code ISO possible pour Sara
        "fr",    # Français (pour comparaison)
    ]
    
    print("\nCodes de langue a verifier:")
    for lang in languages_to_check:
        print(f"  - {lang}")
    
    print("\nPour telecharger depuis Common Voice:")
    print("1. Va sur https://commonvoice.mozilla.org/")
    print("2. Recherche 'Sara' ou 'Chad'")
    print("3. Si des donnees existent, telecharge le dataset")
    print("4. Place les fichiers dans: data/raw/common_voice/")
    
    return None

def check_youtube_videos():
    """Vérifie s'il y a des vidéos YouTube utiles"""
    print("\n" + "="*50)
    print("Recherche sur YouTube")
    print("="*50)
    print("\nPour trouver des videos en langue Sara:")
    print("1. Recherche: 'langue sara tchad'")
    print("2. Recherche: 'apprendre sara'")
    print("3. Recherche: 'conte sara'")
    print("4. Recherche: 'chanson sara'")
    print("\nNote: Respecte les droits d'auteur!")
    print("Si autorise, tu peux extraire l'audio avec:")
    print("  - yt-dlp (outil en ligne de commande)")
    print("  - Puis transcrire avec Whisper")

def main():
    """Fonction principale"""
    create_data_dirs()
    
    print("="*50)
    print("Recherche de sources de donnees supplementaires")
    print("="*50)
    
    # Recherche Common Voice
    search_common_voice()
    
    # Suggestions YouTube
    check_youtube_videos()
    
    print("\n" + "="*50)
    print("Prochaines etapes:")
    print("="*50)
    print("1. Verifier Common Voice manuellement")
    print("2. Explorer YouTube pour videos")
    print("3. Preparer script d'enregistrement audio")
    print("4. Commencer a enregistrer ta voix")

if __name__ == "__main__":
    main()


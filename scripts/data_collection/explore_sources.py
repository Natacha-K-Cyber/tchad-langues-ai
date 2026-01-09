"""
Script pour explorer et rechercher d'autres sources de données
"""

import requests
from pathlib import Path
import json
import yaml
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
CONFIG_FILE = BASE_DIR / "config.yaml"

def load_config():
    """Charge la configuration"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_data_dirs():
    """Crée les répertoires nécessaires"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "exploration").mkdir(exist_ok=True)

def check_common_voice():
    """Vérifie Mozilla Common Voice"""
    print("="*60)
    print("1. MOZILLA COMMON VOICE")
    print("="*60)
    print("URL: https://commonvoice.mozilla.org/")
    print("\nActions:")
    print("  - Va sur https://commonvoice.mozilla.org/")
    print("  - Recherche 'Sara' ou 'Chad' dans les langues")
    print("  - Si disponible, télécharge le dataset")
    print("  - Format: CSV avec colonnes 'sentence', 'path', 'up_votes'")
    print("\nCodes de langue possibles:")
    print("  - 'sre' (Sara)")
    print("  - 'srr' (Serer)")
    print("  - Vérifie sur: https://commonvoice.mozilla.org/languages")
    
    # Essayer de vérifier via l'API (si disponible)
    try:
        # Note: L'API Common Voice peut nécessiter une clé
        print("\nTentative de vérification via API...")
        # API endpoint (à vérifier)
        # response = requests.get("https://commonvoice.mozilla.org/api/v1/languages")
        print("  (Vérification manuelle recommandée)")
    except:
        pass

def check_sil_international():
    """Vérifie SIL International"""
    print("\n" + "="*60)
    print("2. SIL INTERNATIONAL")
    print("="*60)
    print("URL: https://www.sil.org/")
    print("\nRessources:")
    print("  - Ethnologue: https://www.ethnologue.com/language/sre")
    print("  - Base de données de langues")
    print("  - Publications linguistiques")
    print("\nActions:")
    print("  - Recherche 'Sara' sur Ethnologue")
    print("  - Consulte les ressources linguistiques")
    print("  - Contacte SIL pour accès aux données")

def check_glottolog():
    """Vérifie Glottolog"""
    print("\n" + "="*60)
    print("3. GLOTTOLOG")
    print("="*60)
    print("URL: https://glottolog.org/")
    print("\nActions:")
    print("  - Va sur https://glottolog.org/")
    print("  - Recherche 'Sara' ou 'Central Sara'")
    print("  - Consulte les références bibliographiques")
    print("  - Note les codes de langue ISO 639-3")

def check_olac():
    """Vérifie OLAC (Open Language Archives Community)"""
    print("\n" + "="*60)
    print("4. OLAC - OPEN LANGUAGE ARCHIVES COMMUNITY")
    print("="*60)
    print("URL: http://www.language-archives.org/")
    print("\nActions:")
    print("  - Va sur http://www.language-archives.org/")
    print("  - Recherche 'Sara' ou 'Chad'")
    print("  - Explore les archives disponibles")
    print("  - Télécharge les ressources accessibles")

def check_youtube():
    """Guide pour YouTube"""
    print("\n" + "="*60)
    print("5. YOUTUBE")
    print("="*60)
    print("URL: https://www.youtube.com/")
    print("\nRecherches suggérées:")
    searches = [
        "langue sara tchad",
        "apprendre sara",
        "conte sara tchad",
        "chanson sara",
        "cours sara",
        "dialogue sara",
        "prononciation sara"
    ]
    for search in searches:
        print(f"  - '{search}'")
    
    print("\nOutils pour extraire l'audio:")
    print("  - yt-dlp: https://github.com/yt-dlp/yt-dlp")
    print("  - Installation: pip install yt-dlp")
    print("  - Usage: yt-dlp -x --audio-format wav URL_VIDEO")
    print("\nIMPORTANT:")
    print("  - Respecte les droits d'auteur")
    print("  - Vérifie les licences des vidéos")
    print("  - Demande permission si nécessaire")

def check_academic_sources():
    """Sources académiques"""
    print("\n" + "="*60)
    print("6. SOURCES ACADÉMIQUES")
    print("="*60)
    print("\nBases de données:")
    print("  - HAL (Archives ouvertes): https://hal.archives-ouvertes.fr/")
    print("  - Google Scholar: https://scholar.google.com/")
    print("  - ResearchGate: https://www.researchgate.net/")
    print("\nRecherches suggérées:")
    print("  - 'Sara language Chad'")
    print("  - 'Sara-Bagirmi languages'")
    print("  - 'Chad linguistics'")
    print("  - 'Central African languages'")
    print("\nTypes de documents:")
    print("  - Thèses et mémoires")
    print("  - Articles de revues linguistiques")
    print("  - Grammaires et dictionnaires")
    print("  - Corpus linguistiques")

def check_institutions():
    """Institutions à contacter"""
    print("\n" + "="*60)
    print("7. INSTITUTIONS À CONTACTER")
    print("="*60)
    print("\nTchad:")
    print("  - Université de N'Djamena (Département de linguistique)")
    print("  - Bibliothèque Nationale du Tchad")
    print("  - Ministère de l'Éducation")
    print("  - Centre de Recherche en Linguistique Appliquée (CERLA)")
    print("\nInternational:")
    print("  - SIL International (Bureau Tchad)")
    print("  - CNRS (Centre National de la Recherche Scientifique - France)")
    print("  - LLACAN (Langage, Langues et Cultures d'Afrique Noire)")
    print("\nOrganisations culturelles:")
    print("  - Associations de locuteurs Sara")
    print("  - Centres culturels tchadiens")
    print("  - Radio/Télévision nationale tchadienne")

def create_search_queries_file():
    """Crée un fichier avec toutes les recherches à faire"""
    queries = {
        "common_voice": {
            "url": "https://commonvoice.mozilla.org/",
            "searches": ["Sara", "Chad", "sre"],
            "actions": "Vérifier disponibilité et télécharger dataset"
        },
        "youtube": {
            "url": "https://www.youtube.com/",
            "searches": [
                "langue sara tchad",
                "apprendre sara",
                "conte sara tchad",
                "chanson sara",
                "cours sara",
                "dialogue sara"
            ],
            "actions": "Extraire audio avec yt-dlp, transcrire avec Whisper"
        },
        "academic": {
            "urls": [
                "https://hal.archives-ouvertes.fr/",
                "https://scholar.google.com/",
                "https://www.researchgate.net/"
            ],
            "searches": [
                "Sara language Chad",
                "Sara-Bagirmi languages",
                "Chad linguistics",
                "Central African languages"
            ],
            "actions": "Télécharger PDFs, extraire texte"
        },
        "institutions": {
            "contacts": [
                "Université de N'Djamena",
                "SIL International",
                "Bibliothèque Nationale du Tchad"
            ],
            "actions": "Contacter pour accès aux ressources"
        }
    }
    
    output_file = DATA_DIR / "exploration" / "search_queries.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(queries, f, ensure_ascii=False, indent=2)
    
    print(f"\nOK - Fichier de recherches sauvegarde: {output_file}")

def main():
    """Fonction principale"""
    create_data_dirs()
    
    print("\n" + "="*60)
    print("EXPLORATION DES SOURCES DE DONNÉES")
    print("="*60)
    print("\nCe script te guide pour trouver d'autres sources de données")
    print("pour enrichir ton corpus d'entraînement.\n")
    
    # Afficher toutes les sources
    check_common_voice()
    check_sil_international()
    check_glottolog()
    check_olac()
    check_youtube()
    check_academic_sources()
    check_institutions()
    
    # Créer le fichier de recherches
    create_search_queries_file()
    
    print("\n" + "="*60)
    print("PROCHAINES ÉTAPES")
    print("="*60)
    print("\n1. Explore chaque source listée ci-dessus")
    print("2. Note ce que tu trouves dans: data/raw/exploration/")
    print("3. Télécharge les données disponibles")
    print("4. Organise les fichiers par source")
    print("\nAstuce: Commence par Common Voice et YouTube,")
    print("   ce sont les plus accessibles!")

if __name__ == "__main__":
    main()


"""
Script pour préparer un guide d'enregistrement audio
Crée une liste de mots et phrases à enregistrer
"""

import json
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "audio_recordings"
CONFIG_FILE = BASE_DIR / "config.yaml"

def load_config():
    """Charge la configuration"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_data_dirs():
    """Crée les répertoires nécessaires"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "words").mkdir(exist_ok=True)
    (DATA_DIR / "phrases").mkdir(exist_ok=True)
    (DATA_DIR / "dialogues").mkdir(exist_ok=True)

def create_recording_script():
    """Crée un script d'enregistrement avec mots et phrases"""
    
    # Vocabulaire de base à enregistrer
    words_to_record = {
        "greetings": [
            {"french": "bonjour", "sara": "mbay", "phonetic": "mbaj"},
            {"french": "bonsoir", "sara": "mbay kire", "phonetic": "mbaj kiɾe"},
            {"french": "salut", "sara": "ay", "phonetic": "aj"},
            {"french": "au revoir", "sara": "ay bee", "phonetic": "aj be"},
            {"french": "merci", "sara": "salaama", "phonetic": "salaːma"},
        ],
        "numbers": [
            {"french": "un", "sara": "mbe", "phonetic": "mbe"},
            {"french": "deux", "sara": "ndo", "phonetic": "ndo"},
            {"french": "trois", "sara": "ndo", "phonetic": "ndo"},
            # Ajouter plus selon tes connaissances
        ],
        "family": [
            {"french": "père", "sara": "ba", "phonetic": "ba"},
            {"french": "mère", "sara": "ma", "phonetic": "ma"},
            {"french": "frère", "sara": "biri", "phonetic": "biɾi"},
        ]
    }
    
    # Phrases à enregistrer
    phrases_to_record = [
        {
            "french": "Comment allez-vous ?",
            "sara": "kede yo",
            "phonetic": "kede jo",
            "translation": "How are you?"
        },
        {
            "french": "Je vais bien, merci",
            "sara": "jam jam",
            "phonetic": "dʒam dʒam",
            "translation": "I'm fine, thanks"
        },
        {
            "french": "Quel est votre nom ?",
            "sara": "kede nga",
            "phonetic": "kede ŋa",
            "translation": "What is your name?"
        },
        # Ajouter plus de phrases
    ]
    
    # Dialogues courts
    dialogues_to_record = [
        {
            "title": "Salutation",
            "lines": [
                {"speaker": "A", "french": "Bonjour", "sara": "mbay", "phonetic": "mbaj"},
                {"speaker": "B", "french": "Bonjour, comment allez-vous ?", "sara": "mbay, kede yo", "phonetic": "mbaj, kede jo"},
                {"speaker": "A", "french": "Je vais bien, merci", "sara": "jam jam", "phonetic": "dʒam dʒam"},
            ]
        }
    ]
    
    # Sauvegarder les scripts
    script = {
        "words": words_to_record,
        "phrases": phrases_to_record,
        "dialogues": dialogues_to_record,
        "instructions": {
            "format": "WAV ou MP3, 16kHz minimum",
            "quality": "Haute qualité, pas de bruit de fond",
            "pronunciation": "Prononcer naturellement, comme dans une conversation",
            "repetitions": "Enregistrer chaque mot/phrase 3 fois pour variabilité"
        }
    }
    
    output_file = DATA_DIR / "recording_script.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(script, f, ensure_ascii=False, indent=2)
    
    print(f"Script d'enregistrement cree: {output_file}")
    print(f"\nTotal a enregistrer:")
    total_words = sum(len(words) for words in words_to_record.values())
    print(f"  - Mots: {total_words} (x3 repetitions = {total_words * 3})")
    print(f"  - Phrases: {len(phrases_to_record)} (x3 repetitions = {len(phrases_to_record) * 3})")
    print(f"  - Dialogues: {len(dialogues_to_record)}")
    
    return script

def create_recording_guide():
    """Crée un guide d'enregistrement"""
    guide = """
# Guide d'enregistrement audio pour Tchad Langues AI

## Matériel nécessaire
- Microphone de bonne qualité (ou smartphone)
- Logiciel d'enregistrement (Audacity gratuit)
- Environnement calme (peu de bruit de fond)

## Format d'enregistrement
- Format: WAV (non compressé) ou MP3 haute qualité
- Fréquence d'échantillonnage: 16 kHz minimum (44.1 kHz recommandé)
- Mono ou stéréo: Mono suffit
- Durée: 1-3 secondes pour mots, 3-10 secondes pour phrases

## Instructions
1. Lis le mot/phrase en français d'abord
2. Pause de 1 seconde
3. Prononce le mot/phrase en Sara
4. Pause de 2 secondes avant le suivant

## Structure des fichiers
- Mots: `word_[french]_[sara].wav` (ex: word_bonjour_mbay.wav)
- Phrases: `phrase_[number].wav` (ex: phrase_001.wav)
- Dialogues: `dialogue_[title]_[line].wav`

## Qualité
- Prononciation claire et naturelle
- Pas de bruit de fond
- Volume constant
- Pas de coupures ou d'erreurs

## Répétitions
Enregistre chaque élément 3 fois pour avoir de la variabilité:
- word_bonjour_mbay_001.wav
- word_bonjour_mbay_002.wav
- word_bonjour_mbay_003.wav
"""
    
    guide_file = DATA_DIR / "RECORDING_GUIDE.md"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(f"Guide cree: {guide_file}")

def main():
    """Fonction principale"""
    create_data_dirs()
    
    print("="*50)
    print("Preparation du script d'enregistrement audio")
    print("="*50)
    
    script = create_recording_script()
    create_recording_guide()
    
    print("\n" + "="*50)
    print("Prochaines etapes:")
    print("="*50)
    print("1. Ouvre le fichier: data/raw/audio_recordings/recording_script.json")
    print("2. Lis le guide: data/raw/audio_recordings/RECORDING_GUIDE.md")
    print("3. Installe Audacity: https://www.audacityteam.org/")
    print("4. Commence a enregistrer selon le script")
    print("\nAstuce: Tu peux enrichir le script avec plus de mots/phrases!")

if __name__ == "__main__":
    main()


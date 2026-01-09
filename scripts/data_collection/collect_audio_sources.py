"""
Script pour collecter et intégrer des sources audio pour la prononciation
Recherche et organise les ressources audio pour les langues du Tchad
"""

import json
from pathlib import Path
import yaml
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "audio_sources"
CONFIG_FILE = BASE_DIR / "config.yaml"

def load_config():
    """Charge la configuration"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_dirs():
    """Crée les répertoires nécessaires"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "youtube").mkdir(exist_ok=True)
    (DATA_DIR / "common_voice").mkdir(exist_ok=True)
    (DATA_DIR / "recordings").mkdir(exist_ok=True)

def create_audio_collection_plan():
    """Crée un plan de collecte audio structuré"""
    
    plan = {
        "sources": {
            "youtube": {
                "description": "Vidéos YouTube avec audio en langue Sara",
                "search_queries": [
                    "langue sara tchad",
                    "apprendre sara",
                    "conte sara tchad",
                    "chanson sara",
                    "dialogue sara",
                    "prononciation sara",
                    "cours sara tchad",
                    "sara language chad"
                ],
                "tools": {
                    "yt-dlp": "pip install yt-dlp",
                    "usage": "yt-dlp -x --audio-format wav URL_VIDEO"
                },
                "output_dir": str(DATA_DIR / "youtube")
            },
            "common_voice": {
                "description": "Mozilla Common Voice - Dataset audio open source",
                "url": "https://commonvoice.mozilla.org/",
                "languages_to_check": ["sara", "sre", "chad"],
                "output_dir": str(DATA_DIR / "common_voice")
            },
            "manual_recordings": {
                "description": "Enregistrements manuels (ta voix ou locuteurs natifs)",
                "script": "python scripts/data_collection/prepare_audio_recording.py",
                "output_dir": str(DATA_DIR / "recordings")
            },
            "shtooka": {
                "description": "Shtooka Project - Collections d'enregistrements",
                "url": "https://shtooka.net/",
                "output_dir": str(DATA_DIR / "shtooka")
            }
        },
        "audio_requirements": {
            "format": "WAV (non compressé) ou MP3 haute qualité",
            "sample_rate": "16 kHz minimum (44.1 kHz recommandé)",
            "channels": "Mono",
            "duration": {
                "words": "1-3 secondes",
                "phrases": "3-10 secondes",
                "dialogues": "10-30 secondes"
            }
        },
        "processing_steps": [
            "1. Collecter les fichiers audio",
            "2. Transcrire avec Whisper (OpenAI)",
            "3. Aligner audio-transcription",
            "4. Extraire les features audio (MFCC, spectrogrammes)",
            "5. Créer dataset audio-text pour entraînement"
        ]
    }
    
    return plan

def create_whisper_transcription_script():
    """Crée un script pour transcrire l'audio avec Whisper"""
    
    script_content = """#!/usr/bin/env python3
\"\"\"
Script pour transcrire les fichiers audio avec Whisper
Installe Whisper : pip install openai-whisper
\"\"\"

import whisper
from pathlib import Path
import json

# Charger le modèle Whisper
print("Chargement du modele Whisper...")
model = whisper.load_model("base")  # ou "small", "medium" selon la RAM

# Dossier avec les fichiers audio
audio_dir = Path("data/raw/audio_sources")
output_file = Path("data/processed/audio_transcriptions.json")

transcriptions = []

# Parcourir les fichiers audio
for audio_file in audio_dir.rglob("*.wav"):
    print(f"Transcription de {audio_file}...")
    result = model.transcribe(str(audio_file), language="fr")
    
    transcriptions.append({
        "audio_file": str(audio_file),
        "text": result["text"],
        "language": result["language"],
        "segments": result.get("segments", [])
    })

# Sauvegarder
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(transcriptions, f, ensure_ascii=False, indent=2)

print(f"Transcriptions sauvegardees : {output_file}")
"""
    
    script_path = BASE_DIR / "scripts" / "data_processing" / "transcribe_audio.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return script_path

def main():
    """Fonction principale"""
    create_dirs()
    
    print("="*60)
    print("Plan de collecte audio pour prononciation et intonations")
    print("="*60)
    
    # Créer le plan
    plan = create_audio_collection_plan()
    
    # Sauvegarder le plan
    plan_file = DATA_DIR / "audio_collection_plan.json"
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print(f"\nPlan sauvegarde : {plan_file}")
    
    # Créer le script Whisper
    whisper_script = create_whisper_transcription_script()
    print(f"Script Whisper cree : {whisper_script}")
    
    print("\n" + "="*60)
    print("Sources audio identifiees :")
    print("="*60)
    
    for source_name, source_info in plan['sources'].items():
        print(f"\n{source_name.upper()}:")
        print(f"  {source_info['description']}")
        if 'search_queries' in source_info:
            print(f"  Recherches YouTube : {len(source_info['search_queries'])} requetes")
        print(f"  Dossier : {source_info['output_dir']}")
    
    print("\n" + "="*60)
    print("Prochaines etapes :")
    print("="*60)
    print("1. Installer yt-dlp : pip install yt-dlp")
    print("2. Installer Whisper : pip install openai-whisper")
    print("3. Télécharger des vidéos YouTube avec audio Sara")
    print("4. Transcrire avec Whisper")
    print("5. Intégrer dans le dataset d'entraînement")

if __name__ == "__main__":
    main()


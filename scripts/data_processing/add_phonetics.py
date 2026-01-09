"""
Script pour ajouter des transcriptions phonétiques (IPA) aux données
"""

import json
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_FILE = BASE_DIR / "config.yaml"

def load_config():
    """Charge la configuration"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_phonetic_mapping():
    """
    Crée un mapping des sons Sara vers IPA
    Note: À compléter avec tes connaissances ou un linguiste
    """
    phonetic_map = {
        # Consonnes
        "b": "b",
        "B": "ɓ",  # Implosive bilabiale
        "d": "d",
        "d'": "ɗ",  # Implosive alvéolaire
        "g": "g",
        "h": "h",
        "j": "dʒ",
        "k": "k",
        "l": "l",
        "m": "m",
        "n": "n",
        "ng": "ŋ",
        "nj": "ɲ",
        "p": "p",
        "r": "r",
        "s": "s",
        "t": "t",
        "w": "w",
        "y": "j",
        "č": "tʃ",
        
        # Voyelles
        "a": "a",
        "e": "e",
        "i": "i",
        "o": "o",
        "u": "u",
        "ə": "ə",
        "±": "ɨ",  # Barred i
        
        # Voyelles nasales (approximation)
        "ã": "ã",
        "ẽ": "ẽ",
        "ĩ": "ĩ",
        "õ": "õ",
        "ũ": "ũ",
    }
    
    return phonetic_map

def text_to_phonetic(text, phonetic_map):
    """
    Convertit un texte Sara en transcription phonétique approximative
    Note: C'est une approximation basique, idéalement fait par un linguiste
    """
    # Normaliser le texte
    text = text.lower().strip()
    
    # Remplacer selon le mapping
    phonetic = text
    for char, ipa in sorted(phonetic_map.items(), key=lambda x: -len(x[0])):
        phonetic = phonetic.replace(char, ipa)
    
    return phonetic

def process_vocabulary():
    """Traite le vocabulaire et ajoute la phonétique"""
    # Charger le vocabulaire existant (si disponible)
    vocab_file = DATA_DIR / "processed" / "vocabulary.json"
    
    if not vocab_file.exists():
        print("Aucun fichier de vocabulaire trouve.")
        print("Execute d'abord: python scripts/data_processing/prepare_corpus.py")
        return
    
    with open(vocab_file, 'r', encoding='utf-8') as f:
        vocabulary = json.load(f)
    
    phonetic_map = create_phonetic_mapping()
    
    # Ajouter la phonétique à chaque entrée
    for entry in vocabulary:
        if 'sara' in entry:
            entry['phonetic'] = text_to_phonetic(entry['sara'], phonetic_map)
    
    # Sauvegarder
    output_file = DATA_DIR / "processed" / "vocabulary_with_phonetics.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)
    
    print(f"Vocabulaire avec phonetique sauvegarde: {output_file}")
    print(f"Total d'entrees: {len(vocabulary)}")

def main():
    """Fonction principale"""
    print("="*50)
    print("Ajout de transcriptions phonetiques (IPA)")
    print("="*50)
    print("\nNote: Ce script utilise un mapping basique.")
    print("Pour une meilleure precision, consulte un linguiste")
    print("ou utilise des outils specialises comme Praat.\n")
    
    process_vocabulary()
    
    print("\n" + "="*50)
    print("Ressources pour la phonetique:")
    print("="*50)
    print("- IPA Chart: https://www.internationalphoneticassociation.org/content/ipa-chart")
    print("- Praat: https://www.fon.hum.uva.nl/praat/")
    print("- Phonemizer: https://github.com/bootphon/phonemizer")

if __name__ == "__main__":
    main()


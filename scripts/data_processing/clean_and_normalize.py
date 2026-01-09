"""
Script de nettoyage et normalisation linguistique des données
Option 1 : Nettoyage & normalisation avant l'entraînement
"""

import json
from pathlib import Path
import re
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
TRAINING_DIR = DATA_DIR / "training"
PROCESSED_DIR = DATA_DIR / "processed"

def load_training_data():
    """Charge les données d'entraînement brutes"""
    # Essayer d'abord le fichier des entrées brutes du lexique
    raw_entries_file = TRAINING_DIR / "lexicon_entries_raw.json"
    
    if raw_entries_file.exists():
        print(f"   Chargement depuis : {raw_entries_file}")
        with open(raw_entries_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Sinon, essayer le fichier training_data.json (format instruction/input/output)
    training_file = TRAINING_DIR / "training_data.json"
    
    if training_file.exists():
        print(f"   Chargement depuis : {training_file}")
        with open(training_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Convertir le format instruction/input/output vers french/sara_variants
            if data and isinstance(data[0], dict) and 'input' in data[0]:
                print("   Conversion du format instruction/input/output...")
                converted = []
                seen = set()
                for entry in data:
                    french = entry.get('input', '').strip()
                    sara = entry.get('output', '').strip()
                    if french and sara and french not in seen:
                        seen.add(french)
                        converted.append({
                            'french': french,
                            'sara_variants': [sara]
                        })
                return converted
            return data
    
    print(f"ERREUR - Aucun fichier trouve dans {TRAINING_DIR}")
    print("Execute d'abord : python scripts/data_processing/prepare_training_data.py")
    return None

def clean_text(text):
    """
    Nettoie un texte :
    - Enlève les espaces multiples
    - Normalise les caractères spéciaux
    - Enlève les caractères de contrôle
    """
    if not text:
        return ""
    
    # Enlever les caractères de contrôle (sauf sauts de ligne et tabulations)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normaliser les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    
    # Enlever les espaces en début/fin
    text = text.strip()
    
    return text

def normalize_sara_word(word):
    """
    Normalise un mot Sara :
    - Enlève les espaces
    - Normalise les caractères spéciaux
    - Vérifie la longueur minimale
    """
    if not word:
        return None
    
    # Convertir en string si ce n'est pas déjà le cas
    if not isinstance(word, str):
        word = str(word)
    
    # Nettoyer
    word = word.strip()
    
    # Enlever les caractères parasites en début/fin seulement
    word = re.sub(r'^[,:;\s]+|[,:;\s]+$', '', word)
    
    # Vérifier la longueur minimale (au moins 1 caractère)
    if len(word) < 1:
        return None
    
    return word

def normalize_french_word(word):
    """
    Normalise un mot français :
    - Enlève les caractères parasites
    - Normalise la casse si nécessaire
    """
    if not word:
        return None
    
    # Nettoyer
    word = word.strip()
    word = re.sub(r'^\d+\s+', '', word)  # Enlever numéros de page
    
    # Enlever les caractères parasites en début/fin
    word = re.sub(r'^[,:;.\s()]+|[,:;.\s()]+$', '', word)
    
    # Vérifier la longueur minimale
    if len(word) < 1:
        return None
    
    return word

def validate_entry(entry):
    """
    Valide une entrée :
    - Vérifie que le français existe
    - Vérifie qu'il y a au moins une traduction Sara
    - Vérifie les longueurs raisonnables
    """
    french = entry.get('french', '')
    if not isinstance(french, str):
        french = str(french)
    french = french.strip()
    
    sara_variants = entry.get('sara_variants', [])
    if not isinstance(sara_variants, list):
        return False
    
    # Vérifier le français
    if not french or len(french) < 1 or len(french) > 300:
        return False
    
    # Vérifier qu'il y a au moins une traduction Sara valide
    valid_sara = []
    for s in sara_variants:
        if not s:
            continue
        if not isinstance(s, str):
            s = str(s)
        s_clean = s.strip()
        if len(s_clean) > 0 and len(s_clean) < 150:
            valid_sara.append(s_clean)
    
    if not valid_sara:
        return False
    
    return True

def normalize_entries(entries):
    """
    Normalise toutes les entrées :
    - Nettoie le texte
    - Normalise les mots français et Sara
    - Valide les entrées
    - Enlève les doublons
    """
    normalized = []
    seen = set()  # Pour détecter les doublons
    
    print("\nNettoyage et normalisation...")
    
    for entry in tqdm(entries, desc="Normalisation"):
        # Vérifier que c'est un dictionnaire
        if not isinstance(entry, dict):
            continue
        
        # Nettoyer le français
        french_raw = entry.get('french', '')
        if not french_raw:
            continue
        
        french = normalize_french_word(french_raw)
        if not french:
            continue
        
        # Nettoyer les variantes Sara
        sara_variants_raw = entry.get('sara_variants', [])
        if not isinstance(sara_variants_raw, list):
            continue
        
        normalized_sara = []
        for variant in sara_variants_raw:
            normalized_v = normalize_sara_word(variant)
            if normalized_v and normalized_v not in normalized_sara:
                normalized_sara.append(normalized_v)
        
        if not normalized_sara:
            continue
        
        # Créer l'entrée normalisée
        normalized_entry = {
            'french': french,
            'sara_variants': normalized_sara
        }
        
        # Vérifier la validité
        if not validate_entry(normalized_entry):
            continue
        
        # Détecter les doublons (même français)
        entry_key = french.lower()
        if entry_key not in seen:
            seen.add(entry_key)
            normalized.append(normalized_entry)
    
    return normalized

def create_statistics(entries):
    """Crée des statistiques sur les données"""
    stats = {
        'total_entries': len(entries),
        'total_sara_words': sum(len(e.get('sara_variants', [])) for e in entries),
        'avg_variants_per_word': 0,
        'french_words': [e.get('french', '') for e in entries],
        'sara_words': []
    }
    
    # Collecter tous les mots Sara
    for entry in entries:
        stats['sara_words'].extend(entry.get('sara_variants', []))
    
    if stats['total_entries'] > 0:
        stats['avg_variants_per_word'] = stats['total_sara_words'] / stats['total_entries']
    
    return stats

def main():
    """Fonction principale"""
    print("="*60)
    print("Nettoyage et normalisation linguistique")
    print("="*60)
    
    # Charger les données brutes
    print("\n[1/4] Chargement des donnees brutes...")
    entries = load_training_data()
    
    if not entries:
        return
    
    print(f"   {len(entries)} entrees chargees")
    
    # Normaliser
    print("\n[2/4] Normalisation des entrees...")
    normalized = normalize_entries(entries)
    print(f"   {len(normalized)} entrees valides apres normalisation")
    
    # Statistiques
    print("\n[3/4] Calcul des statistiques...")
    stats = create_statistics(normalized)
    print(f"   Total entrees : {stats['total_entries']}")
    print(f"   Total mots Sara : {stats['total_sara_words']}")
    print(f"   Moyenne variantes par mot : {stats['avg_variants_per_word']:.2f}")
    
    # Sauvegarder les données nettoyées
    print("\n[4/4] Sauvegarde des donnees nettoyees...")
    output_file = TRAINING_DIR / "training_data_cleaned.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)
    
    # Sauvegarder les statistiques
    stats_file = TRAINING_DIR / "statistics.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\nOK - Donnees nettoyees sauvegardees : {output_file}")
    print(f"OK - Statistiques sauvegardees : {stats_file}")
    
    print(f"\n" + "="*60)
    print("Nettoyage termine !")
    print("="*60)
    print(f"\nDonnees pretes pour l'entrainement :")
    print(f"   - {len(normalized)} entrees valides")
    print(f"   - {stats['total_sara_words']} traductions Sara")
    print(f"\nProchaine etape : Entrainement du modele")

if __name__ == "__main__":
    main()


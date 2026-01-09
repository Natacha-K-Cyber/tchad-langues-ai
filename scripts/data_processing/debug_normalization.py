"""
Script de debug pour comprendre pourquoi la normalisation rejette tout
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
TRAINING_DIR = BASE_DIR / "data" / "training"

def load_training_data():
    """Charge les données d'entraînement brutes"""
    training_file = TRAINING_DIR / "training_data.json"
    
    with open(training_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    """Affiche des exemples pour comprendre le problème"""
    
    entries = load_training_data()
    
    print(f"Total entrees : {len(entries)}")
    print("\n" + "="*60)
    print("Premieres 10 entrees :")
    print("="*60)
    
    for i, entry in enumerate(entries[:10], 1):
        print(f"\n--- Entree {i} ---")
        print(f"Francais : {repr(entry.get('french', ''))}")
        print(f"Type : {type(entry.get('french', ''))}")
        print(f"Longueur : {len(entry.get('french', ''))}")
        print(f"Sara variants : {entry.get('sara_variants', [])}")
        print(f"Type sara_variants : {type(entry.get('sara_variants', []))}")
        print(f"Nombre de variants : {len(entry.get('sara_variants', []))}")
        
        # Tester la normalisation
        french = entry.get('french', '').strip()
        sara_variants = entry.get('sara_variants', [])
        
        print(f"\nApres strip:")
        print(f"  Francais : {repr(french)}")
        print(f"  Longueur : {len(french)}")
        print(f"  Variants : {[repr(v) for v in sara_variants[:3]]}")

if __name__ == "__main__":
    main()


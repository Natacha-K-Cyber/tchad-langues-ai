"""
Vérifier le format réel du fichier training_data.json
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
TRAINING_DIR = BASE_DIR / "data" / "training"

def main():
    training_file = TRAINING_DIR / "training_data.json"
    
    with open(training_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Type de donnees : {type(data)}")
    print(f"Nombre d'elements : {len(data)}")
    
    if len(data) > 0:
        print(f"\nPremier element :")
        print(f"Type : {type(data[0])}")
        print(f"Contenu : {data[0]}")
        
        print(f"\nClefs disponibles : {list(data[0].keys()) if isinstance(data[0], dict) else 'N/A'}")
        
        # Chercher des entrées avec du contenu
        print(f"\nRecherche d'entrees avec contenu...")
        for i, entry in enumerate(data[:100]):
            if isinstance(entry, dict):
                if entry.get('french') or entry.get('input') or entry.get('instruction'):
                    print(f"\nEntree {i} avec contenu :")
                    print(json.dumps(entry, indent=2, ensure_ascii=False))
                    break

if __name__ == "__main__":
    main()


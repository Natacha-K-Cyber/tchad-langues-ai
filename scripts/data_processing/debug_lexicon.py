"""
Script pour déboguer et voir le format réel des données extraites
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def main():
    """Affiche un échantillon des données pour comprendre le format"""
    
    # Charger les sections
    sections_file = PROCESSED_DIR / "morkeg_lexicon_sections.json"
    
    if not sections_file.exists():
        print(f"ERREUR - Fichier introuvable : {sections_file}")
        return
    
    with open(sections_file, 'r', encoding='utf-8') as f:
        sections = json.load(f)
    
    print("="*60)
    print("DEBUG - Format des donnees extraites")
    print("="*60)
    
    # Afficher un échantillon de la section Français-Sara
    if sections.get('french_sara'):
        text = sections['french_sara']
        print(f"\nLongueur totale : {len(text)} caracteres")
        print(f"\nPremieres 2000 caracteres :")
        print("-"*60)
        print(text[:2000])
        print("-"*60)
        
        # Chercher des patterns
        print(f"\nRecherche de patterns...")
        lines = text.split('\n')
        print(f"Nombre de lignes : {len(lines)}")
        
        # Chercher des lignes avec des mots
        word_lines = [l for l in lines[:100] if len(l.strip()) > 5 and len(l.strip()) < 200]
        print(f"\nPremieres lignes avec du contenu ({len(word_lines)} premieres) :")
        for i, line in enumerate(word_lines[:20], 1):
            print(f"{i:2d}. {line[:100]}")
    
    # Afficher aussi les pages brutes
    pages_file = PROCESSED_DIR / "morkeg_raw_pages.json"
    if pages_file.exists():
        print(f"\n\n" + "="*60)
        print("Echantillon des pages brutes")
        print("="*60)
        
        with open(pages_file, 'r', encoding='utf-8') as f:
            pages = json.load(f)
        
        # Afficher quelques pages
        for i, page in enumerate(pages[:3], 1):
            print(f"\n--- Page {page['page_num']} ---")
            print(page['text'][:500])
            print("...")

if __name__ == "__main__":
    main()


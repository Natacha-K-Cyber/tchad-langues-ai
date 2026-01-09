"""
Script pour préparer les données extraites pour l'entraînement du modèle
Convertit les lexiques en format adapté pour le fine-tuning
"""

import json
from pathlib import Path
import re
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
TRAINING_DIR = DATA_DIR / "training"

def create_dirs():
    """Crée les répertoires nécessaires"""
    TRAINING_DIR.mkdir(parents=True, exist_ok=True)

def parse_lexicon_entries(text):
    """
    Parse les entrées du lexique depuis le texte extrait
    Format attendu: Mot français | Mot Sara (variantes)
    """
    entries = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
        
        # Chercher des patterns comme "mot français | mot sara1 | mot sara2"
        # Ou "mot français    mot sara" (séparés par plusieurs espaces)
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2:
                entries.append({
                    'french': parts[0],
                    'sara_variants': parts[1:] if len(parts) > 1 else []
                })
        elif re.match(r'^[A-Za-zÀ-ÿ]+\s{2,}[A-Za-zÀ-ÿ]', line):
            # Séparés par plusieurs espaces
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 2:
                entries.append({
                    'french': parts[0],
                    'sara_variants': parts[1:]
                })
    
    return entries

def create_training_examples(entries, max_examples=1000):
    """
    Crée des exemples d'entraînement au format conversationnel
    Format pour instruction fine-tuning
    """
    training_examples = []
    
    for entry in tqdm(entries[:max_examples], desc="Creation exemples"):
        french = entry.get('french', '').strip()
        sara_variants = entry.get('sara_variants', [])
        
        if not french or not sara_variants:
            continue
        
        # Prendre la première variante Sara comme principale
        sara = sara_variants[0].strip() if sara_variants else ''
        
        if not sara:
            continue
        
        # Créer différents types d'exemples
        
        # 1. Traduction directe
        training_examples.append({
            'instruction': 'Traduis ce mot en langue Sara.',
            'input': french,
            'output': sara
        })
        
        # 2. Question-réponse
        training_examples.append({
            'instruction': 'Comment dit-on ce mot en Sara ?',
            'input': french,
            'output': f'En Sara, "{french}" se dit "{sara}".'
        })
        
        # 3. Explication
        if len(sara_variants) > 1:
            variants = ', '.join(sara_variants[1:3])  # Limiter à 2 variantes
            training_examples.append({
                'instruction': 'Donne la traduction et les variantes.',
                'input': french,
                'output': f'"{french}" en Sara : {sara}. Variantes : {variants}.'
            })
    
    return training_examples

def load_lexicon_sections():
    """Charge les sections de lexique extraites"""
    sections_file = PROCESSED_DIR / "morkeg_lexicon_sections.json"
    
    if not sections_file.exists():
        print(f"ERREUR - Fichier introuvable : {sections_file}")
        print("Execute d'abord : python scripts/data_processing/extract_pdf_text.py")
        return None
    
    with open(sections_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    """Fonction principale"""
    create_dirs()
    
    print("="*60)
    print("Preparation des donnees pour l'entrainement")
    print("="*60)
    
    # Charger les sections de lexique
    print("\n[1/4] Chargement des sections de lexique...")
    sections = load_lexicon_sections()
    
    if not sections:
        return
    
    all_entries = []
    
    # Traiter la section Français-Sara
    if sections.get('french_sara'):
        print("\n[2/4] Traitement de la section Français-Sara...")
        entries = parse_lexicon_entries(sections['french_sara'])
        print(f"   {len(entries)} entrees trouvees")
        all_entries.extend(entries)
    
    # Traiter la section English-Sara
    if sections.get('english_sara'):
        print("\n[3/4] Traitement de la section English-Sara...")
        entries = parse_lexicon_entries(sections['english_sara'])
        print(f"   {len(entries)} entrees trouvees")
        all_entries.extend(entries)
    
    print(f"\nTotal d'entrees : {len(all_entries)}")
    
    # Créer les exemples d'entraînement
    print("\n[4/4] Creation des exemples d'entrainement...")
    training_examples = create_training_examples(all_entries, max_examples=2000)
    
    print(f"   {len(training_examples)} exemples crees")
    
    # Sauvegarder les données d'entraînement
    output_file = TRAINING_DIR / "training_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_examples, f, ensure_ascii=False, indent=2)
    
    print(f"\nOK - Donnees d'entrainement sauvegardees : {output_file}")
    
    # Statistiques
    print(f"\nStatistiques:")
    print(f"   Entrees de lexique : {len(all_entries)}")
    print(f"   Exemples d'entrainement : {len(training_examples)}")
    print(f"   Fichier cree : {output_file}")
    
    print(f"\nOK - Preparation terminee !")
    print(f"   Tu peux maintenant entrainer le modele !")

if __name__ == "__main__":
    main()


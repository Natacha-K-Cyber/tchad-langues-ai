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
    Format réel: CodeLangue=mot : CodeLangue=mot mot_français
    Exemple: Beb=mbô : Bd=rû Beb=màs , Bd=màs , à côté de
    """
    entries = []
    lines = text.split('\n')
    
    # Codes de langues Sara (abréviations)
    sara_codes = ['Beb', 'Bd', 'Gor', 'Gu', 'Kbb', 'Db', 'Mb', 'Mo', 'Nar', 'KbN', 'NgT', 'Ngb', 'Sr', 'Lk', 'Kul']
    
    current_french = None
    current_sara_variants = []
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
        
        # Ignorer les lignes d'en-tête
        if 'Lexique' in line or 'Introduction' in line or line.startswith('Page'):
            continue
        
        # Pattern 1: Ligne avec codes de langues (ex: Beb=mbô : Bd=rû mot_français)
        # Chercher les codes de langues avec =
        sara_matches = re.findall(r'([A-Z][a-z]?[A-Z]?)=([^:,\n]+)', line)
        
        if sara_matches:
            # Extraire les mots Sara
            sara_words = []
            for code, word in sara_matches:
                word = word.strip().rstrip(',').strip()
                if word and code in sara_codes:
                    sara_words.append(word)
            
            # Extraire le mot français (généralement à la fin de la ligne)
            # Chercher après les codes de langues
            french_match = re.search(r'(?:' + '|'.join(sara_codes) + r'=[^:,\n]+[:\s,]*)+(.+)$', line)
            if french_match:
                french = french_match.group(1).strip().rstrip(',').strip()
                # Nettoyer le français (enlever les codes restants)
                french = re.sub(r'[A-Z][a-z]?[A-Z]?=[^:,\s]+', '', french).strip()
                french = re.sub(r'^[:,\s]+|[:,\s]+$', '', french)
                
                if french and sara_words:
                    entries.append({
                        'french': french,
                        'sara_variants': sara_words
                    })
            elif sara_words and current_french:
                # Utiliser le français de la ligne précédente
                entries.append({
                    'french': current_french,
                    'sara_variants': sara_words
                })
        
        # Pattern 2: Ligne avec juste du français (souvent avant les codes)
        # Format: "mot français" ou "à côté de acide : être"
        elif re.match(r'^[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿa-zA-Z\s,:\-]+$', line):
            # C'est probablement une ligne de français
            french = line.strip().rstrip(':').strip()
            if len(french) > 2 and len(french) < 100:
                current_french = french
        
        # Pattern 3: Format simple "français | sara" ou "français    sara"
        elif '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2:
                entries.append({
                    'french': parts[0],
                    'sara_variants': [p.strip() for p in parts[1:] if p.strip()]
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


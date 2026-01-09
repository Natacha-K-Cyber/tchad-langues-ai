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
    Format réel: 
    - Ligne 1: "mot français"
    - Ligne 2: "Beb=mbô : Bd=rû : Gor=gæd"
    - Ou parfois: "Beb=mbô : Bd=rû mot français"
    """
    entries = []
    lines = text.split('\n')
    
    # Codes de langues Sara (abréviations)
    sara_codes = ['Beb', 'Bd', 'Gor', 'Gu', 'Kbb', 'Db', 'Mb', 'Mo', 'Nar', 'KbN', 'NgT', 'Ngb', 'Sr', 'Lk', 'Kul']
    
    current_french = None
    accumulated_sara = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line or len(line) < 2:
            i += 1
            continue
        
        # Ignorer les lignes d'en-tête
        if 'Lexique' in line or 'Introduction' in line or line.startswith('Page') or line.isdigit():
            i += 1
            continue
        
        # Pattern 1: Ligne avec codes de langues (ex: Beb=mbô : Bd=rû)
        sara_matches = re.findall(r'([A-Z][a-z]?[A-Z]?)=([^:,\n]+)', line)
        
        if sara_matches:
            # Extraire les mots Sara de cette ligne
            sara_words = []
            for code, word in sara_matches:
                word = word.strip().rstrip(',').strip()
                if word and code in sara_codes:
                    sara_words.append(word)
            
            if sara_words:
                accumulated_sara.extend(sara_words)
            
            # Chercher si il y a du français à la fin de cette ligne
            # Enlever les codes de langues pour voir ce qui reste
            remaining = line
            for code in sara_codes:
                remaining = re.sub(rf'{code}=[^:,\s]+', '', remaining)
            remaining = re.sub(r'[:,\s]+', ' ', remaining).strip()
            
            # Si ce qui reste ressemble à du français (pas de caractères spéciaux Sara)
            if remaining and len(remaining) > 2 and not re.search(r'[=:]', remaining):
                # C'est probablement du français à la fin
                if accumulated_sara:
                    entries.append({
                        'french': remaining,
                        'sara_variants': list(set(accumulated_sara))  # Enlever doublons
                    })
                    accumulated_sara = []
                current_french = None
            
            # Vérifier la ligne suivante pour voir si c'est un nouveau mot français
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Si la ligne suivante n'a pas de codes de langues, c'est probablement un nouveau mot français
                if next_line and not re.search(r'[A-Z][a-z]?[A-Z]?=', next_line):
                    # Sauvegarder l'entrée actuelle si on a des données
                    if accumulated_sara and current_french:
                        entries.append({
                            'french': current_french,
                            'sara_variants': list(set(accumulated_sara))
                        })
                        accumulated_sara = []
                    current_french = next_line
                    i += 1  # Passer la ligne suivante aussi
                    continue
        
        # Pattern 2: Ligne avec juste du français (sans codes de langues)
        elif not re.search(r'[A-Z][a-z]?[A-Z]?=', line):
            # C'est probablement une ligne de français
            french = line.strip().rstrip(':').strip()
            # Nettoyer (enlever les numéros de page, etc.)
            french = re.sub(r'^\d+\s+', '', french)  # Enlever numéro de page au début
            
            if len(french) > 2 and len(french) < 150:
                # Si on avait des traductions Sara accumulées, les sauvegarder
                if accumulated_sara and current_french:
                    entries.append({
                        'french': current_french,
                        'sara_variants': list(set(accumulated_sara))
                    })
                    accumulated_sara = []
                
                current_french = french
        
        i += 1
    
    # Sauvegarder la dernière entrée si nécessaire
    if accumulated_sara and current_french:
        entries.append({
            'french': current_french,
            'sara_variants': list(set(accumulated_sara))
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
    
    # Sauvegarder d'abord les entrées brutes du lexique
    print("\n[4/5] Sauvegarde des entrees brutes du lexique...")
    raw_entries_file = TRAINING_DIR / "lexicon_entries_raw.json"
    with open(raw_entries_file, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"   {len(all_entries)} entrees brutes sauvegardees : {raw_entries_file}")
    
    # Créer les exemples d'entraînement seulement si on a des entrées
    print("\n[5/5] Creation des exemples d'entrainement...")
    if all_entries:
        training_examples = create_training_examples(all_entries, max_examples=2000)
        print(f"   {len(training_examples)} exemples crees")
        
        # Sauvegarder les données d'entraînement
        output_file = TRAINING_DIR / "training_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(training_examples, f, ensure_ascii=False, indent=2)
        
        print(f"   Exemples sauvegardes : {output_file}")
    else:
        print("   ATTENTION : Aucune entree trouvee, pas d'exemples crees")
        print("   Le parsing du lexique n'a rien trouve.")
        print("   Verifie le format avec : python scripts/data_processing/debug_lexicon.py")
    
    # Statistiques
    print(f"\nStatistiques:")
    print(f"   Entrees de lexique : {len(all_entries)}")
    if all_entries:
        print(f"   Exemples d'entrainement : {len(training_examples)}")
    print(f"\nOK - Preparation terminee !")
    
    if all_entries:
        print(f"   Prochaine etape : Nettoyage et normalisation")
        print(f"   python scripts/data_processing/clean_and_normalize.py")
    else:
        print(f"   PROBLEME : Aucune entree extraite du lexique")
        print(f"   Il faut corriger le parsing dans prepare_training_data.py")

if __name__ == "__main__":
    main()


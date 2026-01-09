"""
Script pour extraire le texte du PDF Morkeg Books
Extrait les lexiques Français-Sara et English-Sara
"""

import pdfplumber
import json
from pathlib import Path
import re
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw" / "morkeg"
PROCESSED_DIR = DATA_DIR / "processed"

def create_dirs():
    """Crée les répertoires nécessaires"""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """
    Extrait le texte d'un PDF page par page
    
    Args:
        pdf_path: Chemin vers le PDF
        
    Returns:
        Liste de dictionnaires avec page_num et text
    """
    pages_data = []
    
    print(f"Extraction du texte depuis {pdf_path}...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            for page_num, page in enumerate(tqdm(pdf.pages, desc="Extraction pages", total=total_pages), 1):
                text = page.extract_text()
                if text:
                    pages_data.append({
                        'page_num': page_num,
                        'text': text.strip()
                    })
        
        print(f"OK - {len(pages_data)} pages extraites")
        return pages_data
        
    except Exception as e:
        print(f"ERREUR lors de l'extraction : {e}")
        return []

def extract_lexicon_sections(pages_data):
    """
    Extrait les sections de lexique (Français-Sara et English-Sara)
    """
    full_text = '\n\n'.join([p['text'] for p in pages_data])
    
    # Chercher les sections de lexique
    sections = {
        'french_sara': None,
        'english_sara': None
    }
    
    # Zone du lexique Français-Sara (généralement après "Lexique Français – Langues Sara")
    french_section_start = full_text.find('Lexique\nFrançais – Langues Sara')
    if french_section_start == -1:
        french_section_start = full_text.find('Lexique Français')
    
    english_section_start = full_text.find('Lexique\nEnglish – Sara Languages')
    if english_section_start == -1:
        english_section_start = full_text.find('Lexique English')
    
    if french_section_start != -1:
        end_pos = english_section_start if english_section_start != -1 else len(full_text)
        sections['french_sara'] = full_text[french_section_start:end_pos]
        print(f"OK - Section Français-Sara trouvee ({len(sections['french_sara'])} caracteres)")
    
    if english_section_start != -1:
        sections['english_sara'] = full_text[english_section_start:]
        print(f"OK - Section English-Sara trouvee ({len(sections['english_sara'])} caracteres)")
    
    return sections

def save_processed_data(data, output_path):
    """Sauvegarde les données traitées en JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"OK - Donnees sauvegardees : {output_path}")

def main():
    """Fonction principale"""
    create_dirs()
    
    pdf_path = RAW_DIR / "SaraLanguagesLexicon.pdf"
    
    if not pdf_path.exists():
        print(f"ERREUR - PDF introuvable : {pdf_path}")
        print("   Execute d'abord : python scripts/data_collection/download_morkeg.py")
        return
    
    # Extraire le texte
    pages_data = extract_text_from_pdf(pdf_path)
    
    if not pages_data:
        print("ERREUR - Aucune donnee extraite")
        return
    
    # Sauvegarder les pages brutes
    raw_output = PROCESSED_DIR / "morkeg_raw_pages.json"
    save_processed_data(pages_data, raw_output)
    
    # Extraire les sections de lexique
    sections = extract_lexicon_sections(pages_data)
    
    # Sauvegarder les sections
    sections_output = PROCESSED_DIR / "morkeg_lexicon_sections.json"
    save_processed_data(sections, sections_output)
    
    # Statistiques
    print(f"\nStatistiques d'extraction:")
    print(f"   Pages totales : {len(pages_data)}")
    print(f"   Sections trouvees : {len([s for s in sections.values() if s])}")
    print(f"\nOK - Extraction terminee !")
    print(f"   Fichiers crees dans : {PROCESSED_DIR}")

if __name__ == "__main__":
    main()


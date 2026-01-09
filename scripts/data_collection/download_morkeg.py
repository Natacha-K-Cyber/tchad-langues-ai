"""
Script pour télécharger le lexique PDF depuis Morkeg Books
Sara Languages Lexicon - Français/Sara et English/Sara
"""

import requests
from pathlib import Path
import yaml
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "morkeg"
CONFIG_FILE = BASE_DIR / "config.yaml"

def load_config():
    """Charge la configuration"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_data_dirs():
    """Crée les répertoires nécessaires"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_pdf(url, output_path):
    """
    Télécharge un fichier PDF depuis une URL
    """
    try:
        print(f"Telechargement de {url}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f, tqdm(
            desc="Telechargement",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
        
        print(f"OK - PDF telecharge avec succes : {output_path}")
        return True
        
    except Exception as e:
        print(f"ERREUR lors du telechargement : {e}")
        return False

def main():
    """Fonction principale"""
    config = load_config()
    create_data_dirs()
    
    pdf_url = config['data_collection']['morkeg_books']['pdf_url']
    output_filename = "SaraLanguagesLexicon.pdf"
    output_path = DATA_DIR / output_filename
    
    # Vérifier si le fichier existe déjà
    if output_path.exists():
        print(f"Le fichier existe deja : {output_path}")
        response = input("Voulez-vous le telecharger a nouveau ? (o/n): ")
        if response.lower() != 'o':
            print("Telechargement annule.")
            return
    
    # Télécharger le PDF
    success = download_pdf(pdf_url, output_path)
    
    if success:
        file_size = output_path.stat().st_size / (1024 * 1024)  # MB
        print(f"\nStatistiques:")
        print(f"   Fichier : {output_path}")
        print(f"   Taille : {file_size:.2f} MB")
        print(f"\nOK - Pret pour l'extraction du texte !")
        print(f"   Executez : python scripts/data_processing/extract_pdf_text.py")
    else:
        print("\nERREUR - Echec du telechargement. Verifiez votre connexion internet.")

if __name__ == "__main__":
    main()


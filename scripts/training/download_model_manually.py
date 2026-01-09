"""
Script pour télécharger le modèle manuellement avant l'entraînement
Évite les blocages pendant l'entraînement
"""

import yaml
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download
import torch

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_FILE = BASE_DIR / "config.yaml"

def load_config():
    """Charge la configuration"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def download_model_manually():
    """Télécharge le modèle manuellement"""
    config = load_config()
    model_name = config['model']['base_model']
    
    print("="*60)
    print(f"Telechargement manuel du modele : {model_name}")
    print("="*60)
    print("\nCela peut prendre 10-30 minutes selon la connexion...")
    print("Le modele sera mis en cache pour l'entrainement.\n")
    
    try:
        # Télécharger le tokenizer
        print("[1/2] Telechargement du tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir="./.cache/huggingface"
        )
        print("   OK - Tokenizer telecharge")
        
        # Télécharger le modèle (sans le charger en mémoire)
        print("\n[2/2] Telechargement du modele (peut etre long)...")
        snapshot_download(
            repo_id=model_name,
            cache_dir="./.cache/huggingface",
            resume_download=True
        )
        print("   OK - Modele telecharge")
        
        print("\n" + "="*60)
        print("Telechargement termine !")
        print("="*60)
        print("\nLe modele est maintenant en cache.")
        print("L'entrainement devrait etre plus rapide maintenant.")
        
    except Exception as e:
        print(f"\nERREUR lors du telechargement : {e}")
        print("\nSolutions possibles :")
        print("1. Verifier la connexion internet")
        print("2. Reessayer (le telechargement reprendra ou il s'est arrete)")
        print("3. Utiliser un VPN si Hugging Face est bloque")
        print("4. Telecharger manuellement depuis https://huggingface.co/")

if __name__ == "__main__":
    download_model_manually()


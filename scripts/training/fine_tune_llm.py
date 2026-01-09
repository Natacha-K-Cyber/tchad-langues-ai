"""
Script pour fine-tuner un modèle LLM avec les données Tchad Langues
Utilise LoRA (Low-Rank Adaptation) pour un entraînement efficace
"""

import json
import yaml
from pathlib import Path
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
import torch
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "training"
CONFIG_FILE = BASE_DIR / "config.yaml"
MODELS_DIR = BASE_DIR / "models"

def load_config():
    """Charge la configuration"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_training_data():
    """Charge les données d'entraînement nettoyées"""
    data_file = DATA_DIR / "training_data_cleaned.json"
    
    if not data_file.exists():
        print(f"ERREUR - Fichier introuvable : {data_file}")
        print("Execute d'abord : python scripts/data_processing/clean_and_normalize.py")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_training_text(entry):
    """
    Formate une entrée pour l'entraînement
    Format: "Question: [français]\nRéponse: [sara]"
    """
    french = entry.get('french', '').strip()
    sara_variants = entry.get('sara_variants', [])
    
    if not french or not sara_variants:
        return None
    
    # Prendre la première variante comme réponse principale
    sara = sara_variants[0].strip()
    
    # Format conversationnel simple
    text = f"Question: Comment dit-on '{french}' en Sara ?\nRéponse: {sara}"
    
    return text

def prepare_dataset(entries, tokenizer, max_length=512):
    """Prépare le dataset pour l'entraînement"""
    print("Preparation du dataset...")
    
    texts = []
    for entry in tqdm(entries, desc="Formatage"):
        text = format_training_text(entry)
        if text:
            texts.append(text)
    
    print(f"   {len(texts)} exemples prepares")
    
    # Tokeniser
    def tokenize_function(examples):
        return tokenizer(
            examples['text'],
            truncation=True,
            padding='max_length',
            max_length=max_length,
            return_tensors='pt'
        )
    
    # Créer le dataset
    dataset = Dataset.from_dict({'text': texts})
    tokenized = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=['text']
    )
    
    return tokenized

def main():
    """Fonction principale"""
    print("="*60)
    print("Fine-tuning du modele LLM pour Tchad Langues")
    print("="*60)
    
    config = load_config()
    model_config = config['model']
    training_config = config['training']
    
    # Charger les données
    print("\n[1/6] Chargement des donnees...")
    entries = load_training_data()
    
    if not entries:
        return
    
    print(f"   {len(entries)} entrees chargees")
    
    # Charger le tokenizer et le modèle
    print(f"\n[2/6] Chargement du modele : {model_config['base_model']}...")
    print("   (Cela peut prendre quelques minutes...)")
    
    tokenizer = AutoTokenizer.from_pretrained(model_config['base_model'])
    
    # Ajouter un pad_token si nécessaire
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Charger le modèle avec quantization si activé
    if model_config.get('use_quantization', False):
        print("   Utilisation de la quantization 4-bit...")
        from transformers import BitsAndBytesConfig
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            model_config['base_model'],
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_config['base_model'],
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
    
    print("   Modele charge")
    
    # Préparer le modèle pour LoRA
    if model_config.get('use_lora', False):
        print(f"\n[3/6] Configuration LoRA...")
        
        if model_config.get('use_quantization', False):
            model = prepare_model_for_kbit_training(model)
        
        lora_config = LoraConfig(
            r=model_config.get('lora_r', 16),
            lora_alpha=model_config.get('lora_alpha', 32),
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
            lora_dropout=model_config.get('lora_dropout', 0.05),
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        model = get_peft_model(model, lora_config)
        print("   LoRA configure")
    
    # Préparer le dataset
    print(f"\n[4/6] Preparation du dataset...")
    dataset = prepare_dataset(
        entries,
        tokenizer,
        max_length=training_config.get('max_length', 512)
    )
    
    # Diviser en train/val (90/10)
    dataset = dataset.train_test_split(test_size=0.1)
    train_dataset = dataset['train']
    eval_dataset = dataset['test']
    
    print(f"   Train: {len(train_dataset)} exemples")
    print(f"   Validation: {len(eval_dataset)} exemples")
    
    # Configuration de l'entraînement
    print(f"\n[5/6] Configuration de l'entrainement...")
    
    output_dir = MODELS_DIR / training_config['output_dir']
    output_dir.mkdir(parents=True, exist_ok=True)
    
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=training_config.get('num_train_epochs', 3),
        per_device_train_batch_size=training_config.get('per_device_train_batch_size', 2),
        gradient_accumulation_steps=training_config.get('gradient_accumulation_steps', 4),
        learning_rate=training_config.get('learning_rate', 2e-4),
        warmup_steps=training_config.get('warmup_steps', 100),
        logging_steps=training_config.get('logging_steps', 100),
        save_steps=training_config.get('save_steps', 500),
        eval_steps=training_config.get('eval_steps', 500),
        evaluation_strategy="steps",
        save_total_limit=3,
        load_best_model_at_end=True,
        fp16=True,
        report_to="none"
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )
    
    # Entraînement
    print(f"\n[6/6] Debut de l'entrainement...")
    print(f"   Cela peut prendre plusieurs heures selon la configuration")
    print(f"   Surveille la progression ci-dessous...\n")
    
    trainer.train()
    
    # Sauvegarder le modèle final
    print(f"\nSauvegarde du modele final...")
    model.save_pretrained(str(output_dir / "final"))
    tokenizer.save_pretrained(str(output_dir / "final"))
    
    print(f"\n" + "="*60)
    print("Entrainement termine !")
    print("="*60)
    print(f"\nModele sauvegarde dans : {output_dir / 'final'}")
    print(f"\nProchaine etape : Tester le modele")

if __name__ == "__main__":
    main()


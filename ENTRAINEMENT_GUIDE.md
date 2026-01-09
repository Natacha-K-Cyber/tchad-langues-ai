# 🚀 Guide d'entraînement du modèle LLM

## ✅ Données prêtes

- **1923 entrées valides** ✅
- **9417 traductions Sara** ✅
- **4.90 variantes par mot** en moyenne ✅

## 📋 Avant de commencer l'entraînement

### Option 1 : Tester avec un petit modèle d'abord (Recommandé)

Pour valider le pipeline avant d'entraîner Mistral 7B :

1. **Modifier `config.yaml`** :
```yaml
model:
  base_model: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Plus petit, plus rapide
  use_quantization: true
  use_lora: true
```

2. **Tester l'entraînement** (plus rapide, ~30 min au lieu de plusieurs heures)

### Option 2 : Entraîner directement Mistral 7B

Pour un modèle plus performant (nécessite plus de temps et de RAM) :

1. **Vérifier la configuration** dans `config.yaml`
2. **Lancer l'entraînement** (peut prendre plusieurs heures)

## 🔧 Installation des dépendances ML

Sur ta VM Kali :

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Installer PyTorch (CPU version pour 20GB RAM)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Installer les dépendances ML
pip install transformers datasets accelerate peft bitsandbytes sentencepiece tokenizers scipy
```

**Note** : Si tu as un GPU, installe la version CUDA de PyTorch à la place.

## 🚀 Lancer l'entraînement

### Étape 1 : Vérifier la configuration

```bash
# Voir la configuration actuelle
cat config.yaml | grep -A 20 "model:"
```

### Étape 2 : Lancer l'entraînement

```bash
# Lancer l'entraînement (cela peut prendre plusieurs heures)
python scripts/training/fine_tune_llm.py
```

### Étape 3 : Surveiller l'entraînement

Le script affichera :
- La progression de l'entraînement
- Les métriques (loss, perplexity)
- Les sauvegardes automatiques

## ⚙️ Configuration recommandée pour 20GB RAM

Dans `config.yaml`, utilise :

```yaml
model:
  base_model: "mistralai/Mistral-7B-Instruct-v0.2"
  use_quantization: true  # OBLIGATOIRE pour 20GB RAM
  use_lora: true
  lora_r: 16
  lora_alpha: 32
  
training:
  per_device_train_batch_size: 2  # Adapté pour 20GB RAM
  gradient_accumulation_steps: 4  # Simule batch_size=8
  max_length: 512
  save_total_limit: 3  # Garder seulement 3 meilleurs checkpoints
```

## ⏱️ Temps d'entraînement estimé

- **TinyLlama 1.1B** : ~30-60 minutes
- **Mistral 7B** (avec LoRA + 4-bit) : ~3-6 heures
- **Sans GPU** : 2-3x plus long

## 📊 Métriques à surveiller

- **Loss** : Doit diminuer (idéalement < 1.0)
- **Perplexity** : Doit diminuer
- **Learning rate** : Suit le warmup puis décroît

## 💾 Espace disque nécessaire

- **Modèle de base** : ~4-5 GB
- **Checkpoints** : ~500 MB chacun (x3 = 1.5 GB)
- **Total** : ~6-7 GB

## ⚠️ En cas de problème

### Erreur : "Out of memory"
- Réduire `per_device_train_batch_size` à 1
- Augmenter `gradient_accumulation_steps` à 8
- Vérifier que `use_quantization: true`

### Erreur : "Model not found"
- Vérifier la connexion internet
- Le modèle sera téléchargé automatiquement depuis Hugging Face

### Erreur : "CUDA out of memory"
- Tu utilises CPU, cette erreur ne devrait pas arriver
- Si elle arrive, réduire encore le batch size

## ✅ Après l'entraînement

Une fois terminé, le modèle sera sauvegardé dans :
```
models/tchad_langues/final/
```

Tu pourras ensuite :
1. Tester le modèle
2. L'intégrer dans l'application
3. Générer des exercices dynamiques

## 🎯 Prochaines étapes

1. ✅ Données nettoyées (1923 entrées)
2. 🔄 Installer dépendances ML
3. 🔄 Lancer l'entraînement
4. ⏳ Tester le modèle entraîné
5. ⏳ Intégrer dans l'application


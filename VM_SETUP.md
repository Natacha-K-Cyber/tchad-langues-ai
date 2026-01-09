# 🖥️ Configuration VM pour l'entraînement du modèle

## 📊 Comparaison des VMs

### VM Kali Linux (Recommandée ✅)
**Avantages :**
- ✅ Meilleur support pour ML/AI (CUDA, PyTorch)
- ✅ Outils Linux optimisés pour le traitement
- ✅ Meilleure gestion de la mémoire
- ✅ Plus facile pour installer les dépendances ML
- ✅ Support natif pour les GPU (si disponible)

**Inconvénients :**
- Interface en ligne de commande (mais on peut installer un GUI)

### VM Windows 10
**Avantages :**
- Interface graphique familière
- Facile à utiliser

**Inconvénients :**
- ❌ Moins optimal pour ML/AI
- ❌ Installation CUDA plus complexe
- ❌ Performance généralement inférieure

## ⚠️ Limitation importante : 4GB RAM

**Problème** : 4GB de RAM est **très limité** pour entraîner un modèle LLM de 7B (Mistral/Llama).

### Options avec 4GB RAM :

#### Option 1 : Modèle plus petit (Recommandé)
- Utiliser **Mistral 7B** avec **LoRA** + **4-bit quantization**
- Nécessite environ **6-8GB RAM** (limite avec 4GB)
- **Solution** : Utiliser un modèle plus petit comme **TinyLlama 1.1B** ou **Phi-2 (2.7B)**

#### Option 2 : Cloud / Colab (Alternative)
- Utiliser **Google Colab** (gratuit, GPU disponible)
- Ou **Kaggle Notebooks** (gratuit, GPU)
- Ou **Hugging Face Spaces** (gratuit, GPU limité)

#### Option 3 : Fine-tuning très léger
- Utiliser **LoRA** avec paramètres très réduits
- Batch size = 1
- Gradient accumulation
- Risque d'erreurs mémoire

## 🎯 Recommandation

### Pour commencer (POC) :
1. **Utilise Kali Linux** pour l'environnement
2. **Commence avec un modèle plus petit** :
   - **TinyLlama 1.1B** (nécessite ~2-3GB RAM)
   - Ou **Phi-2 (2.7B)** (nécessite ~4-5GB RAM)
3. **Alternative** : Utilise **Google Colab** pour l'entraînement (gratuit, GPU)

### Pour la production (plus tard) :
- Upgrade RAM à **16GB minimum** (idéalement 32GB)
- Ou utilise un service cloud (AWS, GCP, Azure)
- Ou utilise un GPU dédié

## 📋 Plan d'action

### Étape 1 : Choisir la VM
✅ **Kali Linux** (recommandé)

### Étape 2 : Préparer l'environnement sur Kali
```bash
# Installer Python 3.10+
sudo apt update
sudo apt install python3.10 python3-pip git

# Cloner le projet depuis GitHub
git clone https://github.com/Natacha-K-Cyber/tchad-langues-ai.git
cd tchad-langues-ai

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances (version allégée pour 4GB RAM)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers datasets accelerate peft bitsandbytes
pip install streamlit pandas pyyaml
```

### Étape 3 : Choisir le modèle
- **TinyLlama 1.1B** : https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
- **Phi-2** : https://huggingface.co/microsoft/phi-2

### Étape 4 : Alternative Cloud (Recommandé pour POC)
- **Google Colab** : https://colab.research.google.com/
  - GPU gratuit (T4)
  - 12GB RAM
  - Parfait pour tester l'entraînement

## 🔧 Configuration recommandée pour 4GB RAM

```yaml
model:
  base_model: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Plus petit
  use_quantization: true  # 4-bit obligatoire
  use_lora: true
  lora_r: 8  # Réduit (au lieu de 16)
  lora_alpha: 16  # Réduit
  
training:
  per_device_train_batch_size: 1  # Minimum
  gradient_accumulation_steps: 8  # Pour simuler batch_size=8
  max_length: 256  # Réduit (au lieu de 512)
```

## 💡 Suggestion finale

**Pour le POC** : Utilise **Google Colab** pour l'entraînement
- Gratuit
- GPU disponible
- Pas de limitation RAM
- Facile à partager

**Pour la VM** : Utilise **Kali Linux** pour :
- Le développement de l'application
- Le traitement des données
- Les tests locaux

## 📝 Prochaines étapes

1. ✅ Pousser le code sur GitHub
2. 🔄 Cloner sur la VM Kali
3. 🔄 Installer l'environnement
4. 🔄 Tester avec un petit modèle
5. 🔄 Ou utiliser Colab pour l'entraînement

